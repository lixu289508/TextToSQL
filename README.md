<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">TextToSQL v1.0.0</h1>
<h4 align="center">Natural language SQL generation tool based on MCP protocol - generate various SQL statements through conversation, learn SQL or handle database operations!</h4>
<p align="center">
	<a href="https://github.com/lixu289508/TextToSQL/stargazers"><img src="https://img.shields.io/github/stars/lixu289508/TextToSQL?style=flat-square&logo=GitHub"></a>
	<a href="https://github.com/lixu289508/TextToSQL/network/members"><img src="https://img.shields.io/github/forks/lixu289508/TextToSQL?style=flat-square&logo=GitHub"></a>
	<a href="https://github.com/lixu289508/TextToSQL/watchers"><img src="https://img.shields.io/github/watchers/lixu289508/TextToSQL?style=flat-square&logo=GitHub"></a>
	<a href="https://github.com/lixu289508/TextToSQL/blob/master/LICENSE"><img src="https://img.shields.io/github/license/lixu289508/TextToSQL.svg?style=flat-square"></a>
</p>

[English](README.md) | [中文简体](README_CN.md)

## Overview

TextToSQL is an open-source tool that allows users to generate various SQL statements using natural language. It leverages AI capabilities through the Model Context Protocol (MCP) to interpret user requirements and generate appropriate SQL statements. This tool can be used not only for database operations but also as an ideal assistant for learning SQL syntax.

## Project Branches

This project contains two main branches that provide different functionalities:

1. **main branch**: Complete database query tool
   - Generates SQL statements and executes queries
   - Returns actual query results
   - Suitable for scenarios requiring direct database information retrieval

2. **sql_builder branch**: Pure SQL generation tool
   - Only generates SQL statements without executing actual operations
   - Supports all types of SQL operations (SELECT, INSERT, UPDATE, DELETE, CREATE, etc.)
   - Ideal for SQL learning and teaching scenarios
   - Suitable for scenarios where SQL needs to be generated but executed by other systems

## Features

- **Natural Language to SQL**: Use plain English or Chinese to describe requirements and automatically generate SQL statements
- **Support for All SQL Operations**: Generate queries, inserts, updates, deletes, table creation, and more
- **Database Schema Caching**: Cache database structure for faster SQL generation
- **Support for Complex Statements**: Handle JOINs, subqueries, aggregations, transactions, and other advanced SQL features
- **Interactive Refinement**: Engage in a conversation to refine generated SQL statements
- **SQL Learning Tool**: Serve as an auxiliary tool for learning SQL syntax by viewing standard SQL formats for different operations

## Architecture

The system consists of several components:

1. **MCP Server**: Provides the interface between the AI model and the SQL generation tools
2. **Database Structure Retrieval**: Connects to your database to get table structure information (currently supports MySQL/MariaDB via PyMySQL)
3. **Cache Management**: Tools to cache and update database schema information
4. **SQL Generation**: Generates various SQL statements based on natural language requirements and database structure

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

3. Use natural language to generate SQL statements through the AI interface:
   - Write code to use the AI interface to process requirements
   - You can reference the prompts in the `prompt.py` file to guide the model in generating various SQL statements

4. SQL Generation Result Processing:
   The tool generates SQL statements and returns them without executing actual operations:
   ```python
   # Result processing logic in tools/query_table_data.py
   
   # Return the generated SQL statement without executing operations
   return {
     "status": "success",
     "message": f"SQL {operation_type} statement generated",
     "sql": sql,
     "operation_type": operation_type
   }
   ```

### SQL Generation Examples

- "Show me all employees in the IT department" → Generates SELECT query
- "Create a new customer table with ID, name, phone, and address fields" → Generates CREATE TABLE statement
- "Increase the salary of all employees in the sales department by 10%" → Generates UPDATE statement
- "Delete expired order records" → Generates DELETE statement
- "Add an email field to the customer table" → Generates ALTER TABLE statement

## Tools

The system provides several tools through the MCP interface:

- **get_table_data**: Generate various SQL statements (queries, inserts, updates, deletes, creates, etc.)
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
