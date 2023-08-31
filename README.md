# fyers_algo

## Requirements
- `Docker Desktop` (Download it from here: https://www.docker.com/products/docker-desktop/ )
- `PyChram Community Edition` (Download it from here: https://www.jetbrains.com/pycharm/download/)
- `WSL 2` This is required for windows users. If WSL is not installed in your windows system, go to microsoft store and sesarch for `WSL 2`. It will show something like `Windows Subsystem for Linux`, install this. Also you can follow Microsoft documentation here: https://learn.microsoft.com/en-us/windows/wsl/install

### Optional 
- Python 3.9 (Download it from here: https://www.python.org/downloads/release/python-3918/)
- Git (Download it from here: https://git-scm.com/downloads)

## Usage (Only do this if you have done the first time setup)
- If you have done the first time setup then run this else go to First time setup 

  ```commandline
  docker run --rm -it -p 4001:4001 -v C://Users/Sanjay/Documents/fyers_algo:/app python_fyers_algo_min:latest
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

- Make sure docker desktop is running in the background. Enter the following command to check if you have installed teh docker desktop correctly and is running fine.
  ```commandline
   docker --version
  ```
  
  Output: Version might differ in your case, but if it's showing this, then your docker installation is correct.

  ```commandline
  Docker version 20.10.23, build 7155243
  ```

- Run the following command to build the docker image
  - Syntax:
    ```commandline
    docker build -t IMAGE_NAME:latest
    ```
  - Example
    ```commandline
    docker build -t python_fyers_algo_min:latest .
    ```
- Once it is successful run the following command to run the docker
    - `LOCAL_CODE_LOCATION` is the path of your python codes. In my example my python files are downloaded in `/Users/s0p05wq/Documents/Trading Classes/fyers_algo`
    - Syntax:
      ```commandline
      docker run --rm -it -p 4001:4001 -v LOCAL_CODE_LOCATION:/app IMAGE_NAME:latest
      ```
  - Example
    ```commandline
    docker run --rm -it -p 4001:4001 -v C://Users/Sanjay/Documents/fyers_algo:/app python_fyers_algo_min:latest
    ```

## Contributors
[Sanjay Patel](https://github.com/sanju918)

