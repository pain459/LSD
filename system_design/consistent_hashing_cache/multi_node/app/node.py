from flask import Flask, request, jsonify
from cache import Cache
from consistent_hashing import ConsistentHashing
from synchronize import synchronize_data

app = Flask(__name__)

# Initialize consistent hashing with some nodes
ch = ConsistentHashing()
caches = {}

# Add nodes
nodes = ['node1_1', 'node1_2', 'node1_3', 'node2_1', 'node2_2', 'node2_3', 'node3_1', 'node3_2', 'node3_3']
for node in nodes:
    ch.add_node(node)
    caches[node] = Cache()

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

@app.route('/nodes', methods=['GET'])
def get_nodes():
    return jsonify({'nodes': list(ch.get_all_nodes())})

@app.route('/keys', methods=['GET'])
def get_keys():
    node = request.args.get('node')
    if node in caches:
        return jsonify({'keys': caches[node].get_all_keys()})
    return jsonify({'error': 'Node not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
