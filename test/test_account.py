import pytest
from neverbounce.account import Account


@pytest.fixture
def account():
    resp = {
        'success': True,
        'credits': '1000',
        'jobs_completed': '5',
        'jobs_processing': '1',
        'execution_time': 0.021541651,
    }
    return Account(resp['credits'], resp['jobs_completed'], resp['jobs_processing'])


def test_account_str(account):
    assert str(account) == 'credits: 1000, jobs completed: 5, jobs processing: 1'


def test_account_credits(account):
    assert account.credits == 1000


def test_account_jobs_completed(account):
    assert account.jobs_completed == 5


def test_account_jobs_processing(account):
    assert account.jobs_processing == 1
