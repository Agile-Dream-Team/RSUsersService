from sqlalchemy.orm import Session
from app.domain.camera import Camera


class CameraRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, image: Camera):
        try:
            self.db_session.add(image)
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_all(self):
        return self.db_session.query(Camera).all()

    def get_by_id(self, uuid):
        pass

    def delete(self, image):
        pass

    def update(self, image):
        pass




