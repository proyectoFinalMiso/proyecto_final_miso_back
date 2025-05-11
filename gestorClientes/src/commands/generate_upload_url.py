import os
import datetime
import re
import uuid
from google.cloud import storage
from src.commands.base_command import BaseCommand

class GenerateUploadUrl(BaseCommand):
    def __init__(self, request_body: dict):
        self.body = request_body
        self.GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME")

    def check_campos_requeridos(self) -> bool:
        required_fields = ["filename", "contentType"]
        return all(field in self.body and self.body.get(field) for field in required_fields)

    def execute(self):
        if not self.GCS_BUCKET_NAME:
            return {
                "response": {"msg": "GCS_BUCKET_NAME environment variable not set."},
                "status_code": 500
            }

        if not self.check_campos_requeridos():
            return {
                "response": {"msg": "Missing required fields: filename, contentType"},
                "status_code": 400
            }

        filename = self.body["filename"]
        content_type = self.body["contentType"]

        blob_name = filename

        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(self.GCS_BUCKET_NAME)
            blob = bucket.blob(blob_name)

            signed_url = blob.generate_signed_url(
                version="v4",
                expiration=datetime.timedelta(minutes=15),
                method="PUT",
                content_type=content_type,
            )
            
            gcs_path = f"gs://{self.GCS_BUCKET_NAME}/{blob_name}"

            return {
                "response": {
                    "signedUrl": signed_url,
                    "gcsPath": gcs_path
                },
                "status_code": 200
            }
        except Exception as e:
            print(f"Error generating signed URL: {e}")
            return {
                "response": {"msg": f"Error generating signed URL: {str(e)}"},
                "status_code": 500
            }
