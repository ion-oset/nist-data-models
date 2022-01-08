# Project builds: Poetry

# --- Variables

# --- Rules

help_build:
	@echo ""
	@echo "Project builds:"
	@echo ""
	@echo "  install            - Install non-development dependencies and main package"
	@echo "  develop            - Install all dependencies and main package"
	@echo "  depends            - Install dependencies only, without the main package"
	@echo "  refresh            - Update lock file without updating dependencies"
	@echo ""
	@echo "  build              - Build all distributable Python packages"
	@echo "  build-sdist        - Build project as source tarball"
	@echo "  build-wheel        - Build project as wheel"
	@echo ""
	@echo "  clean              - Remove all built Python packages"
	@echo "  clean-sdist        - Remove built tarballs"
	@echo "  clean-wheel        - Remove built wheels"


# --- Development installation

# Install project for release, not including 'dev-dependencies'.
install:
	$(RUN) install --no-dev

# Install project for development, including 'dev-dependencies'.
develop:
	$(RUN) install

# Install dependencies only and not the project.
depends:
	$(RUN) install --no-root

# Refresh the lock file without changing the installated dependencies.
# Useful for debugging the installed dependencies.
refresh:
	$(RUN) lock --no-update

# --- Packages for release

# Build installable package. Only build wheel by default.
build: build-wheel

# Build source distribution as tar archive.
build-sdist:
	$(RUN) build -f sdist

# Build binary distribution as wheel.
build-wheel:
	$(RUN) build -f wheel

# Remove installable packages
clean: clean-sdist clean-wheel

# Remove 'sdist' distributions.
clean-sdist:
	rm -f dist/$(PROJECT)*.tar.gz
	rmdir --ignore-fail-on-non-empty dist

# Remove 'wheel' distributions.
clean-wheel:
	rm -f dist/$(PROJECT)*.whl
	rmdir --ignore-fail-on-non-empty dist


.PHONY: install develop depends refresh
.PHONY: build build-sdist build-wheel
.PHONY: clean clean-sdist clean-wheel
