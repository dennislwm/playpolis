import pytest

from common.cli_request import CliRequest
from common.logger import Logger

@pytest.fixture
def logger():
  return Logger(__name__)

@pytest.fixture
def vars(logger):
  sample = CliRequest(logger, path="tests/")
  logger.info(sample.vars)
  return sample.vars

@pytest.fixture
def mods(logger):
  sample = CliRequest(logger, path="tests/")
  logger.info(sample.mods)
  return sample.mods