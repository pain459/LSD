from flask import Flask, request, jsonify
from cache import Cache
from consistent_hashing import ConsistentHashing
import os
import requests

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
    nodes = ch.get_nodes(key)
    for node in nodes:
        caches[node].set(key, value)
    return jsonify({'nodes': nodes, 'status': 'success'})

@app.route('/get', methods=['GET'])
def get_key():
    key = request.args.get('key')
    nodes = ch.get_nodes(key)
    value = None
    for node in nodes:
        value = caches[node].get(key)
        if value:
            break
    return jsonify({'nodes': nodes, 'value': value})

@app.route('/delete', methods=['DELETE'])
def delete_key():
    key = request.json['key']
    nodes = ch.get_nodes(key)
    for node in nodes:
        caches[node].delete(key)
    return jsonify({'nodes': nodes, 'status': 'success'})

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
    node_cache = caches.pop(node, None)
    
    if node_cache:
        for key in list(node_cache.store.keys()):
            value = node_cache.get(key)
            node_cache.delete(key)
            new_nodes = ch.get_nodes(key)
            for new_node in new_nodes:
                caches[new_node].set(key, value)
    return jsonify({'status': 'success', 'node': node})

@app.route('/list_nodes', methods=['GET'])
def list_nodes():
    return jsonify({'nodes': list(caches.keys())})

@app.route('/list_keys', methods=['GET'])
def list_keys():
    keys = list(caches[node_name].store.keys())
    return jsonify({'keys': keys})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
