class AccessTokenExpired(Exception):
    pass


class NeverBounceAPIError(Exception):
    def __init__(self, response, *args, **kwargs):
        error_message = None
        try:
            json = response.json()
            if 'error' in json:
                error_message = '{error_description} ({error})'.format(**json)
            if 'msg' in json:
                error_message = json['msg']
            if 'error_code' in json:
                error_message = '{error_msg} ({error_code})'.format(**json)
        except:
            pass

        if not error_message:
            error_message = response.text or ''

        self.status = response.status_code
        self.response = response
        self.errors = [error_message]

        message = 'Call to {url} returned {status_code}. {error_message}'.format(
            url=response.url,
            status_code=response.status_code,
            error_message=error_message
        )
        super(NeverBounceAPIError, self).__init__(message, *args, **kwargs)
