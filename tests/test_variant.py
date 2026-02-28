import pytest
from py_wraps_data_types.variant import Variant


# ---------------------------------------------------------------------------
# Fixtures / shared enum definitions
# ---------------------------------------------------------------------------

class Color(Variant):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class BedrockModel(Variant):
    CLAUDE_3_SONNET = "anthropic.claude-3-sonnet-20240229-v1:0"
    CLAUDE_3_HAIKU = "anthropic.claude-3-haiku-20240307-v1:0"
    TITAN_EMBEDDINGS = "amazon.titan-embed-text-v2:0"


class DistanceMetric(Variant):
    COSINE = "cosine"
    L2 = "l2"
    DOT = "dot"


# ---------------------------------------------------------------------------
# Basic enum definition
# ---------------------------------------------------------------------------

class TestVariantDefinition:
    def test_members_accessible_by_name(self):
        assert Color.RED == "red"
        assert Color.GREEN == "green"
        assert Color.BLUE == "blue"

    def test_members_accessible_by_value(self):
        assert Color("red") is Color.RED

    def test_member_count(self):
        assert len(Color) == 3

    def test_is_subclass_of_str(self):
        assert issubclass(Color, str)


# ---------------------------------------------------------------------------
# isinstance() duck-typing with raw strings
# ---------------------------------------------------------------------------

class TestInstanceCheckRawStrings:
    def test_matching_raw_string_passes(self):
        assert isinstance("red", Color)

    def test_all_members_pass_as_raw_strings(self):
        for member in Color:
            assert isinstance(member.value, Color)

    def test_non_matching_raw_string_fails(self):
        assert not isinstance("yellow", Color)

    def test_empty_string_fails(self):
        assert not isinstance("", Color)

    def test_case_sensitive(self):
        assert not isinstance("RED", Color)
        assert not isinstance("Red", Color)

    def test_raw_string_with_complex_value(self):
        assert isinstance("anthropic.claude-3-sonnet-20240229-v1:0", BedrockModel)

    def test_unrelated_string_fails_on_complex_enum(self):
        assert not isinstance("gpt-4", BedrockModel)


# ---------------------------------------------------------------------------
# isinstance() with enum members
# ---------------------------------------------------------------------------

class TestInstanceCheckEnumMembers:
    def test_enum_member_passes_own_class(self):
        assert isinstance(Color.RED, Color)

    def test_enum_member_from_different_class_fails(self):
        assert not isinstance(DistanceMetric.COSINE, Color)

    def test_all_members_pass_their_own_class(self):
        for member in DistanceMetric:
            assert isinstance(member, DistanceMetric)


# ---------------------------------------------------------------------------
# isinstance() with non-string types
# ---------------------------------------------------------------------------

class TestInstanceCheckNonStrings:
    def test_integer_fails(self):
        assert not isinstance(1, Color)

    def test_none_fails(self):
        assert not isinstance(None, Color)

    def test_list_fails(self):
        assert not isinstance(["red"], Color)

    def test_dict_fails(self):
        assert not isinstance({"value": "red"}, Color)


# ---------------------------------------------------------------------------
# String method inheritance
# ---------------------------------------------------------------------------

class TestStringMethods:
    def test_lower(self):
        assert Color.RED.lower() == "red"

    def test_upper(self):
        assert Color.RED.upper() == "RED"

    def test_startswith(self):
        assert BedrockModel.CLAUDE_3_SONNET.startswith("anthropic")

    def test_endswith(self):
        assert BedrockModel.TITAN_EMBEDDINGS.endswith(":0")

    def test_replace(self):
        assert Color.RED.replace("red", "blue") == "blue"

    def test_contains(self):
        assert "claude" in BedrockModel.CLAUDE_3_HAIKU


# ---------------------------------------------------------------------------
# __str__ serialization
# ---------------------------------------------------------------------------

class TestStrSerialization:
    def test_str_returns_value_not_enum_repr(self):
        assert str(Color.RED) == "red"
        assert str(DistanceMetric.COSINE) == "cosine"

    def test_str_does_not_contain_class_name(self):
        assert "Color" not in str(Color.GREEN)
        assert "DistanceMetric" not in str(DistanceMetric.L2)

    def test_f_string_uses_value(self):
        assert f"{Color.BLUE}" == "blue"


# ---------------------------------------------------------------------------
# Equality and comparison
# ---------------------------------------------------------------------------

class TestEquality:
    def test_member_equals_its_raw_string(self):
        assert Color.RED == "red"

    def test_raw_string_equals_member(self):
        assert "cosine" == DistanceMetric.COSINE

    def test_different_members_not_equal(self):
        assert Color.RED != Color.GREEN

    def test_member_not_equal_to_wrong_string(self):
        assert Color.RED != "blue"


# ---------------------------------------------------------------------------
# Usage pattern: validation function (mirrors README example)
# ---------------------------------------------------------------------------

class TestValidationPattern:
    def _query_vector_db(self, metric: str):
        if not isinstance(metric, DistanceMetric):
            raise ValueError(f"Unsupported metric: {metric}")
        return f"querying with {metric}"

    def test_enum_member_accepted(self):
        result = self._query_vector_db(DistanceMetric.COSINE)
        assert result == "querying with cosine"

    def test_raw_string_accepted(self):
        result = self._query_vector_db("l2")
        assert result == "querying with l2"

    def test_invalid_string_raises(self):
        with pytest.raises(ValueError, match="Unsupported metric"):
            self._query_vector_db("euclidean")

    def test_none_raises(self):
        with pytest.raises((ValueError, TypeError)):
            self._query_vector_db(None)
