from collections import OrderedDict
from datetime import datetime
from unittest import TestCase
from neverbounce.objects import VerifiedEmail, Job, JobStatus, Account


class VerifiedEmailTestCase(TestCase):
    def setUp(self):
        self.emails = OrderedDict([
            ('valid', VerifiedEmail('valid@emailaddress.com', 0)),
            ('invalid', VerifiedEmail('invalid@emailaddress.com', 1)),
            ('disposable', VerifiedEmail('disposable@emailaddress.com', 2)),
            ('catchall', VerifiedEmail.from_text_code('catchall@emailaddress.com', 'catchall')),
            ('unknown', VerifiedEmail.from_text_code('unknown@emailaddress.com', 'unknown')),
        ])

    def test_str(self):
        for type, email in self.emails.items():
            self.assertEqual(str(email), '{0}@emailaddress.com: {0}'.format(type))

    def test_email(self):
        for type, email in self.emails.items():
            self.assertEqual(getattr(email, 'email'), '{0}@emailaddress.com'.format(type))

    def test_result_code(self):
        for i, email in enumerate(self.emails.values()):
            self.assertEqual(getattr(email, 'result_code'), i)

    def test_result_text(self):
        for type, email in self.emails.items():
            self.assertEqual(getattr(email, 'result_text'), type)

    def test_boolean_flag(self):
        for email_type, email in self.emails.items():
            for type in VerifiedEmail.text_codes:
                flag = 'is_{}'.format(type)
                if email_type == type:
                    self.assertTrue(getattr(email, flag))
                else:
                    self.assertFalse(getattr(email, flag))


class JobTestCase(TestCase):
    def setUp(self):
        self.job = Job(123456)

    def test_str(self):
        self.assertEqual(str(self.job), 'Job 123456')

    def test_job_id(self):
        self.assertEqual(self.job.job_id, 123456)


class JobStatusTestCase(TestCase):
    def setUp(self):
        self.job_status = JobStatus(
            job_id='123456', status_code='4', type_code='1', orig_name='emails.csv',
            created='2016-01-16 04:05:59', started=None, finished='2016-01-16 04:06:14',
            stats={
                'duplicates': 0, 'disposable': 0, 'unknown': 0, 'catchall': 0, 'total': 3, 'bad_syntax': 0,
                'invalid': 0, 'job_time': 4, 'billable': 3, 'processed': 3, 'valid': 0
            }
        )

    def test_str(self):
        self.assertEqual(str(self.job_status), 'Completed Job 123456')

    def test_job_id(self):
        self.assertEqual(self.job_status.job_id, 123456)

    def test_status_code(self):
        self.assertEqual(self.job_status.status_code, 4)

    def test_status(self):
        self.assertEqual(self.job_status.status, 'completed')

    def test_type_code(self):
        self.assertEqual(self.job_status.type_code, 1)

    def test_type(self):
        self.assertEqual(self.job_status.type, 'API')

    def test_orig_name(self):
        self.assertEqual(self.job_status.orig_name, 'emails.csv')

    def test_created(self):
        self.assertEqual(self.job_status.created, datetime(2016, 1, 16, 4, 5, 59))

    def test_started(self):
        self.assertEqual(self.job_status.started, None)

    def test_finished(self):
        self.assertEqual(self.job_status.finished, datetime(2016, 1, 16, 4, 6, 14))

    def test_stats(self):
        self.assertEqual(
            self.job_status.stats,
            {
                'duplicates': 0, 'disposable': 0, 'unknown': 0, 'catchall': 0, 'total': 3, 'bad_syntax': 0,
                'invalid': 0, 'job_time': 4, 'billable': 3, 'processed': 3, 'valid': 0
            }
        )

    def test_flags(self):
        for status in JobStatus.statuses:
            flag = 'is_{}'.format(status)
            if self.job_status.status == status:
                self.assertTrue(getattr(self.job_status, flag))
            else:
                self.assertFalse(getattr(self.job_status, flag))


class AccountTestCase(TestCase):
    def setUp(self):
        self.account = Account(credits=1000, jobs_completed='5', jobs_processing='1')

    def test_str(self):
        self.assertEqual(str(self.account), 'Credits: 1000, Jobs Completed: 5, Jobs Processing: 1')

    def test_credits(self):
        self.assertEqual(self.account.credits, 1000)

    def test_jobs_completed(self):
        self.assertEqual(self.account.jobs_completed, 5)

    def test_account_jobs_processing(self):
        self.assertEqual(self.account.jobs_processing, 1)