from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Record, Base
import os

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/testdb')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

@app.route('/records', methods=['POST'])
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
def read_record(id):
    session = SessionLocal()
    record = session.query(Record).filter(Record.id == id).first()
    session.close()
    if record:
        return jsonify({"id": record.id, "name": record.name, "address": record.address, "email": record.email}), 200
    else:
        return jsonify({"error": "Record not found"}), 404

@app.route('/records/<int:id>', methods=['PUT'])
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
        session.close()
        return jsonify({"error": "Record not found"}), 404

@app.route('/records/<int:id>', methods=['DELETE'])
def delete_record(id):
    session = SessionLocal()
    record = session.query(Record).filter(Record.id == id).first()
    if record:
        session.delete(record)
        session.commit()
        session.close()
        return jsonify({"message": "Record deleted"}), 200
    else:
        session.close()
        return jsonify({"error": "Record not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
