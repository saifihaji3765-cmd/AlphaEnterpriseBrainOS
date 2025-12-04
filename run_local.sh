#!/bin/bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
export FLASK_APP=backend/app.py
export FLASK_ENV=development
flask db upgrade || true
python backend/app.py
