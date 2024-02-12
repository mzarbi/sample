import logging
import os
import Pyro5.api

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

secrets_manager_url = os.environ.get('BROKER_URL')


def get_value(key="default"):
    logging.info(f"Connecting to {secrets_manager_url}")
    with Pyro5.api.Proxy(secrets_manager_url) as p:
        return p.get_value(key)
