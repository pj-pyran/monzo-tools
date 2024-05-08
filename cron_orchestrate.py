# Cron job which runs daily and orchestrates data processing.
# Refresh token, pull down data, format it and enrich.
# From there data is in a form for easy tracking and analysis.
# Simple single-script execution when we want to on-demand reporting.

from creds import refresh_token as refresh_token
from datetime import datetime
import get_transactions
import logging


def daily_task():
    logging.info('Running daily task at 09:00')
    refresh_token()
    get_transactions.main()


if __name__ == '__main__':
    logging.info('Job started')
    current_time = datetime.now().time()

    if current_time.hour == 9 and current_time.minute < 5:
        daily_task()
        logging.info('Job completed successfully')
    else:
        logging.warning(f'Job not run; cron ran at the wrong time')
