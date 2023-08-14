# fyers_algo

## Requirements
- Python3
- PIP

## Usage
- create a file called '.env' in the root folder of this repo
- Enter the following details in the '.env' file
  ```
  FYERS_CLIENT_ID=<APP_ID_HERE>
  FYERS_SECRET_ID=<SECRET_ID_HERE>
  ```

- Install libraries by running `pip3 install -r requirements.txt`
- Generate the access token `python3 generate_access_token.py`
- Copy the auth code from the URL and enter it when asked for auth token, It will automatically updated the `.env` file with the generated access token
- Run `python3 TFU_sagar_subscribe_Fyers.py` to test


