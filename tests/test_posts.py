from typing import List
from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    posts = [schemas.PostOut(**post) for post in res.json()]

    assert len(posts) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_found(authorized_client, test_posts):
    res = authorized_client.get("/posts/10000")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())

    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert post.Post.user_id == test_posts[0].user_id
    assert res.status_code == 200


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("new title", "new content", True),
        ("new title 2", "new content 2", False),
        ("new title 3", "new content 3", True),
        ("new title 4", "new content 4", False),
    ],
)
def test_create_post(authorized_client, test_user, title, content, published):
    post_data = {"title": title, "content": content, "published": published}
    res = authorized_client.post("/posts/", json=post_data)
    post = schemas.Post(**res.json())

    assert post.title == title
    assert post.content == content
    assert post.published == published
    assert post.user_id == test_user["id"]
    assert res.status_code == 201


def test_create_post_default_published_true(authorized_client, test_user):
    post_data = {"title": "title", "content": "content"}
    res = authorized_client.post("/posts/", json=post_data)
    post = schemas.Post(**res.json())

    assert post.title == "title"
    assert post.content == "content"
    assert post.published == True
    assert post.user_id == test_user["id"]
    assert res.status_code == 201


def test_unauthorized_create_posts(client):
    post_data = {"title": "title", "content": "content"}
    res = client.post("/posts/", json=post_data)
    assert res.status_code == 401


def test_unauthorized_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_not_found(authorized_client):
    res = authorized_client.delete("/posts/10000")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_posts):
    post_data = {"title": "new title", "content": "new content"}
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=post_data)
    post = schemas.Post(**res.json())

    assert post.title == "new title"
    assert post.content == "new content"
    assert res.status_code == 200


def test_update_other_user_post(authorized_client, test_posts):
    post_data = {"title": "new title", "content": "new content"}
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=post_data)
    assert res.status_code == 403


def test_update_post_not_found(authorized_client):
    post_data = {"title": "new title", "content": "new content"}
    res = authorized_client.put("/posts/10000", json=post_data)
    assert res.status_code == 404


def test_unauthorized_update_post(client, test_posts):
    post_data = {"title": "new title", "content": "new content"}
    res = client.put(f"/posts/{test_posts[0].id}", json=post_data)
    assert res.status_code == 401
