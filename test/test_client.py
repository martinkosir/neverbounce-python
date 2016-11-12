import responses
from unittest import TestCase
from neverbounce.client import NeverBounce, NeverBounceAPIError


class ClientTestCase(TestCase):
    def setUp(self):
        self.access_token = 'fake_token'
        self.base_url = 'https://api.fakeneverbounce.com/v3'
        self.neverbounce = NeverBounce('fake_user_name', 'fake_api_key', self.base_url)
        self.access_token_response = {
            'method': responses.POST, 'url': self.base_url + '/access_token', 'status': 200,
            'content_type': 'application/json', 'json': {'access_token': self.access_token}
        }

    def test_access_token(self):
        with responses.RequestsMock() as rsps:
            rsps.add(**self.access_token_response)
            self.assertEqual(
                self.neverbounce.access_token(),
                self.access_token
            )

    def test_get_access_token_invalid_credentials(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.POST, self.base_url + '/access_token', status=400, content_type='application/json',
                json={
                    'error': 'invalid_client',
                    'error_description': 'The client credentials are invalid'
                }
            )
            with self.assertRaises(NeverBounceAPIError) as cm:
                self.neverbounce.access_token()
                self.assertEqual(
                    str(cm.exception),
                    'The client credentials are invalid'
                )

    def test_verify(self):
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(**self.access_token_response)
            rsps.add(
                responses.POST, self.base_url + '/single', status=200, content_type='application/json',
                json={
                    'success': True,
                    'result': 0,
                    'result_details': 0,
                    'execution_time': 0.5
                }
            )
            verified_email = self.neverbounce.verify('valid@email.com')
            self.assertEqual(str(verified_email), 'valid@email.com: valid')

    def test_account(self):
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(**self.access_token_response)
            rsps.add(
                responses.POST, self.base_url + '/account', status=200, content_type='application/json',
                json={
                    'success': True,
                    'credits': '990',
                    'jobs_completed': '1',
                    'jobs_processing': '0',
                    'execution_time': 0.02,
                }
            )
            self.assertEqual(
                str(self.neverbounce.account()),
                'Credits: 990, Jobs Completed: 1, Jobs Processing: 0'
            )

    def test_create_job(self):
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(**self.access_token_response)
            rsps.add(
                responses.POST, self.base_url + '/bulk', status=200, content_type='text/html',  # Really not cool
                json={
                    'success': True,
                    'job_status': 0,
                    'execution_time': 0.088993072509766,
                    'job_id': 123456,
                    'job_file': '/jobs/Neverbounce_Job_48056.csv'
                }
            )
            job = self.neverbounce.create_job(['john.doe@example.com', 'jane.doe@example.com'])
            self.assertEqual(str(job), 'Job 123456')

    def test_check_job(self):
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(**self.access_token_response)
            rsps.add(
                responses.POST, self.base_url + '/status', status=200, content_type='application/json',
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
            job_status = self.neverbounce.check_job(123456)
            self.assertEqual(str(job_status), 'Completed Job 123456')

    def test_create_job_not_allowed(self):
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(**self.access_token_response)
            rsps.add(
                responses.POST, self.base_url + '/bulk', status=200, content_type='application/json',
                json={
                    'success': False,
                    'error_msg': 'Free API usage is limited to single requests only. To unlock bulk API access, please add a default payment method in your account dashboard.',
                    'error_code': 2,
                    'execution_time': 0.45216798782349
                }
            )
            with self.assertRaises(NeverBounceAPIError) as cm:
                self.neverbounce.create_job(['john.doe@example.com', 'jane.doe@example.com'])
                self.assertEqual(
                    str(cm.exception),
                    'Free API usage is limited to single requests only. To unlock bulk API access, please add a default payment method in your account dashboard.'
                )

    def test_results(self):
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(**self.access_token_response)
            rsps.add(
                responses.POST, self.base_url + '/download', status=200, content_type='application/octet-stream',
                body=b'john.doe@gmail.com,valid\nadmin@example.com,catchall\njane.doe@example.com,invalid\n'
            )
            self.assertListEqual(
                [str(email) for email in self.neverbounce.results(56789)],
                ['john.doe@gmail.com: valid', 'admin@example.com: catchall', 'jane.doe@example.com: invalid']
            )
