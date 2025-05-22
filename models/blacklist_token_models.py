from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from models.user_models import User
from db.supabase import Base 


class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    token = Column(String, index=True) 
    blacklisted_on = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey(User.id))
    