<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">TextToSQL v1.0.0</h1>
<h4 align="center">Natural language database query tool based on MCP protocol - access database information through conversation without writing SQL!</h4>
<p align="center">
	<a href="https://github.com/lixu289508/TextToSQL/stargazers"><img src="https://img.shields.io/github/stars/lixu289508/TextToSQL?style=flat-square&logo=GitHub"></a>
	<a href="https://github.com/lixu289508/TextToSQL/network/members"><img src="https://img.shields.io/github/forks/lixu289508/TextToSQL?style=flat-square&logo=GitHub"></a>
	<a href="https://github.com/lixu289508/TextToSQL/watchers"><img src="https://img.shields.io/github/watchers/lixu289508/TextToSQL?style=flat-square&logo=GitHub"></a>
	<a href="https://github.com/lixu289508/TextToSQL/blob/master/LICENSE"><img src="https://img.shields.io/github/license/lixu289508/TextToSQL.svg?style=flat-square"></a>
</p>

[English](README.md) | [中文简体](README_CN.md)

## Overview

TextToSQL is an open-source tool that allows users to query databases using natural language. It leverages AI capabilities through the Model Context Protocol (MCP) to interpret user queries, generate appropriate SQL statements, and execute them against a database.

## Project Branches

This project offers two main branches to accommodate different use cases:

- **main branch**: Complete database query tool
  - Generates SQL statements and executes queries
  - Returns actual query results
  - Suitable for scenarios requiring direct database information retrieval

- **sql_builder branch**: Pure SQL generation tool
  - Only generates SQL statements without executing actual operations
  - Supports all types of SQL operations (SELECT, INSERT, UPDATE, DELETE, CREATE, etc.)
  - Ideal for SQL learning and teaching scenarios
  - Suitable for scenarios where SQL needs to be generated but executed by other systems

## Features

- **Natural Language Queries**: Query your database using plain English or Chinese
- **SQL Generation**: Automatically converts natural language to optimized SQL queries
- **Database Schema Caching**: Caches database structure for faster query generation
- **Support for Complex Queries**: Handles JOINs, subqueries, aggregations, and more
- **Interactive Query Refinement**: Engage in a conversation to refine your database queries

## Architecture

The system consists of several components:

1. **MCP Server**: Provides the interface between the AI model and the database tools
2. **Database Connection**: Connects to your database (currently supports MySQL/MariaDB via PyMySQL)
3. **Cache Management**: Tools to cache and update database schema information
4. **Query Execution**: Tools to execute SQL queries and process results

## Installation

### Prerequisites

- Python 3.8 or higher
- Access to a MySQL/MariaDB database

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/texttosql.git
   cd texttosql
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your database connection:
   Edit the `mcp_servers.py` file to update the `get_apollo_confs()` function with your database credentials.

## Usage

1. Start the MCP server:
   ```bash
   python mcp_servers.py
   ```

2. Configure the MCP server connection in your AI client:
   ```json
   {
     "mcpServers": {
       "sql bot": {
         "timeout": 60,
         "type": "sse",
         "url": "http://127.0.0.1:8000/sse"
       }
     }
   }
   ```

3. Use natural language to query your database through the AI interface:
   - Write code to use the AI interface to process queries
   - You can reference the prompts in the `prompt.py` file to guide the model in generating SQL and executing queries

4. Query Result Processing:
   The current approach saves query results to a fixed path JSON file while also returning the results in JSON format:
   ```python
   # Result processing logic in tools/query_table_data.py
   
   # Save to JSON file
   json_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data.json')
   os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
   with open(json_file_path, 'w', encoding='utf-8') as f:
       json.dump(result_data, f, ensure_ascii=False, indent=4)
   
   # Also return JSON format data
   return {
     "status": "success",
     "message": f"Query successful, saved {len(rows)} records to JSON file",
     "fields_count": len(field_names),
     "records_count": len(rows),
     "sql": sql,  # Return the executed SQL statement for debugging
     "data": result_data  # Contains actual results
   }
   ```

### Example Queries

- "Show me all employees in the IT department"
- "What's the average salary by department?"
- "Find customers who placed orders in the last 3 months"
- "List the top 5 products by sales volume"

## Tools

The system provides several tools through the MCP interface:

- **get_table_data**: Execute SQL queries against the database
- **get_cache_info**: Retrieve cached table and field information
- **update_cache_info**: Update the cache with fresh database schema information

## Customization

You can customize the system by:

1. Modifying the prompt in `prompt.py` to adjust how the AI interprets queries
2. Extending the tools in the `tools/` directory to add new functionality
3. Updating the database connection logic to support additional database types

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- Thanks to all contributors who have helped to improve this project
- Special thanks to the open-source community for providing the tools and libraries that make this project possible

## Contact & Support

### Contact me
<img src="https://toolkitai.cn/wx.png" width="300" alt="WeChat QR Code">

### Support This Project
<img src="https://toolkitai.cn/zs.jpg" width="300" alt="Appreciation Code">
