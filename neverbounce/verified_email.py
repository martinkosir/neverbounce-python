RESULT_CODES = (
    'valid', 'invalid', 'disposable', 'catchall', 'unknown'
)

RESULT_DETAILS_CODES = (
    'No additional details', 'Provided email failed the syntax check'
)


class VerifiedEmail:
    """
    VerifiedEmail holds the information about an email that was verified, like the if it's valid, or disposable
    email address.
    """
    def __init__(self, email, resp):
        self.email = email
        self._resp = resp

    def __str__(self):
        """
        :return: A string representation of VerifiedEmail.
        """
        return '{}: {}'.format(self.email, self.result)

    @property
    def result_code(self):
        """
        :return: An integer verification result code in range from 0 to 4.
        """
        return self._resp['result']

    @property
    def result(self):
        """
        :return: A string (textual) representation of verification result (eg. valid, invalid, disposable,...).
        """
        return RESULT_CODES[self.result_code]

    @property
    def is_valid(self):
        """
        :return: A boolean. True if the email is valid, false otherwise.
        """
        return self.result_code == 0

    @property
    def is_invalid(self):
        """
        :return: A boolean. True if the email is invalid, false otherwise.
        """
        return self.result_code == 1

    @property
    def is_disposable(self):
        """
        :return: A boolean. True if the email is disposable, false otherwise.
        """
        return self.result_code == 2

    @property
    def is_catchall(self):
        """
        :return: A boolean. True if the email is catchall, false otherwise.
        """
        return self.result_code == 3

    @property
    def is_unknown(self):
        """
        :return: A boolean. True if the email is unknown, false otherwise.
        """
        return self.result_code == 4

    @property
    def result_details_code(self):
        """
        :return: An integer verification details code (0 or 1).
        """
        return self._resp['result_details']

    @property
    def result_details(self):
        """
        :return: A string (textual) representation of verification details (eg. Provided email failed the syntax check).
        """
        return RESULT_DETAILS_CODES[self.result_details_code]
