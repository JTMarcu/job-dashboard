# tests/test_fetcher.py

from utils.data_fetcher import call_mcp_tool

def test_fetch_job_postings_returns_results():
    result = call_mcp_tool("fetch_job_postings", {
        "query": "developer",
        "location": "remote",
        "results_per_page": 1
    })
    assert isinstance(result, dict)
    assert "results" in result
    assert isinstance(result["results"], list)
