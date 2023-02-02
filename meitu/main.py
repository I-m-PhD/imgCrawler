from pathlib import Path
from subprocess import Popen

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def main():
    """ https://www.meitu131.net/nvshen/ """
    Path('./log').mkdir(exist_ok=True)
    Popen('scrapy crawl nvshen -s LOG_FILE=./log/nvshen.log'.split())
    Popen('scrapy crawl nvshen_dl -s LOG_FILE=./log/nvshen_dl.log'.split())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
    # print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
