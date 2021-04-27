# vending auto tests
## How test:
### Pre-requisites:
* selenium
* pytest
* requests
---------------
Make sure that Git is installed.
Set Up A Python Virtual Environment
### 1. Install Python. This command creates an environment called venv/ :
$python3 -m venv venv     
### 2. "Activate" your environment:
$source venv/bin/activate
### 3. Update PIP:
$pip install -U pip
$pip install -U setuptools
### 4. Install the project's dependencies inside an active virtual environment:
$pip install -r requirements.txt

----------------
## To run graphql: $pytest -s -v /test_graphql
## To run selenium: $pytest -s -v /test_selenium

