from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Record, Base
from faker import Faker
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/testdb')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def generate_records(session, count=100000):
    fake = Faker()
    for _ in range(count):
        record = Record(
            name=fake.name(),
            address=fake.address(),
            email=fake.email()
        )
        session.add(record)
    session.commit()

if __name__ == "__main__":
    session = SessionLocal()
    generate_records(session)
    session.close()
