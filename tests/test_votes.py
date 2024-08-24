import pytest
from app import models


def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[0].id, "direction": 1}
    )
    assert res.status_code == 201


@pytest.fixture
def test_vote(test_posts, session, test_user):
    vote = models.Vote(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(vote)
    session.commit()


def test_vote_twice_on_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "direction": 1}
    )
    assert res.status_code == 409
    assert res.json()["detail"] == "You have already voted on this post"


def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "direction": 0}
    )
    assert res.status_code == 201


def test_delete_vote_not_found(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "direction": 0}
    )
    assert res.status_code == 404
    assert res.json()["detail"] == "Vote not found"


def test_vote_on_nonexistent_post(authorized_client):
    res = authorized_client.post("/vote/", json={"post_id": 10000, "direction": 1})
    assert res.status_code == 404
    assert res.json()["detail"] == "Post not found"


def test_unauthorized_vote(client, test_posts):
    res = client.post("/vote/", json={"post_id": 1, "direction": 1})
    assert res.status_code == 401
