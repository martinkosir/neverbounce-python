import pytest
from neverbounce.verified_email import VerifiedEmail


@pytest.fixture
def valid_verified_email():
    resp = {
        'success': True,
        'result': 0,
        'result_details': 0,
        'execution_time': 0.5
    }
    return VerifiedEmail('valid@emailaddress.com', resp)


@pytest.fixture
def invalid_verified_email():
    resp = {
        'success': True,
        'result': 1,
        'result_details': 1,
        'execution_time': 0.87218990
    }
    return VerifiedEmail('invalid@emailaddress.com', resp)


def test_valid_verified_email_str(valid_verified_email):
    assert str(valid_verified_email) == 'valid@emailaddress.com: valid'


def test_valid_verified_email_email(valid_verified_email):
    assert valid_verified_email.email == 'valid@emailaddress.com'


def test_valid_verified_email_result_code(valid_verified_email):
    assert valid_verified_email.result_code == 0


def test_valid_verified_email_result(valid_verified_email):
    assert valid_verified_email.result == 'valid'


def test_valid_verified_email_is_valid(valid_verified_email):
    assert valid_verified_email.is_valid


def test_valid_verified_email_result_details_code(valid_verified_email):
    assert valid_verified_email.result_details_code == 0


def test_valid_verified_email_result_details(valid_verified_email):
    assert valid_verified_email.result_details == 'No additional details'


def test_invalid_verified_email_result_code(invalid_verified_email):
    assert invalid_verified_email.result_code == 1


def test_invalid_verified_email_result(invalid_verified_email):
    assert invalid_verified_email.result == 'invalid'


def test_invalid_verified_email_is_valid(invalid_verified_email):
    assert invalid_verified_email.is_invalid


def test_invalid_verified_email_result_details_code(invalid_verified_email):
    assert invalid_verified_email.result_details_code == 1


def test_invalid_verified_email_result_details(invalid_verified_email):
    assert invalid_verified_email.result_details == 'Provided email failed the syntax check'
