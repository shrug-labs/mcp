SUBDIRS := $(wildcard src/*)

.PHONY: test format

build:
	@for dir in $(SUBDIRS); do \
		if [ -f $$dir/pyproject.toml ]; then \
			echo "Building $$dir"; \
			cd $$dir && uv build && cd ../..; \
		fi \
	done

install:
	@for dir in $(SUBDIRS); do \
		if [ -f $$dir/pyproject.toml ]; then \
			echo "Installing $$dir"; \
			cd $$dir && uv pip install . && cd ../..; \
		fi \
	done

sync:
	@for dir in $(SUBDIRS); do \
		if [ -f $$dir/pyproject.toml ]; then \
			echo "Installing $$dir"; \
			cd $$dir && uv sync --locked --all-extras --dev && cd ../..; \
		fi \
	done

lock:
	@for dir in $(SUBDIRS); do \
		if [ -f $$dir/pyproject.toml ]; then \
			echo "Installing $$dir"; \
			cd $$dir && uv lock && cd ../..; \
		fi \
	done

test:
	uv tool run --from 'tox==4.30.2' tox -e lint
	@for dir in $(SUBDIRS); do \
		if [ -f $$dir/pyproject.toml ]; then \
			echo "Testing $$dir"; \
			cd $$dir && uv run pytest && cd ../..; \
		fi \
	done

format:
	uv tool run --from 'tox==4.30.2' tox -e format
