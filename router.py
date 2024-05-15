

from typing import Callable
from django.http import HttpRequest, HttpResponse, JsonResponse

from common.response import ApiJsonResponse


class Route:
    def __init__(self, path, method, handler):
        self.path = path
        self.method = method
        self.handler = handler

    def handle(self, request):
        return self.handler(request)
    
    def match(self, path, method):
        return self.path == path and self.method == method
    
class Middleware:
    handler: Callable[[HttpRequest,HttpResponse],tuple[bool,HttpRequest,HttpResponse]]
    sort: int = 0

    def __init__(self, handler:Callable[[HttpRequest,HttpResponse],tuple[bool,HttpRequest,HttpResponse]],sort:int=0):
        self.handler = handler
        self.sort = sort
    
    def handle(self, request,response):
        return self.handler(request,response)
    
    def __call__(self, request,response):
        return self.handle(request,response)
    
    def __add__(self, other):
        return Middleware(lambda request: self(other(request)))
    
class Router:
    routes: list[Route] = []
    before_middlewares: list[Middleware] = []
    after_middlewares: list[Middleware] = []

    def not_found_handler(self,request: HttpRequest) -> HttpResponse:
        return JsonResponse({'error': 'Not found'}, status=404)
    
    def error_handler(self, request: HttpRequest, error: Exception) -> HttpResponse:
        return JsonResponse({'error': str(error)}, status=500)

    def __init__(self):
        self.routes = []
    
    def add_route(self, path, method, handler):
        self.routes.append(Route(path, method, handler))
    
    def match(self, path, method)->Route:
        for route in self.routes:
            if route.match(path, method):
                return route
        return None

    def handle(self, request):
        route = self.match(request.path, request.method)
        if route:
            try:
                response = ApiJsonResponse()
                # before middleware
                for middleware in self.before_middlewares:
                    next, request, response = middleware.handle(request,response)
                    if not next:
                        return response
                    
                # handler
                response = route.handle(request)

                # after middleware
                for middleware in self.after_middlewares:
                    next, request, response = middleware.handle(request,response)
                    if not next:
                        return response
                return response
            except Exception as e:
                return self.error_handler(request, e)
        else:
            return self.not_found_handler(request)
        
    def route(self, path, method):
        def wrapper(handler):
            self.add_route(path, method, handler)
            return handler
        return wrapper
    
    def get(self, path):
        return self.route(path, 'GET')
    
    def post(self, path):
        return self.route(path, 'POST')
    
    def put(self, path):
        return self.route(path, 'PUT')
    
    def delete(self, path):
        return self.route(path, 'DELETE')
    
    def patch(self, path):
        return self.route(path, 'PATCH')
    
    def register(self, path, api):
        if hasattr(api,'register') and callable(api.register):
            api.register(self,path)

    # middleware 
    def use(self, middleware:Middleware):
        self.before_middlewares.append(middleware)
        self.re_sort_middlewares()

    def after(self, middleware:Middleware):
        self.after_middlewares.append(middleware)
        self.re_sort_middlewares()

    def re_sort_middlewares(self):
        self.before_middlewares.sort(key=lambda x:x.sort)
        self.after_middlewares.sort(key=lambda x:x.sort)

    