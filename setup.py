import os
import shutil
import setuptools

keys = ['readme', 'license', 'todo', 'version']
os.makedirs('idlealib/docs', exist_ok=True)
for file in os.listdir():
    if any(file.lower().startswith(k) for k in keys):
        shutil.copy(file, 'idlealib/docs/' + file.lower())

with open('VERSION.txt') as f:
    version = f.read().strip()

with open('README.md', encoding='u8') as f:
    long_description = f.read().replace('[x]', chr(9989)).replace('[ ]', chr(10062)) # ✅❎

setuptools.setup(
    name='idlea',
    version=version,
    author='Lishixian(znsoooo)',
    author_email='lsx7@sina.com',
    description='IDLE-Advance',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/znsoooo/IDLE-Advance',
    project_urls={
        'Bug Tracker': 'https://github.com/znsoooo/IDLE-Advance/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Framework :: IDLE',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Text Editors :: Integrated Development Environments (IDE)',
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.4',

    # install_requires=['windnd'], # for drag-open file feature
    # extras_requires={'windnd': ['windnd']},
    license='MIT License',
    entry_points={'console_scripts': ['idlea=idlealib:run']},
    package_data={'': ['*.*']},
    keywords='IDLE-Advance IDLE IDLEA IDLEX extension idlelib idlexlib idlealib',
)
