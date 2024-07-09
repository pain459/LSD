import requests

def display_nodes():
    response = requests.get('http://localhost:5000/nodes')
    nodes = response.json().get('nodes', [])
    for node in nodes:
        response = requests.get(f'http://localhost:5000/keys?node={node}')
        keys = response.json().get('keys', [])
        print(f'Node: {node}, Keys: {keys}')

if __name__ == '__main__':
    display_nodes()
