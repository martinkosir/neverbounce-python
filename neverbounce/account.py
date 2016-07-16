class Account:
    """
    Account class holds the information about NeverBounce account, eg. number of credits available, jobs completed, etc.
    """
    def __init__(self, credits, jobs_completed, jobs_processing):
        self.credits = int(credits)
        self.jobs_completed = int(jobs_completed)
        self.jobs_processing = int(jobs_processing)

    def __str__(self):
        """
        :return: A string representation of an account.
        """
        return 'credits: {}, jobs completed: {}, jobs processing: {}'.format(
            self.credits, self.jobs_completed, self.jobs_processing
        )
