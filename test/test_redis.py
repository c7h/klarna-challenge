import unittest
import redis
from klarnachallenge.functions import ackermann_redis


class RedisTestCase(unittest.TestCase):
    def setUp(self):
        # using local redis server
        # TODO: Setup mock tests
        self.myredis = redis.Redis('localhost')
        print(self.myredis)

    def test_redis_ackermann_3_3(self):
        res = ackermann_redis(3, 3, self.myredis)
        print(res)
        self.assertEqual(res, 61)

    @unittest.skip("will exceed recursion depth")
    def test_redis_ackermann_4_2(self):
        res = ackermann_redis(4, 2, self.myredis)
        print(res)
