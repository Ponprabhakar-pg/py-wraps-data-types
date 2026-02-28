# py_wraps_data_types

A lightweight, foundational Python package providing core data structures and extended types for wrapper ecosystems.

Currently, this package provides the `Variant` type: a highly optimized, "duck-typed" Enum designed to reduce boilerplate when validating raw strings at API boundaries.

**Python:** 3.9+ | **PyPI:** `py-wraps-data-types`

---

## Installation

```bash
pip install py_wraps_data_types
# or
uv add py_wraps_data_types
```

---

## Features

### `Variant` — Duck-Typed Enum

Standard Python `Enum` classes require explicit instantiation (e.g. `MyEnum("value")`), which causes friction when parsing raw strings from LLM outputs, JSON payloads, or external APIs.

The `Variant` class extends `str` and `Enum` to allow raw strings to seamlessly pass `isinstance()` checks, backed by O(1) dictionary lookups for high-performance validation.

| Feature | Description |
|---|---|
| **String mixin** | Inherits all standard string methods (`.lower()`, `.startswith()`, …) |
| **Duck-typed validation** | Raw strings matching an Enum value pass `isinstance()` checks |
| **Clean serialization** | `str()` returns the plain value, not `EnumName.MEMBER` |
| **No dependencies** | Zero runtime dependencies |

---

## Usage

Define your constraints by subclassing `Variant`:

```python
from py_wraps_data_types.variant import Variant

class BedrockModel(Variant):
    CLAUDE_3_SONNET = "anthropic.claude-3-sonnet-20240229-v1:0"
    CLAUDE_3_HAIKU  = "anthropic.claude-3-haiku-20240307-v1:0"
    TITAN_EMBEDDINGS = "amazon.titan-embed-text-v2:0"

class DistanceMetric(Variant):
    COSINE = "cosine"
    L2     = "l2"
    DOT    = "dot"
```

Use `isinstance()` directly against raw strings — no pre-casting required:

```python
def query_vector_db(metric: str):
    if not isinstance(metric, DistanceMetric):
        raise ValueError(f"Unsupported metric. Must be one of: {list(DistanceMetric)}")
    # ... execution logic ...

# Works with an enum member
query_vector_db(DistanceMetric.COSINE)

# Works with a raw string from a JSON payload
query_vector_db("cosine")
```

### String methods work naturally

```python
model = BedrockModel.CLAUDE_3_SONNET

model.startswith("anthropic")  # True
model.upper()                  # "ANTHROPIC.CLAUDE-3-SONNET-20240229-V1:0"
"claude" in model              # True
```

### Clean serialization

```python
status = DistanceMetric.COSINE

str(status)     # "cosine"       (not "DistanceMetric.COSINE")
f"{status}"     # "cosine"
repr(status)    # "<DistanceMetric.COSINE: 'cosine'>"
```

---

## Examples

A runnable example is provided in [`examples/basic_usage.py`](examples/basic_usage.py):

```bash
python examples/basic_usage.py
```

---

## Testing

Install dev dependencies and run the test suite with pytest:

```bash
pip install "py_wraps_data_types[dev]"
pytest
```

Or, from a local clone:

```bash
pip install -e ".[dev]"
pytest
```

The test suite covers:

- Enum member definition and access
- `isinstance()` with raw strings (matching and non-matching)
- `isinstance()` with enum members (same class and cross-class)
- Non-string inputs (int, None, list, dict)
- Inherited string methods
- `__str__` serialization
- Equality comparisons
- End-to-end validation function pattern

---

## Requirements

- Python **3.9** or later
- No runtime dependencies
