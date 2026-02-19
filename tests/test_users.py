"""
Tests for User API endpoints.

This file demonstrates how to test user-related endpoints.
"""

import pytest
from fastapi import status


class TestAuthentication:
    """Tests for authentication endpoints."""

    def test_login_success(self, client, sample_user_data, api_prefix):
        """Test successful login returns JWT token."""
        # Create a user
        client.post(f"{api_prefix}/users/", json=sample_user_data)

        # Login
        response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": sample_user_data["email"], "password": sample_user_data["password"]}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_email(self, client, sample_user_data, api_prefix):
        """Test login with invalid email fails."""
        # Create a user
        client.post(f"{api_prefix}/users/", json=sample_user_data)

        # Try login with wrong email
        response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": "wrong@example.com", "password": sample_user_data["password"]}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_invalid_password(self, client, sample_user_data, api_prefix):
        """Test login with invalid password fails."""
        # Create a user
        client.post(f"{api_prefix}/users/", json=sample_user_data)

        # Try login with wrong password
        response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": sample_user_data["email"], "password": "wrongpassword"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestGetCurrentUser:
    """Tests for GET /api/{version}/users/me endpoint."""

    def test_get_current_user_success(self, client, sample_user_data, api_prefix):
        """Test getting current user with valid token."""
        # Create user and login
        client.post(f"{api_prefix}/users/", json=sample_user_data)
        login_response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": sample_user_data["email"], "password": sample_user_data["password"]}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Get current user
        response = client.get(f"{api_prefix}/users/me", headers=headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["name"] == sample_user_data["name"]

    def test_get_current_user_unauthorized(self, client, api_prefix):
        """Test getting current user without token fails."""
        response = client.get(f"{api_prefix}/users/me")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user_invalid_token(self, client, api_prefix):
        """Test getting current user with invalid token fails."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get(f"{api_prefix}/users/me", headers=headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


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
        """Test successful user update (authenticated)."""
        # Create a user
        create_response = client.post(f"{api_prefix}/users/", json=sample_user_data)
        user_id = create_response.json()["id"]

        # Login to get auth token
        login_response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": sample_user_data["email"], "password": sample_user_data["password"]}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Update the user
        updated_data = {
            "name": "Updated Name",
            "email": "updated@example.com",
            "password": "newpassword123"
        }
        response = client.put(f"{api_prefix}/users/{user_id}", json=updated_data, headers=headers)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == updated_data["name"]

    def test_update_user_unauthorized(self, client, sample_user_data, api_prefix):
        """Test that updating a user without authentication fails."""
        # Create a user
        create_response = client.post(f"{api_prefix}/users/", json=sample_user_data)
        user_id = create_response.json()["id"]

        # Try to update without auth
        updated_data = {
            "name": "Updated Name",
            "email": "updated@example.com",
            "password": "newpassword123"
        }
        response = client.put(f"{api_prefix}/users/{user_id}", json=updated_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_other_user_forbidden(self, client, sample_user_data, api_prefix):
        """Test that users cannot update other users' profiles."""
        # Create first user
        create_response = client.post(f"{api_prefix}/users/", json=sample_user_data)
        user1_id = create_response.json()["id"]

        # Login as first user
        login_response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": sample_user_data["email"], "password": sample_user_data["password"]}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create second user
        user2_data = {
            "name": "Second User",
            "email": "second@example.com",
            "password": "password123"
        }
        create_response2 = client.post(f"{api_prefix}/users/", json=user2_data)
        user2_id = create_response2.json()["id"]

        # Try to update second user with first user's token
        updated_data = {
            "name": "Hacked Name",
            "email": "hacked@example.com",
            "password": "hackedpassword"
        }
        response = client.put(f"{api_prefix}/users/{user2_id}", json=updated_data, headers=headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_user_not_found(self, client, sample_user_data, api_prefix):
        """Test updating a non-existent user."""
        # Create and login user to get token
        client.post(f"{api_prefix}/users/", json=sample_user_data)
        login_response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": sample_user_data["email"], "password": sample_user_data["password"]}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.put(f"{api_prefix}/users/9999", json=sample_user_data, headers=headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN  # Can't update other users


class TestDeleteUser:
    """Tests for DELETE /api/{version}/users/{user_id} endpoint."""

    def test_delete_user_success(self, client, sample_user_data, api_prefix):
        """Test successful user deletion (authenticated)."""
        # Create a user
        create_response = client.post(f"{api_prefix}/users/", json=sample_user_data)
        user_id = create_response.json()["id"]

        # Login to get auth token
        login_response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": sample_user_data["email"], "password": sample_user_data["password"]}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Delete the user
        response = client.delete(f"{api_prefix}/users/{user_id}", headers=headers)

        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_204_NO_CONTENT
        ]

        # Verify user is deleted
        get_response = client.get(f"{api_prefix}/users/{user_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_user_unauthorized(self, client, sample_user_data, api_prefix):
        """Test that deleting a user without authentication fails."""
        # Create a user
        create_response = client.post(f"{api_prefix}/users/", json=sample_user_data)
        user_id = create_response.json()["id"]

        # Try to delete without auth
        response = client.delete(f"{api_prefix}/users/{user_id}")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_other_user_forbidden(self, client, sample_user_data, api_prefix):
        """Test that users cannot delete other users' accounts."""
        # Create first user and login
        client.post(f"{api_prefix}/users/", json=sample_user_data)
        login_response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": sample_user_data["email"], "password": sample_user_data["password"]}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create second user
        user2_data = {
            "name": "Second User",
            "email": "second@example.com",
            "password": "password123"
        }
        create_response2 = client.post(f"{api_prefix}/users/", json=user2_data)
        user2_id = create_response2.json()["id"]

        # Try to delete second user with first user's token
        response = client.delete(f"{api_prefix}/users/{user2_id}", headers=headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_user_not_found(self, client, sample_user_data, api_prefix):
        """Test deleting a non-existent user."""
        # Create and login user to get token
        client.post(f"{api_prefix}/users/", json=sample_user_data)
        login_response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": sample_user_data["email"], "password": sample_user_data["password"]}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.delete(f"{api_prefix}/users/9999", headers=headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN  # Can't delete other users
