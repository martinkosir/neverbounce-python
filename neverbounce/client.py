import requests

from neverbounce.exceptions import AccessTokenExpired, NeverBounceAPIError
from .verified_email import VerifiedEmail
from .account import Account


class NeverBounce:
    def __init__(self, api_username, api_key, base_url='https://api.neverbounce.com/v3'):
        self.api_username = api_username
        self.api_key = api_key
        self.base_url = base_url
        self._access_token = None

    def verify_single(self, email):
        """
        Verify a single email and return VerifiedEmail object.
        :param email:
        :return: VerifiedEmail
        """
        resp = self._call('single', {'email': email})
        return VerifiedEmail(email, resp)

    def account(self):
        """
        Check the balance of credits in an account and see how many jobs are currently running.
        :return: Account
        """
        resp = self._call('account')
        return Account(resp)

    def get_access_token(self):
        """
        Retrieve access token to authenticate API calls.
        :return: access_token
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
        try:
            data['access_token'] = self.get_access_token()
            return self._request(endpoint, data)
        except AccessTokenExpired:
            self._access_token = None
            data['access_token'] = self.get_access_token()
            return self._request(endpoint, data)

    def _request(self, endpoint, data, auth=None):
        """
        Make HTTP POST request to an API endpoint. Return response dictionary on success.
        :param endpoint: str
        :param data: dict
        :param auth: tuple | None
        :return: dict
        """
        url = '{}/{}'.format(self.base_url, endpoint)
        response = requests.post(url, data, auth=auth)
        return self._handle_response(response)

    def _handle_response(self, response):
        """
        Handle the response, HTTP errors, API failure messages, expired token.
        Return response dictionary on success.
        :param response: requests.Response
        :return: dict
        """
        if not response.ok:
            raise NeverBounceAPIError(response)
        resp = response.json()
        if 'success' in resp and not resp['success']:
            if 'msg' in resp and resp['msg'] == 'Authentication failed':
                raise AccessTokenExpired
            else:
                raise NeverBounceAPIError(response)
        return resp
