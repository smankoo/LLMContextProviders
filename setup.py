from setuptools import setup, find_packages

setup(
    name='LLMContextProviders',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'asana',
        'python-dotenv',
        'python-dateutil',
        'pytz',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            # Add any command line scripts here if needed
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
