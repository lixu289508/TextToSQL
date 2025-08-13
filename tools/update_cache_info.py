import xml.etree.ElementTree as ET
import os
import pymysql


# 缓存文件路径
CACHE_FILE_PATH = "space.xml"


def update_cache_info(table_comment=None, db_connection=None, sql_config=None):
	"""
	更新缓存中的表和字段信息
	
	Args:
		table_comment: 表名称，如果为空则更新所有表基本信息(不含字段)
		db_connection: 数据库连接
		sql_config: 数据库配置

	Returns:
		更新状态信息
	"""
	print(f"开始更新缓存信息，表注释: {table_comment}")

	# 导入必要的工具函数
	from tools.get_all_tables import get_all_tables
	from tools.query_table_structure import query_table_structure

	# 获取所有表信息
	tables_info = get_all_tables(db_connection, sql_config["database"])
	if not tables_info:
		return {"error": "获取表信息失败", "status": "failed"}

	# 如果表名为空，只更新所有表的基本信息(表名和表说明)，不更新字段
	if not table_comment:
		print("表名为空，更新所有表基本信息(不含字段)")

		# 更新所有表的基本信息
		return update_all_tables_basic_info(tables_info)

	# 如果指定了表名，只更新该表的字段结构
	else:
		print(f"更新指定表的字段结构: {table_comment}")

		# 首先获取表的名字
		table_name = ""
		if tables_info:
			for table, comment in tables_info:
				if table_comment == comment:
					table_name = table

		if not table_name:
			table_name = table_comment  # 如果没找到注释，使用表名作为默认注释
		# 获取表结构
		table_structure = query_table_structure(db_connection, sql_config["database"], table_name)

		if not table_structure :
			return {"error": f"获取表 {table_name} 的结构失败", "status": "failed"}

		# 更新指定表的字段结构
		return update_table_fields(table_name, table_comment, table_structure)


# except Exception as e:
# 	print(f"更新缓存信息失败: {str(e)}")
# 	return {"error": f"更新缓存信息失败: {str(e)}", "status": "failed"}


def update_all_tables_basic_info(tables):
	"""
	只更新所有表的基本信息(表名和表说明)，不更新字段
	
	Args:
		tables: 表信息列表，包含表名称和表说明
		
	Returns:
		更新状态信息
	"""
	try:
		print(f"更新所有表的基本信息，共 {len(tables)} 个表")
		# 如果文件不存在，创建新的 XML 根元素
		if not os.path.exists(CACHE_FILE_PATH):
			print(f"缓存文件不存在，创建新文件: {CACHE_FILE_PATH}")
			root = ET.Element("tables")
			tree = ET.ElementTree(root)
		else:
			# 否则读取现有文件
			tree = ET.parse(CACHE_FILE_PATH)
			root = tree.getroot()

		# 保存现有的字段信息以便稍后恢复
		existing_fields = {}
		for existing_table in root.findall('./table'):
			table_name = existing_table.get('name')
			if table_name:
				# 收集该表所有字段信息
				fields = []
				for field in existing_table.findall('./field'):
					fields.append({
						'name': field.get('name'),
						'comment': field.get('comment')
					})
				if fields:
					existing_fields[table_name] = fields
		# 清空现有的表定义
		for child in list(root):
			root.remove(child)

		# 添加所有表的基本信息
		for name, comment in tables:
			add_table_name = name
			add_table_comment = comment

			table_element = ET.SubElement(root, "table", name=add_table_name, comment=add_table_comment)

			# 如果该表之前有字段信息，恢复它们
			if add_table_name in existing_fields:
				for field in existing_fields[add_table_name]:
					ET.SubElement(
							table_element,
							"field",
							name=field['name'],
							comment=field['comment']
					)

		# 保存到文件
		tree.write(CACHE_FILE_PATH, encoding='utf-8', xml_declaration=True)

		return {
			"message": f"已更新 {len(tables)} 个表的基本信息",
			"status": "success"
		}
	except Exception as e:
		print(f"更新所有表基本信息失败: {str(e)}")
		return {"error": f"更新所有表基本信息失败: {str(e)}", "status": "failed"}


def update_table_fields(table_name, table_comment, fields):
	"""
	更新指定表的字段结构
	
	Args:
		table_name: 表名称
		table_comment: 表说明
		fields: 字段信息列表
		
	Returns:
		更新状态信息
	"""
	try:
		print(f"更新表 {table_name} 的字段结构，共 {len(fields)} 个字段")
		# 如果文件不存在，创建新的 XML 根元素
		if not os.path.exists(CACHE_FILE_PATH):
			print(f"缓存文件不存在，创建新文件: {CACHE_FILE_PATH}")
			root = ET.Element("tables")
			tree = ET.ElementTree(root)
		else:
			# 否则读取现有文件
			tree = ET.parse(CACHE_FILE_PATH)
			root = tree.getroot()
		# 查找是否已存在该表
		existing_table = None
		for table in root.findall('./table'):
			if table.get('name') == table_name:
				existing_table = table
				break

		# 如果表不存在，创建新表元素
		if existing_table is None:
			print(f"创建新表: {table_name}")
			existing_table = ET.SubElement(root, "table", name=table_name, comment=table_comment)
		else:
			# 更新表说明
			existing_table.set('comment', table_comment)
			# 清除原有字段
			for field in list(existing_table):
				existing_table.remove(field)
		# 添加字段信息
		for name, f_type, comment in fields:
			ET.SubElement(existing_table, "field", name=name, f_type=f_type, comment=comment)

		# 保存到文件
		tree.write(CACHE_FILE_PATH, encoding='utf-8', xml_declaration=True)

		return {
			"message": f"已更新表 {table_name} 的 {len(fields)} 个字段",
			"status": "success"
		}
	except Exception as e:
		print(f"更新表 {table_name} 字段结构失败: {str(e)}")
		return {"error": f"更新表 {table_name} 字段结构失败: {str(e)}", "status": "failed"}
