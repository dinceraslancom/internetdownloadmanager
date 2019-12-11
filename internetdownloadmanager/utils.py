from math import ceil
import requests
from threading import Lock
import sys
from time import time
from json import loads, dumps
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

lock = Lock()


def warning(message):
    logger.warning(message)


def info(message):
    logger.info(message)


def error(message):
    logger.error(message)


def write_handler(file, path, part, offset, data, resumable):
    with lock:
        file_handler(file, path).seek(offset)
        file_handler(file, path).write(data)

        if resumable:
            with open(f'{path}.resumable', '+a') as log:
                log.write(f'/{part}')


def round_2(score):
    return round(score, 2)


def fix(score):
    return ceil(score)


def get_now():
    return time()


def set_part_total(file_size, part_size):
    return ceil(file_size / part_size)


def get_resume_info(path):
    with open(path, 'r') as file:
        data = file.read().split('*')

    resume_info = loads(data[0])
    resume_info['downloaded_parts'] = set(int(i) for i in data[1][1::].split('/'))
    resume_info['downloaded_parts_len'] = len(resume_info['downloaded_parts'])
    return resume_info


def get_ranged_data(url, start, end):
    return requests.get(url, headers={'range': f'bytes={start}-{end}'}, stream=True)


def get_file_info(url):
    response_head = requests.head(url)
    if response_head.status_code != 200:
        response_head.raise_for_status()
    _file_info = response_head.headers
    _type, _extension = _file_info['Content-Type'].split("/")

    if 'Content-Length' not in _file_info:
        raise Exception('Can not get Content-Length')

    _size = int(_file_info['Content-Length'])

    return dict(type=_type,
                size=_size,
                extension=_extension)


def url_handler(url):
    if not url:
        raise Exception('URL is Invalid')
    return url


def path_handler(url, extension):
    if url.endswith('/'):
        url = url[:-1]

    path = url.split('/')[-1]

    if len(path):
        path = path[:30]

    if 0 < len(path.split('.')[-1]) < 5:
        return path
    else:
        return f'{path}.{extension}'


def file_handler(file=None, path=None):
    if not file:
        try:
            file = open(path, 'r+b', buffering=0)
        except IOError:
            file = open(path, 'wb', buffering=0)

    return file


def timer(func):
    def decorator(*args, **kwargs):
        self = kwargs['slf']

        start_time = get_now()
        func(*args, **kwargs)
        end_time = get_now()

        take_seconds = end_time - start_time

        will_done = fix(take_seconds * (self._part_total - self._part_count) / self.worker)
        during = fix(get_now() - self._start_time)
        speed = fix((self.part_size / take_seconds) * self.worker / 125)  # (1000/8)

        self.downloaded_data_size += speed

        average_speed = fix(self.downloaded_data_size / self.avg_count)

        percent = round_2((self._part_count / self._part_total) * 100)
        # print()
        sys.stdout.write(
            f'\rStatus: %{percent} | Transfer Rate =  {speed} Kb/s | Time Left: {will_done} sn | Time: {during} sn | AVG Speed={average_speed} Kb/s ')
        sys.stdout.flush()

    return decorator


def write_file_info(self):
    with open(self._path+'.resumable', 'w') as log:
        log.write(dumps(dict(url=self._url,
                             path=self._path,
                             part_size=str(self.part_size),
                             worker=str(self.worker),
                             info=self.info,
                             resumable=self.resumable
                             )) + '*')


def print_file_info(self):
    info(f'\nFile Path:{self._path} \n'
         f'File Size: {self._file_info["size"]} \n'
         f'Worker: {self.worker} \n'
         f'Calculated Part: {self._part_total - len(self._downloaded)} \n'
         )
