from django.conf import settings
from celery import shared_task
import logging
import json
import pandas as pd
import os
import io

from .serializer import UserCSVUploadSerializer


@shared_task
def csv_processor_worker(**kwargs):
    """
    This function is used to process CSV file in the background

    Parameters:
    kwargs (dict): Contains the file

    Returns:
    bool: Returns true.

    """
    try:
        # Load the CSV file into a pandas DataFrame
        file_like_object = io.BytesIO(kwargs.get("file"))
        # Load JSON data from the CSV file into a list of dictionaries
        json_data = json.loads(pd.read_csv(file_like_object).to_json(orient='records'))
        invalid_record = []
        valid_record = 0
        tota_number_of_invalid_record = 0
        # Validate JSON data and save to the database
        for row ,data in enumerate(json_data):
            serialiser = UserCSVUploadSerializer(data = data)
            # Save the data if serializer is valid
            if serialiser.is_valid():
                valid_record+=1
                # Saved to User modal
                serialiser.save()
            else:
                tota_number_of_invalid_record+=1
                errors = serialiser.errors
                # Add row number to the error dictionary
                errors.update({"error_row":row+2})
                # Add the error to the list of invalid records 
                invalid_record.append(errors)
        # Save the report to a JSON file in the project directory
        report = {"Invalid_record":tota_number_of_invalid_record,"valid_record":valid_record,"invalid_record":invalid_record}
        file_path = os.path.join(settings.MEDIA_ROOT, 'report.json')
        # Save the report to a JSON file
        with open(file_path, 'w') as json_file:
            # Use indent to make the JSON more readable
            json.dump(report, json_file, indent=4)
        return True
    except Exception as e:
        logging.error(f"Error processing CSV file: {e}")
        return False
