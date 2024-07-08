from flask import Flask, request, jsonify
from cache import Cache
from consistent_hashing import ConsistentHashing
import os

app = Flask(__name__)

# Get node name from environment variable
node_name = os.getenv('NODE_NAME', 'default_node')

# Initialize consistent hashing with the current node
ch = ConsistentHashing([node_name])
caches = {node_name: Cache()}

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

@app.route('/add_node', methods=['POST'])
def add_node():
    node = request.json['node']
    ch.add_node(node)
    caches[node] = Cache()
    return jsonify({'status': 'success', 'node': node})

@app.route('/remove_node', methods=['POST'])
def remove_node():
    node = request.json['node']
    keys_to_redistribute = ch.remove_node(node)
    for key in list(caches[node].store.keys()):
        value = caches[node].get(key)
        caches[node].delete(key)
        new_node = ch.get_node(key)
        caches[new_node].set(key, value)
    caches.pop(node, None)
    return jsonify({'status': 'success', 'node': node})

@app.route('/list_nodes', methods=['GET'])
def list_nodes():
    return jsonify({'nodes': list(caches.keys())})

@app.route('/list_keys', methods=['GET'])
def list_keys():
    keys = list(caches[node_name].store.keys())
    return jsonify({'keys': keys})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
