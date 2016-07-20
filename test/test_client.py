import pytest
import responses
from neverbounce.client import NeverBounce
from neverbounce.exceptions import NeverBounceAPIError


ACCESS_TOKEN = 'fake_token'
BASE_URL = 'https://api.fakeneverbounce.com/v3'


def create_client():
    neverbounce = NeverBounce('fake_user_name', 'fake_api_key', BASE_URL)
    return neverbounce


def add_access_token_success_response():
    responses.add(
        responses.POST,
        BASE_URL + '/access_token',
        status=200,
        content_type='application/json',
        json={'access_token': ACCESS_TOKEN}
    )


@responses.activate
def test_get_access_token_success():
    add_access_token_success_response()
    neverbounce = create_client()
    access_token = neverbounce.get_access_token()
    assert access_token == ACCESS_TOKEN


@responses.activate
def test_get_access_token_invalid_credentials():
    endpoint_url = BASE_URL + '/access_token'
    responses.add(
        responses.POST,
        endpoint_url,
        status=400,
        content_type='application/json',
        json={
            'error': 'invalid_client',
            'error_description': 'The client credentials are invalid'
        }
    )
    neverbounce = create_client()
    with pytest.raises(NeverBounceAPIError) as exc_info:
        neverbounce.get_access_token()
    assert str(exc_info.value) == 'The client credentials are invalid'.format(endpoint_url)


@responses.activate
def test_verify_single_success():
    add_access_token_success_response()
    responses.add(
        responses.POST,
        BASE_URL + '/single',
        status=200,
        content_type='application/json',
        json={
            'success': True,
            'result': 0,
            'result_details': 0,
            'execution_time': 0.5
        }
    )
    neverbounce = create_client()
    verified_email = neverbounce.verify('valid@email.com')
    assert str(verified_email) == 'valid@email.com: valid'


@responses.activate
def test_check_account():
    add_access_token_success_response()
    responses.add(
        responses.POST,
        BASE_URL + '/account',
        status=200,
        content_type='application/json',
        json={
            'success': True,
            'credits': '990',
            'jobs_completed': '1',
            'jobs_processing': '0',
            'execution_time': 0.02,
        }
    )
    neverbounce = create_client()
    account = neverbounce.check_account()
    assert str(account) == 'credits: 990, jobs completed: 1, jobs processing: 0'


@responses.activate
def test_create_job():
    add_access_token_success_response()
    responses.add(
        responses.POST,
        BASE_URL + '/bulk',
        status=200,
        content_type='text/html',  # Really not cool
        json={
            'success': True,
            'job_status': 0,
            'execution_time': 0.088993072509766,
            'job_id': 123456,
            'job_file': '/jobs/Neverbounce_Job_48056.csv'
        }
    )
    neverbounce = create_client()
    emails = ['john.doe@example.com', 'jane.doe@example.com']
    job = neverbounce.create_job(emails)
    assert str(job) == 'job: 123456'


@responses.activate
def test_check_job():
    add_access_token_success_response()
    responses.add(
        responses.POST,
        BASE_URL + '/status',
        status=200,
        content_type='application/json',
        json={
            'status': '4',
            'type': '1',
            'started': '2016-01-16 04:06:10',
            'created': '2016-01-16 04:05:59',
            'orig_name': 'emails.csv',
            'finished': '2016-01-16 04:06:14',
            'success': True,
            'file_details': '{"error":false,"email_col_i":0,"tot_cols":1,"delimiter":"","has_header":false,"size":65,"tot_records":4,"tot_emails":0}',
            'input_location': '1',
            'stats': {
                'duplicates': 0, 'disposable': 0, 'unknown': 0, 'catchall': 0, 'total': 3, 'bad_syntax': 0,
                'invalid': 0, 'job_time': 4, 'billable': 3, 'processed': 3, 'valid': 0
            },
            'execution_time': 0.40506100654602,
            'id': '123456'
        }

    )
    neverbounce = create_client()
    job_status = neverbounce.check_job(123456)
    assert str(job_status) == 'completed job: 123456'


@responses.activate
def test_create_job_bulk_not_allowed():
    add_access_token_success_response()
    responses.add(
        responses.POST,
        BASE_URL + '/bulk',
        status=200,
        content_type='application/json',
        json={
            'success': False,
            'error_msg': 'Free API usage is limited to single requests only. To unlock bulk API access, please add a default payment method in your account dashboard.',
            'error_code': 2,
            'execution_time': 0.45216798782349
        }
    )
    neverbounce = create_client()
    emails = ['john.doe@example.com', 'jane.doe@example.com']
    with pytest.raises(NeverBounceAPIError) as exc_info:
        neverbounce.create_job(emails)
    assert str(exc_info.value) == 'Free API usage is limited to single requests only. To unlock bulk API access, please add a default payment method in your account dashboard.'


@responses.activate
def test_retrieve_job():
    add_access_token_success_response()
    responses.add(
        responses.POST,
        BASE_URL + '/download',
        status=200,
        content_type='application/octet-stream',
        body=b'john.doe@gmail.com,valid\nadmin@example.com,catchall\njane.doe@example.com,invalid\n'
    )
    neverbounce = create_client()
    verified_emails = neverbounce.retrieve_job(56789)
    assert [str(email) for email in verified_emails] == ['john.doe@gmail.com: valid', 'admin@example.com: catchall', 'jane.doe@example.com: invalid']
