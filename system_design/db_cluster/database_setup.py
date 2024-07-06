from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/testdb')

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String, index=True)
    email = Column(String, index=True)

def create_database():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_database()
