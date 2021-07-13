import argparse
from Model import Model

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Query maker')
    parser.add_argument('-Q', '--query', type=str, metavar='', help='full query')
    args = parser.parse_args()

    model = Model()
    data = model.make_query(args.query)
    print(data)
