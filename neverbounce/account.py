class Account:
    """
    Account class holds the information about NeverBounce account, eg. number of credits available, jobs completed, etc.
    """
    def __init__(self, resp):
        self._resp = resp

    def __str__(self):
        """
        :return: A string representation of an account.
        """
        return 'credits: {}, jobs completed: {}, jobs processing: {}'.format(
            self.credits, self.jobs_completed, self.jobs_processing
        )

    @property
    def credits(self):
        """
        :return: An integer number of credits.
        """
        return int(self._resp['credits'])

    @property
    def jobs_completed(self):
        """
        :return: An integer number of completed jobs.
        """
        return int(self._resp['jobs_completed'])

    @property
    def jobs_processing(self):
        """
        :return: An integer number of processing jobs.
        """
        return int(self._resp['jobs_processing'])
