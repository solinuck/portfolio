#!/bin/bash
source ~/.virtualenvs/flask/bin/activate
export FLASK_ENV=development
export FLASK_APP=portfolio_app
python -m flask run
