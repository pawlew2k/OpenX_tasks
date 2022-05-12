class Node:
    def __init__(self, domain_name: str):
        self.domain_name = domain_name
        self.buyers = []
        self.intermediaries = set()
