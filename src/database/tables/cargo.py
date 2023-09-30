from sqlalchemy import Integer, String, Column, Float, ForeignKey, Date, Boolean, Table
from sqlalchemy.orm import relationship
from .base import BaseModel, Base  
from datetime import datetime
# from .client import Client

cargoes_dangerous_types = Table(
    "cargoes_dangerous_types",
    BaseModel.metadata,
    Column(
        "cargo_id", ForeignKey("cargoes.id", ondelete="CASCADE"),  primary_key=True,
    ),
    Column(
        "dangerous_type_id", ForeignKey("dangerous_types.id", ondelete="CASCADE"), primary_key=True
    ),
)

class Cargo(BaseModel):
    __tablename__ = "cargoes"
    
    name = Column(String(1024), nullable=True)
    comment = Column(String(1024), nullable=False)

    height = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    length = Column(Float, nullable=False)
    ldm = Column(Float, nullable=True)

    weight = Column(Float, nullable=True)

    arrival = Column(
        Date, default= datetime.now().date(), nullable=True
    )
    departure = Column(
        Date, default= datetime.now().date(), nullable=True
    )
    
    temperature_control = Column(Boolean, default=False, nullable=False)
    temperature_celsius = Column(Integer, nullable=True)
    
    auto_in_number = Column(String(200), nullable=True)
    auto_out_number = Column(String(200), nullable=True)

    client_id = Column(
        Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False
    )
    client = relationship(
        "Client",
        back_populates="cargoes",
        foreign_keys="[Cargo.client_id]"
    )

    sender_id = Column(
        Integer, ForeignKey("senders.id", ondelete="CASCADE"), nullable=False
    )
    sender = relationship(
        "Sender",
        back_populates="cargoes",
    )

    recipient_id = Column(
        Integer, ForeignKey("recipients.id", ondelete="CASCADE"), nullable=False
    )
    recipient = relationship(
        "Recipient",
        back_populates="cargoes",
    )

    dangerous_types = relationship(
        "DangerousType",
        secondary=cargoes_dangerous_types,
        cascade="all,delete",
    )

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.name}"


class DangerousType(BaseModel):
    __tablename__ = "dangerous_types"
    
    name = Column(String(1024), unique=True, nullable=False)
    coefficient = Column(Float, nullable=False)
    
    cargoes = relationship(
        "Cargo",
        secondary=cargoes_dangerous_types,
        cascade="all,delete",
        overlaps="dangerous_types" 
    )


class Client(BaseModel):
    __tablename__ = "clients"
    
    name = Column(String(1024), unique=True, nullable=False)
    comment = Column(String(1024), nullable=True)
    unique_param = Column(String(100), unique=True, nullable=False)
    allowed = Column(Boolean, default=False, nullable=False)
    
    senders = Column(String(1024), nullable=False)
    recipient = Column(String(1024), nullable=False)

    country = Column(String(56), nullable=False)
    adress = Column(String(1024), nullable=False)
    
    cargoes = relationship(
        "Cargo",
        back_populates="client",
        foreign_keys="[Cargo.client_id]"
    )

    def __str__(self) -> str:
        return f"{self.name}"


class Sender(BaseModel):
    __tablename__ = "senders"

    name = Column(String(1024), unique=True, nullable=False)
    comment = Column(String(1024), nullable=True)
    customs_address = Column(String(1024), nullable=True)
    adress = Column(String(1024), nullable=True)

    # clients = relationship(
    #     "Client",
    #     secondary=senders_clients,
    #     cascade="all,delete",
    #     overlaps="senders"
    # )
    cargoes = relationship(
        "Cargo",
        back_populates="sender",
    )
    def __str__(self) -> str:
        return f"{self.name}"
    

class Recipient(BaseModel):
    __tablename__ = "recipients"

    name = Column(String(1024), unique=True, nullable=False)
    comment = Column(String(1024), nullable=True)
    customs_address = Column(String(1024), nullable=True)
    adress = Column(String(1024), nullable=True)
    # clients = relationship(
    #     "Client",
    #     secondary=recipients_clients,
    #     cascade="all,delete",
    #     overlaps="recipients"
    # )
    cargoes = relationship(
        "Cargo",
        back_populates="recipient",
    )
    def __str__(self) -> str:
        return f"{self.name}"