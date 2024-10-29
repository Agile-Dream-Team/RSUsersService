from sqlalchemy.orm import Session
from app.domain.user import User


class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, user: User):
        try:
            self.db_session.add(user)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_all(self):
        return self.db_session.query(User).all()

    def get_by_id(self, user_id):
        return self.db_session.query(User).filter(User.id == user_id).first()

    def delete(self, user_id):
        pass

    def update(self, user_id):
        pass




