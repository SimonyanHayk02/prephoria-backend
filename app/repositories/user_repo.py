from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:
    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create(db: Session, email: str, hashed_password: str, full_name: str | None = None):
        user = User(email=email, hashed_password=hashed_password, full_name=full_name)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def update(db: Session, user: User, full_name: str | None):
        user.full_name = full_name
        db.commit()
        db.refresh(user)
        return user
