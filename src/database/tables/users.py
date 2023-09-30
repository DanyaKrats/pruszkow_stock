from sqlalchemy import Integer, String, Column, ForeignKey, Table
from sqlalchemy.orm import relationship
from .base import BaseModel

users_roles = Table(
    "users_roles",
    BaseModel.metadata,
    Column(
        "user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    ),
)

class User(BaseModel):
    __tablename__ = "users"
    
    name = Column(String(1024), nullable=True)
    email = Column(String(1024), nullable=False)

    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=True)
    client = relationship("Client", back_populates="users")

    roles = relationship("Role", secondary=users_roles, cascade="all,delete")

    def __str__(self) -> str:
        return f"{self.name}"


class Role(BaseModel):
    __tablename__ = "roles"
    
    name = Column(String(200), unique=True, nullable=False)
    
    users = relationship(
        "User", 
        secondary=users_roles, 
        cascade="all,delete",
        overlaps="roles"
        )

    def __str__(self) -> str:
        return f"{self.name}"
