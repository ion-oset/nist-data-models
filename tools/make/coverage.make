# Code coverage: Python-Coverage

# --- Variables

# Configuration file
COVERAGE_FILE := $(PROJECT_ROOT)/.coveragerc

# Location of coverage data. Extracted from configuration if present.
COVERAGE_DATA := $(dirname $(shell grep -E "data_file =" $(COVERAGE_FILE) | cut -d ' ' -f 3))

# --- Rules

help_coverage:
	@echo ""
	@echo "Coverage:"
	@echo ""
	@echo "  cover-test         - Run coverage over pytest"
	@echo "  cover-test-full    - Reset coverage data and run tests again"
	@echo "  cover-report       - Generate text report of coverage"
	@echo "                       Skips files with complete coverage"
	@echo "  cover-report-full  - Generate full text report of coverage"
	@echo "  cover-html         - Generate HTML report of coverage"
	@echo "                       Skips files with complete coverage"
	@echo "  cover-html-full    - Generate full HTML report of coverage"
	@echo "  cover-clean        - Clear out existing coverage data"


# Run all tests with coverage, incrementally incorporating prior runs.
cover-test: $(COVERAGE_DATA)
	$(RUN) run coverage run -m pytest

# Run all tests with coverage from scratch.
cover-test-full: cover-clean cover-test

# Generate a text coverage report only for files that are not at full coverage.
cover-report: $(COVERAGE_DATA)
	$(RUN) run coverage report --skip-covered --skip-empty

# Generate a text coverage report for all files
cover-report-full: $(COVERAGE_DATA)
	$(RUN) run coverage report

# Generate an HTML coverage report only for files that are not at full coverage.
cover-html: $(COVERAGE_DATA)
	$(RUN) run coverage html --skip-covered --skip-empty

# Generate an HTML coverage report for all files.
cover-html-full: $(COVERAGE_DATA)
	$(RUN) run coverage html

# Clean up all coverage data
cover-clean:
	$(RUN) run coverage erase


$(COVERAGE_DATA):
	@mkdir -p $(COVERAGE_DATA)


.PHONY: cover-test cover-test-full
.PHONY: cover-report cover-report-full
.PHONY: cover-html cover-html-full
.PHONY: cover-clean
