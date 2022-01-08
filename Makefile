# Makefile.
#
# Task driver.
# Intended as a convenience. All commands should be usable even without make.
#
# Notes:
#
# - The targets are broken up into modules found in 'tools'.
#   Add new modules by using 'include'.
#   They are processed in order. Make sure to keep 'root.make' first!


# --- Modules

include tools/make/root.make
include tools/make/build.make
include tools/make/tests.make
include tools/make/coverage.make
