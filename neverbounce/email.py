RESULT_CODES = {
    0: 'valid',
    1: 'invalid',
    2: 'disposable',
    3: 'catchall',
    4: 'unknown'
}

RESULT_TEXT_CODES = {v: k for k, v in RESULT_CODES.items()}


class Email(object):
    def __init__(self, email, result_code):
        self.email = email
        self.result_code = result_code

    def __str__(self):
        """
        :return: A string representation of VerifiedEmail.
        """
        return '{}: {}'.format(self.email, self.result_text)

    @property
    def result_text(self):
        """
        :return: A string (textual) representation of the verification result (eg. valid, invalid, disposable,...).
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


class VerifiedEmail(Email):
    """
    VerifiedEmail holds the information about an email that was verified, like the if it's valid, or disposable
    email address.
    """
    def __init__(self, email, result_code):
        super(VerifiedEmail, self).__init__(email, result_code)


class VerifiedBulkEmail(Email):
    """
    VerifiedBulkEmail holds the information about an email that was verified in bulk verification job.
    """
    def __init__(self, email, result_text_code):
        result_code = RESULT_TEXT_CODES[result_text_code]
        super(VerifiedBulkEmail, self).__init__(email, result_code)
