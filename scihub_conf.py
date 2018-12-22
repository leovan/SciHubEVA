#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from configparser import ConfigParser


class SciHubConf(ConfigParser):
    def __init__(self, conf_filename, space_around_delimiters=True):
        super(SciHubConf, self).__init__()
        self.optionxform = str

        self._conf_path = os.path.join(os.path.dirname(__file__), conf_filename)
        self.read(self._conf_path)

        self._space_around_delimiters = space_around_delimiters

    def set(self, section, option, value=None):
        super(SciHubConf, self).set(section, option, value)
        self.save()

    def save(self):
        with open(self._conf_path, 'w') as fp:
            self.write(fp=fp, space_around_delimiters=self._space_around_delimiters)
