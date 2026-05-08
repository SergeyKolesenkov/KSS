import time

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def set_useragent_on_request_middleware(get_response):

    def middleware(request: HttpRequest):
        print('before get response')
        request.user_agent = request.META['HTTP_USER_AGENT']
        response = get_response(request)
        print('After get response', id, time)
        return response

    return middleware

class CountRequestsMiddlawer:
    def __init__(self, get_response):
        self.get_response = get_response
        self.last_time_request = {}
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0
        self.throttling = 2

    def __call__(self, request: HttpRequest):
        id = request.META.get('REMOTE_ADDR')
        time_now = round(time.time(), 1)
        if id not in self.last_time_request:
            self.last_time_request[id] = time_now
        else:
            if time_now - self.last_time_request[id] < self.throttling:
                return render(request, 'requestdataapp/error_time.html')
            self.last_time_request[id] = time_now
        self.requests_count += 1
        print('requests count', self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print('responses count', self.responses_count)
        return response

    def exceptions(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print('got', self.exceptions_count, 'exceptions so far')

