PYTHON = python3
VENV = . .venv/bin/activate

setup:
	$(PYTHON) -m venv .venv
	$(VENV); pip3 install -r requirements.txt
	$(VENV); ${PYTHON} ./sqs_setup.py

run:
	$(VENV); ./runall.sh

test:
	$(VENV); ${PYTHON} -m pytest tests/


.PHONY: setup test run
