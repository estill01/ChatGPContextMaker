.PHONY: build
build:
	poetry build

.PHONY: publish
publish: build
	poetry publish

