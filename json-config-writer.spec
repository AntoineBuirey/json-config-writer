# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec file for JSON Config Writer

This file configures PyInstaller to build a standalone executable 
from the JSON Config Writer Python application.

Usage:
    pyinstaller json-config-writer.spec

Generated executable will be in the 'dist' folder.
"""

import sys
import os

# Get the path to the source directory
source_dir = os.path.join(os.path.dirname(os.path.abspath(SPECPATH)), 'json-config-writer/json-config-writer')

# Analysis configuration
a = Analysis(
    # Main script (entry point)
    [os.path.join(source_dir, '__main__.py')],
    
    # Additional paths to search for modules
    pathex=[
        source_dir,
        os.path.dirname(os.path.abspath(SPECPATH))
    ],
    
    # Binary files (libraries) - let PyInstaller auto-detect
    binaries=[],
    
    # Data files to include
    datas=[
        # Include config.xml file
        (os.path.join(source_dir, 'config.xml'), '.'),
    ],
    
    # Hidden imports that PyInstaller might miss
    hiddenimports=[
        'sv_ttk',           # Sun Valley theme
        'darkdetect',       # Dark mode detection
        'pywinstyles',      # Windows styling (conditional)
        'xml.etree.ElementTree',
        'tkinter.colorchooser',
        'tkinter.filedialog',
    ],
    
    # Modules to exclude from the build
    excludes=[
        'matplotlib',       # Often auto-included but not needed
        'numpy',           # Often auto-included but not needed
        'PIL',             # Often auto-included but not needed
        'PyQt5',           # Alternative GUI framework
        'PyQt6',           # Alternative GUI framework
        'PySide2',         # Alternative GUI framework
        'PySide6',         # Alternative GUI framework
    ],
    
    # Disable UPX compression (can cause issues on some systems)
    noarchive=False,
    optimize=0,
)

# PYZ archive configuration
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Executable configuration
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    
    # Output executable name
    name='json-config-writer',
    
    # Debug options
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    
    # Console window (set to False for GUI-only app)
    console=False,
    
    # Windows-specific options
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    
    # Icon file (uncomment and provide path if you have an icon)
    # icon='path/to/icon.ico',
)

# Optional: Create a directory distribution instead of a single file
# Uncomment the following lines if you prefer a directory structure
# This can be faster to start and easier to debug

# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='json-config-writer'
# )

# Platform-specific adjustments
if sys.platform.startswith('win'):
    # Windows-specific configuration
    # Add Windows-specific hidden imports if needed
    pass
elif sys.platform.startswith('darwin'):
    # macOS-specific configuration
    # Create an app bundle for macOS
    app = BUNDLE(
        exe,
        name='JSON Config Writer.app',
        icon=None,  # Provide .icns file path if available
        bundle_identifier='com.jsonconfig.writer',
        info_plist={
            'CFBundleDisplayName': 'JSON Config Writer',
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
            'NSHighResolutionCapable': True,
        }
    )
elif sys.platform.startswith('linux'):
    # Linux-specific configuration
    pass