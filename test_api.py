from requests import request
import sys
import pprint

def main(n_nodes):
    pp = pprint.PrettyPrinter()

    new_trans = {'amount': 420, 'recipient': 'weedman2', 'sender': 'weedman'}
    nodes = list(map(lambda n: f'http://localhost:500{n}', range(n_nodes)))
    base_node = nodes[0]

    res = request('POST', f'{base_node}/transactions/new', json=new_trans)
    res = request('GET', f'{base_node}/mine')


    if n_nodes > 1:
        for node in nodes[1:]:
            res = request("POST", f"{base_node}/nodes/register", data=node)
            pp.pprint(res)

        node = nodes[-1]

        for _ in range(10):
            request('POST', f'{node}/transactions/new', json=new_trans)
            res = request('GET', f'{node}/mine')

    res = request('GET', f'{base_node}/nodes/resolve')
    pp.pprint(res.json())

if __name__ == '__main__':
    n_nodes = int(sys.argv[1])
    main(n_nodes)
