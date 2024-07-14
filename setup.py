from setuptools import setup, find_packages
import os

# Read the contents of the README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='llm-context-providers',
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
    long_description=long_description,
    long_description_content_type='text/markdown', 
    url='https://github.com/smankoo/LLMContextProviders',
    author='Sumeet Singh Mankoo',
    author_email='sumeet@mankoo.ca',
    license='MIT',
)
