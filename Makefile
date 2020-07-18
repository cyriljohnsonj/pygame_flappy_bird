.PHONY:

PY_VER := 3.7

ROOT_DIR := ./
SRC_DIR := ./src
VENV_BIN_DIR := venv/bin

REQUIREMENTS_SRC := requirements.txt

PIP := $(VENV_BIN_DIR)/pip

define create-venv
	virtualenv venv -p python$(PY_VER)
endef

define start-venv
	. $(VENV_BIN_DIR)/activate
	$(VENV_BIN_DIR)/python main.py
endef

venv:
	@$(create-venv)
	@$(PIP) install -r $(REQUIREMENTS_SRC)

freeze:
	@$(PIP) freeze > $(REQUIREMENTS_SRC)

clean:
	@rm -rf .cache
	@find . -name *.pyc -delete
	@find . -type d -name __pycache__ -delete
	@rm -rf venv

runlocal:
	@$(start-venv)
