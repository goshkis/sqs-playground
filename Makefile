PYTHON = python3

setup:
	$(PYTHON) -m venv .venv
	. .venv/bin/activate; pip3 install -r requirements.txt
	. .venv/bin/activate; ${PYTHON} ./sqs_setup.py

run:
	./runall.sh

test:
	${PYTHON} -m pytest tests/


.PHONY: setup test run
