from pathlib import Path
from subprocess import Popen
# from datetime import datetime


def main():
    Popen('python proxy_pool/proxyPool.py schedule')
    Popen('python proxy_pool/proxyPool.py server')

    Path('./log').mkdir(exist_ok=True)
    # log_name = datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S')
    Popen('scrapy crawl nvshen -s LOG_FILE=./log/nvshen.log'.split())
    Popen('scrapy crawl nvshen_dl -s LOG_FILE=./log/nvshen_dl.log'.split())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
