from sqlalchemy.orm import Session
from fastapi import status, HTTPException, APIRouter, Depends

from ..database import get_db
from .. import models, schemas, utils


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserOut
)
def createUser(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash passowrd from user.passowrd

    # hashed_password = pwd_context.hash(user.password)

    check_user = db.query(models.User).filter(models.User.email == user.email).first()

    if check_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {user.email} already exists"
        )

    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exists"
        )

    return user
