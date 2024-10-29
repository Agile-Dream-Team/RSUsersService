from sqlalchemy import Column, BigInteger, Sequence, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class UserRole(Base):
    __tablename__ = 'user_role'

    id = Column(BigInteger, Sequence('user_role_id_seq'), primary_key=True)
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    role_id = Column(BigInteger, ForeignKey('role.id'), nullable=False)
    assigned_at = Column(TIMESTAMP(timezone=False), default=datetime.utcnow)
    assigned_by = Column(BigInteger, ForeignKey('user.id'))

    # Relationships
    user = relationship("User",
                        foreign_keys="UserRole.user_id",
                        back_populates="roles")
    role = relationship("Role",
                        back_populates="users")
    assigner = relationship("User",
                            foreign_keys="UserRole.assigned_by",
                            back_populates="assigned_roles")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'role_id': self.role_id,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None,
            'assigned_by': self.assigned_by,
            'role_name': self.role.name if self.role else None,
            'user_name': self.user.name if self.user else None,
            'assigner_name': self.assigner.name if self.assigner else None
        }
