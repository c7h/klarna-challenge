import os
import redis
import logging
from flask import Flask
from flask_restful import Api, Resource
from werkzeug.routing import IntegerConverter
from errors import errors
from functions import (
        fib_simple,
        ackermann_simple,
        ackermann_wolfram,
        ackermann_redis,
        factorial,
)
from middleware import setup_metrics

# configure logging
log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

wolfram_id = os.environ.get("WOLFRAM_APP_ID")
redis_host = os.environ.get("REDIS_HOST")

log.info("Staring service; Redis at redis://{}".format(redis_host))
log.info("Using Wolfram App {}".format(wolfram_id))

app = Flask(__name__)
api = Api(app, catch_all_404s=True, errors=errors)
setup_metrics(app)


class SimpleFibonacci(Resource):
    """Simple fibonacci using in-memory caching"""
    def get(self, x):
        result = fib_simple(x)
        return {"arguments": {"x": x},
                "result": result}


class SimpleAckermann(Resource):
    """Simple Ackermann function endpoint"""
    def get(self, m, n):
        result = ackermann_simple(m, n)
        return {"arguments": {"m": m, "n": n},
                "result": result}


class SimpleFactorial(Resource):
    """Simple factorial endpoint"""
    def get(self, x):
        if x < 0:
            raise ValueError
        result = factorial(x)
        return {"arguments": {"x": x},
                "result": result}


class ServiceAckermann(Resource):
    """Ackermann as a Service Endpoints"""
    def get(self, m, n):
        result = ackermann_wolfram(m, n, wolfram_id)
        return {"arguments": {"m": m, "n": n},
                "result": result}


class CachedAckermann(Resource):
    """Ackermann using shared, persisted cache"""
    def get(self, m, n):
        redis_instance = redis.Redis('redis')
        result = ackermann_redis(m, n, redis_instance)
        return {"arguments": {"m": m, "n": n},
                "result": result}


# Add Integer Converter for signed ints
class SignedIntConverter(IntegerConverter):
    regex = r'-?\d+'


app.url_map.converters['signed_int'] = SignedIntConverter

api.add_resource(SimpleFibonacci, '/functions/simple/fibonacci/<signed_int:x>')
api.add_resource(SimpleAckermann, '/functions/simple/ackermann/<int:m>/<int:n>')
api.add_resource(SimpleFactorial, '/functions/simple/factorial/<signed_int:x>')
# Advanced Functions come here
api.add_resource(CachedAckermann, '/functions/advanced/ackermann/<int:m>/<int:n>')
api.add_resource(ServiceAckermann, '/functions/service/ackermann/<int:m>/<int:n>')
