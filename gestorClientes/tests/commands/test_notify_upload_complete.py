import pytest
from unittest.mock import patch, MagicMock
from faker import Faker
import os
import json
import datetime

from src.commands.notify_upload_complete import NotifyUploadComplete

fake = Faker()

class TestNotifyUploadComplete:
    @pytest.fixture
    def valid_request_body(self):
        return {
            "blobPath": f"gs://{fake.word()}/{fake.file_name(extension='mp4')}",
            "clientId": fake.uuid4(),
            "vendedorId": fake.uuid4()
        }

    @pytest.fixture
    def request_body_missing_blobPath(self):
        return {
            "clientId": fake.uuid4(),
            "vendedorId": fake.uuid4()
        }

    @pytest.fixture
    def request_body_missing_clientId(self):
        return {
            "blobPath": f"gs://{fake.word()}/{fake.file_name(extension='mp4')}",
            "vendedorId": fake.uuid4()
        }

    @pytest.fixture
    def request_body_missing_vendedorId(self):
        return {
            "blobPath": f"gs://{fake.word()}/{fake.file_name(extension='mp4')}",
            "clientId": fake.uuid4()
        }

    def test_check_campos_requeridos_success(self, valid_request_body):
        command = NotifyUploadComplete(valid_request_body)
        assert command.check_campos_requeridos() is True

    def test_check_campos_requeridos_missing_blobPath(self, request_body_missing_blobPath):
        command = NotifyUploadComplete(request_body_missing_blobPath)
        assert command.check_campos_requeridos() is False

    def test_check_campos_requeridos_missing_clientId(self, request_body_missing_clientId):
        command = NotifyUploadComplete(request_body_missing_clientId)
        assert command.check_campos_requeridos() is False

    def test_check_campos_requeridos_missing_vendedorId(self, request_body_missing_vendedorId):
        command = NotifyUploadComplete(request_body_missing_vendedorId)
        assert command.check_campos_requeridos() is False

    @patch.dict(os.environ, {"PUB_SUB_TOPIC_NAME": ""})
    def test_execute_pub_sub_topic_name_not_set(self, valid_request_body):
        command = NotifyUploadComplete(valid_request_body)
        result = command.execute()
        assert result["status_code"] == 500
        assert "PUB_SUB_TOPIC_NAME environment variable not set" in result["response"]["msg"]

    @patch.dict(os.environ, {"PUB_SUB_TOPIC_NAME": "projects/test-project/topics/test-topic"})
    def test_execute_missing_required_fields(self, request_body_missing_blobPath):
        command = NotifyUploadComplete(request_body_missing_blobPath)
        result = command.execute()
        assert result["status_code"] == 400
        assert "Missing required fields" in result["response"]["msg"]

    @patch.dict(os.environ, {"PUB_SUB_TOPIC_NAME": "projects/test-project/topics/test-topic"})
    @patch('src.commands.notify_upload_complete.pubsub_v1.PublisherClient')
    @patch('src.commands.notify_upload_complete.datetime')
    def test_execute_success(self, mock_datetime, mock_publisher_client, valid_request_body):
        mock_client_instance = MagicMock()
        mock_publisher_client.return_value = mock_client_instance
        
        fake_message_id = fake.uuid4()
        mock_future = MagicMock()
        mock_future.result.return_value = fake_message_id
        mock_client_instance.publish.return_value = mock_future

        fixed_naive_utcnow = datetime.datetime(2025, 5, 8, 12, 0, 0)
        mock_datetime.datetime.utcnow.return_value = fixed_naive_utcnow
        
        command = NotifyUploadComplete(valid_request_body)
        expected_message_data = {
            "Message": f"Video uploaded successfully: {valid_request_body['blobPath']}",
            "BlobPath": valid_request_body['blobPath'],
            "CreationDate": fixed_naive_utcnow.isoformat() + "Z",
            "Customer": valid_request_body['clientId'], 
            "Seller": valid_request_body['vendedorId']
        }
        expected_json_bytes = json.dumps(expected_message_data).encode("utf-8")

        result = command.execute()
        
        assert result["status_code"] == 200
        assert result["response"]["message"] == "Upload notification sent successfully (Avro)."
        assert result["response"]["messageId"] == fake_message_id
        
        mock_publisher_client.assert_called_once()
        
        mock_client_instance.publish.assert_called_once_with(
            "projects/test-project/topics/test-topic", 
            expected_json_bytes
        )
        mock_future.result.assert_called_once()

    @patch.dict(os.environ, {"PUB_SUB_TOPIC_NAME": "projects/test-project/topics/test-topic"})
    @patch('src.commands.notify_upload_complete.pubsub_v1.PublisherClient')
    def test_execute_pubsub_exception(self, mock_publisher_client, valid_request_body):
        mock_client_instance = MagicMock()
        mock_publisher_client.return_value = mock_client_instance
        mock_client_instance.publish.side_effect = Exception("PubSub Error")
        
        command = NotifyUploadComplete(valid_request_body)
        result = command.execute()
        
        assert result["status_code"] == 500
        assert "Error publishing to Pub/Sub: PubSub Error" in result["response"]["msg"]
