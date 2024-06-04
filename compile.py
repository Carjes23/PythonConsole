import os
import subprocess

# Define paths and parameters
script_name = 'main.py'
executable_name = 'TerminalIF'
icon_path = './icon.ico'
spec_file_name = 'TerminalIF.spec'
python_version = '3.10'
virtual_env_path = './.venv'

# Step 1: Create the spec file using PyInstaller
subprocess.run([
    f"{virtual_env_path}/bin/pyinstaller", 
    '--onefile', 
    '--windowed', 
    f'--name={executable_name}', 
    f'--icon={icon_path}', 
    script_name
])

# Step 2: Manually create the spec file with necessary imports and data
spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{script_name}'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('./.venv/lib/python{python_version}/site-packages/PIL', 'PIL'),
        ('./.venv/lib/python{python_version}/site-packages/matplotlib/mpl-data', 'mpl-data'),
        ('/usr/lib/python{python_version}/tkinter', 'tkinter')
    ],
    hiddenimports=['PIL._tkinter_finder', 'tkinter', 'matplotlib.backends.backend_tkagg', 'PIL.ImageTk', '_tkinter', 'serial'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{executable_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='{icon_path}',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{executable_name}',
)
"""

# Write the spec content to the spec file
with open(spec_file_name, 'w') as file:
    file.write(spec_content)

# Step 3: Run PyInstaller with the modified spec file
subprocess.run([
    f"{virtual_env_path}/bin/pyinstaller", 
    spec_file_name
])

# Step 4: Create the install.sh script
install_script = f"""#!/bin/bash

# Copy the executable to /usr/local/bin
sudo cp ./dist/{executable_name} /usr/local/bin/{executable_name}

# Copy the icon to /usr/share/pixmaps
sudo cp {icon_path} /usr/share/pixmaps/{executable_name}.png

# Create the desktop entry
cat <<EOF | sudo tee /usr/share/applications/{executable_name}.desktop
[Desktop Entry]
Version=1.0
Name=TerminalIF
Comment=Microcontroller Interface
Exec=/usr/local/bin/{executable_name}
Icon=/usr/share/pixmaps/{executable_name}.png
Terminal=false
Type=Application
Categories=Utility;
EOF

echo "Installation complete. You can find your app in the applications menu."
"""

# Write the install script to a file
with open('install.sh', 'w') as file:
    file.write(install_script)

# Make the install script executable
os.chmod('install.sh', 0o755)

print("Compilation and installation script generation complete.")
