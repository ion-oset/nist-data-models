import re

import pydantic


def _split_snake_case(text):
    """Tokenize a string using underscores as delimiters."""
    for match in re.finditer("(^_+|[A-Za-z][A-Za-z0-9]*)", text):
        yield match.group(0)


def _snake_to_camel(text):
    """Convert text in 'snake_case' to 'CamelCase'."""
    return "".join(part.capitalize() for part in _split_snake_case(text))


class _NistModelConfig:

    """Settings that apply to all NistModels and subtypes."""

    # Replace leading '@' character in JSON Schema field names.
    # This cannot be the default of '_': Pydantic can't serialize those fields.
    # Note: Consider 'PrivateAttr'?

    _AT_PREFIX = "model__"

    def _field_name_alias(field_name, at_prefix = _AT_PREFIX):
        """Convert fieldnames:

        - Assume snake case for fields, use camel case for serialized JSON.
        - Set the prefix that maps to '@'-prefix schema keys (e.g. '@type').
        """
        if field_name.startswith(at_prefix):
            n = len(at_prefix)
            alias = f"@{field_name[n:]}"
        else:
            alias = _snake_to_camel(field_name)
        return alias

    # Convert field names.
    alias_generator = _field_name_alias


class NistModel(pydantic.BaseModel):

    """Common state for all classes that are models for the NIST JSON Schema."""

    Config = _NistModelConfig

    # Overrides:
    #
    # - Always exclude null values or the data will be littered with nulls.
    # - For JSON always using aliases to be schema-compliant.

    def dict(self, *, exclude_none = True, **opts):
        return super().dict(exclude_none = exclude_none, **opts)

    def json(self, *, by_alias = True, exclude_none = True, **opts):
        return super().json(by_alias = by_alias, exclude_none = exclude_none, **opts)
