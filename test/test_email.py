import pytest
from neverbounce.email import VerifiedEmail, VerifiedBulkEmail


@pytest.fixture
def valid_verified_email():
    return VerifiedEmail('valid@emailaddress.com', 0)


@pytest.fixture
def invalid_verified_email():
    return VerifiedEmail('invalid@emailaddress.com', 1)


@pytest.fixture
def valid_verified_bulk_email():
    return VerifiedBulkEmail('valid@emailaddress.com', 'valid')


@pytest.fixture
def unknown_verified_bulk_email():
    return VerifiedBulkEmail('valid@emailaddress.com', 'unknown')


def test_valid_verified_email_str(valid_verified_email):
    assert str(valid_verified_email) == 'valid@emailaddress.com: valid'


def test_valid_verified_email_email(valid_verified_email):
    assert valid_verified_email.email == 'valid@emailaddress.com'


def test_valid_verified_email_result_code(valid_verified_email):
    assert valid_verified_email.result_code == 0


def test_valid_verified_email_result(valid_verified_email):
    assert valid_verified_email.result_text == 'valid'


def test_valid_verified_email_is_valid(valid_verified_email):
    assert valid_verified_email.is_valid


def test_invalid_verified_email_result_code(invalid_verified_email):
    assert invalid_verified_email.result_code == 1


def test_invalid_verified_email_result(invalid_verified_email):
    assert invalid_verified_email.result_text == 'invalid'


def test_invalid_verified_email_is_valid(invalid_verified_email):
    assert invalid_verified_email.is_invalid


def test_valid_verified_bulk_email_result_code(valid_verified_bulk_email):
    assert valid_verified_bulk_email.result_code == 0


def test_valid_verified_bulk_email_is_valid(valid_verified_bulk_email):
    assert valid_verified_bulk_email.is_valid


def test_unknown_verified_bulk_email_result_code(unknown_verified_bulk_email):
    assert unknown_verified_bulk_email.result_code == 4


def test_valid_verified_bulk_email_is_unknown(unknown_verified_bulk_email):
    assert unknown_verified_bulk_email.is_unknown
