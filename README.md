# py_wraps_data_types

A lightweight, foundational Python package providing core data structures and extended types for wrapper ecosystems. 

Currently, this package provides the `Variant` type: a highly optimized, "duck-typed" Enum designed to reduce boilerplate when validating raw strings at API boundaries.

## Installation

You can install this package using `pip` or `uv`:

```bash
pip install py_wraps_data_types
# or
uv add py_wraps_data_types
```

## Features
Variant **(Duck-Typed Enum)**<br>
Standard Python ```Enum``` classes require explicit instantiation (e.g., ```MyEnum("value")```), which causes friction when parsing raw strings from LLM outputs, JSON payloads, or external APIs.

The ```Variant``` class extends ```str``` and ```Enum``` to allow raw strings to seamlessly pass ```isinstance()``` checks, backed by $O(1)$ dictionary lookups for high-performance validation.

* String Mixin: Inherits all standard string methods (```.lower()```, ```.startswith()```).
* Duck-Typed Validation: Raw strings matching an Enum value return ```True``` for ```isinstance()``` checks.
* Clean Serialization: Overrides ```__str__``` to return the clean string value rather than ```EnumName.MEMBER```.

## Usage
Define your constraints by inheriting from ```Variant```:

```python
from py_wraps_data_types.variant import Variant

class BedrockModel(Variant):
    CLAUDE_3_SONNET = "anthropic.claude-3-sonnet-20240229-v1:0"
    CLAUDE_3_HAIKU = "anthropic.claude-3-haiku-20240307-v1:0"
    TITAN_EMBEDDINGS = "amazon.titan-embed-text-v2:0"

class DistanceMetric(Variant):
    COSINE = "cosine"
    L2 = "l2"
    DOT = "dot"
```
Use standard Python ```isinstance``` checks against raw strings—no pre-casting required:
```python
def query_vector_db(metric: str):
    # The raw string "cosine" will pass this check perfectly
    if not isinstance(metric, DistanceMetric):
        raise ValueError(f"Unsupported metric. Must be one of: {list(DistanceMetric)}")
    
    # ... execution logic ...

# Works perfectly with the Enum member
query_vector_db(DistanceMetric.COSINE)

# Works perfectly with a raw string from a JSON payload
query_vector_db("cosine") 
```