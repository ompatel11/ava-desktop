# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['C:\\Users\\Om\\Desktop\\ava-desktop\\ava_desktop_ui\\main.py'],
             pathex=['C:\\Users\\Om\\Desktop\\ava-desktop\\ava_desktop_ui', 'C:\\Users\\Om\\Desktop\\ava-desktop\\ava_desktop_ui\\.pyupdater\\spec'],
             binaries=[],
             datas=[('application', 'application'), ('Icons', 'Icons')],
             hiddenimports=['pynput.keyboard._win32', 'pynput.mouse._win32'],
             hookspath=['C:\\Programming\\python3.7.1\\lib\\site-packages\\pyupdater\\hooks'],
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
          [],
          exclude_binaries=True,
          name='win',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='win')
