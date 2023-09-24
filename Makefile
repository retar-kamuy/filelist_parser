VENV_HOME = .venv
ifeq ($(OS),Windows_NT)
	PYTHON = $(VENV_HOME)\Scripts\python
	PIP = $(VENV_HOME)\Scripts\pip
	RM = rd /s /q
else
	PYTHON = $(VENV_HOME)/bin/python
	PIP = $(VENV_HOME)/bin/pip
	RM = rm -rf
endif

# PYTHON = $(VENV_HOME)/Scripts/python
# PIP = $(VENV_HOME)/Scripts/pip

MODULE = verilog_filelist_parser

install: $(VENV_HOME)

$(VENV_HOME): requirements.txt
ifeq ($(OS),Windows_NT)
	python -m venv $@
else
	python3 -m venv $@
endif
	$(PIP) install -r requirements.txt

freeze: requirements.txt
requirements.txt:
	$(PIP) freeze > $@

build:
	$(PYTHON) -m $(MODULE)

clean: .venv
	$(RM) .venv