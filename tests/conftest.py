import sys
import pytest

from botocore.stub import Stubber
from connexion import App

sys.path.append('.')
import message
from sqsinterface import sqs_resource

@pytest.fixture
def app():
    app = App(__name__, specification_dir="../")
    app.add_api("swagger.yml")
    app_client = app.app.test_client()
    return app_client

@pytest.fixture(autouse=True)
def sqs_stub():
    with Stubber(sqs_resource.meta.client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()
