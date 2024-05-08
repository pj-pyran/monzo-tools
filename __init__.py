import logging

path_log_file = '/Users/peter/git_repos/cron_logs/cron_job.log'
logging.basicConfig(
    filename=path_log_file,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
