import pymysql
from typing import Optional
from tools.query_table_data import query_table_data
from tools.update_cache_info import update_cache_info as tool_update_cache_info
from tools.get_cache_info import get_cache_info as tool_get_cache_info
from mcp.server.fastmcp import FastMCP

# Create server
mcp = FastMCP("sql bot")


def get_apollo_confs() -> dict:
	return {
		"host": '******************',  # 仅包含主机地址
		"database": '******************',  # 单独存放数据库名
		"username": '******************',
		"password": '******************'
	}


# 获取数据库配置
sql_config = get_apollo_confs()


def create_db_connection():
	"""创建数据库连接"""
	try:
		connection = pymysql.connect(
				host=sql_config["host"],
				user=sql_config["username"],
				password=sql_config["password"],
				database=sql_config["database"],
		)
		# print(f"成功连接到数据库: {sql_config['database']}")
		return connection
	except Exception as e:
		print(f"连接数据库失败: {e}")
		return None


# 注册SQL语句生成工具
@mcp.tool()
def get_table_data(table_name: str, fields: Optional[str] = None, limit: int = 10, where_clause: Optional[str] = None):
	"""
	根据之前获取到的表信息然后构建为 SQL 查询语句，然后根据本工具的格式要求入参；
	本工具会执行 SQL 然后将查询结果进行返回
	示例:
	- 简单查询: get_table_data("employee", "name,age,department", 20, "hire_date > '2023-01-01'")
	- 连接查询: get_table_data("SELECT e.name, d.department_name FROM employee e JOIN department d ON e.dept_id = d.id", limit=15)
	- 条件查询: get_table_data("SELECT * FROM employee WHERE hire_date BETWEEN '2023-01-01' AND '2023-03-31'", limit=10)
	- 聚合查询: get_table_data("SELECT department, COUNT(*) as employee_count FROM employee GROUP BY department", limit=20)

	Args:
		table_name (str): 表名称或完整SQL语句（如"employee"或"SELECT * FROM employee JOIN department ON..."）
		fields (str, optional): 要查询的字段列表，多个字段用逗号分隔，如"id,name,salary"，为空则查询所有字段（仅用于简单查询）
		limit (int, optional): 返回结果的最大行数，默认为10行
		where_clause (str, optional): WHERE条件子句（不含WHERE关键字），如"department='IT' AND salary>5000"（仅用于简单查询）

	Returns:
		dict: 包含查询结果的字典，结果仅在服务器端打印，不会返回给用户
	"""
	db_connection = create_db_connection()
	return query_table_data(db_connection, table_name, fields, limit, where_clause)


# 注册获取缓存信息工具
@mcp.tool()
def get_cache_info(table_comment: str = None):
	"""
	1. 此工具应作为查询流程的第一步使用，用于获取表的基本信息或字段结构。
	2. 首先直接调用 get_cache_info() 不传参获取所有表的基本信息。
	3. 然后根据用户需求，传入表描述参数获取指定表的详细字段信息。
	4. 如果获取到的表信息不完整或缺失字段信息，可以使用update_cache_info工具进行更新。
	
	Args:
		table_comment (str, optional): 表描述/表注释，如"员工表"。如果为None，则返回所有表的基本信息；
		                               如果提供表描述，则返回该表的详细字段信息
	
	Returns:
		list/dict/bool: 
		- 当table_comment为None时：返回所有表的列表，每个表包含表名和表描述，如[{"表名": "employee", "表说明": "员工表"}, ...]
		- 当指定table_comment时：返回该表的字段信息字典，包含字段名、类型和描述，如{"id": {"类型": "int", "描述": "主键"}, ...}
		- 当指定的表不存在时：返回False
	"""
	print(f"获取缓存信息：{table_comment}")
	return tool_get_cache_info(table_comment)


# 注册更新缓存信息工具
@mcp.tool()
def update_cache_info(table_comment: str = None):
	"""
	1. 当get_cache_info未返回所需表信息时，不传参调用此工具更新所有表的基本信息
	2. 当get_cache_info未返回表的字段信息时，传入表描述参数更新该表的字段结构
	3. 更新后再次调用get_cache_info获取最新信息

	Args:
		table_comment (str, optional): 表描述/表注释，如"员工表"。如果为None，则更新所有表的基本信息(不含字段)；
		                               如果提供表描述，则更新指定表的完整字段结构
	
	Returns:
		dict: 更新状态信息，包含成功/失败状态和消息，如{"status": "success", "message": "成功更新员工表的字段信息"}
		     或{"status": "error", "message": "未找到匹配的表"}
	"""
	print(f"调用更新缓存信息工具，表描述: {table_comment}")
	db_connection = create_db_connection()
	return tool_update_cache_info(table_comment, db_connection=db_connection, sql_config=sql_config)


if __name__ == "__main__":
	mcp.run(transport='sse')
