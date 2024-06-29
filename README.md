# identity-reconciliation

Exact logic for can be found in src/contact/interactions/identify.py 
 For running project in local environment
 1. make virtual environment using 
 ```
  $ python3 -m venv .venv
 ```
 2. activate virtual environment
 ```
  $ source .venv/bin/activate
 ```
 3. install all requirements
 ```
  $ python3 -m pip install --upgrade -r requirements.txt
 ```
 4. run server
 ```
    cd src
    uvicorn main:app --reload
 ```