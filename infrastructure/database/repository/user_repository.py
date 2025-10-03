from sqlalchemy.orm import Session
from infrastructure.database.models import UserEntity


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> UserEntity | None:
        return (
            self.session.query(UserEntity)
            .filter(UserEntity.id == user_id)
            .first()
        )

    def get_by_email(self, email: str) -> UserEntity | None:
        return (
            self.session.query(UserEntity).
            filter(UserEntity.email == email).
            first()
        )

    def list(self) -> list[UserEntity]:
        return self.session.query(UserEntity).all()

    def add(self, user: UserEntity) -> UserEntity:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: UserEntity) -> None:
        self.session.delete(user)
        self.session.commit()
