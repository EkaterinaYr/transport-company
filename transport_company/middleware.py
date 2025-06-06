import base64
from django.http import HttpResponse

class BasicAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.username = 'admin'        # поменяй на свой логин
        self.password = 'mypassword'   # поменяй на свой пароль

    def __call__(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION')
        if auth is None:
            return self.unauthorized_response()
        method, credentials = auth.split(' ', 1)
        if method.lower() != 'basic':
            return self.unauthorized_response()
        decoded = base64.b64decode(credentials).decode('utf-8')
        username, password = decoded.split(':', 1)
        if username == self.username and password == self.password:
            return self.get_response(request)
        return self.unauthorized_response()

    def unauthorized_response(self):
        response = HttpResponse('Unauthorized', status=401)
        response['WWW-Authenticate'] = 'Basic realm="Restricted"'
        return response
