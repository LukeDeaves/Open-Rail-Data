import PyInstaller.__main__
import shutil
import os

# Define app name and version
from app import version
appname = 'National Rail Data Downloader'

# Run PyInstaller
PyInstaller.__main__.run([
    '--name=%s' % appname,
    '--onefile',
    '--windowed',
    'app.py'
])

# Check package folder exists
output_folder = 'packages'
os.makedirs(output_folder, exist_ok=True)

# Move app to packages folder
for file in os.listdir('dist'):
    if file.endswith('.app'):
        # Save versioned app
        versioned_path = os.path.join(output_folder, f'{appname} {version}.app')
        if os.path.exists(versioned_path):
            shutil.rmtree(versioned_path)
        shutil.copytree(os.path.join('dist', file), os.path.join(output_folder, f'{appname} {version}.app'))

        # Save master app
        master_path = os.path.join(output_folder, f'{appname}.app')
        if os.path.exists(master_path):
            shutil.rmtree(master_path)
        shutil.move(os.path.join('dist', file), os.path.join(output_folder, file))

# Clean up build files
shutil.rmtree('build')
shutil.rmtree('dist')
shutil.rmtree('__pycache__')
os.remove(f'{appname}.spec')