class AccessTokenExpired(Exception):
    pass


class InvalidResponseError(Exception):
    pass


class NeverBounceAPIError(Exception):
    def __init__(self, response, *args, **kwargs):
        json = response.json()
        self.errors = []
        if 'error_description' in json:
            self.errors.append(json['error_description'])
        if 'msg' in json:
            self.errors.append(json['msg'])
        if 'error_msg' in json:
            self.errors.append(json['error_msg'])
        self.status_code = response.status_code
        self.response = response
        super(NeverBounceAPIError, self).__init__('\n'.join(self.errors), *args, **kwargs)
