import pytest
from datetime import datetime
from neverbounce.job import Job, JobStatus


@pytest.fixture
def job():
    resp = {
        'success': True,
        'job_status': 0,
        'execution_time': 0.098993055509766,
        'job_id': 123456,
        'job_file': '/jobs/Neverbounce_Job_123456.csv'
    }
    return Job(resp['job_id'])


@pytest.fixture
def job_status():
    resp = {
        'success': True,
        'status': '4',
        'type': '1',
        'started': '2016-01-16 04:06:10',
        'created': '2016-01-16 04:05:59',
        'orig_name': 'emails.csv',
        'finished': '2016-01-16 04:06:14',
        'file_details': '{"error":false,"email_col_i":0,"tot_cols":1,"delimiter":"","has_header":false,"size":65,"tot_records":4,"tot_emails":0}',
        'input_location': '1',
        'stats': {
            'duplicates': 0, 'disposable': 0, 'unknown': 0, 'catchall': 0, 'total': 3, 'bad_syntax': 0,
            'invalid': 0, 'job_time': 4, 'billable': 3, 'processed': 3, 'valid': 0
        },
        'execution_time': 0.40506100654602,
        'id': '123456'
    }
    return JobStatus(resp['id'], resp['status'], resp['type'], resp['stats'], resp['orig_name'], resp['created'],
                     resp['started'], resp['finished'])


def test_job_str(job):
    assert str(job) == 'job: 123456'


def test_job_id(job):
    assert job.job_id == 123456


def test_job_status_str(job_status):
    assert str(job_status) == 'completed job: 123456'


def test_job_status_job_id(job_status):
    assert job_status.job_id == 123456


def test_job_status_status_code(job_status):
    assert job_status.status_code == 4


def test_job_status_is_uploading(job_status):
    assert not job_status.is_uploading


def test_job_status_is_received(job_status):
    assert not job_status.is_received


def test_job_status_is_parsing(job_status):
    assert not job_status.is_parsing


def test_job_status_is_parsed(job_status):
    assert not job_status.is_parsed


def test_job_status_is_running(job_status):
    assert not job_status.is_running


def test_job_status_is_completed(job_status):
    assert job_status.is_completed


def test_job_status_is_failed(job_status):
    assert not job_status.is_failed


def test_job_status_status(job_status):
    assert job_status.status == 'completed'


def test_job_status_type_code(job_status):
    assert job_status.type_code == 1


def test_job_status_type(job_status):
    assert job_status.type == 'API'


def test_job_status_stats(job_status):
    assert job_status.stats == {
            'duplicates': 0, 'disposable': 0, 'unknown': 0, 'catchall': 0, 'total': 3, 'bad_syntax': 0,
            'invalid': 0, 'job_time': 4, 'billable': 3, 'processed': 3, 'valid': 0
        }


def test_job_status_orig_name(job_status):
    assert job_status.orig_name == 'emails.csv'


def test_job_status_created(job_status):
    assert job_status.created == datetime(2016, 1, 16, 4, 5, 59)


def test_job_status_started(job_status):
    assert job_status.started == datetime(2016, 1, 16, 4, 6, 10)


def test_job_status_finished(job_status):
    assert job_status.finished == datetime(2016, 1, 16, 4, 6, 14)
