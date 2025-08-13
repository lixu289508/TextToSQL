from typing import List, Dict, Any


def get_all_tables(db_connection, database_name: str) -> List[Dict[str, Any]]:
    """
    查询数据库内所有表
    
    Args:
        db_connection: 数据库连接对象
        database_name: 数据库名称
    
    Returns:
        表信息列表，包含表名称和注释
    """
    result = []
    if db_connection is None:
        return [{"error": "数据库未连接"}]
    
    try:
        with db_connection.cursor() as cursor:
            # 执行查询所有表的SQL，只获取表名和注释
            cursor.execute("""
                SELECT 
                    table_name AS '表名',
                    table_comment AS '表说明'
                FROM 
                    information_schema.TABLES 
                WHERE 
                    table_schema = %s
                ORDER BY 
                    table_name
            """, (database_name,))
            
            tables = cursor.fetchall()
            result = list(tables)  # 转换为列表格式
    except Exception as e:
        result = [{"error": f"查询表失败: {str(e)}"}]
    
    return result 