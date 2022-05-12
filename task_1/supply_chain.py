from node import Node
import requests
import json


def check_domain(domain: str):
    try:
        url = domain_to_url(domain)
        requests.get(url, timeout=1).json()['sellers']
        return True
    except:
        return False


def domain_to_url(domain: str):
    url = f'https://{domain}/sellers.json'
    return url


def print_with_indent(indent: int, string):
    print(' ' * indent + string)


class SupplyChainTree:
    def __init__(self, domain_name: str, max_depth: int):
        self.domain = domain_name
        self.max_depth = max_depth
        self.root = Node(domain_name)
        self.find_supply_chain(self.root, company_domain=domain_name, max_depth=max_depth)

    def find_supply_chain(self, node: Node, company_domain: str, indent: int = 0, max_depth: int = 1):
        if max_depth == 0:
            return

        if not check_domain(company_domain):
            print(company_domain + ' Error: Could not load domain')
            return

        print_with_indent(indent, company_domain)
        indent += 1
        try:
            url = domain_to_url(company_domain)
            sales_list = requests.get(url, timeout=1).json()['sellers']
            buyer_set = set()
            intermediary_set = set()

            for sales in sales_list:
                if sales['seller_type'] in ['PUBLISHER', 'BOTH']:
                    buyer_set |= {sales['domain']}
                if sales['seller_type'] in ['INTERMEDIARY', 'BOTH']:
                    intermediary_set |= {sales['domain']}

            if buyer_set:
                print_with_indent(indent, company_domain + ' DIRECT SELLER:')
                buyer_list = list(buyer_set)
                buyer_list = [buyer.lower() for buyer in buyer_list]
                buyer_list.sort()
                node.buyers = buyer_list
                for buyer in buyer_list:
                    print_with_indent(indent + 1, buyer)
            if intermediary_set and max_depth > 1:
                print_with_indent(indent, company_domain + ' INDIRECT SELLER:')
                intermediary_list = list(intermediary_set)
                intermediary_list.sort()
                for intermediary in intermediary_list:
                    child = Node(intermediary)
                    node.intermediaries |= {child}
                    self.find_supply_chain(child, intermediary, indent + 1, max_depth - 1)
        except:
            print_with_indent(indent, company_domain + ' Error: Could not load sellers from domain')

    def json(self, node: Node = None):
        if node is None:
            node = self.root
        data = {
            'buyer': node.domain_name,
            'direct sellers': node.buyers,
            'indirect sellers': [self.json(node=child) for child in node.intermediaries]
        }
        return data

    def save(self, filename: str):
        folder = 'out/'
        directory_path = folder + filename + '.json'
        # attention, this function may overwrite the file
        with open(directory_path, 'w') as outfile:
            outfile.write(json.dumps(self.json(), indent=4))
            print(f'Supply chain tree for domain {self.domain} has been added to folder {folder}')
