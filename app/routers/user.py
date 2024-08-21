from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app import schemas, models, utils
from app.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.model_dump())
    check_existing = (
        db.query(models.User).filter(models.User.email == new_user.email).first()
    )
    if check_existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserRead)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} not found",
        )
    return user
