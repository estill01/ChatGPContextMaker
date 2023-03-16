.PHONY: build
build:
	poetry build

.PHONY: test
test:
	poetry run pytest


.PHONY: publish
publish: build
	poetry publish

