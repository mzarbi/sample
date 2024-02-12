import logging
import time
import threading
import heapq
from Pyro5.api import expose, Daemon

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


@expose
class Broker(object):
    def __init__(self):
        self.kv = {}
        self.expiry_heap = []
        self.lock = threading.Lock()
        self.shutdown_event = threading.Event()  # Shutdown signal
        self.start_health_check_thread()

    def set_value(self, key, value, expire_in=None):
        with self.lock:
            expire_at = time.time() + expire_in if expire_in is not None else None
            self.kv[key] = (value, expire_at)
            if expire_at:
                heapq.heappush(self.expiry_heap, (expire_at, key))

    def get_value(self, key):
        with self.lock:
            if key in self.kv:
                value, expire_at = self.kv[key]
                if expire_at is None or expire_at > time.time():
                    return value
        return None

    def delete_key(self, key):
        with self.lock:
            if key in self.kv:
                del self.kv[key]
                return True
        return False

    def key_exists(self, key):
        with self.lock:
            return key in self.kv and (self.kv[key][1] is None or self.kv[key][1] > time.time())

    def start_health_check_thread(self):
        def health_check():
            while not self.shutdown_event.is_set():
                with self.lock:
                    now = time.time()
                    while self.expiry_heap and self.expiry_heap[0][0] <= now:
                        _, key = heapq.heappop(self.expiry_heap)
                        if key in self.kv and self.kv[key][1] <= now:
                            del self.kv[key]
                self.shutdown_event.wait(10)  # Wait for 10 seconds or until shutdown is signaled

        thread = threading.Thread(target=health_check, daemon=True)
        thread.start()

    def shutdown(self):
        """Signals the health check thread to shut down."""
        self.shutdown_event.set()


def start_server():
    daemon = Pyro5.api.Daemon(host='broker', port=9090)  # Listen on all interfaces
    uri = daemon.register(Broker, "BROKER")
    logging.info(f"Ready. Object uri = {uri}")
    daemon.requestLoop()


if __name__ == "__main__":
    start_server()
