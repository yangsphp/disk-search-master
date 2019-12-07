# -*- mode: python -*-

block_cipher = None


a = Analysis(['miniSearch.py'],
             pathex=['G:\\PyCharm 2019.1\\project\\TK\\项目\\磁盘搜索工具'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='miniSearch',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='G:\\github\\mini-text-master\\trunk\\icon.ico')
