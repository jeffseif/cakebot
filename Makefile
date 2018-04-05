.DELETE_ON_ERROR:

LOCKFILE = .already.running.lock
LOG_FILE = log.txt
PYTHON = python3.6
VIRTUALENV_LATEST = virtualenv-15.1.0

.PHONY: all
all: daemon

.PHONY: daemon
daemon: $(LOCKFILE)

$(LOCKFILE): config.json $(VENV) | already_running
	@touch $@
	@$(VENV)bin/python \
		-m cakebot.main \
			--verbose \
			--config=$< >> $(LOG_FILE) 2>&1
	@rm -f $@

.PHONY: already_running
already_running:
	@test ! -e $(LOCKFILE) || exit 0

$(VENV): requirements-minimal.txt $(VIRTUALENV_LATEST)/
	@$(PYTHON) ./$(VIRTUALENV_LATEST)/virtualenv.py \
		--no-site-packages \
		--python=$(PYTHON) \
		$@
	@$@/bin/pip install \
		--requirement $<
	@$@/bin/pip install \
		--upgrade pip
	@touch $@

$(VIRTUALENV_LATEST)/: $(VIRTUALENV_LATEST).tar.gz
	@tar \
		--extract \
		--gzip \
		--file $<

$(VIRTUALENV_LATEST).tar.gz:
	@curl \
		--location \
		--silent \
		--remote-name https://pypi.io/packages/source/v/virtualenv/$@ \
		--output $@

.PHONY: clean
clean:
	@rm -f $(LOCKFILE)
	@rm -f $(VIRTUALENV_LATEST).tar.gz
	@rm -rf $(VIRTUALENV_LATEST)/
	@rm -rf $(VENV)
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -type d -delete
