# NIST Data Models

A library of data classes representing records defined by
[NIST SP-1500-10x election specifications][nist-sp-1500].

## Goals

- Provide data classes for NIST data across ElectOS projects.
- Support programming languages used in these projects as natively as possible.
  Records are strongly-typed objects instead of maps/dictionaries.
- Round-tripping between models in memory and serialized data that validates
  under the NIST schemas.
- Follow the naming and coding conventions of each language.
- Utilities for features such as I/O and validation.
- Thorough testing and documentation.

## Repository Structure

This project is a multi-repo: each supported language has its own branch
namespace. You can install it with the appropriate package managers or using
version control by installing or switching to a given `{language}/main` branch.

### Branches

Current supported languages and branches:

- `main`: What you see when you first clone. This branch remains minimal and
   code should _not_ be committed to it.
   You should switch to one of the other `main` branches.
- `scaffold`: Language-agnostic project code and files.
- `python`: Namespace for Python branches.
    - `python/main`: The most recent work on the Python library.
    - `python/scaffold`: Python specific project code and files.

<!-- --- -->

[nist-sp-1500]: https://pages.nist.gov/NIST-Tech-Pubs/SP1500.html
