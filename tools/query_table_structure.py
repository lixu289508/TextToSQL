from typing import List, Dict, Any


def query_table_structure(db_connection, database_name: str, table_name: str) -> List[Dict[str, Any]]:
    """
    查询数据表结构
    
    Args:
        db_connection: 数据库连接对象
        database_name: 数据库名称
        table_name: 表名称
    
    Returns:
        表结构信息，包含字段名、字段类型和字段说明
    """
    result = []
    if db_connection is None:
        return [{"error": "数据库未连接"}]
    
    try:
        with db_connection.cursor() as cursor:
            # 执行查询表结构的SQL，只获取字段名、类型和注释
            cursor.execute("""
                SELECT 
                    column_name AS '字段名',
                    column_type AS '字段类型',
                    column_comment AS '字段说明'
                FROM 
                    information_schema.COLUMNS 
                WHERE 
                    table_schema = %s AND table_name = %s
                ORDER BY 
                    ordinal_position
            """, (database_name, table_name))
            
            columns = cursor.fetchall()
            result = list(columns)  # 转换为列表格式
    except Exception as e:
        result = [{"error": f"查询表结构失败: {str(e)}"}]
    
    return result 