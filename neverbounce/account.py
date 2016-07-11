class Account:
    def __init__(self, resp):
        self._resp = resp

    def __str__(self):
        return 'credits: {}'.format(self.credits)

    @property
    def credits(self):
        """
        Return a number of credits.
        :return: int
        """
        return int(self._resp['credits'])

    @property
    def jobs_completed(self):
        """
        Return a number of completed jobs.
        :return: int
        """
        return int(self._resp['jobs_completed'])

    @property
    def jobs_processing(self):
        """
        Return a number of processing jobs.
        :return: int
        """
        return int(self._resp['jobs_processing'])

    @property
    def execution_time(self):
        """
        Return a verification execution time in seconds.
        :return: float
        """
        return self._resp['execution_time']
