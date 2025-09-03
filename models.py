import os, uuid, datetime as dt
from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship

DB_URL = os.getenv("DB_URL", "sqlite:///./app.db")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase): pass

class Video(Base):
    __tablename__ = "videos"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    owner = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    stored_path = Column(String, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    jobs = relationship("Job", back_populates="video")

class Job(Base):
    __tablename__ = "jobs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    video_id = Column(String, ForeignKey("videos.id"), nullable=False)
    owner = Column(String, nullable=False)
    status = Column(String, default="queued")  # queued|running|completed|failed
    detail = Column(Text, default="")
    output_dir = Column(String, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
    video = relationship("Video", back_populates="jobs")

def init_db():
    Base.metadata.create_all(engine)

