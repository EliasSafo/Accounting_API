from sqlalchemy import Column, Integer, String, Float


from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False, nullable=False)  # parameter for empty string
    balance = Column(Float, nullable=False)
    role = Column(String, unique=False)
