#################################################################################
#
# Makefile to build the project
#
#################################################################################

PROJECT_NAME = docker_project
PYTHON_INTERPRETER = python
WD=$(shell pwd)
PYTHONPATH=${WD}/src
SHELL := /bin/bash
PROFILE = default
PIP:=pip

## Create python interpreter environment.
create-environment:
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> check python3 version"
	( \
		$(PYTHON_INTERPRETER) --version; \
	)
	@echo ">>> Setting up VirtualEnv."
	( \
	    $(PIP) install -q virtualenv virtualenvwrapper; \
	    virtualenv venv --python=$(PYTHON_INTERPRETER); \
	)

# Define utility variable to help calling Python from the virtual environment
ACTIVATE_ENV := source venv/bin/activate

# Execute python related functionalities from within the project's environment
define execute_in_env
	$(ACTIVATE_ENV) && $1
endef

## Build the environment requirements
requirements: create-environment
	$(call execute_in_env, $(PIP) install -r ./requirements.txt)

################################################################################################################
# Set Up
## Install bandit
bandit:
	$(call execute_in_env, $(PIP) install bandit)

## Install safety
safety:
	$(call execute_in_env, $(PIP) install safety)

## Install flake8
flake:
	$(call execute_in_env, $(PIP) install flake8)

## Install coverage
coverage:
	$(call execute_in_env, $(PIP) install coverage)

## Set up dev requirements (bandit, safety, flake8)
dev-setup: bandit safety flake coverage

# Build / Run
## Run autopep8 to fix PEP8 issues
autopep8:
	$(call execute_in_env, autopep8 --in-place --aggressive --aggressive */*.py */*/*.py)


## Run the security test (bandit + safety)
security-test:
	$(call execute_in_env, safety check -r ./requirements.txt)
	$(call execute_in_env, bandit -lll */*.py *c/*/*.py)

## Run the flake8 code check
run-flake:
	$(call execute_in_env, flake8  ./src/*.py ./src/*/*.py ./test/*/*.py)

## Run the unit tests
unit-test-ingestion:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH}/ingestion python -m pytest -vrP test/test_ingestion)
unit-test-processing:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH}/processing python -m pytest -vrP test/test_processing)
unit-test-connection:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH}/connection python -m pytest -vrP test/test_connection)
unit-test-handler:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} python -m pytest -vrP test/test_handler.py)

run-unit-tests: unit-test-ingestion unit-test-processing unit-test-connection unit-test-handler

## Run the coverage check
check-coverage-ingestion:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH}/ingestion coverage run -m --omit 'venv/*' -m pytest test/test_ingestion --ignore=layer && coverage report -m)
check-coverage-processing:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH}/processing coverage run -m --omit 'venv/*' -m pytest test/test_processing --ignore=layer && coverage report -m)
check-coverage-connection:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH}/connection coverage run -m --omit 'venv/*' -m pytest test/test_error_handling --ignore=layer && coverage report -m)
check-coverage-handler:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} coverage run -m --omit 'venv/*' -m pytest test/test_handler.py --ignore=layer && coverage report -m)

run-coverage-checks: check-coverage-ingestion check-coverage-processing check-coverage-connection check-coverage-handler
## Run all checks
run-checks: security-test run-flake run-unit-tests run-coverage-checks

###############################################################################################

all: requirements dev-setup run-checks