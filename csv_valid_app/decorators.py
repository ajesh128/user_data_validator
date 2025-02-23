from rest_framework.response import Response


def validation_check_decorator():
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            file = self.request.FILES.get('file')
            if not file:
                return Response({"error":"No file provided"},status=400)
            elif not file.content_type.endswith('csv'):
                return Response({"error":"Invalid file format. Only CSV file is allowed"},status=400)
            return func(self, request, *args, **kwargs)

        return wrapper

    return decorator