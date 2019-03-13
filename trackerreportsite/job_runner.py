from __future__ import absolute_import
import logging
import logging.handlers
import os
import django

import sys
path_append = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path_append)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackerreportsite.settings')
django.setup()

# to run the job, just run python3 path/to/this/file/ e.g python3 job_runner.py
# This can also be run via cron and should be run via cron

from django.utils import timezone
from trackerreport.job import run_job

FILE_NAME = 'scheduler_logger.log'
job_logger = logging.getLogger('JobLogger')
job_logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(FILE_NAME,
                                               maxBytes=512000,
                                               backupCount=5,
                                               )
job_logger.addHandler(handler)


if __name__ == '__main__':
	run_job()
