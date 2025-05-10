import os
import json
import datetime
from google.cloud import pubsub_v1
from src.commands.base_command import BaseCommand


class NotifyUploadComplete(BaseCommand):
    def __init__(self, request_body: dict):
        self.body = request_body
        self.PUB_SUB_TOPIC_NAME = os.environ.get("PUB_SUB_TOPIC_NAME")

    def check_campos_requeridos(self) -> bool:
        required_fields = ["blobPath", "clientId", "vendedorId"]
        return all(field in self.body and self.body.get(field) for field in required_fields)

    def execute(self):
        if not self.PUB_SUB_TOPIC_NAME:
            return {
                "response": {"msg": "PUB_SUB_TOPIC_NAME environment variable not set."},
                "status_code": 500
            }

        if not self.check_campos_requeridos():
            return {
                "response": {"msg": "Missing required fields: blobPath, clientId, vendedorId"},
                "status_code": 400
            }

        blob_path = self.body["blobPath"]
        client_id = self.body["clientId"]
        vendedor_id = self.body["vendedorId"]

        try:
            publisher = pubsub_v1.PublisherClient()
            topic_path = self.PUB_SUB_TOPIC_NAME

            message_data = {
                "Message": f"Video uploaded successfully: {blob_path}",
                "BlobPath": blob_path,
                "CreationDate": datetime.datetime.utcnow().isoformat() + "Z",
                "Customer": client_id,
                "Seller": vendedor_id
            }

            print(f"Publishing message to topic {topic_path}: {message_data}")
            
            json_message_bytes = json.dumps(message_data).encode("utf-8")

            future = publisher.publish(topic_path, json_message_bytes)
            message_id = future.result()

            return {
                "response": {
                    "message": "Upload notification sent successfully (Avro).",
                    "messageId": message_id
                },
                "status_code": 200
            }
        except Exception as e:
            print(f"Error publishing to Pub/Sub: {e}")
            return {
                "response": {"msg": f"Error publishing to Pub/Sub: {str(e)}"},
                "status_code": 500
            }
