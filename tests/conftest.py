import os
import sys
import logging

from fastapi import Path
import pytest
from fastapi.testclient import TestClient

sys.path.append("..")

@pytest.fixture(scope='module')
def client():
    from pyhgvs.api import app
    yield TestClient(app)