.DELETE_ON_ERROR:

LOCKFILE = .already.running.lock
PYTHON = python3.6
VIRTUALENV_LATEST = virtualenv-15.1.0

.PHONY: all
all: daemon

.PHONY: daemon
daemon: $(LOCKFILE)

$(LOCKFILE): config.json venv | already_running
	@touch $@
	@venv/bin/python \
		-m cakebot.main \
			--config=$< \

.PHONY: already_running
already_running:
	@test ! -e $(LOCKFILE) || exit 0

venv: requirements-minimal.txt $(VIRTUALENV_LATEST)/
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
	@rm -rf venv/
	@find -name '__pycache__' -delete
	@rm -rf $(VIRTUALENV_LATEST)/
	@rm -f $(VIRTUALENV_LATEST).tar.gz
	@rm -f $(HTML)
