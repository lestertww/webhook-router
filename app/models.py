# app/models.py

import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    JSON,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID  # Optional if using Postgres
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# ----------------------
# Routers
# ----------------------
class Router(Base):
    __tablename__ = "routers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=True)  # Optional if you have auth
    inbound_url = Column(String, unique=True, nullable=False)
    secret_key = Column(String, nullable=True)  # Optional, for signature verification
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to rules
    rules = relationship("Rule", back_populates="router")
    events = relationship("Event", back_populates="router")


# ----------------------
# Rules
# ----------------------
class Rule(Base):
    __tablename__ = "rules"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    router_id = Column(String, ForeignKey("routers.id"))
    condition_json = Column(JSON, nullable=False)  # JSON defining matching condition
    target_urls = Column(JSON, nullable=False)     # List of target URLs
    created_at = Column(DateTime, default=datetime.utcnow)

    router = relationship("Router", back_populates="rules")


# ----------------------
# Events
# ----------------------
class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    router_id = Column(String, ForeignKey("routers.id"))
    raw_payload = Column(JSON, nullable=False)
    headers = Column(JSON, nullable=True)
    rules_fired = Column(JSON, nullable=True)     # List of rule IDs that triggered
    forwarded_to = Column(JSON, nullable=True)    # List of URLs payload was sent to
    signature_valid = Column(Boolean, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    router = relationship("Router", back_populates="events")
