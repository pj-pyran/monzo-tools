"""
Cron job which runs daily and orchestrates data processing.
Refresh token, pull down data, format it and enrich.
From there data is in a form for easy tracking and analysis.
Simple single-script execution when we want on-demand reporting.
"""
from logging_config import config_logging
from creds import creds_check
from datetime import datetime
import enrich_transactions
import get_transactions
import logging

config_logging(__file__)


def daily_task():
    logging.info('Retrieving credentials...')
    creds_check()
    logging.info('Getting transactions...')
    get_transactions.main('incremental')
    logging.info('Enriching transactions...')
    enrich_transactions.main()

if __name__ == '__main__':
    logging.info('Job started')
    daily_task()
    logging.info('Job completed successfully')
