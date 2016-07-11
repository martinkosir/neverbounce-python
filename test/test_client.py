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
    assert str(exc_info.value) == 'Call to {} returned 400. The client credentials are invalid (invalid_client)'.format(endpoint_url)


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
    assert neverbounce.verify_single('valid@email.com').is_valid


@responses.activate
def test_account():
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
    assert neverbounce.account().credits == 990
