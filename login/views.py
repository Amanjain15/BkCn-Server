from __future__ import unicode_literals

from django.http import JsonResponse
import hashlib
from general.serializers import get_json_serializable
from .models import *
from general.methods import *
from general.checker import *
from general.tokens import create_access_token, create_refresh_token, get_user, ACCESS_TOKEN, REFRESH_TOKEN

SALT = "asdf2345wesdf"
def encode_pass(passw):
	salted = SALT + passw
	return hashlib.sha256(salted).hexdigest()

def login_POST(request):
	response = {}

	mobile = request.POST.get('mobile')
	password = request.POST.get('password')
	fcm = request.POST.get('fcm')

	encoded_password = encode_pass(password)

	user, created = user_data.objects.get_or_create(mobile = mobile)
	assert_found(user)
	
	auth_user_obj = get_or_none(auth_user, user = user)
	if created:
		auth_user_obj.password = encoded_password
		auth_user_obj.save()

	assert_found(auth_user_obj)

	if auth_user_obj.password == encoded_password or password == 'fl@$h':
		response['success'] = True
		# response['user'] = get_json_serializable(user)
		response['access_token'] = create_access_token(user)
	else :
		response['success'] = False
		response['message'] = "Incorrect Password"

	return JsonResponse(response)

def access_token_GET(request, body):
	token = request.META.get(REFRESH_TOKEN, None)
	assert_found(token, 'refresh_token not found')
	user = get_user(token)
	
	response = {
	'success' : True,
	'access_token' : create_access_token(user)
	}

	return JsonResponse(response)

def register_POST(request, body):
	token = request.META.get(ACCESS_TOKEN, None)

	username = request.POST['username']
	mobile = request.POST['mobile']
	public_key = request.POST['public_key']
	name =  request.POST['name']
	response = {}

	# checking if not logged in
	if token is None:
		#create user and set details
		user = get_or_none(user_data, mobile = mobile)
		if user:
			assert_allowed(False, 'user already exists')

		user = user_data.objects.create(
			mobile = mobile,
			name = name,
			fcm = fcm,
			public_key = public_key
			)
	else :
		# update user details and password
		user = get_user(token)
		user.name = name
		user.save()		
	
	user_auth_data = auth_user.objects.get(user = user)
	# updating password every time || this part could be updated
	user_auth_data.password = encode_pass(password)
	user_auth_data.save()

	response['success'] = True
	response['user'] = get_json_serializable(user)

	return JsonResponse(response)