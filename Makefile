.PHONY: format
format:
	isort src/
	blue src/

.PHONY: format-check
format-check:
	isort src/ --check
	blue src/ --check

.PHONY: lint
lint:
	pylint src/

