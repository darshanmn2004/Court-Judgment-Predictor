from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# ---------------- USER TABLE ----------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

    # relationship (optional but good practice)
    predictions = relationship("PredictionHistory", back_populates="user")


# ---------------- PREDICTION HISTORY ----------------
class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    case_text = Column(Text)
    verdict = Column(String)
    ipc_section = Column(String, nullable=True)
    penalty = Column(Integer, nullable=True)

    relevant_laws = Column(Text, nullable=True)
    similar_cases = Column(Text, nullable=True)   # ✅ ADDED
    case_summary = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    # relationship
    user = relationship("User", back_populates="predictions")
