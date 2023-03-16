import redis

REDIS_HOST = '127.0.0.1'

class GameState:
    def __init__(self):
        self.redis = redis.Redis(host=REDIS_HOST, port=6379)

    def add_player(self, name, ip, port):
        self.redis.hset(f"player:{name}", mapping={'name': name, 'ip': ip, 'port': port})

    def remove_player
