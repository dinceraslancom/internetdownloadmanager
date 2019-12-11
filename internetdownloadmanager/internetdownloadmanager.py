from concurrent.futures import ThreadPoolExecutor

from .utils import get_file_info, set_part_total, url_handler, path_handler, file_handler, \
    write_handler, timer, get_ranged_data, get_resume_info, write_file_info, print_file_info, get_now, error, warning


class Downloader:
    def __init__(self, worker=25, part_size=1000000, info=True, resumable=False, _downloaded=set(), _part_count=0):
        self.worker = worker
        self.part_size = part_size
        self.info = info
        self.resumable = resumable
        self._downloaded = _downloaded

        self._file = None
        self._url = None
        self._path = None
        self._file_info = None

        self.downloaded_data_size = 0
        self.avg_count = 0

        self._part_count = _part_count
        self._part_total = 0
        self._start_time = None

    @timer
    def _downloader(self, part, start, end, slf):
        self.avg_count += 1
        response = get_ranged_data(url=self._url, start=start, end=end)
        if response.status_code not in [206, 200]:
            error('Request not allowed\nClosing..')

        write_handler(file=self._file,
                      path=self._path,
                      part=part,
                      offset=start,
                      data=response.content,
                      resumable=self.resumable)

        self._part_count += 1

    def download(self, url=None, path=None):

        self._url = url_handler(url)

        self._file_info = get_file_info(self._url)

        self._path = path or path_handler(self._url, self._file_info['extension'])
        self._file = file_handler(path=self._path)

        self._part_total = set_part_total(self._file_info['size'], self.part_size)

        if self.info:
            print_file_info(self)

        if not self._downloaded and self.resumable:
            write_file_info(self)

        self._start_time = get_now()

        warning('Download Starting')
        with ThreadPoolExecutor(max_workers=self.worker) as executor:
            for part in (set(range(0, self._part_total)) - self._downloaded):
                executor.submit(self._downloader,
                                part,
                                self.part_size * part,
                                self.part_size * part + self.part_size,
                                slf=self)

        file_handler(self._file).close()

    @classmethod
    def resume(cls, path):
        resume_info = get_resume_info(path)

        _resume = cls(info=resume_info['info'],
                      worker=int(resume_info['worker']),
                      resumable=resume_info['resumable'],
                      part_size=int(resume_info['part_size']),
                      _downloaded=resume_info['downloaded_parts'],
                      _part_count=resume_info['downloaded_parts_len'])

        _resume.download(url=resume_info['url'], path=resume_info['path'])
