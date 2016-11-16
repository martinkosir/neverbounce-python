from enum import Enum
from datetime import datetime


class VerifiedEmail(object):
    """
    VerifiedEmail holds the information about an email that was verified, like the if it's valid, or disposable
    email address.
    """
    class Codes(Enum):
        """
        Enumeration of possible codes.
        """
        valid = 0
        invalid = 1
        disposable = 2
        catchall = 3
        unknown = 4

    def __init__(self, email, result_code):
        self.email = email
        self.result_code = result_code

    @classmethod
    def from_text_code(cls, email, result_text_code):
        """
        Alternative method to create an instance of VerifiedEmail object from a text code.
        :param str email: Email address.
        :param str result_text_code: A result of verification represented by text (e.g. valid, unknown).
        :return: An instance of object.
        """
        result_code = cls.Codes[result_text_code].value
        return cls(email, result_code)

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
        return self.Codes(self.result_code).name

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


class Job(object):
    """
    Job class holds the information about NeverBounce bulk processing job.
    """
    def __init__(self, job_id):
        self.job_id = int(job_id)

    def __str__(self):
        return 'job {}'.format(self.job_id).title()


class JobStatus(object):
    """
    JobStatus class holds the information about NeverBounce bulk verification job status.
    """
    class Statuses(Enum):
        """
        Enumeration of possible job statuses.
        """
        uploading = -1
        received = 0
        parsing = 1
        parsed = 2
        running = 3
        completed = 4
        failed = 5

    class Types(Enum):
        """
        Enumeration of possible job types.
        """
        dashboard = 0
        API = 1

    def __init__(self, job_id, status_code, type_code, stats, orig_name, created, started, finished, **kwargs):
        self.job_id = int(job_id)
        self.status_code = int(status_code)
        self.status = self.Statuses(self.status_code).name
        self.type_code = int(type_code)
        self.type = self.Types(self.type_code).name
        self.stats = stats
        self.orig_name = orig_name
        self.created = datetime.strptime(created, '%Y-%m-%d %H:%M:%S') if created is not None else None
        self.started = datetime.strptime(started, '%Y-%m-%d %H:%M:%S') if started is not None else None
        self.finished = datetime.strptime(finished, '%Y-%m-%d %H:%M:%S') if finished is not None else None

    def __str__(self):
        return '{} job {}'.format(self.status, self.job_id).title()

    @property
    def is_uploading(self):
        return self.status_code == -1

    @property
    def is_received(self):
        return self.status_code == 0

    @property
    def is_parsing(self):
        return self.status_code == 1

    @property
    def is_parsed(self):
        return self.status_code == 2

    @property
    def is_running(self):
        return self.status_code == 3

    @property
    def is_completed(self):
        return self.status_code == 4

    @property
    def is_failed(self):
        return self.status_code == 5


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
        ).title()
