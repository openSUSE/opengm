import logging

from redis import BlockingConnectionPool, Redis

from opengm import REDIS_HOST, REDIS_PORT, REDIS_PWD

LOGGER = logging.getLogger(__name__)
pool = None
REDIS = None


def init_redis():
    LOGGER.debug("Initializing Redis..")
    pool = BlockingConnectionPool(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PWD,
    )
    Redis(connection_pool=pool)
    LOGGER.debug("Redis init complete!")
