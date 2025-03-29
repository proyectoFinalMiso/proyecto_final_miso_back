import pytest
from unittest.mock import patch
from flask import Flask

from src.commands.health_check import HealthCheck

class TestHealthCheck:
    def test_execute_returns_200_response(self):
        # Arrange
        command = HealthCheck()
        
        # Act
        response, status_code = command.execute()
        
        # Assert
        assert status_code == 200
        
        # Convert response to json
        json_data = response.get_json()
        assert "message" in json_data
        assert json_data["message"] == "pong" 
