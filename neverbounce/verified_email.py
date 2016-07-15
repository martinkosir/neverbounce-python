RESULT_CODES = (
    'valid', 'invalid', 'disposable', 'catchall', 'unknown'
)

RESULT_DETAILS_CODES = (
    'No additional details', 'Provided email failed the syntax check'
)


class VerifiedEmail:
    def __init__(self, email, resp):
        self.email = email
        self._resp = resp

    def __str__(self):
        return '{}: {}'.format(self.email, self.result)

    @property
    def result_code(self):
        """
        Return verification result code as an integer in range from 0 to 4.
        :return: int
        """
        return self._resp['result']

    @property
    def result(self):
        """
        Return a text representation of verification result (eg. valid, invalid, disposable,...).
        :return: str
        """
        return RESULT_CODES[self.result_code]

    @property
    def is_valid(self):
        """
        Return True if the email is valid.
        :return: bool
        """
        return self.result_code == 0

    @property
    def is_invalid(self):
        """
        Return True if the email is invalid.
        :return: bool
        """
        return self.result_code == 1

    @property
    def is_disposable(self):
        """
        Return True if the email is disposable.
        :return: bool
        """
        return self.result_code == 2

    @property
    def is_catchall(self):
        """
        Return True if the email is catchall.
        :return: bool
        """
        return self.result_code == 3

    @property
    def is_unknown(self):
        """
        Return True if the email is unknown.
        :return: bool
        """
        return self.result_code == 4

    @property
    def result_details_code(self):
        """
        Return verification result details code as an integer in range from 0 to 1.
        :return: int
        """
        return self._resp['result_details']

    @property
    def result_details(self):
        """
        Return a text representation of verification details (eg. Provided email failed the syntax check).
        :return: str
        """
        return RESULT_DETAILS_CODES[self.result_details_code]
