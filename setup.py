#!/usr/bin/env python
from setuptools import setup

setup(
        name = 'spootipy',
        packages = ['spootipy'],
        version = '0.0.1',
        include_package_data = True,
        description = 'CLI Based Spotipy Interface',
        author = 'Brett Henderson',
        author_email = 'bretth18@gmail.com',
        license='MIT',
        entry_points={'console_scripts': ['spotipy-tui=spotipy_tui.app:run']},
        url = 'https://github.com/bretth18',
        download_url = '',
        keywords = ['spotify', 'remote', 'audio', 'music', 'tui', 'curses'],
        install_requires=['requests'],
        classifiers = [
                'Intended Audience :: End Users/Desktop',
                'Environment :: Console :: Curses',
                'Operating System :: MacOS :: MacOS X',
                'Natural Language :: English',
                'Programming Language :: Python :: 3.1',
                'Programming Language :: Python :: 3.2',
                'Programming Language :: Python :: 3.3',
                'Programming Language :: Python :: 3.4',
                'Topic :: Terminals',
                'Topic :: Multimedia :: Sound/Audio :: Players',
              ],

        )
