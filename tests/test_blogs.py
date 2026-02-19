"""
Tests for Blog API endpoints.

This file demonstrates how to test blog-related endpoints.
"""

import pytest
from fastapi import status


class TestCreateBlog:
    """Tests for POST /api/{version}/blogs/ endpoint."""

    def test_create_blog_success(self, client, sample_user_data, sample_blog_data, api_prefix):
        """Test successful blog creation (authenticated)."""
        # First create a user (author)
        user_response = client.post(f"{api_prefix}/users/", json=sample_user_data)
        user_id = user_response.json()["id"]

        # Login to get auth token
        login_response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": sample_user_data["email"], "password": sample_user_data["password"]}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create blog with the user's ID
        blog_data = {**sample_blog_data, "author_id": user_id}
        response = client.post(f"{api_prefix}/blogs/", json=blog_data, headers=headers)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == sample_blog_data["title"]
        assert data["content"] == sample_blog_data["content"]
        assert "id" in data

    def test_create_blog_unauthorized(self, client, sample_user_data, sample_blog_data, api_prefix):
        """Test that creating a blog without authentication fails."""
        # Create a user first
        user_response = client.post(f"{api_prefix}/users/", json=sample_user_data)
        user_id = user_response.json()["id"]

        # Try to create blog without auth
        blog_data = {**sample_blog_data, "author_id": user_id}
        response = client.post(f"{api_prefix}/blogs/", json=blog_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_blog_missing_title(self, client, sample_user_data, api_prefix):
        """Test that creating a blog without title fails."""
        # Create a user and login
        user_response = client.post(f"{api_prefix}/users/", json=sample_user_data)
        user_id = user_response.json()["id"]

        login_response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": sample_user_data["email"], "password": sample_user_data["password"]}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        incomplete_data = {
            "content": "Some content",
            "author_id": user_id
        }

        response = client.post(f"{api_prefix}/blogs/", json=incomplete_data, headers=headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_blog_empty_content(self, client, sample_user_data, api_prefix):
        """Test creating a blog with empty content."""
        # Create a user and login
        user_response = client.post(f"{api_prefix}/users/", json=sample_user_data)
        user_id = user_response.json()["id"]

        login_response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": sample_user_data["email"], "password": sample_user_data["password"]}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        blog_data = {
            "title": "Test Title",
            "content": "",
            "author_id": user_id
        }

        response = client.post(f"{api_prefix}/blogs/", json=blog_data, headers=headers)

        # This might succeed or fail based on your validation rules
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_422_UNPROCESSABLE_ENTITY
        ]


