## To start project, please proceed the following steps:

- `git clone https://github.com/Dimitrionian/wallet`
- create an .env file in the root of the project using the .env.base template
- `docker compose build`
- `docker compose up`
- Go to the `http://0.0.0.0:8000/api/schema/swagger-ui/` url
- Feel free to play around with entities: create a wallet, positive and negative transactions, use ordering, filtering...

## To run the test suite:

- Install virtualenv: `sudo apt install python3.11-venv`
- Create a virtualenv: `python3.11 -m venv virtual`
- Activate the virtualenv: `source virtual/bin/activate`
- Install requirements: `pip install -r requirements.txt`
- run tests: `pytest`
