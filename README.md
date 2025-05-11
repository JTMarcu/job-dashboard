# MCP Dashboard Template

A minimal, generic template for building real-time dashboards using **Streamlit**, **FastAPI**, and **Model Context Protocol (MCP)**. This scaffold lets you plug in your own tools and visualize data with zero external dependencies.

---

## Features

✅ Minimal setup — just run and build  
✅ FastAPI + MCP-ready server  
✅ Streamlit UI for tool testing  
✅ Modular codebase for easy expansion  
✅ `.env` config support  
✅ No API keys required  

---

## Folder Structure

```

mcp-dashboard-template/
├── app.py
├── mcp\_server/
│   ├── server.py
│   └── tools/
│       └── tool\_a.py
├── modules/
│   └── dashboard\_template.py
├── utils/
│   └── data\_fetcher.py
├── tests/
│   └── test\_fetcher.py
├── .env
├── requirements.txt
├── setup\_env.bat / setup\_env.sh
├── start\_dashboard.bat / start\_dashboard.sh
└── README.md

````

---

## Setup Instructions

### Windows

```bash
setup_env.bat
start_dashboard.bat
````

### macOS / Linux

```bash
chmod +x setup_env.sh start_dashboard.sh
./setup_env.sh
./start_dashboard.sh
```

---

## Add a New Tool

1. Create a new file in `mcp_server/tools/` (e.g. `tool_b.py`):

```python
def do_something_else(param="test"):
    return {"output": param}
```

2. Register it in `server.py`:

```python
from tools.tool_b import do_something_else

@app.post("/tools/tool_b/invoke")
async def invoke_tool_b(request: Request):
    data = await request.json()
    return do_something_else(**data)
```

3. Call it via Streamlit UI:

   * Tool name: `tool_b`
   * Payload: `{ "param": "hello" }`

---

## Build Your Dashboard

Modify `modules/dashboard_template.py` to control how results display:

```python
def display_dashboard(data):
    st.title("Results")
    st.json(data)
```

---

## Run Tests

```bash
pytest tests/
```

---

## License

MIT License
Built with ❤️ using [Streamlit](https://streamlit.io), [FastAPI](https://fastapi.tiangolo.com), and [Model Context Protocol](https://modelcontextprotocol.io)