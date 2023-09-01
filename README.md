# fyers_algo

## Requirements
- `Docker Desktop` (Download it from here: https://www.docker.com/products/docker-desktop/ )
- `PyChram Community Edition` (Download it from here: https://www.jetbrains.com/pycharm/download/)
- `WSL 2` This is required for Windows users. If WSL is not installed in your windows system, go to microsoft store and sesarch for `WSL 2`. It will show something like `Windows Subsystem for Linux`, install this. Also you can follow Microsoft documentation here: https://learn.microsoft.com/en-us/windows/wsl/install

### Optional 
- Python 3.9 (Download it from here: https://www.python.org/downloads/release/python-3918/)
- Git (Download it from here: https://git-scm.com/downloads)

## Usage (Only do this if you have done the first time setup)
 - Watch the video how to run, link: 

## First time setup
- Create a file called `.env` in the root folder of this repo
- Enter the following details in the `.env` file and make necessary changes to the parameters.
- `APP_ID` should not contain `-100`
- `TOTP_KEY` Can be generated from the profile file, will share video link how to set it up
- `FYERS_ID` Is the client id or profile id, will share video link how to get this.

  ```
  APP_ID=X31YYXXYY
  APP_TYPE=100
  FYERS_SECRET_KEY=86AAVEX
  FYERS_ID=XB17834
  APP_ID_TYPE=2
  TOTP_KEY=KDFD493LDKJFDLJAK2KD
  PIN=1234
  REDIRECT_URL=https://www.sanjaythegreatcoder.com
  ```
- Download the repo from: https://github.com/sanju918/fyers_algo/archive/refs/heads/main.zip
- Extract the zip file and copy the path of the folder where it is extracted.
- Download the image from docker hub
  ```commandline
  docker pull cenzer2/python_fyers_algo_min:latest
  ```
- Once the image has been pulled, run this command to start docker. Replace the path where the repo is extracted.
  
  - Syntax: `docker run  -it -p 4001:4001 -v REPO_PATH_IN_LOCAL:/app python_fyers_algo_min:latest`
  - Example:
  ```commandline
  docker run -it -p 4001:4001 -v D:\Trading\repos\fyers_algo:/app cenzer2/python_fyers_algo_min:latest
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

