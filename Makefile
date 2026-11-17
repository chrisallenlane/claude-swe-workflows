.PHONY: help lint

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-8s %s\n", $$1, $$2}'

lint: ## Check frontmatter, description length, file length, tables, references, and mode contracts
	python3 scripts/lint.py
