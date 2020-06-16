try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages
setup(
    name='gis-tools',
    version='1.1.0',
    description='Python scripts for process geo data ',
    author='yunica',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4==4.9.0',
        'certifi==2019.11.28',
        'chardet==3.0.4',
        'click==7.1.2',
        'idna==2.9',
        'MouseInfo==0.1.3',
        'numpy==1.18.5',
        'pandas==1.0.4',
        'Pillow==7.1.2',
        'PyAutoGUI==0.9.50',
        'PyGetWindow==0.0.8',
        'PyMsgBox==1.0.7',
        'pyperclip==1.8.0',
        'PyRect==0.1.4',
        'PyScreeze==0.1.26',
        'python-dateutil==2.8.1',
        'python3-xlib==0.15',
        'PyTweening==1.0.3',
        'pytz==2020.1',
        'pywhatkit==1.8',
        'requests==2.23.0',
        'Shapely==1.7.0',
        'six==1.15.0',
        'soupsieve==2.0',
        'urllib3==1.25.8',
        'wikipedia==1.4.0',
    ],
    entry_points={
        'console_scripts': [
            'gfw=scripts.gfw.__init__:main',

        ],
    },
)
