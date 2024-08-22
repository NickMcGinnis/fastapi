from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from app import oauth2, schemas, models
from app.database import get_db

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    if (vote.direction != 1) and (vote.direction != 0):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vote direction must be 1 or 0",
        )

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()
    if vote.direction == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already voted on this post",
            )
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote not found",
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote removed"}
