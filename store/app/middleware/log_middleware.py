import datetime


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        timestamp = datetime.datetime.now()
        response = self.get_response(request)

        file_name = 'app/middleware/files/log.txt'
        file = open(file_name, mode='a')
        file_content = f'{timestamp} {request.path} {request.method}\n'
        file.write(file_content)
        file.close()

        return response
