from neo4j import GraphDatabase


class Neo4jService:
    _instance = None

    def __init__(self):
        # 初始化 Neo4j 连接
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "gyb20010204"))  # 替换为你的信息

    @classmethod
    def get_instance(cls):
        # 实现单例模式，确保只创建一个实例
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def close(self):
        # 关闭数据库连接
        self.driver.close()

    def query_process(self, process_type: str):
        # 查询工艺对应的子工艺
        with self.driver.session() as session:
            query = """
            MATCH (p:Process {name: $process_type})-[:INCLUDES]->(s:SubProcess)
            RETURN s.name AS sub_process
            """
            result = session.run(query, process_type=process_type)
            return [record["sub_process"] for record in result]

    def query_all_processes(self):
        # 查询所有的工艺类型
        with self.driver.session() as session:
            query = """
            MATCH (p:Process)
            RETURN p.name AS process_type
            """
            result = session.run(query)
            return [record["process_type"] for record in result]
