from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.conf import settings
import os
import shutil
from csv_valid_app.task import csv_processor_worker


class CsvDataUploadTest(APITestCase):
    """
    Test case for CSV data upload.
    """

    def setUp(self):
        # Ensure the test upload directory exists before running the test
        self.test_uploads_dir = os.path.join(settings.BASE_DIR, 'test_uploads')
        os.makedirs(self.test_uploads_dir)

           
        
    @override_settings(
        MEDIA_ROOT=os.path.join(settings.BASE_DIR, 'test_uploads'), # Optional: change media URL for test
    )
    def test_create_account_with_valid_csv_file(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('csv')
        file = SimpleUploadedFile("test.csv", b"name,age,email\nhshsh,2,a@gmail.com\nahahhaha,77,b@gmail.com\nahahhahaaaa,88,c@gmail.com\naaaaaas,22,a@gmail.com\njjfjf,11,djdjdjdjd\nhfhfhfhf,2,s@gmail.com\n", content_type="text/csv")
        response = self.client.post(url, {"file":file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_account_with_text_file(self):
        """
        Ensure we can't create a new account object.
        """
        url = reverse('csv')
        file = SimpleUploadedFile("test.csv", b"name,age,email\nhshsh,2,a@gmail.com\nahahhaha,77,b@gmail.com\nahahhahaaaa,88,c@gmail.com\naaaaaas,22,a@gmail.com\njjfjf,11,djdjdjdjd\nhfhfhfhf,2,s@gmail.com\n")
        response = self.client.post(url, {"file":file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(
        MEDIA_ROOT=os.path.join(settings.BASE_DIR, 'invalid'), # Optional: change media URL for test
    )
    def test_create_account_with_invalid_path(self):
        """
        Ensure we can't create a new account object.
        """
        file = SimpleUploadedFile("test.csv", b"name,age,email\nhshsh,2,a@gmail.com\nahahhaha,77,b@gmail.com\nahahhahaaaa,88,c@gmail.com\naaaaaas,22,a@gmail.com\njjfjf,11,djdjdjdjd\nhfhfhfhf,2,s@gmail.com\n", content_type="text/csv")
        response = csv_processor_worker(file = file.read())
        self.assertEqual(response, False)

    def test_create_account_without_mandatory_field(self):
        """
        Ensure we can't create a new account object.
        """
        url = reverse('csv')
        response = self.client.post(url, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        

    def tearDown(self):
        # Clean up: Remove the test folder after tests are done
        MEDIA_ROOT=os.path.join(settings.BASE_DIR, 'test_uploads')
        shutil.rmtree(MEDIA_ROOT)









