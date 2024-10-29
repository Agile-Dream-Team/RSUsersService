from sqlalchemy.orm import Session
from app.domain.role import Role


class RoleRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, role: Role):
        try:
            self.db_session.add(role)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_all(self):
        return self.db_session.query(Role).all()

    def get_by_id(self, role_id):
        return self.db_session.query(Role).filter(Role.id == role_id).first()

    def delete(self, role_id):
        pass

    def update(self, role_id):
        pass




