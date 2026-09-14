"""
Tests for the root endpoint GET /.
"""

import pytest


def test_root_redirects_to_static_index_html(client):
    """
    Arrange: Make a GET request to /
    Act: Send the request
    Assert: Verify it redirects to /static/index.html
    """
    # Arrange & Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307  # Temporary redirect status
    assert response.headers["location"] == "/static/index.html"


def test_root_with_follow_redirects(client):
    """
    Arrange: Make a GET request to / with follow_redirects=True
    Act: Send the request
    Assert: Verify redirect chain works correctly
    """
    # Arrange & Act
    response = client.get("/", follow_redirects=True)
    
    # Assert - in test context, static files are served
    assert response.status_code == 200
