from generate_access_token import generate_access_token
from fyers_server import run_server


def main():
    data = generate_access_token()
    expiry = data['expiry']
    print(expiry)
    run_server(data)


if __name__ == '__main__':
    main()
