"""
API tests for JSONPlaceholder posts endpoints.

This test suite covers:
- GET /posts/{id} — fetching post details (valid and invalid IDs)
- GET /users/{id} — fetching user details
- POST /posts — creating new posts
- PUT /posts/{id} — updating existing posts
- DELETE /posts/{id} — deleting and simulating deletion (valid and invalid IDs)

Notes:
    - The API is a mock service. POST, PUT, and DELETE operations are faked.
    - Only GET requests return real persisted data.
"""


import pytest
import requests
from pytest_html import extras as html_extras



# -------------------------------------------------------------------------------------
# GET
# -------------------------------------------------------------------------------------
@pytest.mark.parametrize("post_id, expected_title, expected_status_code", [
    (1, "sunt aut facere repellat provident occaecati excepturi optio reprehenderit", 200),
    (2, "qui est esse", 200),
])
def test_get_post_by_id(api_base_url, post_id, expected_title, expected_status_code, record_property, extras):
    """Tests GET /posts/{id} endpoint returns correct data."""
    response = requests.get(f"{api_base_url}/posts/{post_id}")
    data = response.json()

    record_property("url", response.url)
    record_property("status_code", response.status_code)
    record_property("title", data["title"])

    extras.append(html_extras.html(
        f"<div style='padding:4px;margin:2px;border:1px solid #ccc;border-radius:5px; background: #e3f2fd;'>"
        f"<b>GET /posts/{post_id}</b><br>"
        f"Status: {response.status_code}<br>"
        f"Title: {data['title']}</div>"
    ))

    assert response.status_code == expected_status_code
    assert data["id"] == post_id
    assert data["title"] == expected_title


@pytest.mark.parametrize("user_id, expected_user_name, expected_status_code", [
    (1, "Bret", 200),
    (10, "Moriah.Stanton", 200),
])
def test_get_user_name_by_id(api_base_url, user_id, expected_user_name, expected_status_code, record_property, extras):
    """Tests GET /users/{id} endpoint returns correct data."""
    response = requests.get(f"{api_base_url}/users/{user_id}")
    data = response.json()

    record_property("url", response.url)
    record_property("status_code", response.status_code)
    record_property("username", data["username"])

    extras.append(html_extras.html(
        f"<div style='padding:4px;margin:2px;border:1px solid #ccc;border-radius:5px;'>"
        f"<b>GET /users/{user_id}</b><br>"
        f"Status: {response.status_code}<br>"
        f"Username: {data['username']}</div>"
    ))

    assert response.status_code == expected_status_code
    assert data["id"] == user_id
    assert data["username"] == expected_user_name


@pytest.mark.parametrize("invalid_id, expected_status_code", [
    (0, 404),
    (9999, 404),
    (-1, 404),
])
def test_get_post_invalid_id_returns_404(api_base_url, invalid_id, expected_status_code, record_property, extras):
    """Ensures GET /posts/{id} returns 404 for non-existent IDs."""
    response = requests.get(f"{api_base_url}/posts/{invalid_id}")

    record_property("url", response.url)
    record_property("status_code", response.status_code)

    extras.append(html_extras.html(
        f"<b>GET /posts/{invalid_id}</b><br>Status: {response.status_code}"
    ))

    assert response.status_code == expected_status_code



# -------------------------------------------------------------------------------------
# CREATE
# -------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "title, body, user_id, expected_status",
    [
        ("pytest demo post", "This is a test post created during API testing.", 1, 201),
        ("second post", "Another body for API testing", 2, 201),
        ("empty title", "", 3, 201),
    ],
    ids=["normal_post", "another_post", "empty_body"]
)
def test_create_new_post(api_base_url, title, body, user_id, expected_status, record_property, extras):
    """Tests POST /posts endpoint with different payloads."""
    payload = {
        "title": title,
        "body": body,
        "userId": user_id
    }

    response = requests.post(f"{api_base_url}/posts", json=payload)
    data = response.json()

    record_property("url", response.url)
    record_property("status_code", response.status_code)
    record_property("response_id", data.get("id"))
    record_property("title_sent", title)

    extras.append(html_extras.html(
        f"<div style='padding:4px;margin:2px;border:1px solid #ccc;border-radius:5px;'>"
        f"<b>POST /posts</b><br>"
        f"Status: {response.status_code}<br>"
        f"Title: {data.get('title')}<br>"
        f"UserId: {data.get('userId')}<br>"
        f"Response ID: {data.get('id')}</div>"
    ))

    assert response.status_code == expected_status
    assert data["title"] == title
    assert data["body"] == body
    assert data["userId"] == user_id


# -------------------------------------------------------------------------------------
# UPDATE
# -------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "post_id, new_title, new_body, expected_status",
    [
        (1, "Updated title", "Updated body content", 200),
        (2, "Another update", "Different content here", 200),
    ],
    ids=["update_post_1", "update_post_2"]
)
def test_update_post(api_base_url, post_id, new_title, new_body, expected_status, record_property, extras):
    """Tests PUT /posts/{id} endpoint updates an existing resource."""
    payload = {
        "id": post_id,
        "title": new_title,
        "body": new_body
    }

    response = requests.put(f"{api_base_url}/posts/{post_id}", json=payload)
    data = response.json()

    record_property("url", response.url)
    record_property("status_code", response.status_code)
    record_property("updated_title", data.get("title"))

    extras.append(html_extras.html(
        f"<div style='padding:4px;margin:2px;border:1px solid #ccc;border-radius:5px;'>"
        f"<b>PUT /posts/{post_id}</b><br>"
        f"Status: {response.status_code}<br>"
        f"Title after update: {data.get('title')}</div>"
    ))

    assert response.status_code == expected_status
    assert data["title"] == new_title
    assert data["body"] == new_body
    assert data["id"] == post_id


# -------------------------------------------------------------------------------------
# DELETE
# -------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "post_id, expected_status",
    [
        (1, 200),
        (2, 200),
    ],
    ids=["delete_post_1", "delete_post_2"]
)
def test_delete_post(api_base_url, post_id, expected_status, record_property, extras):
    """Tests DELETE /posts/{id} endpoint removes a resource."""
    response = requests.delete(f"{api_base_url}/posts/{post_id}")

    record_property("url", response.url)
    record_property("status_code", response.status_code)

    extras.append(html_extras.html(
        f"<div style='padding:4px;margin:2px;border:1px solid #ccc;border-radius:5px;'>"
        f"<b>DELETE /posts/{post_id}</b><br>"
        f"Status: {response.status_code}</div>"
    ))

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "post_id, expected_status",
    [
        (9999, 200), # API always returns 200 (mock API behavior)
        (-1, 200),
        (0, 200),
    ],
    ids=["non_existent_post", "negative_id", "zero_id"]
)
def test_delete_invalid_post(api_base_url, post_id, expected_status, record_property, extras):
    """Tests DELETE /posts/{id} on invalid IDs (mock API always returns 200)."""
    response = requests.delete(f"{api_base_url}/posts/{post_id}")

    record_property("url", response.url)
    record_property("status_code", response.status_code)

    extras.append(html_extras.html(
        f"<div style='padding:4px;margin:2px;border:1px solid #ccc;border-radius:5px;'>"
        f"<b>DELETE /posts/{post_id}</b><br>"
        f"Status: {response.status_code}</div>"
    ))

    assert response.status_code == expected_status