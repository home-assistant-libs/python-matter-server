"""Mock Matter."""
import logging
from unittest.mock import Mock


def get_mock_matter():
    return Mock(adapter=Mock(logger=logging.getLogger("mock_matter")))
