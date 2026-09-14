"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint.
"""

import pytest


def test_unregister_existing_participant_success(client):
    """
    Arrange: Valid activity and registered participant
    Act: DELETE unregister request
    Assert: Returns 200 with success message and participant is removed
    """
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    
    # Act
    response = client.delete(
        f"/activities/{activity}/unregister?email={email}",
        headers={"accept": "application/json"}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    assert email in response.json()["message"]
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity]["participants"]


def test_unregister_participant_not_registered_returns_400(client):
    """
    Arrange: Try to unregister from activity participant is not in
    Act: DELETE unregister request
    Assert: Returns 400 with error message
    """
    # Arrange
    activity = "Chess Club"
    email = "notregistered@mergington.edu"  # Not registered
    
    # Act
    response = client.delete(
        f"/activities/{activity}/unregister?email={email}",
        headers={"accept": "application/json"}
    )
    
    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"].lower()


def test_unregister_activity_not_found_returns_404(client):
    """
    Arrange: Try to unregister from non-existent activity
    Act: DELETE unregister request to invalid activity
    Assert: Returns 404 with error message
    """
    # Arrange
    activity = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity}/unregister?email={email}",
        headers={"accept": "application/json"}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_signup_then_unregister_workflow(client):
    """
    Arrange: Sign up for activity then unregister
    Act: POST signup, then DELETE unregister
    Assert: Workflow succeeds at each step
    """
    # Arrange
    activity = "Programming Class"
    email = "workflow@mergington.edu"
    
    # Act - Sign up
    signup_response = client.post(
        f"/activities/{activity}/signup?email={email}",
        headers={"accept": "application/json"}
    )
    assert signup_response.status_code == 200
    
    # Act - Verify added
    activities_check = client.get("/activities")
    assert email in activities_check.json()[activity]["participants"]
    
    # Act - Unregister
    unregister_response = client.delete(
        f"/activities/{activity}/unregister?email={email}",
        headers={"accept": "application/json"}
    )
    assert unregister_response.status_code == 200
    
    # Act - Verify removed
    activities_check2 = client.get("/activities")
    assert email not in activities_check2.json()[activity]["participants"]


def test_signup_then_unregister_then_signup_again(client):
    """
    Arrange: Sign up, unregister, and sign up again
    Act: Perform the sequence
    Assert: All operations succeed (duplicate check is cleared)
    """
    # Arrange
    activity = "Gym Class"
    email = "returnstudent@mergington.edu"
    
    # Act - First signup
    response1 = client.post(
        f"/activities/{activity}/signup?email={email}",
        headers={"accept": "application/json"}
    )
    assert response1.status_code == 200
    
    # Act - Unregister
    response2 = client.delete(
        f"/activities/{activity}/unregister?email={email}",
        headers={"accept": "application/json"}
    )
    assert response2.status_code == 200
    
    # Act - Second signup (should succeed now)
    response3 = client.post(
        f"/activities/{activity}/signup?email={email}",
        headers={"accept": "application/json"}
    )
    assert response3.status_code == 200
    
    # Assert - Verify participant is added again
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity]["participants"]


def test_unregister_all_participants_one_by_one(client):
    """
    Arrange: Activity has multiple participants
    Act: Unregister each participant
    Assert: All removed successfully
    """
    # Arrange
    activity = "Chess Club"
    initial_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    # Act & Assert
    for email in initial_participants:
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}",
            headers={"accept": "application/json"}
        )
        assert response.status_code == 200
    
    # Verify all participants are removed
    activities_response = client.get("/activities")
    assert len(activities_response.json()[activity]["participants"]) == 0


def test_unregister_response_message_format(client):
    """
    Arrange: Valid unregister request
    Act: DELETE unregister request
    Assert: Response message has expected format
    """
    # Arrange
    activity = "Chess Club"
    email = "daniel@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity}/unregister?email={email}",
        headers={"accept": "application/json"}
    )
    
    # Assert
    assert response.status_code == 200
    message = response.json()["message"]
    assert email in message
    assert activity in message
    assert "Unregistered" in message
