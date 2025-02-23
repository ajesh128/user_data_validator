# myapp/views.py
from . decorators import validation_check_decorator
from .task import csv_processor_worker
from rest_framework.views import APIView
from rest_framework.response import Response

class UploadCsv(APIView):
    """
    View to upload CSV file and validate JSON data
    """
    @validation_check_decorator()
    def post(self, request, *args, **kwargs):
        """
        Upload CSV file and process it in the background.

        Returns:
        Response: JSON response with success or error message."""
        try:
            # check if file is provided and its type is CSV
            file = request.FILES.get('file')
            # read the csv file as a file-like object
            binary_file = file.read()
            # Adding a background job to process the csv file
            csv_processor_worker.delay(file = binary_file)
            return Response({"message":"CSV file data uploaded successfully"},status=200)
        except Exception as exc:
            return Response({"error": str(exc)}, status=500)
        

