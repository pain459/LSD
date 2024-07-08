from flask import Flask, request, jsonify
from cache import Cache
from consistent_hashing import ConsistentHashing

app = Flask(__name__)

# Initialize consistent hashing with some nodes
nodes = ['node1', 'node2', 'node3']
ch = ConsistentHashing(nodes)
caches = {node: Cache() for node in nodes}

@app.route('/set', methods=['POST'])
def set_key():
    data = request.json
    key, value = data['key'], data['value']
    node = ch.get_node(key)
    caches[node].set(key, value)
    return jsonify({'node': node, 'status': 'success'})

@app.route('/get', methods=['GET'])
def get_key():
    key = request.args.get('key')
    node = ch.get_node(key)
    value = caches[node].get(key)
    return jsonify({'node': node, 'value': value})

@app.route('/delete', methods=['DELETE'])
def delete_key():
    key = request.json['key']
    node = ch.get_node(key)
    caches[node].delete(key)
    return jsonify({'node': node, 'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
