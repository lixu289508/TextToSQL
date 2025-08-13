import re
from typing import Dict, Any, Optional


def query_table_data(
		db_connection,
		table_name: str,
		fields: Optional[str] = None,
		limit: int = 10,
		where_clause: Optional[str] = None
) -> Dict[str, Any]:
	"""
	生成SQL查询语句并返回，不执行实际查询。
	支持复杂查询，包括连接查询、子查询等。
	仅支持查询操作，禁止执行插入、修改、删除等数据修改操作。
	
	本工具只负责生成SQL语句，不执行查询。

	Args:
		db_connection: 数据库连接对象（在此版本中不使用）
		table_name: 表名称或完整SQL查询语句（如包含JOIN、子查询等）
		fields: 要查询的字段，多个字段用逗号分隔，为空则查询所有字段
		limit: 返回行数限制，默认10行
		where_clause: 可选的WHERE条件，不含WHERE关键字

	Returns:
		包含生成的SQL语句的字典
	"""
	# 安全检查：确保SQL操作仅为查询，不包含修改操作
	if isinstance(table_name, str):
		sql_lower = table_name.lower()
		unsafe_keywords = ['insert', 'update', 'delete', 'drop', 'alter', 'truncate', 'create', 'replace']

		for keyword in unsafe_keywords:
			if keyword in sql_lower:
				return {
					"status": "error",
					"message": f"安全限制：不允许执行 {keyword.upper()} 操作，仅支持查询操作"
				}

	# 判断table_name是否是SQL语句（含有JOIN、SELECT等关键字）
	is_sql_query = re.search(r'\b(JOIN|SELECT|FROM|UNION|INTERSECT|EXCEPT|GROUP BY|ORDER BY|HAVING)\b',
							 table_name, re.IGNORECASE) is not None

	if is_sql_query:
		# 再次进行安全检查，确保只执行SELECT查询
		if not re.search(r'^\s*SELECT\b', table_name, re.IGNORECASE):
			return {
				"status": "error",
				"message": "安全限制：复杂SQL查询必须以SELECT开头"
			}

		# 如果是SQL语句，直接使用它
		sql = table_name

		# 如果有WHERE条件但SQL语句中没有WHERE，添加它
		if where_clause and where_clause.strip() and 'WHERE' not in sql.upper():
			sql += f" WHERE {where_clause}"
		# 如果SQL语句中已有WHERE条件且用户提供了额外条件
		elif where_clause and where_clause.strip() and 'WHERE' in sql.upper():
			sql += f" AND {where_clause}"

		# 添加LIMIT限制（如果SQL中没有）
		if 'LIMIT' not in sql.upper() and limit > 0:
			sql += f" LIMIT {limit}"
	else:
		# 构建简单查询SQL
		field_list = '*' if not fields else fields
		sql = f"SELECT {field_list} FROM `{table_name}`"

		# 如果有WHERE条件，添加到查询中
		if where_clause and where_clause.strip():
			sql += f" WHERE {where_clause}"

		# 添加LIMIT限制
		if limit > 0:
			sql += f" LIMIT {limit}"

	print(f"生成SQL查询: {sql}")

	# 直接返回生成的SQL语句，不执行查询
	return {
		"status": "success",
		"message": "SQL查询语句已生成",
		"sql": sql
	}
