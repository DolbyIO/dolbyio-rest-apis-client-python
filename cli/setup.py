"""
Setup project
"""

import os
import pathlib
import setuptools

current_path = pathlib.Path(__file__).parent.resolve()

with open(os.path.join(current_path, 'README.md'), 'r', encoding='UTF-8') as f:
    long_description = f.read()

with open(os.path.join(current_path, 'requirements.txt'), 'r', encoding='UTF-8') as f:
    requirements = f.readlines()

setuptools.setup(
    name='dolbyio-rest-apis-cli',
    author='Dolby.io',
    author_email='fabien.lavocat@dolby.com',
    description='A command line wrapper for the Dolby.io REST APIs.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/dolbyio/dolbyio-rest-apis-client-python',
    project_urls={
        'Documentation': 'https://docs.dolby.io/communications-apis/reference',
        'Source': 'https://github.com/dolbyio/dolbyio-rest-apis-client-python',
        'Bug Tracker': 'https://github.com/dolbyio/dolbyio-rest-apis-client-python/issues',
    },
    package_dir={'': os.path.join(current_path, 'src')},
    packages=setuptools.find_packages(where=os.path.join(current_path, 'src')),
    entry_points={
        'console_scripts': [
            'communications=dolbyio_rest_apis_cli.communications.cli:cli',
            'media=dolbyio_rest_apis_cli.media.cli:cli',
        ],
    },
    python_requires='>=3.7',
    use_scm_version= {
        'local_scheme': 'no-local-version',
        'version_scheme': 'release-branch-semver',
    },
    setup_requires=[
        'setuptools_scm',
    ],
    install_requires=requirements,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
    ],
)
