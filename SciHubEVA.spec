# -*- mode: python -*-

block_cipher = None


a = Analysis(['scihub_eva.py'],
             pathex=['/Users/leo/Documents/Projects/Python/SciHubEVA'],
             binaries=[],
             datas=[('LICENSE', '.'), ('SciHubEVA.conf', '.'), ('images/SciHubEVA.png', 'images'), ('translations/SciHubEVA_zh_CN.qm', 'translations')],
             hiddenimports=['PyQt5.Qt', 'PyQt5.QtQuick'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='SciHubEVA',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='images/SciHubEVA.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='SciHubEVA')
app = BUNDLE(coll,
             name='SciHubEVA.app',
             icon='images/SciHubEVA.icns',
             bundle_identifier=None)
