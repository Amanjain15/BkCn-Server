from .tokens import get_user, ACCESS_TOKEN
from django.http import JsonResponse
from .checker import assert_valid, assert_allowed, assert_found

def JWT(function):
	def check_validity(request, *args, **kwargs):
		token = request.META.get(ACCESS_TOKEN, None)
		assert_found(token, 'access_token not found')
		# print token,"aaa"
		user = get_user(token)

		response = {
		'success' : True
		}

		return function(request, user, copy.deepcopy(response), *args, **kwargs)
	return check_validity

def get_or_none(classmodel, **kwargs):
	try:
		return classmodel.objects.get(**kwargs)
	except classmodel.DoesNotExist:
		return None
