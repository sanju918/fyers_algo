from generate_access_token import generate_access_token
from fyers_server import run_server


def main():
    data = generate_access_token()
    run_server(access_token=data[0], conf=data[1])


if __name__ == '__main__':
    main()
