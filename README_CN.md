<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">TextToSQL v1.0.0</h1>
<h4 align="center">基于MCP协议的自然语言SQL生成工具，直接用对话方式生成各类SQL语句，学习SQL或处理数据库操作！</h4>
<p align="center">
	<a href="https://github.com/lixu289508/TextToSQL/stargazers"><img src="https://img.shields.io/github/stars/lixu289508/TextToSQL?style=flat-square&logo=GitHub"></a>
	<a href="https://github.com/lixu289508/TextToSQL/network/members"><img src="https://img.shields.io/github/forks/lixu289508/TextToSQL?style=flat-square&logo=GitHub"></a>
	<a href="https://github.com/lixu289508/TextToSQL/watchers"><img src="https://img.shields.io/github/watchers/lixu289508/TextToSQL?style=flat-square&logo=GitHub"></a>
	<a href="https://github.com/lixu289508/TextToSQL/blob/master/LICENSE"><img src="https://img.shields.io/github/license/lixu289508/TextToSQL.svg?style=flat-square"></a>
</p>

[English](README.md) | [中文简体](README_CN.md)

## 概述

TextToSQL是一个开源工具，允许用户使用自然语言生成各类SQL语句。它通过模型上下文协议(MCP)利用AI能力来解释用户需求，生成适当的SQL语句。该工具不仅可用于数据库操作，还是学习SQL语法的理想助手。

## 项目分支

本项目包含两个主要分支，提供不同的功能：

1. **main分支**：完整的数据库查询工具
   - 生成SQL语句并执行查询
   - 返回实际查询结果
   - 适合需要直接获取数据库信息的场景

2. **sql_builder分支**：纯SQL生成工具
   - 仅生成SQL语句，不执行实际操作
   - 支持所有类型的SQL操作（SELECT、INSERT、UPDATE、DELETE、CREATE等）
   - 适合SQL学习和教学场景
   - 适合需要生成SQL但由其他系统执行的场景

## 特性

- **自然语言转SQL**：使用普通中文或英文描述需求，自动生成SQL语句
- **支持全部SQL操作**：生成查询、插入、更新、删除、创建表等各类SQL语句
- **数据库结构缓存**：缓存数据库结构以加快SQL生成
- **支持复杂语句**：处理JOIN、子查询、聚合、事务等高级SQL功能
- **交互式优化**：通过对话方式优化生成的SQL语句
- **SQL学习工具**：作为学习SQL语法的辅助工具，查看不同操作的标准SQL写法

## 架构

系统由以下几个组件组成：

1. **MCP服务器**：提供AI模型和SQL生成工具之间的接口
2. **数据库结构获取**：连接到您的数据库获取表结构信息（目前通过PyMySQL支持MySQL/MariaDB）
3. **缓存管理**：用于缓存和更新数据库结构信息的工具
4. **SQL生成**：根据自然语言需求和数据库结构生成各类SQL语句

## 安装

### 前提条件

- Python 3.8或更高版本
- 访问MySQL/MariaDB数据库的权限

### 设置

1. 克隆仓库：
   ```bash
   git clone https://github.com/yourusername/texttosql.git
   cd texttosql
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 配置数据库连接：
   编辑`mcp_servers.py`文件，更新`get_apollo_confs()`函数中的数据库凭据。

## 使用方法

1. 启动MCP服务器：
   ```bash
   python mcp_servers.py
   ```

2. 在AI客户端中配置MCP服务器连接：
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

3. 通过AI接口使用自然语言生成SQL语句：
   - 编写代码，使用AI接口调用模型进行处理
   - 可以参考`prompt.py`文件中的提示词来指导模型生成各类SQL语句

4. SQL生成结果的处理方式：
   工具会生成SQL语句并返回，不执行实际操作：
   ```python
   # 在tools/query_table_data.py中的结果处理逻辑
   
   # 直接返回生成的SQL语句，不执行操作
   return {
     "status": "success",
     "message": f"SQL{operation_type}语句已生成",
     "sql": sql,
     "operation_type": operation_type
   }
   ```

### SQL生成示例

- "显示IT部门的所有员工" → 生成SELECT查询
- "创建一个新的客户表，包含ID、姓名、电话和地址字段" → 生成CREATE TABLE语句
- "将销售部所有员工的薪资上调10%" → 生成UPDATE语句
- "删除过期的订单记录" → 生成DELETE语句
- "为客户表添加邮箱字段" → 生成ALTER TABLE语句

## 工具

系统通过MCP接口提供了几个工具：

- **get_table_data**：生成各类SQL语句（查询、插入、更新、删除、创建等）
- **get_cache_info**：检索缓存的表和字段信息
- **update_cache_info**：使用最新的数据库结构更新缓存

## 自定义

您可以通过以下方式自定义系统：

1. 修改`prompt.py`中的提示词，调整AI解释查询的方式
2. 扩展`tools/`目录中的工具，添加新功能
3. 更新数据库连接逻辑，支持其他类型的数据库

## 许可证

该项目采用MIT许可证 - 详情请参阅LICENSE文件。

## 致谢

- 感谢所有帮助改进此项目的贡献者
- 特别感谢开源社区提供的工具和库，使这个项目成为可能

## 联系与支持

### 联系我
<img src="https://toolkitai.cn/wx.png" width="300" alt="微信二维码">

### 支持本项目
<img src="https://toolkitai.cn/zs.jpg" width="300" alt="赞赏码">