class TestGetBlogs:
    """Tests for GET /api/{version}/blogs/ endpoint."""

    def test_get_all_blogs_empty(self, client, api_prefix):
        """Test getting blogs when database is empty."""
        response = client.get(f"{api_prefix}/blogs/")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_get_all_blogs_with_data(self, client, sample_user_data, sample_blog_data, api_prefix):
        """Test getting blogs when blogs exist."""
        # Create a user and login
        user_response = client.post(f"{api_prefix}/users/", json=sample_user_data)
        user_id = user_response.json()["id"]

        login_response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": sample_user_data["email"], "password": sample_user_data["password"]}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create a blog
        blog_data = {**sample_blog_data, "author_id": user_id}
        client.post(f"{api_prefix}/blogs/", json=blog_data, headers=headers)

        response = client.get(f"{api_prefix}/blogs/")

        assert response.status_code == status.HTTP_200_OK
        blogs = response.json()
        assert len(blogs) == 1
        assert blogs[0]["title"] == sample_blog_data["title"]

    def test_get_multiple_blogs(self, client, sample_user_data, api_prefix):
        """Test getting multiple blogs."""
        # Create a user and login
        user_response = client.post(f"{api_prefix}/users/", json=sample_user_data)
        user_id = user_response.json()["id"]

        login_response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": sample_user_data["email"], "password": sample_user_data["password"]}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create multiple blogs
        for i in range(3):
            blog_data = {
                "title": f"Blog {i}",
                "content": f"Content {i}",
                "author_id": user_id
            }
            client.post(f"{api_prefix}/blogs/", json=blog_data, headers=headers)

        response = client.get(f"{api_prefix}/blogs/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 3


class TestGetBlogById:
    """Tests for GET /api/{version}/blogs/{blog_id} endpoint."""

    def test_get_blog_by_id_success(self, client, sample_user_data, sample_blog_data, api_prefix):
        """Test getting a blog by valid ID."""
        # Create a user and login
        user_response = client.post(f"{api_prefix}/users/", json=sample_user_data)
        user_id = user_response.json()["id"]

        login_response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": sample_user_data["email"], "password": sample_user_data["password"]}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create a blog
        blog_data = {**sample_blog_data, "author_id": user_id}
        create_response = client.post(f"{api_prefix}/blogs/", json=blog_data, headers=headers)
        blog_id = create_response.json()["id"]

        response = client.get(f"{api_prefix}/blogs/{blog_id}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == blog_id
        assert response.json()["title"] == sample_blog_data["title"]

    def test_get_blog_by_id_not_found(self, client, api_prefix):
        """Test getting a blog with non-existent ID."""
        response = client.get(f"{api_prefix}/blogs/9999")

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateBlog:
    """Tests for PUT /api/{version}/blogs/{blog_id} endpoint."""

    def test_update_blog_success(self, client, sample_user_data, sample_blog_data, api_prefix):
        """Test successful blog update (authenticated)."""
        # Create a user and login
        user_response = client.post(f"{api_prefix}/users/", json=sample_user_data)
        user_id = user_response.json()["id"]

        login_response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": sample_user_data["email"], "password": sample_user_data["password"]}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create a blog
        blog_data = {**sample_blog_data, "author_id": user_id}
        create_response = client.post(f"{api_prefix}/blogs/", json=blog_data, headers=headers)
        blog_id = create_response.json()["id"]

        # Update the blog
        updated_data = {
            "title": "Updated Title",
            "content": "Updated content",
            "author_id": user_id
        }
        response = client.put(f"{api_prefix}/blogs/{blog_id}", json=updated_data, headers=headers)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == updated_data["title"]
        assert response.json()["content"] == updated_data["content"]

    def test_update_blog_unauthorized(self, client, sample_user_data, sample_blog_data, api_prefix):
        """Test that updating a blog without authentication fails."""
        # Create a user and login to create blog
        user_response = client.post(f"{api_prefix}/users/", json=sample_user_data)
        user_id = user_response.json()["id"]

        login_response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": sample_user_data["email"], "password": sample_user_data["password"]}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create a blog
        blog_data = {**sample_blog_data, "author_id": user_id}
        create_response = client.post(f"{api_prefix}/blogs/", json=blog_data, headers=headers)
        blog_id = create_response.json()["id"]

        # Try to update without auth
        updated_data = {
            "title": "Updated Title",
            "content": "Updated content",
            "author_id": user_id
        }
        response = client.put(f"{api_prefix}/blogs/{blog_id}", json=updated_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_blog_not_found(self, client, sample_user_data, sample_blog_data, api_prefix):
        """Test updating a non-existent blog."""
        # Create a user and login
        client.post(f"{api_prefix}/users/", json=sample_user_data)
        login_response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": sample_user_data["email"], "password": sample_user_data["password"]}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.put(f"{api_prefix}/blogs/9999", json=sample_blog_data, headers=headers)

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteBlog:
    """Tests for DELETE /api/{version}/blogs/{blog_id} endpoint."""

    def test_delete_blog_success(self, client, sample_user_data, sample_blog_data, api_prefix):
        """Test successful blog deletion (authenticated)."""
        # Create a user and login
        user_response = client.post(f"{api_prefix}/users/", json=sample_user_data)
        user_id = user_response.json()["id"]

        login_response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": sample_user_data["email"], "password": sample_user_data["password"]}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create a blog
        blog_data = {**sample_blog_data, "author_id": user_id}
        create_response = client.post(f"{api_prefix}/blogs/", json=blog_data, headers=headers)
        blog_id = create_response.json()["id"]

        # Delete the blog
        response = client.delete(f"{api_prefix}/blogs/{blog_id}", headers=headers)

        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_204_NO_CONTENT
        ]

        # Verify blog is deleted
        get_response = client.get(f"{api_prefix}/blogs/{blog_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_blog_unauthorized(self, client, sample_user_data, sample_blog_data, api_prefix):
        """Test that deleting a blog without authentication fails."""
        # Create a user and login to create blog
        user_response = client.post(f"{api_prefix}/users/", json=sample_user_data)
        user_id = user_response.json()["id"]

        login_response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": sample_user_data["email"], "password": sample_user_data["password"]}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create a blog
        blog_data = {**sample_blog_data, "author_id": user_id}
        create_response = client.post(f"{api_prefix}/blogs/", json=blog_data, headers=headers)
        blog_id = create_response.json()["id"]

        # Try to delete without auth
        response = client.delete(f"{api_prefix}/blogs/{blog_id}")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_blog_not_found(self, client, sample_user_data, api_prefix):
        """Test deleting a non-existent blog."""
        # Create a user and login
        client.post(f"{api_prefix}/users/", json=sample_user_data)
        login_response = client.post(
            f"{api_prefix}/auth/login",
            data={"username": sample_user_data["email"], "password": sample_user_data["password"]}
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.delete(f"{api_prefix}/blogs/9999", headers=headers)

        assert response.status_code == status.HTTP_404_NOT_FOUND
