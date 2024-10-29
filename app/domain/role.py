from sqlalchemy import Column, BigInteger, Sequence, ForeignKey, VARCHAR, TIMESTAMP
from sqlalchemy.orm import relationship
from .base import Base


class Role(Base):
    __tablename__ = 'role'

    id = Column(BigInteger, Sequence('role_id_seq'), primary_key=True)
    name = Column(VARCHAR(255), unique=True, nullable=False)
    description = Column(VARCHAR(255))

    # Relationships
    users = relationship("UserRole", back_populates="role")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }