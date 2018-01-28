from login.views import *
from chain.views import *
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
import json, copy

INTERNAL_ERROR = JsonResponse({
	'success' : False,
	'message' : 'something went wrong'
	}, status = 500)

NOT_FOUND = JsonResponse({
	'success' : False,
	'message' : 'method not found'
	}, status = 400)


def get_view(function_name, method):
	return '%s_%s(request, *args, **kwargs)'%(function_name, method)

def VMS(*methods):
	def _function_wrapper(function):
		def view_name_segregator(request, *args, **kwargs):
			if request.method in methods:
				try:
					return eval(get_view(function.__name__, request.method))
				except Exception as e:
					print "// " , e , " //"
					err_data = e.message
					try:
						return JsonResponse(err_data, status = err_data['status_code'])
					except :
						return  INTERNAL_ERROR
			else :
				return NOT_FOUND
		return view_name_segregator
	return _function_wrapper

@VMS('POST')
def login():
	pass

@VMS('GET')
def access_token():
	pass

@VMS('POST')
def register():
	pass

@VMS('GET')
def runt():
	pass

@VMS('POST')
def product_owners():
	pass

@VMS('POST')
def create_transaction():
	pass