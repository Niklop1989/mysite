import time

from django.http import HttpRequest,HttpResponseBadRequest
from django.shortcuts import render


def set_useragent_on_request_middleware(get_response):

    print('initial call')
    def middleware(request:HttpRequest):
        print('before get response')
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print('after get response')
        return response

    return middleware



class CountRequestMiddlewarw:
    def __init__(self,get_response):
        self.get_response = get_response
        self.request_count = 0
        self.response_count = 0
        self.exeption_count = 0


    def __call__(self, request:HttpRequest):
        self.request_time = {"time":round(time.time()) * 1,'ip-address':request.META.get('REMOTE_ADDR')}
        self.request_count += 1
        print(f"request_count {self.request_count}")
        response = self.get_response(request)
        self.response_count += 1
        print(f'response_count {self.response_count}')
        print('time',self.request_time)
        return response

    def process_exception(self,request:HttpRequest,exception:Exception):
        self.exeption_count += 1
        print('got', self.exeption_count, 'exception so far')



