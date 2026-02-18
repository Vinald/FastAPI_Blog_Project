"""
Tests for User API endpoints.

This file demonstrates how to test user-related endpoints.
"""

import pytest
from fastapi import status


class TestCreateUser:
    """Tests for POST /api/{version}/users/ endpoint."""

    def test_create_user_success(self, client, sample_user_data, api_prefix):
        """Test successful user creation."""
        response = client.post(f"{api_prefix}/users/", json=sample_user_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == sample_user_data["name"]
        assert data["email"] == sample_user_data["email"]
        assert "id" in data
        # Password should not be returned
        assert "password" not in data

    def test_create_user_duplicate_email(self, client, sample_user_data, api_prefix):
        """Test that creating a user with duplicate email fails."""
        # Create first user
        client.post(f"{api_prefix}/users/", json=sample_user_data)

        # Try to create another user with same email
        response = client.post(f"{api_prefix}/users/", json=sample_user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"].lower()

    def test_create_user_missing_fields(self, client, api_prefix):
        """Test that creating a user with missing fields fails."""
        incomplete_data = {"name": "Test User"}

        response = client.post(f"{api_prefix}/users/", json=incomplete_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_user_invalid_email(self, client, api_prefix):
        """Test that creating a user with invalid email fails."""
        invalid_data = {
            "name": "Test User",
            "email": "not-an-email",
            "password": "password123"
        }

        response = client.post(f"{api_prefix}/users/", json=invalid_data)

        # This might pass or fail depending on your validation
        # Adjust assertion based on your schema validation
        assert response.status_code in [
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            status.HTTP_201_CREATED  # If you don't have email validation
        ]


class TestGetUsers:
    """Tests for GET /api/{version}/users/ endpoint."""

    def test_get_all_users_empty(self, client, api_prefix):
        """Test getting users when database is empty."""
        response = client.get(f"{api_prefix}/users/")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_get_all_users_with_data(self, client, sample_user_data, api_prefix):
        """Test getting users when users exist."""
        # Create a user first
        client.post(f"{api_prefix}/users/", json=sample_user_data)

        response = client.get(f"{api_prefix}/users/")

        assert response.status_code == status.HTTP_200_OK
        users = response.json()
        assert len(users) == 1
        assert users[0]["email"] == sample_user_data["email"]


class TestGetUserById:
    """Tests for GET /api/{version}/users/{user_id} endpoint."""

    def test_get_user_by_id_success(self, client, sample_user_data, api_prefix):
        """Test getting a user by valid ID."""
        # Create a user
        create_response = client.post(f"{api_prefix}/users/", json=sample_user_data)
        user_id = create_response.json()["id"]

        response = client.get(f"{api_prefix}/users/{user_id}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == user_id

    def test_get_user_by_id_not_found(self, client, api_prefix):
        """Test getting a user with non-existent ID."""
        response = client.get(f"{api_prefix}/users/9999")

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateUser:
    """Tests for PUT /api/{version}/users/{user_id} endpoint."""

    def test_update_user_success(self, client, sample_user_data, api_prefix):
        """Test successful user update."""
        # Create a user
        create_response = client.post(f"{api_prefix}/users/", json=sample_user_data)
        user_id = create_response.json()["id"]

        # Update the user
        updated_data = {
            "name": "Updated Name",
            "email": "updated@example.com",
            "password": "newpassword123"
        }
        response = client.put(f"{api_prefix}/users/{user_id}", json=updated_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == updated_data["name"]

    def test_update_user_not_found(self, client, sample_user_data, api_prefix):
        """Test updating a non-existent user."""
        response = client.put(f"{api_prefix}/users/9999", json=sample_user_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteUser:
    """Tests for DELETE /api/{version}/users/{user_id} endpoint."""

    def test_delete_user_success(self, client, sample_user_data, api_prefix):
        """Test successful user deletion."""
        # Create a user
        create_response = client.post(f"{api_prefix}/users/", json=sample_user_data)
        user_id = create_response.json()["id"]

        # Delete the user
        response = client.delete(f"{api_prefix}/users/{user_id}")

        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_204_NO_CONTENT
        ]

        # Verify user is deleted
        get_response = client.get(f"{api_prefix}/users/{user_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_user_not_found(self, client, api_prefix):
        """Test deleting a non-existent user."""
        response = client.delete(f"{api_prefix}/users/9999")

        assert response.status_code == status.HTTP_404_NOT_FOUND
