# tests/test_fetcher.py

from utils.data_fetcher import call_mcp_tool

def test_tool_a_returns_fields():
    result = call_mcp_tool("tool_a", {"input1": "test_value"})
    assert isinstance(result, dict)
    assert "field_a" in result
    assert "message" in result
