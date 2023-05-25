#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import opencc

from pathlib import Path


if __name__ == '__main__':
    tw_converter = opencc.OpenCC('s2twp')
    hk_converter = opencc.OpenCC('s2hk')

    i18n_directory = Path(os.path.dirname(__file__)) / '..' / 'i18n'

    with open(i18n_directory / 'SciHubEVA_zh_CN.ts', 'r',
              encoding='utf-8') as zh_i18n_f:
        zh_i18n_str = zh_i18n_f.read()

        hk_i18n_str = hk_converter.convert(zh_i18n_str)
        with open(i18n_directory / 'SciHubEVA_zh_HK.ts', 'w',
                  encoding='utf-8') as hk_i18n_f:
            hk_i18n_f.write(hk_i18n_str)

        tw_i18n_str = tw_converter.convert(zh_i18n_str)
        with open(i18n_directory / 'SciHubEVA_zh_TW.ts', 'w',
                  encoding='utf-8') as tw_i18n_f:
            tw_i18n_f.write(tw_i18n_str)
