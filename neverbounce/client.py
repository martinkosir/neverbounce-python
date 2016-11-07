import requests
import warnings
from collections import namedtuple
from neverbounce.exceptions import AccessTokenExpired, NeverBounceAPIError, InvalidResponseError
from neverbounce.objects import Job, JobStatus, Account, VerifiedEmail


class NeverBounce(object):
    """
    NeverBounce API client used to verify an email address in realtime.
    """
    def __init__(self, api_username, api_key, base_url='https://api.neverbounce.com/v3'):
        self.api_username = api_username
        self.api_key = api_key
        self.base_url = base_url
        self._cached_access_token = None

    def verify(self, email):
        """
        Verify a single email address.
        :param str email: Email address to verify.
        :return: A VerifiedEmail object.
        """
        resp = self._call(endpoint='single', data={'email': email})
        return VerifiedEmail(email, resp['result'])

    def create_job(self, emails):
        """
        Create a new bulk verification job for the list of emails.
        :param list emails: Email addresses to verify.
        :return: A Job object.
        """
        resp = self._call(endpoint='bulk', data={'input_location': '1', 'input': '\n'.join(emails)})
        return Job(resp['job_id'])

    def check_job(self, job_id):
        """
        Check the status of a bulk verification job.
        :param int job_id: ID of a job to check the status of.
        :return: A JobStatus object.
        """
        resp = self._call(endpoint='status', data={'job_id': job_id})
        map = {'id': 'job_id', 'status': 'status_code', 'type': 'type_code'}
        job_status_args = {map.get(k, k): v for k, v in resp.items()}
        return JobStatus(**job_status_args)

    def results(self, job_id):
        """
        Yield the result of a completed bulk verification job.
        :param int job_id: ID of a job to retrieve the results for.
        :yields: The next VerifiedEmail objects.
        """
        resp = self._call(endpoint='download', data={'job_id': job_id})
        Row = namedtuple('Row', ['email', 'result_text_code'])
        for line in resp:
            row = Row(*line.decode('utf-8').split(','))
            yield VerifiedEmail.from_text_code(row.email, row.result_text_code)

    def retrieve_job(self, job_id):
        """
        Result of a completed bulk verification job.
        :param int job_id: ID of a job to retrieve the results for.
        :return: A list of VerifiedEmail objects.
        """
        warnings.warn('Use results generator method instead of retrieve_job which returns a list', UserWarning)
        return list(self.results(job_id))

    def account(self):
        """
        Get the API account details like balance of credits.
        :return: An Account object.
        """
        resp = self._call(endpoint='account')
        return Account(resp['credits'], resp['jobs_completed'], resp['jobs_processing'])

    def check_account(self):
        warnings.warn('check_account method is now called account', DeprecationWarning)
        return self.account()

    def access_token(self):
        """
        Retrieve and cache an access token to authenticate API calls.
        :return: An access token string.
        """
        if self._cached_access_token is not None:
            return self._cached_access_token
        resp = self._request(endpoint='access_token', data={'grant_type': 'client_credentials', 'scope': 'basic user'},
                             auth=(self.api_username, self.api_key))
        self._cached_access_token = resp['access_token']
        return self._cached_access_token

    def get_access_token(self):
        warnings.warn('get_access_token method is now called access_token', DeprecationWarning)
        return self.access_token()

    def _call(self, endpoint, data=None):
        """
        Make an authorized API call to specified endpoint.
        :param str endpoint: API endpoint's relative URL, eg. `/account`.
        :param dict data: POST request data.
        :return: A dictionary or a string with response data.
        """
        data = {} if data is None else data
        try:
            data['access_token'] = self.access_token()
            return self._request(endpoint, data)
        except AccessTokenExpired:
            self._cached_access_token = None
            data['access_token'] = self.access_token()
            return self._request(endpoint, data)

    def _request(self, endpoint, data, auth=None):
        """
        Make HTTP POST request to an API endpoint.
        :param str endpoint: API endpoint's relative URL, eg. `/account`.
        :param dict data: POST request data.
        :param tuple auth: HTTP basic auth credentials.
        :return: A dictionary or a string with response data.
        """
        url = '{}/{}'.format(self.base_url, endpoint)
        response = requests.post(url, data, auth=auth)
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response):
        """
        Handle the response and possible failures.
        :param Response response: Response data.
        :return: A dictionary or a string with response data.
        :raises: NeverBounceAPIError if the API call fails.
        """
        if not response.ok:
            raise NeverBounceAPIError(response)
        if response.headers.get('Content-Type') == 'application/octet-stream':
            return response.iter_lines()

        try:
            resp = response.json()
        except ValueError:
             raise InvalidResponseError('Failed to handle the response content-type {}.'.format(
                 response.headers.get('Content-Type'))
             )
        if 'success' in resp and not resp['success']:
            if 'msg' in resp and resp['msg'] == 'Authentication failed':
                raise AccessTokenExpired
            else:
                raise NeverBounceAPIError(response)
        return resp
