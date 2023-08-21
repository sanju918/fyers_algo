# fyers_algo

## Requirements
- Python3
- PIP

## Usage
- create a file called `.env` in the root folder of this repo
- Enter the following details in the `.env` file
  ```
  FYERS_CLIENT_ID=<APP_ID_HERE>
  FYERS_SECRET_ID=<SECRET_ID_HERE>
  ACCESS_TOKEN=<access_token_here>
  TIME_STAMP=1692626858.385683
  ```

- Install libraries by running `pip3 install -r requirements.txt`
- Run `python3 orchestrator.py` to run the live server. 
- If the access token is older than 6 hours then the code will ask to generate new access token.
- When it ask to generate a new access code, it will openup a web browser, follow the instructions. Once done it will redirect it to the redirect URL set on the API, copy the entire URL and enter it when asked for auth token, It will automatically updated the `.env` file with the generated access token

## Contributors
[Sanjay Patel](https://github.com/sanju918)

