import xml.etree.ElementTree as ET
import os

# 缓存文件路径
CACHE_FILE_PATH = "space.xml"


def get_cache_info(table_comment=None):
	"""
	获取缓存中的表和字段信息

	Args:
		table_comment: 表描述，如果为空则返回所有表的基本信息，否则返回指定表的字段信息

	Returns:
		缓存中的表信息或指定表的字段信息
	"""
	try:
		if not os.path.exists(CACHE_FILE_PATH):
			print(f"缓存文件不存在: {CACHE_FILE_PATH}")
			return {"error": "缓存文件不存在", "status": "failed"}

		tree = ET.parse(CACHE_FILE_PATH)
		root = tree.getroot()

		# 如果table_comment为空，返回所有表的名称和描述
		if not table_comment:
			tables_info = []
			
			for table in root.findall('./table'):
				table_name = table.get('name')
				table_comment = table.get('comment')
				tables_info.append({"table_name": table_name, "table_comment": table_comment})

			return {"tables": tables_info, "status": "success"}
		
		# 如果指定了table_comment，查找对应的表并返回其字段信息
		else:
			table_found = False
			fields_info = []
			table_name = ""
			
			# 遍历查找匹配描述的表
			for table in root.findall('./table'):
				if table.get('comment') == table_comment:
					table_found = True
					table_name = table.get('name')

					# 获取该表的所有字段
					for field in table.findall('./field'):
						field_info = {
							"field_name": field.get('name'),
							"field_type": field.get('f_type'),
							"field_comment": field.get('comment')
						}
						fields_info.append(field_info)

					break
			
			# 如果找到了表，返回其字段信息
			if table_found:
				return {
					"table_name": table_name,
					"table_comment": table_comment,
					"fields": fields_info,
					"status": "success"
				}
			# 如果没有找到表，返回False
			else:
				print(f"未找到表描述为 '{table_comment}' 的表")
				return False

	except Exception as e:
		print(f"获取缓存信息失败: {str(e)}")
		return {"error": f"获取缓存信息失败: {str(e)}", "status": "failed"}


if __name__ == "__main__":
	# 测试所有表
	all_tables = get_cache_info()
	print("\n所有表信息:", all_tables)
	
	# 测试单个表
	single_table = get_cache_info("员工表")
	print("\n员工表信息:", single_table)
	
	# 测试不存在的表
	non_exist = get_cache_info("不存在的表")
	print("\n不存在的表:", non_exist)
