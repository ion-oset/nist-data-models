# Testing: PyTest

# --- Variables

# --- Rules

help_tests:
	@echo ""
	@echo "Tests:"
	@echo ""
	@echo "  test-all           - Run all test cases"
	@echo "  test-one           - Run until first failing case"
	@echo "  test-debug         - Run debugger if any cases fail"

# --- Testing

test-all:
	$(RUN) run pytest

test-one:
	$(RUN) run pytest -x

test-debug:
	$(RUN) run pytest -x --pdb


.PHONY: test-all test-one test-debug
