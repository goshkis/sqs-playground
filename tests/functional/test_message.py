import json

def test_message_create(sqs_stub, app):
    response = {'MD5OfMessageBody': '7614fb89be75015138a0db2ffa6a1b3b',
        'MessageId': 'f2553c48-bca4-4cc5-a3e8-0c90c14b3670',
        'ResponseMetadata': {
            'RequestId': '07d343ef-f429-503e-ab37-1b46a058723f',
            'HTTPStatusCode': 200,
            'HTTPHeaders': {
                'x-amzn-requestid': '07d343ef-f429-503e-ab37-1b46a058723f',
                'content-type': 'text/xml', 
                'content-length': '378'},
            'RetryAttempts': 0
            }
        }

    sqs_stub.add_response('send_message', service_response=response)
    response = app.post('/api/message', data=json.dumps({"body":"Simple and valid message"}),
                    content_type='application/json')

    assert response.status_code == 201

def test_message_create_empty(app):
    response = app.post('/api/message', data=json.dumps({"body":""}),
                    content_type='application/json')

    assert response.status_code == 400
    assert b"body parameter is missing or empty" in response.data

def test_message_create_missed_parameter(app):
    response = app.post('/api/message', data=json.dumps({"NOTbody":"Simple and valid message"}),
                    content_type='application/json')

    assert response.status_code == 400
    assert b"body parameter is missing or empty" in response.data


def test_message_create_client_failure_masked(sqs_stub, app):

    sqs_stub.add_client_error('send_message', service_error_code='499')
    
    response = app.post('/api/message', data=json.dumps({"body":"Simple and valid message"}),
                    content_type='application/json')

    assert response.status_code == 500

def test_message_create_client_failure_passthrough(sqs_stub, app):

    sqs_stub.add_client_error('send_message', service_error_code='429')
    
    response = app.post('/api/message', data=json.dumps({"body":"Simple and valid message"}),
                    content_type='application/json')

    assert response.status_code == 429

