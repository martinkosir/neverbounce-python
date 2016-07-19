from datetime import datetime


STATUS_CODES = {
    -1: 'uploading',
    0: 'received',
    1: 'parsing',
    2: 'parsed',
    3: 'running',
    4: 'completed',
    5: 'failed',
}

TYPE_CODES = {
    0: 'dashboard',
    1: 'API',
}


class Job:
    """
    Job class holds the information about NeverBounce bulk processing job.
    """
    def __init__(self, job_id):
        self.job_id = int(job_id)

    def __str__(self):
        return 'job: {}'.format(self.job_id)


class JobStatus(Job):
    """
    JobStatus class holds the information about NeverBounce bulk verification job status.
    """
    def __init__(self, job_id, status_code, type_code, stats, orig_name, created, started, finished):
        self.status_code = int(status_code)
        self.status = STATUS_CODES[self.status_code]
        self.type_code = int(type_code)
        self.type = TYPE_CODES[self.type_code]
        self.stats = stats
        self.orig_name = orig_name
        self.created = datetime.strptime(created, '%Y-%m-%d %H:%M:%S')
        self.started = datetime.strptime(started, '%Y-%m-%d %H:%M:%S')
        self.finished = datetime.strptime(finished, '%Y-%m-%d %H:%M:%S')
        super(JobStatus, self).__init__(job_id)

    def __str__(self):
        return '{} job: {}'.format(self.status, self.job_id)

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
