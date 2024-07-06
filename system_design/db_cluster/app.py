from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from database_setup import Record, Base
import os
import time
from prometheus_client import Counter, Summary, generate_latest, REGISTRY

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/testdb')
print(f"Using database URL: {DATABASE_URL}")

# Prometheus metrics
REQUEST_COUNT = Counter('request_count', 'Total count of requests', ['method', 'endpoint'])
REQUEST_LATENCY = Summary('request_latency_seconds', 'Latency of requests in seconds', ['method', 'endpoint'])

# Retry logic for database connection
for _ in range(10):  # Try to connect 10 times
    try:
        engine = create_engine(DATABASE_URL)
        engine.connect()
        break
    except OperationalError:
        print("Database connection failed. Retrying in 5 seconds...")
        time.sleep(5)
else:
    print("Failed to connect to the database after several attempts.")
    exit(1)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def track_metrics(func):
    def wrapper(*args, **kwargs):
        method = request.method
        endpoint = request.path
        REQUEST_COUNT.labels(method, endpoint).inc()
        with REQUEST_LATENCY.labels(method, endpoint).time():
            return func(*args, **kwargs)
    wrapper.__name__ = func.__name__  # Ensure the wrapper retains the original function name
    return wrapper

@app.route('/metrics')
def metrics():
    return generate_latest(REGISTRY), 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}

@app.route('/records', methods=['POST'])
@track_metrics
def create_record():
    session = SessionLocal()
    data = request.get_json()
    new_record = Record(name=data['name'], address=data['address'], email=data['email'])
    session.add(new_record)
    session.commit()
    session.refresh(new_record)
    session.close()
    return jsonify({"id": new_record.id}), 201

@app.route('/records/<int:id>', methods=['GET'])
@track_metrics
def read_record(id):
    session = SessionLocal()
    record = session.query(Record).filter(Record.id == id).first()
    session.close()
    if record:
        return jsonify({"id": record.id, "name": record.name, "address": record.address, "email": record.email}), 200
    else:
        return jsonify({"error": "Record not found"}), 404

@app.route('/records/<int:id>', methods=['PUT'])
@track_metrics
def update_record(id):
    session = SessionLocal()
    data = request.get_json()
    record = session.query(Record).filter(Record.id == id).first()
    if record:
        record.name = data['name']
        record.address = data['address']
        record.email = data['email']
        session.commit()
        session.close()
        return jsonify({"message": "Record updated"}), 200
    else:
        return jsonify({"error": "Record not found"}), 404

@app.route('/records/<int:id>', methods=['DELETE'])
@track_metrics
def delete_record(id):
    session = SessionLocal()
    record = session.query(Record).filter(Record.id == id).first()
    if record:
        session.delete(record)
        session.commit()
        session.close()
        return jsonify({"message": "Record deleted"}), 200
    else:
        return jsonify({"error": "Record not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
