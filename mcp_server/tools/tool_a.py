# mcp_server/tools/tool_a.py

def do_something(input1="default", input2=None):
    return {
        "field_a": input1,
        "field_b": input2,
        "message": "Tool A executed successfully"
    }
