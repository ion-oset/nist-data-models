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

<!-- --- -->

[nist-sp-1500]: https://pages.nist.gov/NIST-Tech-Pubs/SP1500.html
