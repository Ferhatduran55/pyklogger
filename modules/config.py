import configparser

config = configparser.ConfigParser()
config.read('config.ini')

cfg = config['LOGGER']
max_file_size = int(cfg['max_file_size'])

log_folder = cfg['log_folder']
log_file_format = cfg['log_file_format']
log_file_date_format = cfg['log_file_date_format']
log_format = cfg['log_format']
log_date_format = cfg['log_date_format']
log_level = cfg['log_level']