"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest
from urllib.parse import quote


def test_signup_new_participant_success(client):
    """
    Arrange: Valid activity and new email
    Act: POST signup request
    Assert: Returns 200 with success message and participant is added
    """
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup?email={email}",
        headers={"accept": "application/json"}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert email in response.json()["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity]["participants"]


def test_signup_duplicate_email_returns_400(client):
    """
    Arrange: Try to signup with email already registered
    Act: POST signup request with existing participant
    Assert: Returns 400 with error message
    """
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup?email={email}",
        headers={"accept": "application/json"}
    )
    
    # Assert
    assert response.status_code == 400
    assert "already" in response.json()["detail"].lower()


def test_signup_activity_not_found_returns_404(client):
    """
    Arrange: Try to signup for non-existent activity
    Act: POST signup request to invalid activity
    Assert: Returns 404 with error message
    """
    # Arrange
    activity = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup?email={email}",
        headers={"accept": "application/json"}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_signup_multiple_participants_same_activity(client):
    """
    Arrange: Add different emails to same activity
    Act: POST multiple signup requests
    Assert: All participants are added successfully
    """
    # Arrange
    activity = "Programming Class"
    new_emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
    
    # Act & Assert
    for email in new_emails:
        response = client.post(
            f"/activities/{activity}/signup?email={email}",
            headers={"accept": "application/json"}
        )
        assert response.status_code == 200
    
    # Verify all participants were added
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity]["participants"]
    for email in new_emails:
        assert email in participants


def test_signup_response_message_format(client):
    """
    Arrange: Valid signup request
    Act: POST signup request
    Assert: Response message has expected format
    """
    # Arrange
    activity = "Gym Class"
    email = "athlete@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup?email={email}",
        headers={"accept": "application/json"}
    )
    
    # Assert
    assert response.status_code == 200
    message = response.json()["message"]
    assert email in message
    assert activity in message
    assert "Signed up" in message


def test_signup_with_special_characters_in_email(client):
    """
    Arrange: Email with special characters (valid format)
    Act: POST signup request with proper URL encoding
    Assert: Participant is added successfully
    """
    # Arrange
    activity = "Chess Club"
    email = "student.name+tag@mergington.edu"
    
    # Act - Use quote to properly encode the email in the URL
    response = client.post(
        f"/activities/{activity}/signup?email={quote(email)}",
        headers={"accept": "application/json"}
    )
    
    # Assert
    assert response.status_code == 200
    
    # Verify participant was added
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity]["participants"]
