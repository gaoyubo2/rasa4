from neo4j import GraphDatabase
import logging
import sys

logger = logging.getLogger(__name__)


class Neo4jConnector:
    def __init__(self, uri, user, password):
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            logger.debug('Neo4j 数据库连接成功')
        except Exception as e:
            logger.error('Neo4j 数据库连接失败: {}, 请检查'.format(e))
            sys.exit(-1)

    def close(self):
        self.driver.close()
