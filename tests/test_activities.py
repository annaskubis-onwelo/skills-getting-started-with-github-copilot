"""
Tests for the GET /activities endpoint.
"""

import pytest


def test_get_activities_returns_all_activities(client, test_activities_data):
    """
    Arrange: Test data contains 3 activities
    Act: Send GET request to /activities
    Assert: Response contains all activities with correct structure
    """
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert len(activities) == 3
    assert set(activities.keys()) == set(test_activities_data.keys())


def test_get_activities_response_structure(client):
    """
    Arrange: Request /activities endpoint
    Act: Send GET request
    Assert: Each activity has required fields
    """
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    required_fields = {"description", "schedule", "max_participants", "participants"}
    for activity_name, activity_details in activities.items():
        assert isinstance(activity_name, str)
        assert isinstance(activity_details, dict)
        assert required_fields.issubset(activity_details.keys())


def test_get_activities_participants_format(client):
    """
    Arrange: Request /activities endpoint
    Act: Send GET request
    Assert: Participants list is properly formatted as array of emails
    """
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_details in activities.items():
        assert isinstance(activity_details["participants"], list)
        assert len(activity_details["participants"]) > 0
        for participant in activity_details["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant  # Basic email format check


def test_get_activities_max_participants_is_integer(client):
    """
    Arrange: Request /activities endpoint
    Act: Send GET request
    Assert: max_participants is an integer
    """
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_details in activities.items():
        assert isinstance(activity_details["max_participants"], int)
        assert activity_details["max_participants"] > 0


def test_get_activities_chess_club_details(client):
    """
    Arrange: Test data includes Chess Club
    Act: Send GET request to /activities
    Assert: Chess Club has expected details and participants
    """
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert "Chess Club" in activities
    chess_club = activities["Chess Club"]
    assert chess_club["max_participants"] == 12
    assert len(chess_club["participants"]) == 2
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]
