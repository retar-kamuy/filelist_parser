###############################################################################
# Settings
###############################################################################
MODULE = filelist_parser

VENV_HOME = .venv

ifeq ($(OS),Windows_NT)
	PY3 = python
	PYTHON = $(VENV_HOME)\Scripts\python
	PIP = $(VENV_HOME)\Scripts\pip
	RM = rd /s /q
else
	PY3 = python3
	PYTHON = $(VENV_HOME)/bin/python
	PIP = $(VENV_HOME)/bin/pip
	RM = rm -rf
endif


###############################################################################
# Commands
###############################################################################
install: $(VENV_HOME)

freeze: requirements.txt

$(VENV_HOME): requirements.txt
	$(PY3) -m venv $@
	$(PIP) install -r requirements.txt

requirements.txt:
	$(PIP) freeze > $@

build:
	$(PYTHON) -m $(MODULE)

clean: .venv
	$(RM) .venv
