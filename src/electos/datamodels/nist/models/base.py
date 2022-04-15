import re

import pydantic

from electos.datamodels.nist.utility.cases import Cases


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
        - Doesn't alias Pydantic custom root types: that breaks construction.
          See: https://pydantic.helpmanual.io/usage/models/#custom-root-types
        """
        if field_name.startswith(at_prefix):
            n = len(at_prefix)
            alias = f"@{field_name[n:]}"
        elif field_name.startswith("__"):
            alias = field_name
        else:
            alias = Cases.snake_to_camel(field_name)
        return alias

    # Convert field names.
    alias_generator = _field_name_alias

    # Unknown attributes should cause validation to fail.
    # Defined in the JSON Schema using 'additionalProperties'.
    # All NIST-1500 election schemas set 'additionalProperties' to false.
    extra = pydantic.Extra.forbid

    # Strict type checking of assignment to fields.
    # Enables assembling a model one step at a time.
    validate_assignment = True


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
