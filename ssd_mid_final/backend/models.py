from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

    uploaded_files = relationship("File", back_populates="uploader", foreign_keys="[File.uploaded_by]")
    received_files = relationship("File", back_populates="receiver", foreign_keys="[File.shared_with]")

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    upload_time = Column(DateTime, default=datetime.utcnow)
    
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    shared_with = Column(Integer, ForeignKey("users.id"))

    uploader = relationship("User", foreign_keys=[uploaded_by], back_populates="uploaded_files")
    receiver = relationship("User", foreign_keys=[shared_with], back_populates="received_files")

