import os

import requests
import logging

import time


class FlashairAPI(object):
    def __init__(self, host, target_dir):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.host = host
        self.target_dir = target_dir

        self.synced_files = []
        self.last_content_hash = None

        self._init_cache()
        self.root_dir = '/DCIM'
        self.timeout = 3

        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)


    def _init_cache(self):
        path = os.path.abspath(self.target_dir)

        for root, dirs, files in os.walk(path):
            for file_name in files:
                if file_name.lower().endswith(".jpg"):
                    subdir_path = root.split(path)[1]
                    full_name = os.path.join(subdir_path, file_name)
                    self.synced_files.append(full_name)

    @property
    def _ts(self):
        return int(time.time() * 1000)

    def has_updates(self):
        self.logger.debug('scanning...')

        try:
            resp = requests.get('http://%s/command.cgi?op=121&TIME=%s' % (self.host, self._ts), timeout=self.timeout)
            if resp.status_code != 200:
                self.logger.error('invalid status code: %d' % resp.status_code)
                return False
        except requests.exceptions.ReadTimeout:
            self.logger.error('timeout in request')
            return False

        retval = resp.content
        lastval = self.last_content_hash
        self.last_content_hash = retval
        change = False
        if retval != lastval:
            change = True

        if not change:
            return False

        return True

    def get_updates(self):
        ts = int(time.time() * 1000)

        self.logger.info('changes detected. analyzing...')

        try:
            resp = requests.get('http://%s/command.cgi?op=100&DIR=%s&TIME=%s' % (self.host, self.root_dir, ts), timeout=self.timeout)
            if resp.status_code != 200:
                self.logger.error('invalid status code: %d' % resp.status_code)
                return []
        except requests.exceptions.ReadTimeout:
            self.logger.error('timeout in request')
            return []

        retval = resp.content
        lines = retval.split('\r\n')

        files = []
        subdirs = []
        for line in lines[1:]:
            if ',' not in line:
                break

            filename = line.split(',')[1]
            filesize = line.split(',')[2]

            if filesize == '0':
                final_name = '%s/%s' % (self.root_dir, filename)
                if final_name not in self.synced_files:
                    subdirs.append(final_name)
                elif filename.lower().endswith('jpg'):
                    files.append(final_name)

        if not files and not subdirs:
            self.logger.info('no new files found.')
            return []

        for subdir in subdirs:
            self.logger.debug('scanning folder %s...' % subdir)
            try:
                resp = requests.get('http://%s/command.cgi?op=100&DIR=%s&TIME=%s' % (self.host, subdir, ts), timeout=self.timeout)
                if resp.status_code != 200:
                    self.logger.error('invalid status code: %d' % resp.status_code)
                    return []
            except requests.exceptions.ReadTimeout:
                self.logger.error('timeout in request')
                return []

            retval = resp.content
            lines = retval.split('\r\n')

            for line in lines[1:]:
                if ',' not in line:
                    break
                filename = line.split(',')[1]
                if filename.lower().endswith('jpg'):
                    final_name = '%s/%s' % (subdir, filename)
                    if final_name not in self.synced_files:
                        files.append(final_name)

        if not files:
            self.logger.info('no new files found.')
            return []

        self.logger.info('found %d new files.' % len(files))

        return files

    def download_file(self, file):

        self.logger.info('downloading file %s...' % file)
        
        try:
            resp = requests.get('http://%s%s' % (self.host, file), timeout=self.timeout)
            if resp.status_code != 200:
                self.logger.error('invalid status code: %d' % resp.status_code)
                return
        except requests.exceptions.ReadTimeout:
            self.logger.error('timeout in request')
            return

        self.logger.info('downloaded %.2f MB.' % (len(resp.content) / 1024.0 / 1024))

        elms = file.split('/')

        filename = elms[-1]
        path = os.path.abspath(os.path.join(self.target_dir, '/'.join(elms[:-1])[1:]))

        self.logger.debug('saving %s to %s...' % (filename, path))
        if not os.path.exists(path):
            os.makedirs(path)

        target_file = '%s/%s' % (path, filename)

        fh = open(target_file, 'wb')
        fh.write(resp.content)
        fh.close()
        self.logger.debug('file saved.')

        self.synced_files.append(file)
