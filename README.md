# fyers_algo

## Requirements
- Python3
- PIP
- Docker Desktop

## Usage
- If you have done the first time setup then run this else go to First time setup 

```commandline
docker run -rm -p 4001:4001 python_fyers_algo:latest
```
- If the access token is older than 6 hours then the code will ask to generate new access token.
- When it ask to generate a new access code, it will open up a web browser, follow the instructions. 
- Once done it will redirect it to the redirect URL set on the API, copy the entire URL and enter it when asked for auth token, It will automatically updated the `.env` file with the generated access token

## First time setup
- create a file called `.env` in the root folder of this repo
- Enter the following details in the `.env` file and make necessary changes to the parameters.

  ```
  FYERS_CLIENT_ID=X81xxxxxx120
  FYERS_SECRET_ID=LCBxxxx3A
  ACCESS_TOKEN=LIXXX34XXX
  TIME_STAMP=1693402413
  ```

- Make sure docker desktop is running in the background.
- Run the following command to build the docker image
  `docker build -t python_fyers_algo:latest .`
- Once it is successful run the following command to run the docker
  `docker run -rm -p 4001:4001 python_fyers_algo:latest`

## Contributors
[Sanjay Patel](https://github.com/sanju918)

