"""
Basic usage examples for py_wraps_data_types.

Run this file directly:
    python examples/basic_usage.py
"""

from py_wraps_data_types.variant import Variant


# ---------------------------------------------------------------------------
# Example 1: AI model identifiers
# ---------------------------------------------------------------------------

class BedrockModel(Variant):
    CLAUDE_3_SONNET = "anthropic.claude-3-sonnet-20240229-v1:0"
    CLAUDE_3_HAIKU = "anthropic.claude-3-haiku-20240307-v1:0"
    TITAN_EMBEDDINGS = "amazon.titan-embed-text-v2:0"


def invoke_model(model_id: str) -> str:
    if not isinstance(model_id, BedrockModel):
        raise ValueError(
            f"Unknown model '{model_id}'. "
            f"Supported: {[m.value for m in BedrockModel]}"
        )
    return f"Invoking {model_id} ..."


print("=== Example 1: AI Model Identifiers ===")

# Using an enum member directly
print(invoke_model(BedrockModel.CLAUDE_3_HAIKU))

# Using a raw string from a JSON payload — no pre-casting required
raw_from_api = "anthropic.claude-3-sonnet-20240229-v1:0"
print(invoke_model(raw_from_api))

try:
    invoke_model("gpt-4")
except ValueError as e:
    print(f"Caught expected error: {e}")


# ---------------------------------------------------------------------------
# Example 2: Vector database distance metrics
# ---------------------------------------------------------------------------

class DistanceMetric(Variant):
    COSINE = "cosine"
    L2 = "l2"
    DOT = "dot"


def query_vector_db(query: str, metric: str) -> dict:
    if not isinstance(metric, DistanceMetric):
        raise ValueError(
            f"Unsupported metric '{metric}'. "
            f"Must be one of: {list(DistanceMetric)}"
        )
    return {"query": query, "metric": str(metric), "results": []}


print("\n=== Example 2: Vector DB Distance Metrics ===")

# Enum member
result = query_vector_db("find similar docs", DistanceMetric.COSINE)
print(f"Query result: {result}")

# Raw string (e.g. from a REST request body)
result = query_vector_db("find similar docs", "l2")
print(f"Query result: {result}")


# ---------------------------------------------------------------------------
# Example 3: Serialization — str() returns the clean value
# ---------------------------------------------------------------------------

class Status(Variant):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


print("\n=== Example 3: Serialization ===")

status = Status.RUNNING
print(f"str()  : {str(status)}")       # "running"  (not "Status.RUNNING")
print(f"f-str  : {status}")            # "running"
print(f"repr() : {repr(status)}")      # "<Status.RUNNING: 'running'>"


# ---------------------------------------------------------------------------
# Example 4: String methods work naturally
# ---------------------------------------------------------------------------

print("\n=== Example 4: String Methods ===")

model = BedrockModel.CLAUDE_3_SONNET
print(f"startswith('anthropic') : {model.startswith('anthropic')}")
print(f"upper()                 : {model.upper()}")
print(f"'claude' in model       : {'claude' in model}")
