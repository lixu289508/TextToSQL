import json
import os
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
	查询数据表数据，将结果保存到JSON文件。
	支持复杂查询，包括连接查询、子查询等。
	仅支持查询操作，禁止执行插入、修改、删除等数据修改操作。
	
	本工具负责执行查询和更新前端数据源，SQL语句的生成由大模型负责。

	Args:
		db_connection: 数据库连接对象
		table_name: 表名称或完整SQL查询语句（如包含JOIN、子查询等）
		fields: 要查询的字段，多个字段用逗号分隔，为空则查询所有字段
		limit: 返回行数限制，默认10行
		where_clause: 可选的WHERE条件，不含WHERE关键字

	Returns:
		查询状态信息，不包含实际数据
	"""
	if db_connection is None:
		return {"status": "error", "message": "数据库未连接"}

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

	try:
		with db_connection.cursor() as cursor:
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

			print(f"执行SQL查询: {sql}")

			# 执行查询
			cursor.execute(sql)

			# 获取字段名
			field_names = [desc[0] for desc in cursor.description]

			# 获取结果
			rows = cursor.fetchall()

			# 准备JSON数据
			result_data = {
				"sql": sql,  # 包含实际执行的SQL语句，便于调试
				"fields": field_names,  # 使用实际返回的字段名
				"field_comments": {},  # 字段描述信息（如果可获取）
				"records": []
			}

			# 转换查询结果为记录列表
			for row in rows:
				record = {}
				for i, field_name in enumerate(field_names):
					# 适当处理各种数据类型
					if row[i] is None:
						record[field_name] = None
					else:
						record[field_name] = str(row[i])
				result_data["records"].append(record)

			# 保存到JSON文件
			json_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data.json')
			os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
			with open(json_file_path, 'w', encoding='utf-8') as f:
				json.dump(result_data, f, ensure_ascii=False, indent=4)


			# 返回查询状态信息，但不包含实际数据
			return {
				"status": "success",
				"message": f"数据查询成功，已保存 {len(rows)} 条记录到JSON文件",
				"fields_count": len(field_names),
				"records_count": len(rows),
				"sql": sql,  # 返回执行的SQL语句，便于调试
				"data": result_data  # 包含实际结果，如果不想暴露数据，可以注释掉，并且修改上方注释的保存逻辑
			}

	except Exception as e:
		return {
			"status": "error",
			"message": f"查询失败: {str(e)}"
		}
