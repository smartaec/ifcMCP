# ifcMCP
An MCP server that enables LLM agents to talk with IFC (Industry Foundation Classes) files

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=smartaec/ifcMCP&type=Date)](https://www.star-history.com/#smartaec/ifcMCP&Date)

# related packages
1. ifcopenshell
2. FastMCP

# supported tools
1. get_entities
2. get_named_property_of_entities
3. get_entity_properties
4. get_entity_location
5. get_entities_in_spatial
6. get_openings_on_wall
7. get_space_boundaries

# how to use it
1. clone this repo
2. install packages needed: [ifcopenshell](https://docs.ifcopenshell.org/ifcopenshell-python/installation.html), FastMCP
3. start command line interface in folder `ifcMCP`, and run the command `python server.py`
4. open your favorite LLM tools and setup MCP server with the following configuration:
```
{
  "mcpServers": {
    "ifcMCP-server": {
      "name": "ifcMCP",
      "type": "streamableHttp",
      "description": "A simple MCP server to handle ifc files",
      "isActive": true,
      "tags": [],
      "baseUrl": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

# contributors
Jia-Rui Lin (lin611#tsinghua.edu.cn)

Department of Civil Engineering, Tsinghua University

Key Laboratory of Digital Construction and Digital Twin led by Prof. Peng Pan

# cite us
```
@article{JRLin2506,
	author = {Jia-Rui Lin and Peng Pan},
	title = {ifcMCP: Enabling LLM agents to talk with IFC files},
	year = {2025}
}
```