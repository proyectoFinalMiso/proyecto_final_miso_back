import pytest
import os
from dotenv import load_dotenv, find_dotenv
from tests.fixtures import *

os.environ['ENV'] = 'test'

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
  env_file = find_dotenv('.env.test')
  load_dotenv(env_file)
  return config