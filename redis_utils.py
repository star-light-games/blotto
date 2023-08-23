import redis as r
from typing import Optional, Any
from redis_lock import Lock
import json

redis = r.Redis(connection_pool=r.ConnectionPool(host='localhost', port=6379, db=6))

def rget(key: str) -> Optional[str]:
    raw_result = redis.get(key)
    return raw_result.decode('utf-8') if raw_result is not None else None


def can_be_inted(x):
    try:
        int(x)
        return True
    except:
        return False


def jsonKeys2int(x):
    if isinstance(x, dict):
        return {int(k) if can_be_inted(k) else k:v for k,v in x.items()}
    return x


def rget_json(key: str):
    raw_result = rget(key)
    return json.loads(raw_result, object_hook=jsonKeys2int) if raw_result is not None else None


def rset(key: str, value: Any) -> None:
    redis.set(key, value)


def rset_json(key: str, value: Any) -> None:
    rset(key, json.dumps(value))


def rlock(key: str):
    return Lock(redis, key)
