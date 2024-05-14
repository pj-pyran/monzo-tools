import logging

def config_logging(file):
    path_log_file = 'monzo_logs.log'
    logging.basicConfig(
        filename=path_log_file,
        level=logging.INFO,
        format=f'%(asctime)s [{file}] [%(levelname)s] %(message)s'
    )
    logging.info('Logging configured.')
    return True