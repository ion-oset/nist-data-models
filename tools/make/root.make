# Base state shared by all Makefiles

# --- Variables

# Project name
PROJECT_NAME := "{Project}"

# Absolute path to the directory containing this root 'Makefile'
PROJECT_ROOT := $(abspath $(dir $(firstword $(MAKEFILE_LIST))))

# Command runner, if any
RUN := poetry

# --- Rules

# Show help by default
help: help_prefix help_build help_suffix


# Block appearing before all other help output
help_prefix:
	@echo "Project name: $(PROJECT_NAME)"
	@echo "Project path: $(PROJECT_ROOT)"
	@echo ""
	@echo "Make targets:"
	@echo "-------------"


# Block appearing after all other help output
help_suffix:


.PHONY: help help_prefix help_suffix
