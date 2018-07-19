import logging
import sys
import os


sys.setrecursionlimit(100000)

logger = logging.getLogger(__name__)

logging.basicConfig(
    stream=sys.stdout, level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

