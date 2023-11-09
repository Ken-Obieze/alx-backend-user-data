#!/usr/bin/env python3
"""Module for defining models"""
from models.base import Base
from sqlalchemy import Column, String

class UserSession(Base):
    """UserSession model."""
    __tablename__ = 'user_sessions'

    user_id = Column(String(60), nullable=False)
    session_id = Column(String(60), nullable=False)
