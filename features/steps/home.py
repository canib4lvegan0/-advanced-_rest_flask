import json

from deepdiff import DeepDiff
from nose.tools import assert_equal

from app import app
from behave import *

def check_json(json_expected, json_response):
    d = DeepDiff(json_expected, json_response, ignore_order=True, report_repetition=True)
    if d != {}:
        raise AssertionError("Expected: <%s>\nbut was <%s>\n" % (str(json_expected), str(json_response)))

@when('{method} request to {url} is made')
def json_request(context, method, url):
    data = None
    headers = {}
    content_type = 'application/json'

    if 'json_body' in context:
        data = json.dumps(context.json_body)

    client = app.test_client()

    response = getattr(client, method)(url, data=data, content_type=content_type, headers=headers)
    context.response = response
    try:
        context.response.json = json.loads(context.response.data)
    except Exception:
        pass


@then('should return status code {status_code} {status_name}')
def response_status_code(context, status_code, status_name):
    assert_equal(context.response.status_code, int(status_code))

@then('the response should have body')
def step_impl(context):
    body = context.text
    check_json(json.loads(body), json.loads(context.response.data))
