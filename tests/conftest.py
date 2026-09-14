"""
Pytest configuration and shared fixtures for API tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def test_activities_data():
    """
    Fixture providing fresh test data for activities.
    Returns a copy of the activities dictionary to prevent test pollution.
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }


@pytest.fixture
def client(test_activities_data, monkeypatch):
    """
    Fixture providing a TestClient with isolated test data.
    Uses monkeypatch to replace the app's activities with test data.
    """
    # Replace the app's activities with test data
    monkeypatch.setattr("src.app.activities", test_activities_data)
    
    # Return a TestClient instance
    return TestClient(app)
