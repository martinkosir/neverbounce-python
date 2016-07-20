import requests
from .exceptions import AccessTokenExpired, NeverBounceAPIError, InvalidResponseError
from .email import VerifiedEmail, VerifiedBulkEmail
from .account import Account
from .job import Job, JobStatus


class NeverBounce(object):
    """
    NeverBounce API client class used to verify an email address in realtime, check the account status, etc.
    """
    def __init__(self, api_username, api_key, base_url='https://api.neverbounce.com/v3'):
        self.api_username = api_username
        self.api_key = api_key
        self.base_url = base_url
        self._access_token = None

    def verify(self, email):
        """
        Verify a single email address.
        :param str email: Email address to verify.
        :return: A VerifiedEmail object.
        """
        resp = self._call('single', {'email': email})
        return VerifiedEmail(email, resp['result'])

    def create_job(self, emails):
        """
        Create a new bulk verification job for the list of emails.
        :param list emails: Email addresses to verify.
        :return: A Job object.
        """
        resp = self._call('bulk', {'input_location': '1', 'input': '\n'.join(emails)})
        return Job(resp['job_id'])

    def check_job(self, job_id):
        """
        Check the status of a bulk verification job.
        :param int job_id: ID of a job to check the status of.
        :return: A Status object.
        """
        resp = self._call('status', {'job_id': job_id})
        return JobStatus(resp['id'], resp['status'], resp['type'], resp['stats'], resp['orig_name'],
                         resp['created'], resp['started'], resp['finished'])

    def retrieve_job(self, job_id):
        """
        Retrieve the results of a completed bulk verification job.
        :param int job_id: ID of a job to retrieve the results for.
        :return: A list of VerifiedBulkEmail objects.
        """
        resp = self._call('download', {'job_id': job_id})
        return [VerifiedBulkEmail(d['email'], d['result_text_code']) for d in self._parse_csv(resp)]

    def check_account(self):
        """
        Check the API account details like balance of credits.
        :return: An Account object.
        """
        resp = self._call('account')
        return Account(resp['credits'], resp['jobs_completed'], resp['jobs_processing'])

    def get_access_token(self):
        """
        Retrieve an access token to authenticate subsequential API calls.
        :return: An access token string.
        """
        if self._access_token:
            return self._access_token
        resp = self._request(
            'access_token',
            {'grant_type': 'client_credentials', 'scope': 'basic user'},
            (self.api_username, self.api_key),
        )
        self._access_token = resp['access_token']
        return self._access_token

    def _call(self, endpoint, data={}):
        """
        Make an authorized API call to specified endpoint.
        :param str endpoint: API endpoint's relative URL, eg. `/account`.
        :param dict data: POST request data.
        :return: A dictionary or a string with response data.
        """
        try:
            data['access_token'] = self.get_access_token()
            return self._request(endpoint, data)
        except AccessTokenExpired:
            self._access_token = None
            data['access_token'] = self.get_access_token()
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

    def _handle_response(self, response):
        """
        Handle the response and possible failures.
        :param dict response: Response data.
        :return: A dictionary or a string with response data.
        :raises: NeverBounceAPIError if the API call fails.
        """
        if not response.ok:
            raise NeverBounceAPIError(response)
        # Handle the download response.
        if response.headers.get('Content-Type') == 'application/octet-stream':
            return response.content.decode('utf-8')
        else:
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

    def _parse_csv(self, csv):
        """
        Parse the CSV with 2 columns (email, verification result).
        :param str csv: CSV data to parse.
        :return: A list of dictionaries.
        """
        data = []
        for line in csv.strip().split('\n'):
            cols = line.split(',')
            data.append({'email': cols[0], 'result_text_code': cols[1]})
        return data
