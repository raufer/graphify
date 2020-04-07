import logging
import sys
import os


sys.setrecursionlimit(100000)

logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s, %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG
)


