import os
try:
    import importlib_resources
except ImportError:
    import importlib.resources as importlib_resources

# Allow abstracting out whether a test raises an exception
from pytest import raises
from contextlib import nullcontext as raises_none


def load_test_data(path, file):
    """Load test files from the test data package.

    Parameters:

    path (Path): Path to test data package.
        A relative path is a sub-path of the package root.
    file (Path): Name of the test file.
    """
    package_root = "tests.data"
    assert not os.path.isabs(path), \
        "Path to package must be relative (to test data root: {package_root})"
    sub_package = path.replace("/", ".")
    package = f"{package_root}.{sub_package}"
    path = importlib_resources.files(package).joinpath(file)
    with path.open() as input:
        data = input.read()
        return data
