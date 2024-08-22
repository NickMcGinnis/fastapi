from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import oauth2, schemas, models
from app.database import get_db

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: str = "",
):
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return posts


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    new_post = models.Post(user_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this post",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_posts(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    if post is not None and post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this post",
        )
    post_query.update(dict(updated_post), synchronize_session=False)
    db.commit()
    return post_query.first()
