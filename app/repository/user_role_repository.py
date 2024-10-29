from sqlalchemy.orm import Session
from app.domain.user_role import UserRole


class RoleRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, user_role: UserRole):
        try:
            self.db_session.add(user_role)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_all(self):
        return self.db_session.query(UserRole).all()

    def get_by_id(self, user_role_id):
        return self.db_session.query(UserRole).filter(UserRole.id == user_role_id).first()

    def delete(self, user_role_id):
        pass

    def update(self, user_role_id):
        pass




