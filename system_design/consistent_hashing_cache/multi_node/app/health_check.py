import requests
import time

nodes = ['node1', 'node2', 'node3']
node_ports = {
    'node1': 5001,
    'node2': 5002,
    'node3': 5003
}

def is_node_healthy(node):
    try:
        response = requests.get(f'http://localhost:{node_ports[node]}/health')
        return response.status_code == 200
    except requests.RequestException:
        return False

def remove_node(node):
    try:
        # Remove node from another healthy node
        healthy_node = next(n for n in nodes if n != node and is_node_healthy(n))
        requests.post(f'http://localhost:{node_ports[healthy_node]}/remove_node', json={'node': node})
        print(f"Removed {node} from the cluster")
    except StopIteration:
        print(f"No healthy nodes available to remove {node} from the cluster")

while True:
    for node in nodes:
        if not is_node_healthy(node):
            print(f"{node} is down")
            remove_node(node)
        else:
            print(f"{node} is healthy")
    time.sleep(30)
