import requests
from requests.auth import HTTPBasicAuth


class BaseHttpAdapter:
    def __init__(self, url:str, auth_credentials:dict = None):
        self.session = requests.Session()
        self.url = url
        self.auth_credentials = auth_credentials

    def authenticate(self):
        """
        Sets up HTTP Basic Authentication for the session.
        """
        if self.auth_credentials and "username" in self.auth_credentials and "password" in self.auth_credentials:
            self.session.auth = HTTPBasicAuth(
                self.auth_credentials["username"], self.auth_credentials["password"]
            )
        else:
            raise ValueError("Invalid or missing authentication credentials.")