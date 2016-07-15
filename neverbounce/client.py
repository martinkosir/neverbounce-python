import requests

from .exceptions import AccessTokenExpired, NeverBounceAPIError
from .verified_email import VerifiedEmail
from .account import Account


class NeverBounce:
    """
    NeverBounce API client class used to verify an email address in realtime, check the account status, etc.
    """
    def __init__(self, api_username, api_key, base_url='https://api.neverbounce.com/v3'):
        self.api_username = api_username
        self.api_key = api_key
        self.base_url = base_url
        self._access_token = None

    def verify_single(self, email):
        """
        Verify a single email address.
        :param str email: Email address to verify.
        :return: A VerifiedEmail object.
        """
        resp = self._call('single', {'email': email})
        return VerifiedEmail(email, resp)

    def account(self):
        """
        Check the API account details like balance of credits.
        :return: An Account object.
        """
        resp = self._call('account')
        return Account(resp)

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
        :return: A dictionary with response data.
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
        :return: A dictionary with response data.
        """
        url = '{}/{}'.format(self.base_url, endpoint)
        response = requests.post(url, data, auth=auth)
        return self._handle_response(response)

    def _handle_response(self, response):
        """
        Handle the response and possible failures.
        :param dict response: Response data.
        :return: A dictionary with response data.
        :raises: NeverBounceAPIError if the API call fails.
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
