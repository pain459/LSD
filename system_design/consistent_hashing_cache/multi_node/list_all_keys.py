import requests

nodes = ['node1', 'node2', 'node3']
node_ports = {
    'node1': 5001,
    'node2': 5002,
    'node3': 5003
}

all_keys = {}

for node in nodes:
    try:
        response = requests.get(f'http://localhost:{node_ports[node]}/list_keys')
        if response.status_code == 200:
            keys = response.json().get('keys', [])
            all_keys[node] = keys
    except Exception as e:
        print(f"Error connecting to {node}: {e}")

for node, keys in all_keys.items():
    print(f"Keys in {node}: {keys}")
