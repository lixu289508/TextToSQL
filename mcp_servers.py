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

# 缓存文件路径 - 更新为与工具文件一致的路径
CACHE_FILE_PATH = "space.xml"


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
	生成SQL语句并返回，不执行实际操作。
	支持所有SQL操作，包括SELECT、INSERT、UPDATE、DELETE、CREATE、DROP等。

	Args:
		table_name (str): 表名称或完整SQL语句（如"employee"或"SELECT * FROM employee JOIN department ON..."或"INSERT INTO employee..."）
		fields (str, optional): 要查询的字段列表，多个字段用逗号分隔，如"id,name,salary"，为空则查询所有字段（仅用于简单查询）
		limit (int, optional): 返回结果的最大行数，默认为10行（仅用于查询操作）
		where_clause (str, optional): WHERE条件子句（不含WHERE关键字），如"department='IT' AND salary>5000"（仅用于简单操作）

	Returns:
		dict: 包含生成的SQL语句的字典，如{"status": "success", "message": "SQL查询语句已生成", "sql": "SELECT * FROM employee LIMIT 10"}
	"""
	db_connection = create_db_connection()
	return query_table_data(db_connection, table_name, fields, limit, where_clause)


# 注册获取缓存信息工具
@mcp.tool()
def get_cache_info(table_comment: str = None):
	"""
	获取缓存中的表和字段信息
	
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
	更新缓存中的表和字段信息
	
	Args:
		table_comment (str, optional): 表描述/表注释，如"员工表"。如果为None，则更新所有表的基本信息(不含字段)；
		                               如果提供表描述，则更新指定表的完整字段结构
	
	Returns:
		dict: 更新状态信息，包含成功/失败状态和消息，如{"status": "success", "message": "成功更新员工表的字段信息"}
		     或{"status": "error", "message": "未找到匹配的表"}
	"""
	print(f"调用更新缓存信息工具，表描述: {table_comment}")
	return tool_update_cache_info(table_comment, db_connection=create_db_connection(), sql_config=sql_config)


if __name__ == "__main__":
	mcp.run(transport='sse')
