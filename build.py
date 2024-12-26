import PyInstaller.__main__
import shutil
import os

# Define app name and version
from app import version

appname = 'National Rail Data Downloader'
version = f'{appname} {version}'

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
        versioned_path = os.path.join(output_folder, version)
        shutil.make_archive(versioned_path, 'zip', root_dir='dist', base_dir=file)

        # Save master app
        shutil.move(os.path.join('dist', file), os.path.join(output_folder, f'{version}.app'))

# Clean up build files
shutil.rmtree('build')
shutil.rmtree('dist')
shutil.rmtree('__pycache__')
os.remove(f'{appname}.spec')