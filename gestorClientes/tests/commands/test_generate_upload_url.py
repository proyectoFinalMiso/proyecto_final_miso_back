import pytest
from unittest.mock import patch, MagicMock
from faker import Faker
import os
import datetime

from src.commands.generate_upload_url import GenerateUploadUrl

fake = Faker()

class TestGenerateUploadUrl:
    @pytest.fixture
    def valid_request_body(self):
        return {
            "filename": fake.file_name(extension="mp4"),
            "contentType": "video/mp4",
            "clientId": fake.uuid4()
        }

    @pytest.fixture
    def request_body_missing_filename(self):
        return {
            "contentType": "video/mp4",
            "clientId": fake.uuid4()
        }

    @pytest.fixture
    def request_body_missing_contentType(self):
        return {
            "filename": fake.file_name(extension="mp4"),
            "clientId": fake.uuid4()
        }

    def test_check_campos_requeridos_success(self, valid_request_body):
        command = GenerateUploadUrl(valid_request_body)
        assert command.check_campos_requeridos() is True

    def test_check_campos_requeridos_missing_filename(self, request_body_missing_filename):
        command = GenerateUploadUrl(request_body_missing_filename)
        assert command.check_campos_requeridos() is False

    def test_check_campos_requeridos_missing_contentType(self, request_body_missing_contentType):
        command = GenerateUploadUrl(request_body_missing_contentType)
        assert command.check_campos_requeridos() is False

    @patch.dict(os.environ, {"GCS_BUCKET_NAME": ""})
    def test_execute_gcs_bucket_name_not_set(self, valid_request_body):
        command = GenerateUploadUrl(valid_request_body)
        result = command.execute()
        assert result["status_code"] == 500
        assert "GCS_BUCKET_NAME environment variable not set" in result["response"]["msg"]

    @patch.dict(os.environ, {"GCS_BUCKET_NAME": "test-bucket"})
    def test_execute_missing_required_fields(self, request_body_missing_filename):
        command = GenerateUploadUrl(request_body_missing_filename)
        result = command.execute()
        assert result["status_code"] == 400
        assert "Missing required fields" in result["response"]["msg"]

    @patch.dict(os.environ, {"GCS_BUCKET_NAME": "test-bucket"})
    @patch('src.commands.generate_upload_url.storage.Client')
    def test_execute_success(self, mock_storage_client, valid_request_body):
        mock_client_instance = MagicMock()
        mock_bucket_instance = MagicMock()
        mock_blob_instance = MagicMock()
        
        mock_storage_client.return_value = mock_client_instance
        mock_client_instance.bucket.return_value = mock_bucket_instance
        mock_bucket_instance.blob.return_value = mock_blob_instance
        
        fake_signed_url = "https://fake-signed-url.com/upload"
        mock_blob_instance.generate_signed_url.return_value = fake_signed_url
        
        command = GenerateUploadUrl(valid_request_body)
        result = command.execute()
        
        assert result["status_code"] == 200
        assert "signedUrl" in result["response"]
        assert result["response"]["signedUrl"] == fake_signed_url
        assert "gcsPath" in result["response"]
        expected_gcs_path = f"gs://test-bucket/{valid_request_body['filename']}"
        assert result["response"]["gcsPath"] == expected_gcs_path
        
        mock_storage_client.assert_called_once()
        mock_client_instance.bucket.assert_called_once_with("test-bucket")
        mock_bucket_instance.blob.assert_called_once_with(valid_request_body['filename'])
        mock_blob_instance.generate_signed_url.assert_called_once_with(
            version="v4",
            expiration=datetime.timedelta(minutes=15),
            method="PUT",
            content_type=valid_request_body['contentType']
        )

    @patch.dict(os.environ, {"GCS_BUCKET_NAME": "test-bucket"})
    @patch('src.commands.generate_upload_url.storage.Client')
    def test_execute_gcs_exception(self, mock_storage_client, valid_request_body):
        mock_client_instance = MagicMock()
        mock_bucket_instance = MagicMock()
        mock_blob_instance = MagicMock()
        
        mock_storage_client.return_value = mock_client_instance
        mock_client_instance.bucket.return_value = mock_bucket_instance
        mock_bucket_instance.blob.return_value = mock_blob_instance
        
        mock_blob_instance.generate_signed_url.side_effect = Exception("GCS Error")
        
        command = GenerateUploadUrl(valid_request_body)
        result = command.execute()
        
        assert result["status_code"] == 500
        assert "Error generating signed URL: GCS Error" in result["response"]["msg"]
