""" p1exporter CLI"""
from p1exporter import P1Reader, P1Collector, CRCException

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

from unittest.mock import patch
import time
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())

# TODO
# - parametrize port and USB device

if __name__ == "__main__":
    collector = P1Collector()
    REGISTRY.register(collector)
    start_http_server(8080)
    with P1Reader() as p1_reader:
        while True:
            try:
                telegram = p1_reader.read()
            except CRCException as error:
                print(f"Error {error}")

            print(telegram)
            collector.update(telegram)
