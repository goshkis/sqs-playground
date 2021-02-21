PYTHON = python3

all: setup

setup:
	$(PYTHON) -m venv .venv
	. .venv/bin/activate; pip3 install -r requirements.txt
	${PYTHON} ./sqs_setup.py

run:
	./runall.sh

test:
	${PYTHON} -m pytest tests/


.PHONY: setup test run activate
