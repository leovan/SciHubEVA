#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from configparser import ConfigParser

class SciHubConf(ConfigParser):
    def __init__(self, conf_filename=None):
        super(SciHubConf, self).__init__()

        conf_filename_ = conf_filename if conf_filename else 'SciHubEVA.conf'
        self._conf_path = os.path.join(os.path.dirname(__file__), conf_filename_)
        self.read(self._conf_path)

    def set(self, section, option, value=None):
        super(SciHubConf, self).set(section, option, value)
        self.save()

    def save(self):
        with open(self._conf_path, 'w') as fp:
            self.write(fp=fp)

if __name__ == '__main__':
    pass
