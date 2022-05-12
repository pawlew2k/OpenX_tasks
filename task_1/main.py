from supply_chain import SupplyChainTree
import sys


def main():
    if len(sys.argv) < 3:
        print('Execution: main.py <domain_name> <max_depth>')
    else:
        # sample domain_names: openx.com, ascendeum.com
        domain_name, max_depth = sys.argv[1], sys.argv[2]
        sct = SupplyChainTree(domain_name, max_depth=int(max_depth))
        sct.save(domain_name + '_' + max_depth)


if __name__ == '__main__':
    main()

