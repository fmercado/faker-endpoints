from django.shortcuts import render

from django.http import JsonResponse

from rest.endpoints import Responser

from json import loads, dumps

from rest.models import Cache

def error(error_message):
	return JsonResponse({"error": error_message}, status=500)


def get_contents(name, request):
	r = Responser.from_file(name, request.GET)
	return r.gen()

def rtt(request, name):

	request_path = request.get_full_path()

	if request.GET.get("no-cache"):
		return JsonResponse(get_contents(name, request))

	try:
		cache = Cache.objects.get(url=request_path)
		return JsonResponse(loads(cache.response_text))
	except Cache.DoesNotExist:
		resp = get_contents(name, request)
		Cache.objects.create(url=request_path, response_text=dumps(resp))
		return JsonResponse(resp)
    
