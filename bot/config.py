import logging


def setup_log(path):
    logging.basicConfig(
    filename =  path + "\\" + "bacen.log", 
    level = logging.INFO, 
    #filemode='w', 
    encoding='utf8',
    format = "%(asctime)s :: %(message)s",
    datefmt = '%d-%m-%Y %H:%M:%S')

def print_log(msg):
    print(msg)
    logging.info(msg)

TRYS = {
    'start': 1,
    'max': 10
}
