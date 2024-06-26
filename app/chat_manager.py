from redis import Redis

class ChatManager:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = Redis(host=host, port=port, db=db)

    def save_message(self, message):
        self.redis.rpush("chat", message)

    def get_messages(self):
        return self.redis.lrange("chat", 0, -1)
