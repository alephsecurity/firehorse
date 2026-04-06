"""
Firehorse - Research & Exploitation framework for Qualcomm EDL Firehose programmers

By Roee Hay & Noam Hadad, Aleph Research, HCL Technologies
"""

__version__ = "1.0.0"
__author__ = "Roee Hay & Noam Hadad"
__email__ = "research@alephsecurity.com"
__license__ = "Apache License 2.0"

try:
    from ._version import version as __version__
except ImportError:
    pass

from .firehorse import main
from .fh import *
from .target import *
from .fw import *
from .log import *

__all__ = [
    "main",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]
