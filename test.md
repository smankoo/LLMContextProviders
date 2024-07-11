```bash
./requirements.txt
```
```
asana
python-dotenv
python-dateutil
pytz
pyyaml
```
```bash
./.pytest_cache/CACHEDIR.TAG
```
```
Signature: 8a477f597d28d172789f06886806bc55
# This file is a cache directory tag created by pytest.
# For information about cache directory tags, see:
#	https://bford.info/cachedir/spec.html
```
```bash
./.pytest_cache/README.md
```
```
# pytest cache directory #

This directory contains data from the pytest's cache plugin,
which provides the `--lf` and `--ff` options, as well as the `cache` fixture.

**Do not** commit this to version control.

See [the docs](https://docs.pytest.org/en/stable/how-to/cache.html) for more information.
```
```bash
./.pytest_cache/.gitignore
```
```
# Created by pytest automatically.
*
```
```bash
./.pytest_cache/v/cache/nodeids
```
```
[
  "tests/test_asana_context_provider.py::test_fetch_context_async",
  "tests/test_asana_context_provider.py::test_fetch_context_sync",
  "tests/test_asana_context_provider.py::test_missing_project_id",
  "tests/test_context_manager.py::test_fetch_all_contexts",
  "tests/test_context_manager.py::test_fetch_all_contexts_async"
]
```
```bash
./.pytest_cache/v/cache/lastfailed
```
```
{}
```
```bash
./.pytest_cache/v/cache/stepwise
```
```
[]
```
```bash
./tests/__init__.py
```
```

```
```bash
./tests/test_context_manager.py
```
```
import pytest
from unittest.mock import patch, AsyncMock
from llm_context_providers import ContextManager, AsanaContextProvider

@pytest.mark.asyncio
async def test_fetch_all_contexts_async():
    config = {
        'context_providers': {
            'asana': {
                'enabled': True,
                'project_id': 'test_project_id',
                'timezone': 'America/Toronto',
                'fields': {
                    "Task": "name",
                    "Task ID": "gid",
                    "Created At": "created_at",
                    "Modified At": "modified_at",
                    "Completed": "completed",
                    "Assignee": "assignee",
                    "Due On": "due_on",
                    "Notes": "notes"
                }
            }
        }
    }
    with patch('llm_context_providers.context_provider.ContextProvider.get_provider_class', return_value=AsanaContextProvider):
        manager = ContextManager(config['context_providers'])
        with patch.object(AsanaContextProvider, 'fetch_context_async', new=AsyncMock()) as mock_fetch:
            await manager.fetch_contexts_async()
            mock_fetch.assert_called_once()

def test_fetch_all_contexts():
    config = {
        'context_providers': {
            'asana': {
                'enabled': True,
                'project_id': 'test_project_id',
                'timezone': 'America/Toronto',
                'fields': {
                    "Task": "name",
                    "Task ID": "gid",
                    "Created At": "created_at",
                    "Modified At": "modified_at",
                    "Completed": "completed",
                    "Assignee": "assignee",
                    "Due On": "due_on",
                    "Notes": "notes"
                }
            }
        }
    }
    with patch('llm_context_providers.context_provider.ContextProvider.get_provider_class', return_value=AsanaContextProvider):
        manager = ContextManager(config['context_providers'])
        with patch.object(AsanaContextProvider, 'fetch_context', return_value=None) as mock_fetch:
            manager.fetch_contexts()
            mock_fetch.assert_called_once()
```
```bash
./tests/test_asana_context_provider.py
```
```
import os
import pytest
from unittest.mock import patch, AsyncMock
from llm_context_providers import AsanaContextProvider
from dotenv import load_dotenv

load_dotenv()

@pytest.mark.asyncio
async def test_fetch_context_async():
    provider = AsanaContextProvider(
        project_id=os.getenv("ASANA_PROJECT_ID", "test_project_id"),
        timezone="America/Toronto",
        fields={
            "Task": "name",
            "Task ID": "gid",
            "Created At": "created_at",
            "Modified At": "modified_at",
            "Completed": "completed",
            "Assignee": "assignee",
            "Due On": "due_on",
            "Notes": "notes"
        }
    )
    with patch.object(provider, 'get_project_info', new=AsyncMock(return_value={
            'name': 'Test Project', 
            'gid': '12345', 
            'created_at': '2024-07-07T11:00:00Z', 
            'modified_at': '2024-07-10T12:34:00Z',
            'owner': {'name': 'Test Owner'},
            'notes': '',
            'start_on': None,
            'due_on': None
        })), \
         patch.object(provider, 'get_tasks_info', new=AsyncMock(return_value=[])):
        await provider.fetch_context_async()
        context = provider.get_context()
        assert context is not None
        assert "Project:" in context

def test_fetch_context_sync():
    provider = AsanaContextProvider(
        project_id=os.getenv("ASANA_PROJECT_ID", "test_project_id"),
        timezone="America/Toronto",
        fields={
            "Task": "name",
            "Task ID": "gid",
            "Created At": "created_at",
            "Modified At": "modified_at",
            "Completed": "completed",
            "Assignee": "assignee",
            "Due On": "due_on",
            "Notes": "notes"
        }
    )
    with patch.object(provider, 'get_project_info_sync', return_value={
            'name': 'Test Project', 
            'gid': '12345', 
            'created_at': '2024-07-07T11:00:00Z', 
            'modified_at': '2024-07-10T12:34:00Z',
            'owner': {'name': 'Test Owner'},
            'notes': '',
            'start_on': None,
            'due_on': None
        }), \
         patch.object(provider, 'get_tasks_info_sync', return_value=[]):
        provider.fetch_context()
        context = provider.get_context()
        assert context is not None
        assert "Project:" in context

def test_missing_project_id():
    with pytest.raises(ValueError, match="Asana project ID is not set"):
        AsanaContextProvider(
            project_id=None,
            timezone="America/Toronto",
            fields={
                "Task": "name",
                "Task ID": "gid",
                "Created At": "created_at",
                "Modified At": "modified_at",
                "Completed": "completed",
                "Assignee": "assignee",
                "Due On": "due_on",
                "Notes": "notes"
            }
        )
```
```bash
./README.md
```
```
# LLM Context Providers

A Python package to manage and fetch context from various sources like Asana, Quip, OneNote, Outlook Calendar, etc. This package is designed to be easily extensible, allowing new context providers to be added with minimal changes to the core logic.

## Features

- Fetch context from multiple sources asynchronously or synchronously.
- Easily extendable with new context providers.
- Configurable through YAML configuration.
- Handles retries and errors gracefully.

## Installation

```bash
pip install llm-context-providers
```

## Configuration

Create a `config.yml` file to configure your context providers. Here is an example configuration:

```yaml
context_providers:
  asana:
    enabled: true
    project_id: "your_asana_project_id"
    fields:
      Task: "name"
      Task ID: "gid"
      Created At: "created_at"
      Modified At: "modified_at"
      Completed: "completed"
      Assignee: "assignee"
      Due On: "due_on"
      Notes: "notes"
    timezone: "America/Toronto"
  # Add other context providers here
```

Create a `.env` file to store your credentials:

```
ASANA_PERSONAL_ACCESS_TOKEN=your_asana_personal_access_token
# Add other environment variables here
```

## Usage

### Initializing Context Manager

```python
import yaml
from llm_context_providers import ContextManager

def load_config(config_file='config.yml'):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

config = load_config()
manager = ContextManager(config['context_providers'])
```

### Fetching Context Asynchronously

```python
import asyncio

async def fetch_async():
    await manager.fetch_contexts_async()
    context = manager.get_combined_context()
    print("Async Fetch Context:
", context)

asyncio.run(fetch_async())
```

### Fetching Context Synchronously

```python
manager.fetch_contexts()
context = manager.get_combined_context()
print("Sync Fetch Context:
", context)
```

### Fetching Specific Context Providers

#### Asynchronously

```python
async def fetch_specific_async():
    await manager.fetch_contexts_async(providers=['asana'])
    context = manager.get_combined_context(providers=['asana'])
    print("Async Fetch Specific Context:
", context)

asyncio.run(fetch_specific_async())
```

#### Synchronously

```python
manager.fetch_contexts(providers=['asana'])
context = manager.get_combined_context(providers=['asana'])
print("Sync Fetch Specific Context:
", context)
```

## Extending with New Context Providers

To add a new context provider, create a new class that inherits from `ContextProvider` and implement the necessary methods:

```python
from llm_context_providers import ContextProvider

class NewContextProvider(ContextProvider):
    def __init__(self, **kwargs):
        super().__init__()
        # Initialize with necessary credentials and configurations

    async def fetch_context_async(self, full_fetch: bool = False):
        # Implement async context fetching logic
        pass

    def fetch_context(self, full_fetch: bool = False):
        # Implement sync context fetching logic
        pass

    def get_context(self):
        # Return the context information
        pass

    async def index_context(self):
        # Implement indexing logic
        pass

    async def search_index(self, query: str):
        # Implement search logic
        pass

    def load_from_index(self, search_results):
        # Implement logic to load search results into context
        pass
```

Add the new context provider to your configuration file and ensure the package's `ContextProvider` class can recognize the new provider.

## Testing

To run the test application:

1. Create a `test_app.py` file with the following content:

```python
import yaml
import asyncio
from llm_context_providers import ContextManager

def load_config(config_file='config.yml'):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

async def main_async(config):
    manager = ContextManager(config['context_providers'])
    await manager.fetch_contexts_async()
    context = manager.get_combined_context()
    print("Async Fetch Context (All):
", context)

async def main_async_specific(config):
    manager = ContextManager(config['context_providers'])
    await manager.fetch_contexts_async(providers=['asana'])
    context = manager.get_combined_context(providers=['asana'])
    print("Async Fetch Context (Specific):
", context)

def main_sync(config):
    manager = ContextManager(config['context_providers'])
    manager.fetch_contexts()
    context = manager.get_combined_context()
    print("Sync Fetch Context (All):
", context)

def main_sync_specific(config):
    manager = ContextManager(config['context_providers'])
    manager.fetch_contexts(providers=['asana'])
    context = manager.get_combined_context(providers=['asana'])
    print("Sync Fetch Context (Specific):
", context)

if __name__ == "__main__":
    config = load_config()

    print("Testing Async Fetch (All):")
    asyncio.run(main_async(config))

    print("
Testing Async Fetch (Specific):")
    asyncio.run(main_async_specific(config))

    print("
Testing Sync Fetch (All):")
    main_sync(config)

    print("
Testing Sync Fetch (Specific):")
    main_sync_specific(config)
```

2. Run the test application:

```bash
python test_app.py
```

## Contributing

Contributions are welcome! Please create a pull request or raise an issue to discuss your ideas.

## License

This project is licensed under the MIT License.
```
```bash
./setup.py
```
```
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
```
```bash
./.gitignore
```
```
.venv/
__pycache__/
*.pyc
.env

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/latest/usage/project/#working-with-version-control
.pdm.toml
.pdm-python
.pdm-build/

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/
```
```bash
./.env
```
```
ASANA_PERSONAL_ACCESS_TOKEN=2/1207751230398966/1207751185240172:a3f5b651e61c1da05ae5b2de2a01d190
```
```bash
./.venv/bin/pip3.9
```
```
#!/Users/sumeet/projects/LLMContextProviders/.venv/bin/python
# -*- coding: utf-8 -*-
import re
import sys
from pip._internal.cli.main import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
```
```bash
./.venv/bin/Activate.ps1
```
```
<#
.Synopsis
Activate a Python virtual environment for the current PowerShell session.

.Description
Pushes the python executable for a virtual environment to the front of the
$Env:PATH environment variable and sets the prompt to signify that you are
in a Python virtual environment. Makes use of the command line switches as
well as the `pyvenv.cfg` file values present in the virtual environment.

.Parameter VenvDir
Path to the directory that contains the virtual environment to activate. The
default value for this is the parent of the directory that the Activate.ps1
script is located within.

.Parameter Prompt
The prompt prefix to display when this virtual environment is activated. By
default, this prompt is the name of the virtual environment folder (VenvDir)
surrounded by parentheses and followed by a single space (ie. '(.venv) ').

.Example
Activate.ps1
Activates the Python virtual environment that contains the Activate.ps1 script.

.Example
Activate.ps1 -Verbose
Activates the Python virtual environment that contains the Activate.ps1 script,
and shows extra information about the activation as it executes.

.Example
Activate.ps1 -VenvDir C:\Users\MyUser\Common\.venv
Activates the Python virtual environment located in the specified location.

.Example
Activate.ps1 -Prompt "MyPython"
Activates the Python virtual environment that contains the Activate.ps1 script,
and prefixes the current prompt with the specified string (surrounded in
parentheses) while the virtual environment is active.

.Notes
On Windows, it may be required to enable this Activate.ps1 script by setting the
execution policy for the user. You can do this by issuing the following PowerShell
command:

PS C:\> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

For more information on Execution Policies: 
https://go.microsoft.com/fwlink/?LinkID=135170

#>
Param(
    [Parameter(Mandatory = $false)]
    [String]
    $VenvDir,
    [Parameter(Mandatory = $false)]
    [String]
    $Prompt
)

<# Function declarations --------------------------------------------------- #>

<#
.Synopsis
Remove all shell session elements added by the Activate script, including the
addition of the virtual environment's Python executable from the beginning of
the PATH variable.

.Parameter NonDestructive
If present, do not remove this function from the global namespace for the
session.

#>
function global:deactivate ([switch]$NonDestructive) {
    # Revert to original values

    # The prior prompt:
    if (Test-Path -Path Function:_OLD_VIRTUAL_PROMPT) {
        Copy-Item -Path Function:_OLD_VIRTUAL_PROMPT -Destination Function:prompt
        Remove-Item -Path Function:_OLD_VIRTUAL_PROMPT
    }

    # The prior PYTHONHOME:
    if (Test-Path -Path Env:_OLD_VIRTUAL_PYTHONHOME) {
        Copy-Item -Path Env:_OLD_VIRTUAL_PYTHONHOME -Destination Env:PYTHONHOME
        Remove-Item -Path Env:_OLD_VIRTUAL_PYTHONHOME
    }

    # The prior PATH:
    if (Test-Path -Path Env:_OLD_VIRTUAL_PATH) {
        Copy-Item -Path Env:_OLD_VIRTUAL_PATH -Destination Env:PATH
        Remove-Item -Path Env:_OLD_VIRTUAL_PATH
    }

    # Just remove the VIRTUAL_ENV altogether:
    if (Test-Path -Path Env:VIRTUAL_ENV) {
        Remove-Item -Path env:VIRTUAL_ENV
    }

    # Just remove the _PYTHON_VENV_PROMPT_PREFIX altogether:
    if (Get-Variable -Name "_PYTHON_VENV_PROMPT_PREFIX" -ErrorAction SilentlyContinue) {
        Remove-Variable -Name _PYTHON_VENV_PROMPT_PREFIX -Scope Global -Force
    }

    # Leave deactivate function in the global namespace if requested:
    if (-not $NonDestructive) {
        Remove-Item -Path function:deactivate
    }
}

<#
.Description
Get-PyVenvConfig parses the values from the pyvenv.cfg file located in the
given folder, and returns them in a map.

For each line in the pyvenv.cfg file, if that line can be parsed into exactly
two strings separated by `=` (with any amount of whitespace surrounding the =)
then it is considered a `key = value` line. The left hand string is the key,
the right hand is the value.

If the value starts with a `'` or a `"` then the first and last character is
stripped from the value before being captured.

.Parameter ConfigDir
Path to the directory that contains the `pyvenv.cfg` file.
#>
function Get-PyVenvConfig(
    [String]
    $ConfigDir
) {
    Write-Verbose "Given ConfigDir=$ConfigDir, obtain values in pyvenv.cfg"

    # Ensure the file exists, and issue a warning if it doesn't (but still allow the function to continue).
    $pyvenvConfigPath = Join-Path -Resolve -Path $ConfigDir -ChildPath 'pyvenv.cfg' -ErrorAction Continue

    # An empty map will be returned if no config file is found.
    $pyvenvConfig = @{ }

    if ($pyvenvConfigPath) {

        Write-Verbose "File exists, parse `key = value` lines"
        $pyvenvConfigContent = Get-Content -Path $pyvenvConfigPath

        $pyvenvConfigContent | ForEach-Object {
            $keyval = $PSItem -split "\s*=\s*", 2
            if ($keyval[0] -and $keyval[1]) {
                $val = $keyval[1]

                # Remove extraneous quotations around a string value.
                if ("'""".Contains($val.Substring(0, 1))) {
                    $val = $val.Substring(1, $val.Length - 2)
                }

                $pyvenvConfig[$keyval[0]] = $val
                Write-Verbose "Adding Key: '$($keyval[0])'='$val'"
            }
        }
    }
    return $pyvenvConfig
}


<# Begin Activate script --------------------------------------------------- #>

# Determine the containing directory of this script
$VenvExecPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$VenvExecDir = Get-Item -Path $VenvExecPath

Write-Verbose "Activation script is located in path: '$VenvExecPath'"
Write-Verbose "VenvExecDir Fullname: '$($VenvExecDir.FullName)"
Write-Verbose "VenvExecDir Name: '$($VenvExecDir.Name)"

# Set values required in priority: CmdLine, ConfigFile, Default
# First, get the location of the virtual environment, it might not be
# VenvExecDir if specified on the command line.
if ($VenvDir) {
    Write-Verbose "VenvDir given as parameter, using '$VenvDir' to determine values"
}
else {
    Write-Verbose "VenvDir not given as a parameter, using parent directory name as VenvDir."
    $VenvDir = $VenvExecDir.Parent.FullName.TrimEnd("\/")
    Write-Verbose "VenvDir=$VenvDir"
}

# Next, read the `pyvenv.cfg` file to determine any required value such
# as `prompt`.
$pyvenvCfg = Get-PyVenvConfig -ConfigDir $VenvDir

# Next, set the prompt from the command line, or the config file, or
# just use the name of the virtual environment folder.
if ($Prompt) {
    Write-Verbose "Prompt specified as argument, using '$Prompt'"
}
else {
    Write-Verbose "Prompt not specified as argument to script, checking pyvenv.cfg value"
    if ($pyvenvCfg -and $pyvenvCfg['prompt']) {
        Write-Verbose "  Setting based on value in pyvenv.cfg='$($pyvenvCfg['prompt'])'"
        $Prompt = $pyvenvCfg['prompt'];
    }
    else {
        Write-Verbose "  Setting prompt based on parent's directory's name. (Is the directory name passed to venv module when creating the virutal environment)"
        Write-Verbose "  Got leaf-name of $VenvDir='$(Split-Path -Path $venvDir -Leaf)'"
        $Prompt = Split-Path -Path $venvDir -Leaf
    }
}

Write-Verbose "Prompt = '$Prompt'"
Write-Verbose "VenvDir='$VenvDir'"

# Deactivate any currently active virtual environment, but leave the
# deactivate function in place.
deactivate -nondestructive

# Now set the environment variable VIRTUAL_ENV, used by many tools to determine
# that there is an activated venv.
$env:VIRTUAL_ENV = $VenvDir

if (-not $Env:VIRTUAL_ENV_DISABLE_PROMPT) {

    Write-Verbose "Setting prompt to '$Prompt'"

    # Set the prompt to include the env name
    # Make sure _OLD_VIRTUAL_PROMPT is global
    function global:_OLD_VIRTUAL_PROMPT { "" }
    Copy-Item -Path function:prompt -Destination function:_OLD_VIRTUAL_PROMPT
    New-Variable -Name _PYTHON_VENV_PROMPT_PREFIX -Description "Python virtual environment prompt prefix" -Scope Global -Option ReadOnly -Visibility Public -Value $Prompt

    function global:prompt {
        Write-Host -NoNewline -ForegroundColor Green "($_PYTHON_VENV_PROMPT_PREFIX) "
        _OLD_VIRTUAL_PROMPT
    }
}

# Clear PYTHONHOME
if (Test-Path -Path Env:PYTHONHOME) {
    Copy-Item -Path Env:PYTHONHOME -Destination Env:_OLD_VIRTUAL_PYTHONHOME
    Remove-Item -Path Env:PYTHONHOME
}

# Add the venv to the PATH
Copy-Item -Path Env:PATH -Destination Env:_OLD_VIRTUAL_PATH
$Env:PATH = "$VenvExecDir$([System.IO.Path]::PathSeparator)$Env:PATH"
```
```bash
./.venv/bin/dotenv
```
```
#!/Users/sumeet/projects/LLMContextProviders/.venv/bin/python
# -*- coding: utf-8 -*-
import re
import sys
from dotenv.__main__ import cli
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(cli())
```
```bash
./.venv/bin/pytest
```
```
#!/Users/sumeet/projects/LLMContextProviders/.venv/bin/python
# -*- coding: utf-8 -*-
import re
import sys
from pytest import console_main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(console_main())
```
```bash
./.venv/bin/pip3
```
```
#!/Users/sumeet/projects/LLMContextProviders/.venv/bin/python
# -*- coding: utf-8 -*-
import re
import sys
from pip._internal.cli.main import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
```
```bash
./.venv/bin/activate.fish
```
```
# This file must be used with "source <venv>/bin/activate.fish" *from fish*
# (https://fishshell.com/); you cannot run it directly.

function deactivate  -d "Exit virtual environment and return to normal shell environment"
    # reset old environment variables
    if test -n "$_OLD_VIRTUAL_PATH"
        set -gx PATH $_OLD_VIRTUAL_PATH
        set -e _OLD_VIRTUAL_PATH
    end
    if test -n "$_OLD_VIRTUAL_PYTHONHOME"
        set -gx PYTHONHOME $_OLD_VIRTUAL_PYTHONHOME
        set -e _OLD_VIRTUAL_PYTHONHOME
    end

    if test -n "$_OLD_FISH_PROMPT_OVERRIDE"
        functions -e fish_prompt
        set -e _OLD_FISH_PROMPT_OVERRIDE
        functions -c _old_fish_prompt fish_prompt
        functions -e _old_fish_prompt
    end

    set -e VIRTUAL_ENV
    if test "$argv[1]" != "nondestructive"
        # Self-destruct!
        functions -e deactivate
    end
end

# Unset irrelevant variables.
deactivate nondestructive

set -gx VIRTUAL_ENV "/Users/sumeet/projects/LLMContextProviders/.venv"

set -gx _OLD_VIRTUAL_PATH $PATH
set -gx PATH "$VIRTUAL_ENV/bin" $PATH

# Unset PYTHONHOME if set.
if set -q PYTHONHOME
    set -gx _OLD_VIRTUAL_PYTHONHOME $PYTHONHOME
    set -e PYTHONHOME
end

if test -z "$VIRTUAL_ENV_DISABLE_PROMPT"
    # fish uses a function instead of an env var to generate the prompt.

    # Save the current fish_prompt function as the function _old_fish_prompt.
    functions -c fish_prompt _old_fish_prompt

    # With the original prompt function renamed, we can override with our own.
    function fish_prompt
        # Save the return status of the last command.
        set -l old_status $status

        # Output the venv prompt; color taken from the blue of the Python logo.
        printf "%s%s%s" (set_color 4B8BBE) "(.venv) " (set_color normal)

        # Restore the return status of the previous command.
        echo "exit $old_status" | .
        # Output the original/"old" prompt.
        _old_fish_prompt
    end

    set -gx _OLD_FISH_PROMPT_OVERRIDE "$VIRTUAL_ENV"
end
```
```bash
./.venv/bin/pip
```
```
#!/Users/sumeet/projects/LLMContextProviders/.venv/bin/python
# -*- coding: utf-8 -*-
import re
import sys
from pip._internal.cli.main import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
```
```bash
./.venv/bin/activate
```
```
# This file must be used with "source bin/activate" *from bash*
# you cannot run it directly

deactivate () {
    # reset old environment variables
    if [ -n "${_OLD_VIRTUAL_PATH:-}" ] ; then
        PATH="${_OLD_VIRTUAL_PATH:-}"
        export PATH
        unset _OLD_VIRTUAL_PATH
    fi
    if [ -n "${_OLD_VIRTUAL_PYTHONHOME:-}" ] ; then
        PYTHONHOME="${_OLD_VIRTUAL_PYTHONHOME:-}"
        export PYTHONHOME
        unset _OLD_VIRTUAL_PYTHONHOME
    fi

    # This should detect bash and zsh, which have a hash command that must
    # be called to get it to forget past commands.  Without forgetting
    # past commands the $PATH changes we made may not be respected
    if [ -n "${BASH:-}" -o -n "${ZSH_VERSION:-}" ] ; then
        hash -r 2> /dev/null
    fi

    if [ -n "${_OLD_VIRTUAL_PS1:-}" ] ; then
        PS1="${_OLD_VIRTUAL_PS1:-}"
        export PS1
        unset _OLD_VIRTUAL_PS1
    fi

    unset VIRTUAL_ENV
    if [ ! "${1:-}" = "nondestructive" ] ; then
    # Self destruct!
        unset -f deactivate
    fi
}

# unset irrelevant variables
deactivate nondestructive

VIRTUAL_ENV="/Users/sumeet/projects/LLMContextProviders/.venv"
export VIRTUAL_ENV

_OLD_VIRTUAL_PATH="$PATH"
PATH="$VIRTUAL_ENV/bin:$PATH"
export PATH

# unset PYTHONHOME if set
# this will fail if PYTHONHOME is set to the empty string (which is bad anyway)
# could use `if (set -u; : $PYTHONHOME) ;` in bash
if [ -n "${PYTHONHOME:-}" ] ; then
    _OLD_VIRTUAL_PYTHONHOME="${PYTHONHOME:-}"
    unset PYTHONHOME
fi

if [ -z "${VIRTUAL_ENV_DISABLE_PROMPT:-}" ] ; then
    _OLD_VIRTUAL_PS1="${PS1:-}"
    PS1="(.venv) ${PS1:-}"
    export PS1
fi

# This should detect bash and zsh, which have a hash command that must
# be called to get it to forget past commands.  Without forgetting
# past commands the $PATH changes we made may not be respected
if [ -n "${BASH:-}" -o -n "${ZSH_VERSION:-}" ] ; then
    hash -r 2> /dev/null
fi
```
```bash
./.venv/bin/py.test
```
```
#!/Users/sumeet/projects/LLMContextProviders/.venv/bin/python
# -*- coding: utf-8 -*-
import re
import sys
from pytest import console_main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(console_main())
```
```bash
./.venv/bin/activate.csh
```
```
# This file must be used with "source bin/activate.csh" *from csh*.
# You cannot run it directly.
# Created by Davide Di Blasi <davidedb@gmail.com>.
# Ported to Python 3.3 venv by Andrew Svetlov <andrew.svetlov@gmail.com>

alias deactivate 'test $?_OLD_VIRTUAL_PATH != 0 && setenv PATH "$_OLD_VIRTUAL_PATH" && unset _OLD_VIRTUAL_PATH; rehash; test $?_OLD_VIRTUAL_PROMPT != 0 && set prompt="$_OLD_VIRTUAL_PROMPT" && unset _OLD_VIRTUAL_PROMPT; unsetenv VIRTUAL_ENV; test "\!:*" != "nondestructive" && unalias deactivate'

# Unset irrelevant variables.
deactivate nondestructive

setenv VIRTUAL_ENV "/Users/sumeet/projects/LLMContextProviders/.venv"

set _OLD_VIRTUAL_PATH="$PATH"
setenv PATH "$VIRTUAL_ENV/bin:$PATH"


set _OLD_VIRTUAL_PROMPT="$prompt"

if (! "$?VIRTUAL_ENV_DISABLE_PROMPT") then
    set prompt = "(.venv) $prompt"
endif

alias pydoc python -m pydoc

rehash
```
```bash
./.venv/pyvenv.cfg
```
```
home = /Library/Developer/CommandLineTools/usr/bin
include-system-site-packages = false
version = 3.9.6
```
```bash
./.venv/.gitignore
```
```
*
```
```bash
./.venv/lib/python3.9/site-packages/packaging/tags.py
```
```
# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import logging
import platform
import re
import struct
import subprocess
import sys
import sysconfig
from importlib.machinery import EXTENSION_SUFFIXES
from typing import (
    Iterable,
    Iterator,
    Sequence,
    Tuple,
    cast,
)

from . import _manylinux, _musllinux

logger = logging.getLogger(__name__)

PythonVersion = Sequence[int]
MacVersion = Tuple[int, int]

INTERPRETER_SHORT_NAMES: dict[str, str] = {
    "python": "py",  # Generic.
    "cpython": "cp",
    "pypy": "pp",
    "ironpython": "ip",
    "jython": "jy",
}


_32_BIT_INTERPRETER = struct.calcsize("P") == 4


class Tag:
    """
    A representation of the tag triple for a wheel.

    Instances are considered immutable and thus are hashable. Equality checking
    is also supported.
    """

    __slots__ = ["_interpreter", "_abi", "_platform", "_hash"]

    def __init__(self, interpreter: str, abi: str, platform: str) -> None:
        self._interpreter = interpreter.lower()
        self._abi = abi.lower()
        self._platform = platform.lower()
        # The __hash__ of every single element in a Set[Tag] will be evaluated each time
        # that a set calls its `.disjoint()` method, which may be called hundreds of
        # times when scanning a page of links for packages with tags matching that
        # Set[Tag]. Pre-computing the value here produces significant speedups for
        # downstream consumers.
        self._hash = hash((self._interpreter, self._abi, self._platform))

    @property
    def interpreter(self) -> str:
        return self._interpreter

    @property
    def abi(self) -> str:
        return self._abi

    @property
    def platform(self) -> str:
        return self._platform

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tag):
            return NotImplemented

        return (
            (self._hash == other._hash)  # Short-circuit ASAP for perf reasons.
            and (self._platform == other._platform)
            and (self._abi == other._abi)
            and (self._interpreter == other._interpreter)
        )

    def __hash__(self) -> int:
        return self._hash

    def __str__(self) -> str:
        return f"{self._interpreter}-{self._abi}-{self._platform}"

    def __repr__(self) -> str:
        return f"<{self} @ {id(self)}>"


def parse_tag(tag: str) -> frozenset[Tag]:
    """
    Parses the provided tag (e.g. `py3-none-any`) into a frozenset of Tag instances.

    Returning a set is required due to the possibility that the tag is a
    compressed tag set.
    """
    tags = set()
    interpreters, abis, platforms = tag.split("-")
    for interpreter in interpreters.split("."):
        for abi in abis.split("."):
            for platform_ in platforms.split("."):
                tags.add(Tag(interpreter, abi, platform_))
    return frozenset(tags)


def _get_config_var(name: str, warn: bool = False) -> int | str | None:
    value: int | str | None = sysconfig.get_config_var(name)
    if value is None and warn:
        logger.debug(
            "Config variable '%s' is unset, Python ABI tag may be incorrect", name
        )
    return value


def _normalize_string(string: str) -> str:
    return string.replace(".", "_").replace("-", "_").replace(" ", "_")


def _is_threaded_cpython(abis: list[str]) -> bool:
    """
    Determine if the ABI corresponds to a threaded (`--disable-gil`) build.

    The threaded builds are indicated by a "t" in the abiflags.
    """
    if len(abis) == 0:
        return False
    # expect e.g., cp313
    m = re.match(r"cp\d+(.*)", abis[0])
    if not m:
        return False
    abiflags = m.group(1)
    return "t" in abiflags


def _abi3_applies(python_version: PythonVersion, threading: bool) -> bool:
    """
    Determine if the Python version supports abi3.

    PEP 384 was first implemented in Python 3.2. The threaded (`--disable-gil`)
    builds do not support abi3.
    """
    return len(python_version) > 1 and tuple(python_version) >= (3, 2) and not threading


def _cpython_abis(py_version: PythonVersion, warn: bool = False) -> list[str]:
    py_version = tuple(py_version)  # To allow for version comparison.
    abis = []
    version = _version_nodot(py_version[:2])
    threading = debug = pymalloc = ucs4 = ""
    with_debug = _get_config_var("Py_DEBUG", warn)
    has_refcount = hasattr(sys, "gettotalrefcount")
    # Windows doesn't set Py_DEBUG, so checking for support of debug-compiled
    # extension modules is the best option.
    # https://github.com/pypa/pip/issues/3383#issuecomment-173267692
    has_ext = "_d.pyd" in EXTENSION_SUFFIXES
    if with_debug or (with_debug is None and (has_refcount or has_ext)):
        debug = "d"
    if py_version >= (3, 13) and _get_config_var("Py_GIL_DISABLED", warn):
        threading = "t"
    if py_version < (3, 8):
        with_pymalloc = _get_config_var("WITH_PYMALLOC", warn)
        if with_pymalloc or with_pymalloc is None:
            pymalloc = "m"
        if py_version < (3, 3):
            unicode_size = _get_config_var("Py_UNICODE_SIZE", warn)
            if unicode_size == 4 or (
                unicode_size is None and sys.maxunicode == 0x10FFFF
            ):
                ucs4 = "u"
    elif debug:
        # Debug builds can also load "normal" extension modules.
        # We can also assume no UCS-4 or pymalloc requirement.
        abis.append(f"cp{version}{threading}")
    abis.insert(0, f"cp{version}{threading}{debug}{pymalloc}{ucs4}")
    return abis


def cpython_tags(
    python_version: PythonVersion | None = None,
    abis: Iterable[str] | None = None,
    platforms: Iterable[str] | None = None,
    *,
    warn: bool = False,
) -> Iterator[Tag]:
    """
    Yields the tags for a CPython interpreter.

    The tags consist of:
    - cp<python_version>-<abi>-<platform>
    - cp<python_version>-abi3-<platform>
    - cp<python_version>-none-<platform>
    - cp<less than python_version>-abi3-<platform>  # Older Python versions down to 3.2.

    If python_version only specifies a major version then user-provided ABIs and
    the 'none' ABItag will be used.

    If 'abi3' or 'none' are specified in 'abis' then they will be yielded at
    their normal position and not at the beginning.
    """
    if not python_version:
        python_version = sys.version_info[:2]

    interpreter = f"cp{_version_nodot(python_version[:2])}"

    if abis is None:
        if len(python_version) > 1:
            abis = _cpython_abis(python_version, warn)
        else:
            abis = []
    abis = list(abis)
    # 'abi3' and 'none' are explicitly handled later.
    for explicit_abi in ("abi3", "none"):
        try:
            abis.remove(explicit_abi)
        except ValueError:
            pass

    platforms = list(platforms or platform_tags())
    for abi in abis:
        for platform_ in platforms:
            yield Tag(interpreter, abi, platform_)

    threading = _is_threaded_cpython(abis)
    use_abi3 = _abi3_applies(python_version, threading)
    if use_abi3:
        yield from (Tag(interpreter, "abi3", platform_) for platform_ in platforms)
    yield from (Tag(interpreter, "none", platform_) for platform_ in platforms)

    if use_abi3:
        for minor_version in range(python_version[1] - 1, 1, -1):
            for platform_ in platforms:
                interpreter = "cp{version}".format(
                    version=_version_nodot((python_version[0], minor_version))
                )
                yield Tag(interpreter, "abi3", platform_)


def _generic_abi() -> list[str]:
    """
    Return the ABI tag based on EXT_SUFFIX.
    """
    # The following are examples of `EXT_SUFFIX`.
    # We want to keep the parts which are related to the ABI and remove the
    # parts which are related to the platform:
    # - linux:   '.cpython-310-x86_64-linux-gnu.so' => cp310
    # - mac:     '.cpython-310-darwin.so'           => cp310
    # - win:     '.cp310-win_amd64.pyd'             => cp310
    # - win:     '.pyd'                             => cp37 (uses _cpython_abis())
    # - pypy:    '.pypy38-pp73-x86_64-linux-gnu.so' => pypy38_pp73
    # - graalpy: '.graalpy-38-native-x86_64-darwin.dylib'
    #                                               => graalpy_38_native

    ext_suffix = _get_config_var("EXT_SUFFIX", warn=True)
    if not isinstance(ext_suffix, str) or ext_suffix[0] != ".":
        raise SystemError("invalid sysconfig.get_config_var('EXT_SUFFIX')")
    parts = ext_suffix.split(".")
    if len(parts) < 3:
        # CPython3.7 and earlier uses ".pyd" on Windows.
        return _cpython_abis(sys.version_info[:2])
    soabi = parts[1]
    if soabi.startswith("cpython"):
        # non-windows
        abi = "cp" + soabi.split("-")[1]
    elif soabi.startswith("cp"):
        # windows
        abi = soabi.split("-")[0]
    elif soabi.startswith("pypy"):
        abi = "-".join(soabi.split("-")[:2])
    elif soabi.startswith("graalpy"):
        abi = "-".join(soabi.split("-")[:3])
    elif soabi:
        # pyston, ironpython, others?
        abi = soabi
    else:
        return []
    return [_normalize_string(abi)]


def generic_tags(
    interpreter: str | None = None,
    abis: Iterable[str] | None = None,
    platforms: Iterable[str] | None = None,
    *,
    warn: bool = False,
) -> Iterator[Tag]:
    """
    Yields the tags for a generic interpreter.

    The tags consist of:
    - <interpreter>-<abi>-<platform>

    The "none" ABI will be added if it was not explicitly provided.
    """
    if not interpreter:
        interp_name = interpreter_name()
        interp_version = interpreter_version(warn=warn)
        interpreter = "".join([interp_name, interp_version])
    if abis is None:
        abis = _generic_abi()
    else:
        abis = list(abis)
    platforms = list(platforms or platform_tags())
    if "none" not in abis:
        abis.append("none")
    for abi in abis:
        for platform_ in platforms:
            yield Tag(interpreter, abi, platform_)


def _py_interpreter_range(py_version: PythonVersion) -> Iterator[str]:
    """
    Yields Python versions in descending order.

    After the latest version, the major-only version will be yielded, and then
    all previous versions of that major version.
    """
    if len(py_version) > 1:
        yield f"py{_version_nodot(py_version[:2])}"
    yield f"py{py_version[0]}"
    if len(py_version) > 1:
        for minor in range(py_version[1] - 1, -1, -1):
            yield f"py{_version_nodot((py_version[0], minor))}"


def compatible_tags(
    python_version: PythonVersion | None = None,
    interpreter: str | None = None,
    platforms: Iterable[str] | None = None,
) -> Iterator[Tag]:
    """
    Yields the sequence of tags that are compatible with a specific version of Python.

    The tags consist of:
    - py*-none-<platform>
    - <interpreter>-none-any  # ... if `interpreter` is provided.
    - py*-none-any
    """
    if not python_version:
        python_version = sys.version_info[:2]
    platforms = list(platforms or platform_tags())
    for version in _py_interpreter_range(python_version):
        for platform_ in platforms:
            yield Tag(version, "none", platform_)
    if interpreter:
        yield Tag(interpreter, "none", "any")
    for version in _py_interpreter_range(python_version):
        yield Tag(version, "none", "any")


def _mac_arch(arch: str, is_32bit: bool = _32_BIT_INTERPRETER) -> str:
    if not is_32bit:
        return arch

    if arch.startswith("ppc"):
        return "ppc"

    return "i386"


def _mac_binary_formats(version: MacVersion, cpu_arch: str) -> list[str]:
    formats = [cpu_arch]
    if cpu_arch == "x86_64":
        if version < (10, 4):
            return []
        formats.extend(["intel", "fat64", "fat32"])

    elif cpu_arch == "i386":
        if version < (10, 4):
            return []
        formats.extend(["intel", "fat32", "fat"])

    elif cpu_arch == "ppc64":
        # TODO: Need to care about 32-bit PPC for ppc64 through 10.2?
        if version > (10, 5) or version < (10, 4):
            return []
        formats.append("fat64")

    elif cpu_arch == "ppc":
        if version > (10, 6):
            return []
        formats.extend(["fat32", "fat"])

    if cpu_arch in {"arm64", "x86_64"}:
        formats.append("universal2")

    if cpu_arch in {"x86_64", "i386", "ppc64", "ppc", "intel"}:
        formats.append("universal")

    return formats


def mac_platforms(
    version: MacVersion | None = None, arch: str | None = None
) -> Iterator[str]:
    """
    Yields the platform tags for a macOS system.

    The `version` parameter is a two-item tuple specifying the macOS version to
    generate platform tags for. The `arch` parameter is the CPU architecture to
    generate platform tags for. Both parameters default to the appropriate value
    for the current system.
    """
    version_str, _, cpu_arch = platform.mac_ver()
    if version is None:
        version = cast("MacVersion", tuple(map(int, version_str.split(".")[:2])))
        if version == (10, 16):
            # When built against an older macOS SDK, Python will report macOS 10.16
            # instead of the real version.
            version_str = subprocess.run(
                [
                    sys.executable,
                    "-sS",
                    "-c",
                    "import platform; print(platform.mac_ver()[0])",
                ],
                check=True,
                env={"SYSTEM_VERSION_COMPAT": "0"},
                stdout=subprocess.PIPE,
                text=True,
            ).stdout
            version = cast("MacVersion", tuple(map(int, version_str.split(".")[:2])))
    else:
        version = version
    if arch is None:
        arch = _mac_arch(cpu_arch)
    else:
        arch = arch

    if (10, 0) <= version and version < (11, 0):
        # Prior to Mac OS 11, each yearly release of Mac OS bumped the
        # "minor" version number.  The major version was always 10.
        for minor_version in range(version[1], -1, -1):
            compat_version = 10, minor_version
            binary_formats = _mac_binary_formats(compat_version, arch)
            for binary_format in binary_formats:
                yield "macosx_{major}_{minor}_{binary_format}".format(
                    major=10, minor=minor_version, binary_format=binary_format
                )

    if version >= (11, 0):
        # Starting with Mac OS 11, each yearly release bumps the major version
        # number.   The minor versions are now the midyear updates.
        for major_version in range(version[0], 10, -1):
            compat_version = major_version, 0
            binary_formats = _mac_binary_formats(compat_version, arch)
            for binary_format in binary_formats:
                yield "macosx_{major}_{minor}_{binary_format}".format(
                    major=major_version, minor=0, binary_format=binary_format
                )

    if version >= (11, 0):
        # Mac OS 11 on x86_64 is compatible with binaries from previous releases.
        # Arm64 support was introduced in 11.0, so no Arm binaries from previous
        # releases exist.
        #
        # However, the "universal2" binary format can have a
        # macOS version earlier than 11.0 when the x86_64 part of the binary supports
        # that version of macOS.
        if arch == "x86_64":
            for minor_version in range(16, 3, -1):
                compat_version = 10, minor_version
                binary_formats = _mac_binary_formats(compat_version, arch)
                for binary_format in binary_formats:
                    yield "macosx_{major}_{minor}_{binary_format}".format(
                        major=compat_version[0],
                        minor=compat_version[1],
                        binary_format=binary_format,
                    )
        else:
            for minor_version in range(16, 3, -1):
                compat_version = 10, minor_version
                binary_format = "universal2"
                yield "macosx_{major}_{minor}_{binary_format}".format(
                    major=compat_version[0],
                    minor=compat_version[1],
                    binary_format=binary_format,
                )


def _linux_platforms(is_32bit: bool = _32_BIT_INTERPRETER) -> Iterator[str]:
    linux = _normalize_string(sysconfig.get_platform())
    if not linux.startswith("linux_"):
        # we should never be here, just yield the sysconfig one and return
        yield linux
        return
    if is_32bit:
        if linux == "linux_x86_64":
            linux = "linux_i686"
        elif linux == "linux_aarch64":
            linux = "linux_armv8l"
    _, arch = linux.split("_", 1)
    archs = {"armv8l": ["armv8l", "armv7l"]}.get(arch, [arch])
    yield from _manylinux.platform_tags(archs)
    yield from _musllinux.platform_tags(archs)
    for arch in archs:
        yield f"linux_{arch}"


def _generic_platforms() -> Iterator[str]:
    yield _normalize_string(sysconfig.get_platform())


def platform_tags() -> Iterator[str]:
    """
    Provides the platform tags for this installation.
    """
    if platform.system() == "Darwin":
        return mac_platforms()
    elif platform.system() == "Linux":
        return _linux_platforms()
    else:
        return _generic_platforms()


def interpreter_name() -> str:
    """
    Returns the name of the running interpreter.

    Some implementations have a reserved, two-letter abbreviation which will
    be returned when appropriate.
    """
    name = sys.implementation.name
    return INTERPRETER_SHORT_NAMES.get(name) or name


def interpreter_version(*, warn: bool = False) -> str:
    """
    Returns the version of the running interpreter.
    """
    version = _get_config_var("py_version_nodot", warn=warn)
    if version:
        version = str(version)
    else:
        version = _version_nodot(sys.version_info[:2])
    return version


def _version_nodot(version: PythonVersion) -> str:
    return "".join(map(str, version))


def sys_tags(*, warn: bool = False) -> Iterator[Tag]:
    """
    Returns the sequence of tag triples for the running interpreter.

    The order of the sequence corresponds to priority order for the
    interpreter, from most to least important.
    """

    interp_name = interpreter_name()
    if interp_name == "cp":
        yield from cpython_tags(warn=warn)
    else:
        yield from generic_tags()

    if interp_name == "pp":
        interp = "pp3"
    elif interp_name == "cp":
        interp = "cp" + interpreter_version(warn=warn)
    else:
        interp = None
    yield from compatible_tags(interpreter=interp)
```
```bash
./.venv/lib/python3.9/site-packages/packaging/_musllinux.py
```
```
"""PEP 656 support.

This module implements logic to detect if the currently running Python is
linked against musl, and what musl version is used.
"""

from __future__ import annotations

import functools
import re
import subprocess
import sys
from typing import Iterator, NamedTuple, Sequence

from ._elffile import ELFFile


class _MuslVersion(NamedTuple):
    major: int
    minor: int


def _parse_musl_version(output: str) -> _MuslVersion | None:
    lines = [n for n in (n.strip() for n in output.splitlines()) if n]
    if len(lines) < 2 or lines[0][:4] != "musl":
        return None
    m = re.match(r"Version (\d+)\.(\d+)", lines[1])
    if not m:
        return None
    return _MuslVersion(major=int(m.group(1)), minor=int(m.group(2)))


@functools.lru_cache
def _get_musl_version(executable: str) -> _MuslVersion | None:
    """Detect currently-running musl runtime version.

    This is done by checking the specified executable's dynamic linking
    information, and invoking the loader to parse its output for a version
    string. If the loader is musl, the output would be something like::

        musl libc (x86_64)
        Version 1.2.2
        Dynamic Program Loader
    """
    try:
        with open(executable, "rb") as f:
            ld = ELFFile(f).interpreter
    except (OSError, TypeError, ValueError):
        return None
    if ld is None or "musl" not in ld:
        return None
    proc = subprocess.run([ld], stderr=subprocess.PIPE, text=True)
    return _parse_musl_version(proc.stderr)


def platform_tags(archs: Sequence[str]) -> Iterator[str]:
    """Generate musllinux tags compatible to the current platform.

    :param archs: Sequence of compatible architectures.
        The first one shall be the closest to the actual architecture and be the part of
        platform tag after the ``linux_`` prefix, e.g. ``x86_64``.
        The ``linux_`` prefix is assumed as a prerequisite for the current platform to
        be musllinux-compatible.

    :returns: An iterator of compatible musllinux tags.
    """
    sys_musl = _get_musl_version(sys.executable)
    if sys_musl is None:  # Python not dynamically linked against musl.
        return
    for arch in archs:
        for minor in range(sys_musl.minor, -1, -1):
            yield f"musllinux_{sys_musl.major}_{minor}_{arch}"


if __name__ == "__main__":  # pragma: no cover
    import sysconfig

    plat = sysconfig.get_platform()
    assert plat.startswith("linux-"), "not linux"

    print("plat:", plat)
    print("musl:", _get_musl_version(sys.executable))
    print("tags:", end=" ")
    for t in platform_tags(re.sub(r"[.-]", "_", plat.split("-", 1)[-1])):
        print(t, end="
      ")
```
```bash
./.venv/lib/python3.9/site-packages/packaging/metadata.py
```
```
from __future__ import annotations

import email.feedparser
import email.header
import email.message
import email.parser
import email.policy
import typing
from typing import (
    Any,
    Callable,
    Generic,
    Literal,
    TypedDict,
    cast,
)

from . import requirements, specifiers, utils
from . import version as version_module

T = typing.TypeVar("T")


try:
    ExceptionGroup
except NameError:  # pragma: no cover

    class ExceptionGroup(Exception):
        """A minimal implementation of :external:exc:`ExceptionGroup` from Python 3.11.

        If :external:exc:`ExceptionGroup` is already defined by Python itself,
        that version is used instead.
        """

        message: str
        exceptions: list[Exception]

        def __init__(self, message: str, exceptions: list[Exception]) -> None:
            self.message = message
            self.exceptions = exceptions

        def __repr__(self) -> str:
            return f"{self.__class__.__name__}({self.message!r}, {self.exceptions!r})"

else:  # pragma: no cover
    ExceptionGroup = ExceptionGroup


class InvalidMetadata(ValueError):
    """A metadata field contains invalid data."""

    field: str
    """The name of the field that contains invalid data."""

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        super().__init__(message)


# The RawMetadata class attempts to make as few assumptions about the underlying
# serialization formats as possible. The idea is that as long as a serialization
# formats offer some very basic primitives in *some* way then we can support
# serializing to and from that format.
class RawMetadata(TypedDict, total=False):
    """A dictionary of raw core metadata.

    Each field in core metadata maps to a key of this dictionary (when data is
    provided). The key is lower-case and underscores are used instead of dashes
    compared to the equivalent core metadata field. Any core metadata field that
    can be specified multiple times or can hold multiple values in a single
    field have a key with a plural name. See :class:`Metadata` whose attributes
    match the keys of this dictionary.

    Core metadata fields that can be specified multiple times are stored as a
    list or dict depending on which is appropriate for the field. Any fields
    which hold multiple values in a single field are stored as a list.

    """

    # Metadata 1.0 - PEP 241
    metadata_version: str
    name: str
    version: str
    platforms: list[str]
    summary: str
    description: str
    keywords: list[str]
    home_page: str
    author: str
    author_email: str
    license: str

    # Metadata 1.1 - PEP 314
    supported_platforms: list[str]
    download_url: str
    classifiers: list[str]
    requires: list[str]
    provides: list[str]
    obsoletes: list[str]

    # Metadata 1.2 - PEP 345
    maintainer: str
    maintainer_email: str
    requires_dist: list[str]
    provides_dist: list[str]
    obsoletes_dist: list[str]
    requires_python: str
    requires_external: list[str]
    project_urls: dict[str, str]

    # Metadata 2.0
    # PEP 426 attempted to completely revamp the metadata format
    # but got stuck without ever being able to build consensus on
    # it and ultimately ended up withdrawn.
    #
    # However, a number of tools had started emitting METADATA with
    # `2.0` Metadata-Version, so for historical reasons, this version
    # was skipped.

    # Metadata 2.1 - PEP 566
    description_content_type: str
    provides_extra: list[str]

    # Metadata 2.2 - PEP 643
    dynamic: list[str]

    # Metadata 2.3 - PEP 685
    # No new fields were added in PEP 685, just some edge case were
    # tightened up to provide better interoptability.


_STRING_FIELDS = {
    "author",
    "author_email",
    "description",
    "description_content_type",
    "download_url",
    "home_page",
    "license",
    "maintainer",
    "maintainer_email",
    "metadata_version",
    "name",
    "requires_python",
    "summary",
    "version",
}

_LIST_FIELDS = {
    "classifiers",
    "dynamic",
    "obsoletes",
    "obsoletes_dist",
    "platforms",
    "provides",
    "provides_dist",
    "provides_extra",
    "requires",
    "requires_dist",
    "requires_external",
    "supported_platforms",
}

_DICT_FIELDS = {
    "project_urls",
}


def _parse_keywords(data: str) -> list[str]:
    """Split a string of comma-separate keyboards into a list of keywords."""
    return [k.strip() for k in data.split(",")]


def _parse_project_urls(data: list[str]) -> dict[str, str]:
    """Parse a list of label/URL string pairings separated by a comma."""
    urls = {}
    for pair in data:
        # Our logic is slightly tricky here as we want to try and do
        # *something* reasonable with malformed data.
        #
        # The main thing that we have to worry about, is data that does
        # not have a ',' at all to split the label from the Value. There
        # isn't a singular right answer here, and we will fail validation
        # later on (if the caller is validating) so it doesn't *really*
        # matter, but since the missing value has to be an empty str
        # and our return value is dict[str, str], if we let the key
        # be the missing value, then they'd have multiple '' values that
        # overwrite each other in a accumulating dict.
        #
        # The other potentional issue is that it's possible to have the
        # same label multiple times in the metadata, with no solid "right"
        # answer with what to do in that case. As such, we'll do the only
        # thing we can, which is treat the field as unparseable and add it
        # to our list of unparsed fields.
        parts = [p.strip() for p in pair.split(",", 1)]
        parts.extend([""] * (max(0, 2 - len(parts))))  # Ensure 2 items

        # TODO: The spec doesn't say anything about if the keys should be
        #       considered case sensitive or not... logically they should
        #       be case-preserving and case-insensitive, but doing that
        #       would open up more cases where we might have duplicate
        #       entries.
        label, url = parts
        if label in urls:
            # The label already exists in our set of urls, so this field
            # is unparseable, and we can just add the whole thing to our
            # unparseable data and stop processing it.
            raise KeyError("duplicate labels in project urls")
        urls[label] = url

    return urls


def _get_payload(msg: email.message.Message, source: bytes | str) -> str:
    """Get the body of the message."""
    # If our source is a str, then our caller has managed encodings for us,
    # and we don't need to deal with it.
    if isinstance(source, str):
        payload: str = msg.get_payload()
        return payload
    # If our source is a bytes, then we're managing the encoding and we need
    # to deal with it.
    else:
        bpayload: bytes = msg.get_payload(decode=True)
        try:
            return bpayload.decode("utf8", "strict")
        except UnicodeDecodeError:
            raise ValueError("payload in an invalid encoding")


# The various parse_FORMAT functions here are intended to be as lenient as
# possible in their parsing, while still returning a correctly typed
# RawMetadata.
#
# To aid in this, we also generally want to do as little touching of the
# data as possible, except where there are possibly some historic holdovers
# that make valid data awkward to work with.
#
# While this is a lower level, intermediate format than our ``Metadata``
# class, some light touch ups can make a massive difference in usability.

# Map METADATA fields to RawMetadata.
_EMAIL_TO_RAW_MAPPING = {
    "author": "author",
    "author-email": "author_email",
    "classifier": "classifiers",
    "description": "description",
    "description-content-type": "description_content_type",
    "download-url": "download_url",
    "dynamic": "dynamic",
    "home-page": "home_page",
    "keywords": "keywords",
    "license": "license",
    "maintainer": "maintainer",
    "maintainer-email": "maintainer_email",
    "metadata-version": "metadata_version",
    "name": "name",
    "obsoletes": "obsoletes",
    "obsoletes-dist": "obsoletes_dist",
    "platform": "platforms",
    "project-url": "project_urls",
    "provides": "provides",
    "provides-dist": "provides_dist",
    "provides-extra": "provides_extra",
    "requires": "requires",
    "requires-dist": "requires_dist",
    "requires-external": "requires_external",
    "requires-python": "requires_python",
    "summary": "summary",
    "supported-platform": "supported_platforms",
    "version": "version",
}
_RAW_TO_EMAIL_MAPPING = {raw: email for email, raw in _EMAIL_TO_RAW_MAPPING.items()}


def parse_email(data: bytes | str) -> tuple[RawMetadata, dict[str, list[str]]]:
    """Parse a distribution's metadata stored as email headers (e.g. from ``METADATA``).

    This function returns a two-item tuple of dicts. The first dict is of
    recognized fields from the core metadata specification. Fields that can be
    parsed and translated into Python's built-in types are converted
    appropriately. All other fields are left as-is. Fields that are allowed to
    appear multiple times are stored as lists.

    The second dict contains all other fields from the metadata. This includes
    any unrecognized fields. It also includes any fields which are expected to
    be parsed into a built-in type but were not formatted appropriately. Finally,
    any fields that are expected to appear only once but are repeated are
    included in this dict.

    """
    raw: dict[str, str | list[str] | dict[str, str]] = {}
    unparsed: dict[str, list[str]] = {}

    if isinstance(data, str):
        parsed = email.parser.Parser(policy=email.policy.compat32).parsestr(data)
    else:
        parsed = email.parser.BytesParser(policy=email.policy.compat32).parsebytes(data)

    # We have to wrap parsed.keys() in a set, because in the case of multiple
    # values for a key (a list), the key will appear multiple times in the
    # list of keys, but we're avoiding that by using get_all().
    for name in frozenset(parsed.keys()):
        # Header names in RFC are case insensitive, so we'll normalize to all
        # lower case to make comparisons easier.
        name = name.lower()

        # We use get_all() here, even for fields that aren't multiple use,
        # because otherwise someone could have e.g. two Name fields, and we
        # would just silently ignore it rather than doing something about it.
        headers = parsed.get_all(name) or []

        # The way the email module works when parsing bytes is that it
        # unconditionally decodes the bytes as ascii using the surrogateescape
        # handler. When you pull that data back out (such as with get_all() ),
        # it looks to see if the str has any surrogate escapes, and if it does
        # it wraps it in a Header object instead of returning the string.
        #
        # As such, we'll look for those Header objects, and fix up the encoding.
        value = []
        # Flag if we have run into any issues processing the headers, thus
        # signalling that the data belongs in 'unparsed'.
        valid_encoding = True
        for h in headers:
            # It's unclear if this can return more types than just a Header or
            # a str, so we'll just assert here to make sure.
            assert isinstance(h, (email.header.Header, str))

            # If it's a header object, we need to do our little dance to get
            # the real data out of it. In cases where there is invalid data
            # we're going to end up with mojibake, but there's no obvious, good
            # way around that without reimplementing parts of the Header object
            # ourselves.
            #
            # That should be fine since, if mojibacked happens, this key is
            # going into the unparsed dict anyways.
            if isinstance(h, email.header.Header):
                # The Header object stores it's data as chunks, and each chunk
                # can be independently encoded, so we'll need to check each
                # of them.
                chunks: list[tuple[bytes, str | None]] = []
                for bin, encoding in email.header.decode_header(h):
                    try:
                        bin.decode("utf8", "strict")
                    except UnicodeDecodeError:
                        # Enable mojibake.
                        encoding = "latin1"
                        valid_encoding = False
                    else:
                        encoding = "utf8"
                    chunks.append((bin, encoding))

                # Turn our chunks back into a Header object, then let that
                # Header object do the right thing to turn them into a
                # string for us.
                value.append(str(email.header.make_header(chunks)))
            # This is already a string, so just add it.
            else:
                value.append(h)

        # We've processed all of our values to get them into a list of str,
        # but we may have mojibake data, in which case this is an unparsed
        # field.
        if not valid_encoding:
            unparsed[name] = value
            continue

        raw_name = _EMAIL_TO_RAW_MAPPING.get(name)
        if raw_name is None:
            # This is a bit of a weird situation, we've encountered a key that
            # we don't know what it means, so we don't know whether it's meant
            # to be a list or not.
            #
            # Since we can't really tell one way or another, we'll just leave it
            # as a list, even though it may be a single item list, because that's
            # what makes the most sense for email headers.
            unparsed[name] = value
            continue

        # If this is one of our string fields, then we'll check to see if our
        # value is a list of a single item. If it is then we'll assume that
        # it was emitted as a single string, and unwrap the str from inside
        # the list.
        #
        # If it's any other kind of data, then we haven't the faintest clue
        # what we should parse it as, and we have to just add it to our list
        # of unparsed stuff.
        if raw_name in _STRING_FIELDS and len(value) == 1:
            raw[raw_name] = value[0]
        # If this is one of our list of string fields, then we can just assign
        # the value, since email *only* has strings, and our get_all() call
        # above ensures that this is a list.
        elif raw_name in _LIST_FIELDS:
            raw[raw_name] = value
        # Special Case: Keywords
        # The keywords field is implemented in the metadata spec as a str,
        # but it conceptually is a list of strings, and is serialized using
        # ", ".join(keywords), so we'll do some light data massaging to turn
        # this into what it logically is.
        elif raw_name == "keywords" and len(value) == 1:
            raw[raw_name] = _parse_keywords(value[0])
        # Special Case: Project-URL
        # The project urls is implemented in the metadata spec as a list of
        # specially-formatted strings that represent a key and a value, which
        # is fundamentally a mapping, however the email format doesn't support
        # mappings in a sane way, so it was crammed into a list of strings
        # instead.
        #
        # We will do a little light data massaging to turn this into a map as
        # it logically should be.
        elif raw_name == "project_urls":
            try:
                raw[raw_name] = _parse_project_urls(value)
            except KeyError:
                unparsed[name] = value
        # Nothing that we've done has managed to parse this, so it'll just
        # throw it in our unparseable data and move on.
        else:
            unparsed[name] = value

    # We need to support getting the Description from the message payload in
    # addition to getting it from the the headers. This does mean, though, there
    # is the possibility of it being set both ways, in which case we put both
    # in 'unparsed' since we don't know which is right.
    try:
        payload = _get_payload(parsed, data)
    except ValueError:
        unparsed.setdefault("description", []).append(
            parsed.get_payload(decode=isinstance(data, bytes))
        )
    else:
        if payload:
            # Check to see if we've already got a description, if so then both
            # it, and this body move to unparseable.
            if "description" in raw:
                description_header = cast(str, raw.pop("description"))
                unparsed.setdefault("description", []).extend(
                    [description_header, payload]
                )
            elif "description" in unparsed:
                unparsed["description"].append(payload)
            else:
                raw["description"] = payload

    # We need to cast our `raw` to a metadata, because a TypedDict only support
    # literal key names, but we're computing our key names on purpose, but the
    # way this function is implemented, our `TypedDict` can only have valid key
    # names.
    return cast(RawMetadata, raw), unparsed


_NOT_FOUND = object()


# Keep the two values in sync.
_VALID_METADATA_VERSIONS = ["1.0", "1.1", "1.2", "2.1", "2.2", "2.3"]
_MetadataVersion = Literal["1.0", "1.1", "1.2", "2.1", "2.2", "2.3"]

_REQUIRED_ATTRS = frozenset(["metadata_version", "name", "version"])


class _Validator(Generic[T]):
    """Validate a metadata field.

    All _process_*() methods correspond to a core metadata field. The method is
    called with the field's raw value. If the raw value is valid it is returned
    in its "enriched" form (e.g. ``version.Version`` for the ``Version`` field).
    If the raw value is invalid, :exc:`InvalidMetadata` is raised (with a cause
    as appropriate).
    """

    name: str
    raw_name: str
    added: _MetadataVersion

    def __init__(
        self,
        *,
        added: _MetadataVersion = "1.0",
    ) -> None:
        self.added = added

    def __set_name__(self, _owner: Metadata, name: str) -> None:
        self.name = name
        self.raw_name = _RAW_TO_EMAIL_MAPPING[name]

    def __get__(self, instance: Metadata, _owner: type[Metadata]) -> T:
        # With Python 3.8, the caching can be replaced with functools.cached_property().
        # No need to check the cache as attribute lookup will resolve into the
        # instance's __dict__ before __get__ is called.
        cache = instance.__dict__
        value = instance._raw.get(self.name)

        # To make the _process_* methods easier, we'll check if the value is None
        # and if this field is NOT a required attribute, and if both of those
        # things are true, we'll skip the the converter. This will mean that the
        # converters never have to deal with the None union.
        if self.name in _REQUIRED_ATTRS or value is not None:
            try:
                converter: Callable[[Any], T] = getattr(self, f"_process_{self.name}")
            except AttributeError:
                pass
            else:
                value = converter(value)

        cache[self.name] = value
        try:
            del instance._raw[self.name]  # type: ignore[misc]
        except KeyError:
            pass

        return cast(T, value)

    def _invalid_metadata(
        self, msg: str, cause: Exception | None = None
    ) -> InvalidMetadata:
        exc = InvalidMetadata(
            self.raw_name, msg.format_map({"field": repr(self.raw_name)})
        )
        exc.__cause__ = cause
        return exc

    def _process_metadata_version(self, value: str) -> _MetadataVersion:
        # Implicitly makes Metadata-Version required.
        if value not in _VALID_METADATA_VERSIONS:
            raise self._invalid_metadata(f"{value!r} is not a valid metadata version")
        return cast(_MetadataVersion, value)

    def _process_name(self, value: str) -> str:
        if not value:
            raise self._invalid_metadata("{field} is a required field")
        # Validate the name as a side-effect.
        try:
            utils.canonicalize_name(value, validate=True)
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{value!r} is invalid for {{field}}", cause=exc
            )
        else:
            return value

    def _process_version(self, value: str) -> version_module.Version:
        if not value:
            raise self._invalid_metadata("{field} is a required field")
        try:
            return version_module.parse(value)
        except version_module.InvalidVersion as exc:
            raise self._invalid_metadata(
                f"{value!r} is invalid for {{field}}", cause=exc
            )

    def _process_summary(self, value: str) -> str:
        """Check the field contains no newlines."""
        if "
" in value:
            raise self._invalid_metadata("{field} must be a single line")
        return value

    def _process_description_content_type(self, value: str) -> str:
        content_types = {"text/plain", "text/x-rst", "text/markdown"}
        message = email.message.EmailMessage()
        message["content-type"] = value

        content_type, parameters = (
            # Defaults to `text/plain` if parsing failed.
            message.get_content_type().lower(),
            message["content-type"].params,
        )
        # Check if content-type is valid or defaulted to `text/plain` and thus was
        # not parseable.
        if content_type not in content_types or content_type not in value.lower():
            raise self._invalid_metadata(
                f"{{field}} must be one of {list(content_types)}, not {value!r}"
            )

        charset = parameters.get("charset", "UTF-8")
        if charset != "UTF-8":
            raise self._invalid_metadata(
                f"{{field}} can only specify the UTF-8 charset, not {list(charset)}"
            )

        markdown_variants = {"GFM", "CommonMark"}
        variant = parameters.get("variant", "GFM")  # Use an acceptable default.
        if content_type == "text/markdown" and variant not in markdown_variants:
            raise self._invalid_metadata(
                f"valid Markdown variants for {{field}} are {list(markdown_variants)}, "
                f"not {variant!r}",
            )
        return value

    def _process_dynamic(self, value: list[str]) -> list[str]:
        for dynamic_field in map(str.lower, value):
            if dynamic_field in {"name", "version", "metadata-version"}:
                raise self._invalid_metadata(
                    f"{value!r} is not allowed as a dynamic field"
                )
            elif dynamic_field not in _EMAIL_TO_RAW_MAPPING:
                raise self._invalid_metadata(f"{value!r} is not a valid dynamic field")
        return list(map(str.lower, value))

    def _process_provides_extra(
        self,
        value: list[str],
    ) -> list[utils.NormalizedName]:
        normalized_names = []
        try:
            for name in value:
                normalized_names.append(utils.canonicalize_name(name, validate=True))
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {{field}}", cause=exc
            )
        else:
            return normalized_names

    def _process_requires_python(self, value: str) -> specifiers.SpecifierSet:
        try:
            return specifiers.SpecifierSet(value)
        except specifiers.InvalidSpecifier as exc:
            raise self._invalid_metadata(
                f"{value!r} is invalid for {{field}}", cause=exc
            )

    def _process_requires_dist(
        self,
        value: list[str],
    ) -> list[requirements.Requirement]:
        reqs = []
        try:
            for req in value:
                reqs.append(requirements.Requirement(req))
        except requirements.InvalidRequirement as exc:
            raise self._invalid_metadata(f"{req!r} is invalid for {{field}}", cause=exc)
        else:
            return reqs


class Metadata:
    """Representation of distribution metadata.

    Compared to :class:`RawMetadata`, this class provides objects representing
    metadata fields instead of only using built-in types. Any invalid metadata
    will cause :exc:`InvalidMetadata` to be raised (with a
    :py:attr:`~BaseException.__cause__` attribute as appropriate).
    """

    _raw: RawMetadata

    @classmethod
    def from_raw(cls, data: RawMetadata, *, validate: bool = True) -> Metadata:
        """Create an instance from :class:`RawMetadata`.

        If *validate* is true, all metadata will be validated. All exceptions
        related to validation will be gathered and raised as an :class:`ExceptionGroup`.
        """
        ins = cls()
        ins._raw = data.copy()  # Mutations occur due to caching enriched values.

        if validate:
            exceptions: list[Exception] = []
            try:
                metadata_version = ins.metadata_version
                metadata_age = _VALID_METADATA_VERSIONS.index(metadata_version)
            except InvalidMetadata as metadata_version_exc:
                exceptions.append(metadata_version_exc)
                metadata_version = None

            # Make sure to check for the fields that are present, the required
            # fields (so their absence can be reported).
            fields_to_check = frozenset(ins._raw) | _REQUIRED_ATTRS
            # Remove fields that have already been checked.
            fields_to_check -= {"metadata_version"}

            for key in fields_to_check:
                try:
                    if metadata_version:
                        # Can't use getattr() as that triggers descriptor protocol which
                        # will fail due to no value for the instance argument.
                        try:
                            field_metadata_version = cls.__dict__[key].added
                        except KeyError:
                            exc = InvalidMetadata(key, f"unrecognized field: {key!r}")
                            exceptions.append(exc)
                            continue
                        field_age = _VALID_METADATA_VERSIONS.index(
                            field_metadata_version
                        )
                        if field_age > metadata_age:
                            field = _RAW_TO_EMAIL_MAPPING[key]
                            exc = InvalidMetadata(
                                field,
                                "{field} introduced in metadata version "
                                "{field_metadata_version}, not {metadata_version}",
                            )
                            exceptions.append(exc)
                            continue
                    getattr(ins, key)
                except InvalidMetadata as exc:
                    exceptions.append(exc)

            if exceptions:
                raise ExceptionGroup("invalid metadata", exceptions)

        return ins

    @classmethod
    def from_email(cls, data: bytes | str, *, validate: bool = True) -> Metadata:
        """Parse metadata from email headers.

        If *validate* is true, the metadata will be validated. All exceptions
        related to validation will be gathered and raised as an :class:`ExceptionGroup`.
        """
        raw, unparsed = parse_email(data)

        if validate:
            exceptions: list[Exception] = []
            for unparsed_key in unparsed:
                if unparsed_key in _EMAIL_TO_RAW_MAPPING:
                    message = f"{unparsed_key!r} has invalid data"
                else:
                    message = f"unrecognized field: {unparsed_key!r}"
                exceptions.append(InvalidMetadata(unparsed_key, message))

            if exceptions:
                raise ExceptionGroup("unparsed", exceptions)

        try:
            return cls.from_raw(raw, validate=validate)
        except ExceptionGroup as exc_group:
            raise ExceptionGroup(
                "invalid or unparsed metadata", exc_group.exceptions
            ) from None

    metadata_version: _Validator[_MetadataVersion] = _Validator()
    """:external:ref:`core-metadata-metadata-version`
    (required; validated to be a valid metadata version)"""
    name: _Validator[str] = _Validator()
    """:external:ref:`core-metadata-name`
    (required; validated using :func:`~packaging.utils.canonicalize_name` and its
    *validate* parameter)"""
    version: _Validator[version_module.Version] = _Validator()
    """:external:ref:`core-metadata-version` (required)"""
    dynamic: _Validator[list[str] | None] = _Validator(
        added="2.2",
    )
    """:external:ref:`core-metadata-dynamic`
    (validated against core metadata field names and lowercased)"""
    platforms: _Validator[list[str] | None] = _Validator()
    """:external:ref:`core-metadata-platform`"""
    supported_platforms: _Validator[list[str] | None] = _Validator(added="1.1")
    """:external:ref:`core-metadata-supported-platform`"""
    summary: _Validator[str | None] = _Validator()
    """:external:ref:`core-metadata-summary` (validated to contain no newlines)"""
    description: _Validator[str | None] = _Validator()  # TODO 2.1: can be in body
    """:external:ref:`core-metadata-description`"""
    description_content_type: _Validator[str | None] = _Validator(added="2.1")
    """:external:ref:`core-metadata-description-content-type` (validated)"""
    keywords: _Validator[list[str] | None] = _Validator()
    """:external:ref:`core-metadata-keywords`"""
    home_page: _Validator[str | None] = _Validator()
    """:external:ref:`core-metadata-home-page`"""
    download_url: _Validator[str | None] = _Validator(added="1.1")
    """:external:ref:`core-metadata-download-url`"""
    author: _Validator[str | None] = _Validator()
    """:external:ref:`core-metadata-author`"""
    author_email: _Validator[str | None] = _Validator()
    """:external:ref:`core-metadata-author-email`"""
    maintainer: _Validator[str | None] = _Validator(added="1.2")
    """:external:ref:`core-metadata-maintainer`"""
    maintainer_email: _Validator[str | None] = _Validator(added="1.2")
    """:external:ref:`core-metadata-maintainer-email`"""
    license: _Validator[str | None] = _Validator()
    """:external:ref:`core-metadata-license`"""
    classifiers: _Validator[list[str] | None] = _Validator(added="1.1")
    """:external:ref:`core-metadata-classifier`"""
    requires_dist: _Validator[list[requirements.Requirement] | None] = _Validator(
        added="1.2"
    )
    """:external:ref:`core-metadata-requires-dist`"""
    requires_python: _Validator[specifiers.SpecifierSet | None] = _Validator(
        added="1.2"
    )
    """:external:ref:`core-metadata-requires-python`"""
    # Because `Requires-External` allows for non-PEP 440 version specifiers, we
    # don't do any processing on the values.
    requires_external: _Validator[list[str] | None] = _Validator(added="1.2")
    """:external:ref:`core-metadata-requires-external`"""
    project_urls: _Validator[dict[str, str] | None] = _Validator(added="1.2")
    """:external:ref:`core-metadata-project-url`"""
    # PEP 685 lets us raise an error if an extra doesn't pass `Name` validation
    # regardless of metadata version.
    provides_extra: _Validator[list[utils.NormalizedName] | None] = _Validator(
        added="2.1",
    )
    """:external:ref:`core-metadata-provides-extra`"""
    provides_dist: _Validator[list[str] | None] = _Validator(added="1.2")
    """:external:ref:`core-metadata-provides-dist`"""
    obsoletes_dist: _Validator[list[str] | None] = _Validator(added="1.2")
    """:external:ref:`core-metadata-obsoletes-dist`"""
    requires: _Validator[list[str] | None] = _Validator(added="1.1")
    """``Requires`` (deprecated)"""
    provides: _Validator[list[str] | None] = _Validator(added="1.1")
    """``Provides`` (deprecated)"""
    obsoletes: _Validator[list[str] | None] = _Validator(added="1.1")
    """``Obsoletes`` (deprecated)"""
```
```bash
./.venv/lib/python3.9/site-packages/packaging/version.py
```
```
# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.
"""
.. testsetup::

    from packaging.version import parse, Version
"""

from __future__ import annotations

import itertools
import re
from typing import Any, Callable, NamedTuple, SupportsInt, Tuple, Union

from ._structures import Infinity, InfinityType, NegativeInfinity, NegativeInfinityType

__all__ = ["VERSION_PATTERN", "parse", "Version", "InvalidVersion"]

LocalType = Tuple[Union[int, str], ...]

CmpPrePostDevType = Union[InfinityType, NegativeInfinityType, Tuple[str, int]]
CmpLocalType = Union[
    NegativeInfinityType,
    Tuple[Union[Tuple[int, str], Tuple[NegativeInfinityType, Union[int, str]]], ...],
]
CmpKey = Tuple[
    int,
    Tuple[int, ...],
    CmpPrePostDevType,
    CmpPrePostDevType,
    CmpPrePostDevType,
    CmpLocalType,
]
VersionComparisonMethod = Callable[[CmpKey, CmpKey], bool]


class _Version(NamedTuple):
    epoch: int
    release: tuple[int, ...]
    dev: tuple[str, int] | None
    pre: tuple[str, int] | None
    post: tuple[str, int] | None
    local: LocalType | None


def parse(version: str) -> Version:
    """Parse the given version string.

    >>> parse('1.0.dev1')
    <Version('1.0.dev1')>

    :param version: The version string to parse.
    :raises InvalidVersion: When the version string is not a valid version.
    """
    return Version(version)


class InvalidVersion(ValueError):
    """Raised when a version string is not a valid version.

    >>> Version("invalid")
    Traceback (most recent call last):
        ...
    packaging.version.InvalidVersion: Invalid version: 'invalid'
    """


class _BaseVersion:
    _key: tuple[Any, ...]

    def __hash__(self) -> int:
        return hash(self._key)

    # Please keep the duplicated `isinstance` check
    # in the six comparisons hereunder
    # unless you find a way to avoid adding overhead function calls.
    def __lt__(self, other: _BaseVersion) -> bool:
        if not isinstance(other, _BaseVersion):
            return NotImplemented

        return self._key < other._key

    def __le__(self, other: _BaseVersion) -> bool:
        if not isinstance(other, _BaseVersion):
            return NotImplemented

        return self._key <= other._key

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _BaseVersion):
            return NotImplemented

        return self._key == other._key

    def __ge__(self, other: _BaseVersion) -> bool:
        if not isinstance(other, _BaseVersion):
            return NotImplemented

        return self._key >= other._key

    def __gt__(self, other: _BaseVersion) -> bool:
        if not isinstance(other, _BaseVersion):
            return NotImplemented

        return self._key > other._key

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, _BaseVersion):
            return NotImplemented

        return self._key != other._key


# Deliberately not anchored to the start and end of the string, to make it
# easier for 3rd party code to reuse
_VERSION_PATTERN = r"""
    v?
    (?:
        (?:(?P<epoch>[0-9]+)!)?                           # epoch
        (?P<release>[0-9]+(?:\.[0-9]+)*)                  # release segment
        (?P<pre>                                          # pre-release
            [-_\.]?
            (?P<pre_l>alpha|a|beta|b|preview|pre|c|rc)
            [-_\.]?
            (?P<pre_n>[0-9]+)?
        )?
        (?P<post>                                         # post release
            (?:-(?P<post_n1>[0-9]+))
            |
            (?:
                [-_\.]?
                (?P<post_l>post|rev|r)
                [-_\.]?
                (?P<post_n2>[0-9]+)?
            )
        )?
        (?P<dev>                                          # dev release
            [-_\.]?
            (?P<dev_l>dev)
            [-_\.]?
            (?P<dev_n>[0-9]+)?
        )?
    )
    (?:\+(?P<local>[a-z0-9]+(?:[-_\.][a-z0-9]+)*))?       # local version
"""

VERSION_PATTERN = _VERSION_PATTERN
"""
A string containing the regular expression used to match a valid version.

The pattern is not anchored at either end, and is intended for embedding in larger
expressions (for example, matching a version number as part of a file name). The
regular expression should be compiled with the ``re.VERBOSE`` and ``re.IGNORECASE``
flags set.

:meta hide-value:
"""


class Version(_BaseVersion):
    """This class abstracts handling of a project's versions.

    A :class:`Version` instance is comparison aware and can be compared and
    sorted using the standard Python interfaces.

    >>> v1 = Version("1.0a5")
    >>> v2 = Version("1.0")
    >>> v1
    <Version('1.0a5')>
    >>> v2
    <Version('1.0')>
    >>> v1 < v2
    True
    >>> v1 == v2
    False
    >>> v1 > v2
    False
    >>> v1 >= v2
    False
    >>> v1 <= v2
    True
    """

    _regex = re.compile(r"^\s*" + VERSION_PATTERN + r"\s*$", re.VERBOSE | re.IGNORECASE)
    _key: CmpKey

    def __init__(self, version: str) -> None:
        """Initialize a Version object.

        :param version:
            The string representation of a version which will be parsed and normalized
            before use.
        :raises InvalidVersion:
            If the ``version`` does not conform to PEP 440 in any way then this
            exception will be raised.
        """

        # Validate the version and parse it into pieces
        match = self._regex.search(version)
        if not match:
            raise InvalidVersion(f"Invalid version: '{version}'")

        # Store the parsed out pieces of the version
        self._version = _Version(
            epoch=int(match.group("epoch")) if match.group("epoch") else 0,
            release=tuple(int(i) for i in match.group("release").split(".")),
            pre=_parse_letter_version(match.group("pre_l"), match.group("pre_n")),
            post=_parse_letter_version(
                match.group("post_l"), match.group("post_n1") or match.group("post_n2")
            ),
            dev=_parse_letter_version(match.group("dev_l"), match.group("dev_n")),
            local=_parse_local_version(match.group("local")),
        )

        # Generate a key which will be used for sorting
        self._key = _cmpkey(
            self._version.epoch,
            self._version.release,
            self._version.pre,
            self._version.post,
            self._version.dev,
            self._version.local,
        )

    def __repr__(self) -> str:
        """A representation of the Version that shows all internal state.

        >>> Version('1.0.0')
        <Version('1.0.0')>
        """
        return f"<Version('{self}')>"

    def __str__(self) -> str:
        """A string representation of the version that can be rounded-tripped.

        >>> str(Version("1.0a5"))
        '1.0a5'
        """
        parts = []

        # Epoch
        if self.epoch != 0:
            parts.append(f"{self.epoch}!")

        # Release segment
        parts.append(".".join(str(x) for x in self.release))

        # Pre-release
        if self.pre is not None:
            parts.append("".join(str(x) for x in self.pre))

        # Post-release
        if self.post is not None:
            parts.append(f".post{self.post}")

        # Development release
        if self.dev is not None:
            parts.append(f".dev{self.dev}")

        # Local version segment
        if self.local is not None:
            parts.append(f"+{self.local}")

        return "".join(parts)

    @property
    def epoch(self) -> int:
        """The epoch of the version.

        >>> Version("2.0.0").epoch
        0
        >>> Version("1!2.0.0").epoch
        1
        """
        return self._version.epoch

    @property
    def release(self) -> tuple[int, ...]:
        """The components of the "release" segment of the version.

        >>> Version("1.2.3").release
        (1, 2, 3)
        >>> Version("2.0.0").release
        (2, 0, 0)
        >>> Version("1!2.0.0.post0").release
        (2, 0, 0)

        Includes trailing zeroes but not the epoch or any pre-release / development /
        post-release suffixes.
        """
        return self._version.release

    @property
    def pre(self) -> tuple[str, int] | None:
        """The pre-release segment of the version.

        >>> print(Version("1.2.3").pre)
        None
        >>> Version("1.2.3a1").pre
        ('a', 1)
        >>> Version("1.2.3b1").pre
        ('b', 1)
        >>> Version("1.2.3rc1").pre
        ('rc', 1)
        """
        return self._version.pre

    @property
    def post(self) -> int | None:
        """The post-release number of the version.

        >>> print(Version("1.2.3").post)
        None
        >>> Version("1.2.3.post1").post
        1
        """
        return self._version.post[1] if self._version.post else None

    @property
    def dev(self) -> int | None:
        """The development number of the version.

        >>> print(Version("1.2.3").dev)
        None
        >>> Version("1.2.3.dev1").dev
        1
        """
        return self._version.dev[1] if self._version.dev else None

    @property
    def local(self) -> str | None:
        """The local version segment of the version.

        >>> print(Version("1.2.3").local)
        None
        >>> Version("1.2.3+abc").local
        'abc'
        """
        if self._version.local:
            return ".".join(str(x) for x in self._version.local)
        else:
            return None

    @property
    def public(self) -> str:
        """The public portion of the version.

        >>> Version("1.2.3").public
        '1.2.3'
        >>> Version("1.2.3+abc").public
        '1.2.3'
        >>> Version("1.2.3+abc.dev1").public
        '1.2.3'
        """
        return str(self).split("+", 1)[0]

    @property
    def base_version(self) -> str:
        """The "base version" of the version.

        >>> Version("1.2.3").base_version
        '1.2.3'
        >>> Version("1.2.3+abc").base_version
        '1.2.3'
        >>> Version("1!1.2.3+abc.dev1").base_version
        '1!1.2.3'

        The "base version" is the public version of the project without any pre or post
        release markers.
        """
        parts = []

        # Epoch
        if self.epoch != 0:
            parts.append(f"{self.epoch}!")

        # Release segment
        parts.append(".".join(str(x) for x in self.release))

        return "".join(parts)

    @property
    def is_prerelease(self) -> bool:
        """Whether this version is a pre-release.

        >>> Version("1.2.3").is_prerelease
        False
        >>> Version("1.2.3a1").is_prerelease
        True
        >>> Version("1.2.3b1").is_prerelease
        True
        >>> Version("1.2.3rc1").is_prerelease
        True
        >>> Version("1.2.3dev1").is_prerelease
        True
        """
        return self.dev is not None or self.pre is not None

    @property
    def is_postrelease(self) -> bool:
        """Whether this version is a post-release.

        >>> Version("1.2.3").is_postrelease
        False
        >>> Version("1.2.3.post1").is_postrelease
        True
        """
        return self.post is not None

    @property
    def is_devrelease(self) -> bool:
        """Whether this version is a development release.

        >>> Version("1.2.3").is_devrelease
        False
        >>> Version("1.2.3.dev1").is_devrelease
        True
        """
        return self.dev is not None

    @property
    def major(self) -> int:
        """The first item of :attr:`release` or ``0`` if unavailable.

        >>> Version("1.2.3").major
        1
        """
        return self.release[0] if len(self.release) >= 1 else 0

    @property
    def minor(self) -> int:
        """The second item of :attr:`release` or ``0`` if unavailable.

        >>> Version("1.2.3").minor
        2
        >>> Version("1").minor
        0
        """
        return self.release[1] if len(self.release) >= 2 else 0

    @property
    def micro(self) -> int:
        """The third item of :attr:`release` or ``0`` if unavailable.

        >>> Version("1.2.3").micro
        3
        >>> Version("1").micro
        0
        """
        return self.release[2] if len(self.release) >= 3 else 0


def _parse_letter_version(
    letter: str | None, number: str | bytes | SupportsInt | None
) -> tuple[str, int] | None:
    if letter:
        # We consider there to be an implicit 0 in a pre-release if there is
        # not a numeral associated with it.
        if number is None:
            number = 0

        # We normalize any letters to their lower case form
        letter = letter.lower()

        # We consider some words to be alternate spellings of other words and
        # in those cases we want to normalize the spellings to our preferred
        # spelling.
        if letter == "alpha":
            letter = "a"
        elif letter == "beta":
            letter = "b"
        elif letter in ["c", "pre", "preview"]:
            letter = "rc"
        elif letter in ["rev", "r"]:
            letter = "post"

        return letter, int(number)
    if not letter and number:
        # We assume if we are given a number, but we are not given a letter
        # then this is using the implicit post release syntax (e.g. 1.0-1)
        letter = "post"

        return letter, int(number)

    return None


_local_version_separators = re.compile(r"[\._-]")


def _parse_local_version(local: str | None) -> LocalType | None:
    """
    Takes a string like abc.1.twelve and turns it into ("abc", 1, "twelve").
    """
    if local is not None:
        return tuple(
            part.lower() if not part.isdigit() else int(part)
            for part in _local_version_separators.split(local)
        )
    return None


def _cmpkey(
    epoch: int,
    release: tuple[int, ...],
    pre: tuple[str, int] | None,
    post: tuple[str, int] | None,
    dev: tuple[str, int] | None,
    local: LocalType | None,
) -> CmpKey:
    # When we compare a release version, we want to compare it with all of the
    # trailing zeros removed. So we'll use a reverse the list, drop all the now
    # leading zeros until we come to something non zero, then take the rest
    # re-reverse it back into the correct order and make it a tuple and use
    # that for our sorting key.
    _release = tuple(
        reversed(list(itertools.dropwhile(lambda x: x == 0, reversed(release))))
    )

    # We need to "trick" the sorting algorithm to put 1.0.dev0 before 1.0a0.
    # We'll do this by abusing the pre segment, but we _only_ want to do this
    # if there is not a pre or a post segment. If we have one of those then
    # the normal sorting rules will handle this case correctly.
    if pre is None and post is None and dev is not None:
        _pre: CmpPrePostDevType = NegativeInfinity
    # Versions without a pre-release (except as noted above) should sort after
    # those with one.
    elif pre is None:
        _pre = Infinity
    else:
        _pre = pre

    # Versions without a post segment should sort before those with one.
    if post is None:
        _post: CmpPrePostDevType = NegativeInfinity

    else:
        _post = post

    # Versions without a development segment should sort after those with one.
    if dev is None:
        _dev: CmpPrePostDevType = Infinity

    else:
        _dev = dev

    if local is None:
        # Versions without a local segment should sort before those with one.
        _local: CmpLocalType = NegativeInfinity
    else:
        # Versions with a local segment need that segment parsed to implement
        # the sorting rules in PEP440.
        # - Alpha numeric segments sort before numeric segments
        # - Alpha numeric segments sort lexicographically
        # - Numeric segments sort numerically
        # - Shorter versions sort before longer versions when the prefixes
        #   match exactly
        _local = tuple(
            (i, "") if isinstance(i, int) else (NegativeInfinity, i) for i in local
        )

    return epoch, _release, _pre, _post, _dev, _local
```
```bash
./.venv/lib/python3.9/site-packages/packaging/__init__.py
```
```
# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

__title__ = "packaging"
__summary__ = "Core utilities for Python packages"
__uri__ = "https://github.com/pypa/packaging"

__version__ = "24.1"

__author__ = "Donald Stufft and individual contributors"
__email__ = "donald@stufft.io"

__license__ = "BSD-2-Clause or Apache-2.0"
__copyright__ = "2014 %s" % __author__
```
```bash
./.venv/lib/python3.9/site-packages/packaging/_parser.py
```
```
"""Handwritten parser of dependency specifiers.

The docstring for each __parse_* function contains EBNF-inspired grammar representing
the implementation.
"""

from __future__ import annotations

import ast
from typing import NamedTuple, Sequence, Tuple, Union

from ._tokenizer import DEFAULT_RULES, Tokenizer


class Node:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}('{self}')>"

    def serialize(self) -> str:
        raise NotImplementedError


class Variable(Node):
    def serialize(self) -> str:
        return str(self)


class Value(Node):
    def serialize(self) -> str:
        return f'"{self}"'


class Op(Node):
    def serialize(self) -> str:
        return str(self)


MarkerVar = Union[Variable, Value]
MarkerItem = Tuple[MarkerVar, Op, MarkerVar]
MarkerAtom = Union[MarkerItem, Sequence["MarkerAtom"]]
MarkerList = Sequence[Union["MarkerList", MarkerAtom, str]]


class ParsedRequirement(NamedTuple):
    name: str
    url: str
    extras: list[str]
    specifier: str
    marker: MarkerList | None


# --------------------------------------------------------------------------------------
# Recursive descent parser for dependency specifier
# --------------------------------------------------------------------------------------
def parse_requirement(source: str) -> ParsedRequirement:
    return _parse_requirement(Tokenizer(source, rules=DEFAULT_RULES))


def _parse_requirement(tokenizer: Tokenizer) -> ParsedRequirement:
    """
    requirement = WS? IDENTIFIER WS? extras WS? requirement_details
    """
    tokenizer.consume("WS")

    name_token = tokenizer.expect(
        "IDENTIFIER", expected="package name at the start of dependency specifier"
    )
    name = name_token.text
    tokenizer.consume("WS")

    extras = _parse_extras(tokenizer)
    tokenizer.consume("WS")

    url, specifier, marker = _parse_requirement_details(tokenizer)
    tokenizer.expect("END", expected="end of dependency specifier")

    return ParsedRequirement(name, url, extras, specifier, marker)


def _parse_requirement_details(
    tokenizer: Tokenizer,
) -> tuple[str, str, MarkerList | None]:
    """
    requirement_details = AT URL (WS requirement_marker?)?
                        | specifier WS? (requirement_marker)?
    """

    specifier = ""
    url = ""
    marker = None

    if tokenizer.check("AT"):
        tokenizer.read()
        tokenizer.consume("WS")

        url_start = tokenizer.position
        url = tokenizer.expect("URL", expected="URL after @").text
        if tokenizer.check("END", peek=True):
            return (url, specifier, marker)

        tokenizer.expect("WS", expected="whitespace after URL")

        # The input might end after whitespace.
        if tokenizer.check("END", peek=True):
            return (url, specifier, marker)

        marker = _parse_requirement_marker(
            tokenizer, span_start=url_start, after="URL and whitespace"
        )
    else:
        specifier_start = tokenizer.position
        specifier = _parse_specifier(tokenizer)
        tokenizer.consume("WS")

        if tokenizer.check("END", peek=True):
            return (url, specifier, marker)

        marker = _parse_requirement_marker(
            tokenizer,
            span_start=specifier_start,
            after=(
                "version specifier"
                if specifier
                else "name and no valid version specifier"
            ),
        )

    return (url, specifier, marker)


def _parse_requirement_marker(
    tokenizer: Tokenizer, *, span_start: int, after: str
) -> MarkerList:
    """
    requirement_marker = SEMICOLON marker WS?
    """

    if not tokenizer.check("SEMICOLON"):
        tokenizer.raise_syntax_error(
            f"Expected end or semicolon (after {after})",
            span_start=span_start,
        )
    tokenizer.read()

    marker = _parse_marker(tokenizer)
    tokenizer.consume("WS")

    return marker


def _parse_extras(tokenizer: Tokenizer) -> list[str]:
    """
    extras = (LEFT_BRACKET wsp* extras_list? wsp* RIGHT_BRACKET)?
    """
    if not tokenizer.check("LEFT_BRACKET", peek=True):
        return []

    with tokenizer.enclosing_tokens(
        "LEFT_BRACKET",
        "RIGHT_BRACKET",
        around="extras",
    ):
        tokenizer.consume("WS")
        extras = _parse_extras_list(tokenizer)
        tokenizer.consume("WS")

    return extras


def _parse_extras_list(tokenizer: Tokenizer) -> list[str]:
    """
    extras_list = identifier (wsp* ',' wsp* identifier)*
    """
    extras: list[str] = []

    if not tokenizer.check("IDENTIFIER"):
        return extras

    extras.append(tokenizer.read().text)

    while True:
        tokenizer.consume("WS")
        if tokenizer.check("IDENTIFIER", peek=True):
            tokenizer.raise_syntax_error("Expected comma between extra names")
        elif not tokenizer.check("COMMA"):
            break

        tokenizer.read()
        tokenizer.consume("WS")

        extra_token = tokenizer.expect("IDENTIFIER", expected="extra name after comma")
        extras.append(extra_token.text)

    return extras


def _parse_specifier(tokenizer: Tokenizer) -> str:
    """
    specifier = LEFT_PARENTHESIS WS? version_many WS? RIGHT_PARENTHESIS
              | WS? version_many WS?
    """
    with tokenizer.enclosing_tokens(
        "LEFT_PARENTHESIS",
        "RIGHT_PARENTHESIS",
        around="version specifier",
    ):
        tokenizer.consume("WS")
        parsed_specifiers = _parse_version_many(tokenizer)
        tokenizer.consume("WS")

    return parsed_specifiers


def _parse_version_many(tokenizer: Tokenizer) -> str:
    """
    version_many = (SPECIFIER (WS? COMMA WS? SPECIFIER)*)?
    """
    parsed_specifiers = ""
    while tokenizer.check("SPECIFIER"):
        span_start = tokenizer.position
        parsed_specifiers += tokenizer.read().text
        if tokenizer.check("VERSION_PREFIX_TRAIL", peek=True):
            tokenizer.raise_syntax_error(
                ".* suffix can only be used with `==` or `!=` operators",
                span_start=span_start,
                span_end=tokenizer.position + 1,
            )
        if tokenizer.check("VERSION_LOCAL_LABEL_TRAIL", peek=True):
            tokenizer.raise_syntax_error(
                "Local version label can only be used with `==` or `!=` operators",
                span_start=span_start,
                span_end=tokenizer.position,
            )
        tokenizer.consume("WS")
        if not tokenizer.check("COMMA"):
            break
        parsed_specifiers += tokenizer.read().text
        tokenizer.consume("WS")

    return parsed_specifiers


# --------------------------------------------------------------------------------------
# Recursive descent parser for marker expression
# --------------------------------------------------------------------------------------
def parse_marker(source: str) -> MarkerList:
    return _parse_full_marker(Tokenizer(source, rules=DEFAULT_RULES))


def _parse_full_marker(tokenizer: Tokenizer) -> MarkerList:
    retval = _parse_marker(tokenizer)
    tokenizer.expect("END", expected="end of marker expression")
    return retval


def _parse_marker(tokenizer: Tokenizer) -> MarkerList:
    """
    marker = marker_atom (BOOLOP marker_atom)+
    """
    expression = [_parse_marker_atom(tokenizer)]
    while tokenizer.check("BOOLOP"):
        token = tokenizer.read()
        expr_right = _parse_marker_atom(tokenizer)
        expression.extend((token.text, expr_right))
    return expression


def _parse_marker_atom(tokenizer: Tokenizer) -> MarkerAtom:
    """
    marker_atom = WS? LEFT_PARENTHESIS WS? marker WS? RIGHT_PARENTHESIS WS?
                | WS? marker_item WS?
    """

    tokenizer.consume("WS")
    if tokenizer.check("LEFT_PARENTHESIS", peek=True):
        with tokenizer.enclosing_tokens(
            "LEFT_PARENTHESIS",
            "RIGHT_PARENTHESIS",
            around="marker expression",
        ):
            tokenizer.consume("WS")
            marker: MarkerAtom = _parse_marker(tokenizer)
            tokenizer.consume("WS")
    else:
        marker = _parse_marker_item(tokenizer)
    tokenizer.consume("WS")
    return marker


def _parse_marker_item(tokenizer: Tokenizer) -> MarkerItem:
    """
    marker_item = WS? marker_var WS? marker_op WS? marker_var WS?
    """
    tokenizer.consume("WS")
    marker_var_left = _parse_marker_var(tokenizer)
    tokenizer.consume("WS")
    marker_op = _parse_marker_op(tokenizer)
    tokenizer.consume("WS")
    marker_var_right = _parse_marker_var(tokenizer)
    tokenizer.consume("WS")
    return (marker_var_left, marker_op, marker_var_right)


def _parse_marker_var(tokenizer: Tokenizer) -> MarkerVar:
    """
    marker_var = VARIABLE | QUOTED_STRING
    """
    if tokenizer.check("VARIABLE"):
        return process_env_var(tokenizer.read().text.replace(".", "_"))
    elif tokenizer.check("QUOTED_STRING"):
        return process_python_str(tokenizer.read().text)
    else:
        tokenizer.raise_syntax_error(
            message="Expected a marker variable or quoted string"
        )


def process_env_var(env_var: str) -> Variable:
    if env_var in ("platform_python_implementation", "python_implementation"):
        return Variable("platform_python_implementation")
    else:
        return Variable(env_var)


def process_python_str(python_str: str) -> Value:
    value = ast.literal_eval(python_str)
    return Value(str(value))


def _parse_marker_op(tokenizer: Tokenizer) -> Op:
    """
    marker_op = IN | NOT IN | OP
    """
    if tokenizer.check("IN"):
        tokenizer.read()
        return Op("in")
    elif tokenizer.check("NOT"):
        tokenizer.read()
        tokenizer.expect("WS", expected="whitespace after 'not'")
        tokenizer.expect("IN", expected="'in' after 'not'")
        return Op("not in")
    elif tokenizer.check("OP"):
        return Op(tokenizer.read().text)
    else:
        return tokenizer.raise_syntax_error(
            "Expected marker operator, one of "
            "<=, <, !=, ==, >=, >, ~=, ===, in, not in"
        )
```
```bash
./.venv/lib/python3.9/site-packages/packaging/utils.py
```
```
# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import re
from typing import NewType, Tuple, Union, cast

from .tags import Tag, parse_tag
from .version import InvalidVersion, Version

BuildTag = Union[Tuple[()], Tuple[int, str]]
NormalizedName = NewType("NormalizedName", str)


class InvalidName(ValueError):
    """
    An invalid distribution name; users should refer to the packaging user guide.
    """


class InvalidWheelFilename(ValueError):
    """
    An invalid wheel filename was found, users should refer to PEP 427.
    """


class InvalidSdistFilename(ValueError):
    """
    An invalid sdist filename was found, users should refer to the packaging user guide.
    """


# Core metadata spec for `Name`
_validate_regex = re.compile(
    r"^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$", re.IGNORECASE
)
_canonicalize_regex = re.compile(r"[-_.]+")
_normalized_regex = re.compile(r"^([a-z0-9]|[a-z0-9]([a-z0-9-](?!--))*[a-z0-9])$")
# PEP 427: The build number must start with a digit.
_build_tag_regex = re.compile(r"(\d+)(.*)")


def canonicalize_name(name: str, *, validate: bool = False) -> NormalizedName:
    if validate and not _validate_regex.match(name):
        raise InvalidName(f"name is invalid: {name!r}")
    # This is taken from PEP 503.
    value = _canonicalize_regex.sub("-", name).lower()
    return cast(NormalizedName, value)


def is_normalized_name(name: str) -> bool:
    return _normalized_regex.match(name) is not None


def canonicalize_version(
    version: Version | str, *, strip_trailing_zero: bool = True
) -> str:
    """
    This is very similar to Version.__str__, but has one subtle difference
    with the way it handles the release segment.
    """
    if isinstance(version, str):
        try:
            parsed = Version(version)
        except InvalidVersion:
            # Legacy versions cannot be normalized
            return version
    else:
        parsed = version

    parts = []

    # Epoch
    if parsed.epoch != 0:
        parts.append(f"{parsed.epoch}!")

    # Release segment
    release_segment = ".".join(str(x) for x in parsed.release)
    if strip_trailing_zero:
        # NB: This strips trailing '.0's to normalize
        release_segment = re.sub(r"(\.0)+$", "", release_segment)
    parts.append(release_segment)

    # Pre-release
    if parsed.pre is not None:
        parts.append("".join(str(x) for x in parsed.pre))

    # Post-release
    if parsed.post is not None:
        parts.append(f".post{parsed.post}")

    # Development release
    if parsed.dev is not None:
        parts.append(f".dev{parsed.dev}")

    # Local version segment
    if parsed.local is not None:
        parts.append(f"+{parsed.local}")

    return "".join(parts)


def parse_wheel_filename(
    filename: str,
) -> tuple[NormalizedName, Version, BuildTag, frozenset[Tag]]:
    if not filename.endswith(".whl"):
        raise InvalidWheelFilename(
            f"Invalid wheel filename (extension must be '.whl'): {filename}"
        )

    filename = filename[:-4]
    dashes = filename.count("-")
    if dashes not in (4, 5):
        raise InvalidWheelFilename(
            f"Invalid wheel filename (wrong number of parts): {filename}"
        )

    parts = filename.split("-", dashes - 2)
    name_part = parts[0]
    # See PEP 427 for the rules on escaping the project name.
    if "__" in name_part or re.match(r"^[\w\d._]*$", name_part, re.UNICODE) is None:
        raise InvalidWheelFilename(f"Invalid project name: {filename}")
    name = canonicalize_name(name_part)

    try:
        version = Version(parts[1])
    except InvalidVersion as e:
        raise InvalidWheelFilename(
            f"Invalid wheel filename (invalid version): {filename}"
        ) from e

    if dashes == 5:
        build_part = parts[2]
        build_match = _build_tag_regex.match(build_part)
        if build_match is None:
            raise InvalidWheelFilename(
                f"Invalid build number: {build_part} in '{filename}'"
            )
        build = cast(BuildTag, (int(build_match.group(1)), build_match.group(2)))
    else:
        build = ()
    tags = parse_tag(parts[-1])
    return (name, version, build, tags)


def parse_sdist_filename(filename: str) -> tuple[NormalizedName, Version]:
    if filename.endswith(".tar.gz"):
        file_stem = filename[: -len(".tar.gz")]
    elif filename.endswith(".zip"):
        file_stem = filename[: -len(".zip")]
    else:
        raise InvalidSdistFilename(
            f"Invalid sdist filename (extension must be '.tar.gz' or '.zip'):"
            f" {filename}"
        )

    # We are requiring a PEP 440 version, which cannot contain dashes,
    # so we split on the last dash.
    name_part, sep, version_part = file_stem.rpartition("-")
    if not sep:
        raise InvalidSdistFilename(f"Invalid sdist filename: {filename}")

    name = canonicalize_name(name_part)

    try:
        version = Version(version_part)
    except InvalidVersion as e:
        raise InvalidSdistFilename(
            f"Invalid sdist filename (invalid version): {filename}"
        ) from e

    return (name, version)
```
```bash
./.venv/lib/python3.9/site-packages/packaging/requirements.py
```
```
# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.
from __future__ import annotations

from typing import Any, Iterator

from ._parser import parse_requirement as _parse_requirement
from ._tokenizer import ParserSyntaxError
from .markers import Marker, _normalize_extra_values
from .specifiers import SpecifierSet
from .utils import canonicalize_name


class InvalidRequirement(ValueError):
    """
    An invalid requirement was found, users should refer to PEP 508.
    """


class Requirement:
    """Parse a requirement.

    Parse a given requirement string into its parts, such as name, specifier,
    URL, and extras. Raises InvalidRequirement on a badly-formed requirement
    string.
    """

    # TODO: Can we test whether something is contained within a requirement?
    #       If so how do we do that? Do we need to test against the _name_ of
    #       the thing as well as the version? What about the markers?
    # TODO: Can we normalize the name and extra name?

    def __init__(self, requirement_string: str) -> None:
        try:
            parsed = _parse_requirement(requirement_string)
        except ParserSyntaxError as e:
            raise InvalidRequirement(str(e)) from e

        self.name: str = parsed.name
        self.url: str | None = parsed.url or None
        self.extras: set[str] = set(parsed.extras or [])
        self.specifier: SpecifierSet = SpecifierSet(parsed.specifier)
        self.marker: Marker | None = None
        if parsed.marker is not None:
            self.marker = Marker.__new__(Marker)
            self.marker._markers = _normalize_extra_values(parsed.marker)

    def _iter_parts(self, name: str) -> Iterator[str]:
        yield name

        if self.extras:
            formatted_extras = ",".join(sorted(self.extras))
            yield f"[{formatted_extras}]"

        if self.specifier:
            yield str(self.specifier)

        if self.url:
            yield f"@ {self.url}"
            if self.marker:
                yield " "

        if self.marker:
            yield f"; {self.marker}"

    def __str__(self) -> str:
        return "".join(self._iter_parts(self.name))

    def __repr__(self) -> str:
        return f"<Requirement('{self}')>"

    def __hash__(self) -> int:
        return hash(
            (
                self.__class__.__name__,
                *self._iter_parts(canonicalize_name(self.name)),
            )
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Requirement):
            return NotImplemented

        return (
            canonicalize_name(self.name) == canonicalize_name(other.name)
            and self.extras == other.extras
            and self.specifier == other.specifier
            and self.url == other.url
            and self.marker == other.marker
        )
```
```bash
./.venv/lib/python3.9/site-packages/packaging/_structures.py
```
```
# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.


class InfinityType:
    def __repr__(self) -> str:
        return "Infinity"

    def __hash__(self) -> int:
        return hash(repr(self))

    def __lt__(self, other: object) -> bool:
        return False

    def __le__(self, other: object) -> bool:
        return False

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __gt__(self, other: object) -> bool:
        return True

    def __ge__(self, other: object) -> bool:
        return True

    def __neg__(self: object) -> "NegativeInfinityType":
        return NegativeInfinity


Infinity = InfinityType()


class NegativeInfinityType:
    def __repr__(self) -> str:
        return "-Infinity"

    def __hash__(self) -> int:
        return hash(repr(self))

    def __lt__(self, other: object) -> bool:
        return True

    def __le__(self, other: object) -> bool:
        return True

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __gt__(self, other: object) -> bool:
        return False

    def __ge__(self, other: object) -> bool:
        return False

    def __neg__(self: object) -> InfinityType:
        return Infinity


NegativeInfinity = NegativeInfinityType()
```
```bash
./.venv/lib/python3.9/site-packages/packaging/markers.py
```
```
# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import operator
import os
import platform
import sys
from typing import Any, Callable, TypedDict, cast

from ._parser import MarkerAtom, MarkerList, Op, Value, Variable
from ._parser import parse_marker as _parse_marker
from ._tokenizer import ParserSyntaxError
from .specifiers import InvalidSpecifier, Specifier
from .utils import canonicalize_name

__all__ = [
    "InvalidMarker",
    "UndefinedComparison",
    "UndefinedEnvironmentName",
    "Marker",
    "default_environment",
]

Operator = Callable[[str, str], bool]


class InvalidMarker(ValueError):
    """
    An invalid marker was found, users should refer to PEP 508.
    """


class UndefinedComparison(ValueError):
    """
    An invalid operation was attempted on a value that doesn't support it.
    """


class UndefinedEnvironmentName(ValueError):
    """
    A name was attempted to be used that does not exist inside of the
    environment.
    """


class Environment(TypedDict):
    implementation_name: str
    """The implementation's identifier, e.g. ``'cpython'``."""

    implementation_version: str
    """
    The implementation's version, e.g. ``'3.13.0a2'`` for CPython 3.13.0a2, or
    ``'7.3.13'`` for PyPy3.10 v7.3.13.
    """

    os_name: str
    """
    The value of :py:data:`os.name`. The name of the operating system dependent module
    imported, e.g. ``'posix'``.
    """

    platform_machine: str
    """
    Returns the machine type, e.g. ``'i386'``.

    An empty string if the value cannot be determined.
    """

    platform_release: str
    """
    The system's release, e.g. ``'2.2.0'`` or ``'NT'``.

    An empty string if the value cannot be determined.
    """

    platform_system: str
    """
    The system/OS name, e.g. ``'Linux'``, ``'Windows'`` or ``'Java'``.

    An empty string if the value cannot be determined.
    """

    platform_version: str
    """
    The system's release version, e.g. ``'#3 on degas'``.

    An empty string if the value cannot be determined.
    """

    python_full_version: str
    """
    The Python version as string ``'major.minor.patchlevel'``.

    Note that unlike the Python :py:data:`sys.version`, this value will always include
    the patchlevel (it defaults to 0).
    """

    platform_python_implementation: str
    """
    A string identifying the Python implementation, e.g. ``'CPython'``.
    """

    python_version: str
    """The Python version as string ``'major.minor'``."""

    sys_platform: str
    """
    This string contains a platform identifier that can be used to append
    platform-specific components to :py:data:`sys.path`, for instance.

    For Unix systems, except on Linux and AIX, this is the lowercased OS name as
    returned by ``uname -s`` with the first part of the version as returned by
    ``uname -r`` appended, e.g. ``'sunos5'`` or ``'freebsd8'``, at the time when Python
    was built.
    """


def _normalize_extra_values(results: Any) -> Any:
    """
    Normalize extra values.
    """
    if isinstance(results[0], tuple):
        lhs, op, rhs = results[0]
        if isinstance(lhs, Variable) and lhs.value == "extra":
            normalized_extra = canonicalize_name(rhs.value)
            rhs = Value(normalized_extra)
        elif isinstance(rhs, Variable) and rhs.value == "extra":
            normalized_extra = canonicalize_name(lhs.value)
            lhs = Value(normalized_extra)
        results[0] = lhs, op, rhs
    return results


def _format_marker(
    marker: list[str] | MarkerAtom | str, first: bool | None = True
) -> str:
    assert isinstance(marker, (list, tuple, str))

    # Sometimes we have a structure like [[...]] which is a single item list
    # where the single item is itself it's own list. In that case we want skip
    # the rest of this function so that we don't get extraneous () on the
    # outside.
    if (
        isinstance(marker, list)
        and len(marker) == 1
        and isinstance(marker[0], (list, tuple))
    ):
        return _format_marker(marker[0])

    if isinstance(marker, list):
        inner = (_format_marker(m, first=False) for m in marker)
        if first:
            return " ".join(inner)
        else:
            return "(" + " ".join(inner) + ")"
    elif isinstance(marker, tuple):
        return " ".join([m.serialize() for m in marker])
    else:
        return marker


_operators: dict[str, Operator] = {
    "in": lambda lhs, rhs: lhs in rhs,
    "not in": lambda lhs, rhs: lhs not in rhs,
    "<": operator.lt,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne,
    ">=": operator.ge,
    ">": operator.gt,
}


def _eval_op(lhs: str, op: Op, rhs: str) -> bool:
    try:
        spec = Specifier("".join([op.serialize(), rhs]))
    except InvalidSpecifier:
        pass
    else:
        return spec.contains(lhs, prereleases=True)

    oper: Operator | None = _operators.get(op.serialize())
    if oper is None:
        raise UndefinedComparison(f"Undefined {op!r} on {lhs!r} and {rhs!r}.")

    return oper(lhs, rhs)


def _normalize(*values: str, key: str) -> tuple[str, ...]:
    # PEP 685 ‚Äì Comparison of extra names for optional distribution dependencies
    # https://peps.python.org/pep-0685/
    # > When comparing extra names, tools MUST normalize the names being
    # > compared using the semantics outlined in PEP 503 for names
    if key == "extra":
        return tuple(canonicalize_name(v) for v in values)

    # other environment markers don't have such standards
    return values


def _evaluate_markers(markers: MarkerList, environment: dict[str, str]) -> bool:
    groups: list[list[bool]] = [[]]

    for marker in markers:
        assert isinstance(marker, (list, tuple, str))

        if isinstance(marker, list):
            groups[-1].append(_evaluate_markers(marker, environment))
        elif isinstance(marker, tuple):
            lhs, op, rhs = marker

            if isinstance(lhs, Variable):
                environment_key = lhs.value
                lhs_value = environment[environment_key]
                rhs_value = rhs.value
            else:
                lhs_value = lhs.value
                environment_key = rhs.value
                rhs_value = environment[environment_key]

            lhs_value, rhs_value = _normalize(lhs_value, rhs_value, key=environment_key)
            groups[-1].append(_eval_op(lhs_value, op, rhs_value))
        else:
            assert marker in ["and", "or"]
            if marker == "or":
                groups.append([])

    return any(all(item) for item in groups)


def format_full_version(info: sys._version_info) -> str:
    version = "{0.major}.{0.minor}.{0.micro}".format(info)
    kind = info.releaselevel
    if kind != "final":
        version += kind[0] + str(info.serial)
    return version


def default_environment() -> Environment:
    iver = format_full_version(sys.implementation.version)
    implementation_name = sys.implementation.name
    return {
        "implementation_name": implementation_name,
        "implementation_version": iver,
        "os_name": os.name,
        "platform_machine": platform.machine(),
        "platform_release": platform.release(),
        "platform_system": platform.system(),
        "platform_version": platform.version(),
        "python_full_version": platform.python_version(),
        "platform_python_implementation": platform.python_implementation(),
        "python_version": ".".join(platform.python_version_tuple()[:2]),
        "sys_platform": sys.platform,
    }


class Marker:
    def __init__(self, marker: str) -> None:
        # Note: We create a Marker object without calling this constructor in
        #       packaging.requirements.Requirement. If any additional logic is
        #       added here, make sure to mirror/adapt Requirement.
        try:
            self._markers = _normalize_extra_values(_parse_marker(marker))
            # The attribute `_markers` can be described in terms of a recursive type:
            # MarkerList = List[Union[Tuple[Node, ...], str, MarkerList]]
            #
            # For example, the following expression:
            # python_version > "3.6" or (python_version == "3.6" and os_name == "unix")
            #
            # is parsed into:
            # [
            #     (<Variable('python_version')>, <Op('>')>, <Value('3.6')>),
            #     'and',
            #     [
            #         (<Variable('python_version')>, <Op('==')>, <Value('3.6')>),
            #         'or',
            #         (<Variable('os_name')>, <Op('==')>, <Value('unix')>)
            #     ]
            # ]
        except ParserSyntaxError as e:
            raise InvalidMarker(str(e)) from e

    def __str__(self) -> str:
        return _format_marker(self._markers)

    def __repr__(self) -> str:
        return f"<Marker('{self}')>"

    def __hash__(self) -> int:
        return hash((self.__class__.__name__, str(self)))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Marker):
            return NotImplemented

        return str(self) == str(other)

    def evaluate(self, environment: dict[str, str] | None = None) -> bool:
        """Evaluate a marker.

        Return the boolean from evaluating the given marker against the
        environment. environment is an optional argument to override all or
        part of the determined environment.

        The environment is determined from the current Python process.
        """
        current_environment = cast("dict[str, str]", default_environment())
        current_environment["extra"] = ""
        # Work around platform.python_version() returning something that is not PEP 440
        # compliant for non-tagged Python builds. We preserve default_environment()'s
        # behavior of returning platform.python_version() verbatim, and leave it to the
        # caller to provide a syntactically valid version if they want to override it.
        if current_environment["python_full_version"].endswith("+"):
            current_environment["python_full_version"] += "local"
        if environment is not None:
            current_environment.update(environment)
            # The API used to allow setting extra to None. We need to handle this
            # case for backwards compatibility.
            if current_environment["extra"] is None:
                current_environment["extra"] = ""

        return _evaluate_markers(self._markers, current_environment)
```
```bash
./.venv/lib/python3.9/site-packages/packaging/py.typed
```
```

```
```bash
./.venv/lib/python3.9/site-packages/packaging/_manylinux.py
```
```
from __future__ import annotations

import collections
import contextlib
import functools
import os
import re
import sys
import warnings
from typing import Generator, Iterator, NamedTuple, Sequence

from ._elffile import EIClass, EIData, ELFFile, EMachine

EF_ARM_ABIMASK = 0xFF000000
EF_ARM_ABI_VER5 = 0x05000000
EF_ARM_ABI_FLOAT_HARD = 0x00000400


# `os.PathLike` not a generic type until Python 3.9, so sticking with `str`
# as the type for `path` until then.
@contextlib.contextmanager
def _parse_elf(path: str) -> Generator[ELFFile | None, None, None]:
    try:
        with open(path, "rb") as f:
            yield ELFFile(f)
    except (OSError, TypeError, ValueError):
        yield None


def _is_linux_armhf(executable: str) -> bool:
    # hard-float ABI can be detected from the ELF header of the running
    # process
    # https://static.docs.arm.com/ihi0044/g/aaelf32.pdf
    with _parse_elf(executable) as f:
        return (
            f is not None
            and f.capacity == EIClass.C32
            and f.encoding == EIData.Lsb
            and f.machine == EMachine.Arm
            and f.flags & EF_ARM_ABIMASK == EF_ARM_ABI_VER5
            and f.flags & EF_ARM_ABI_FLOAT_HARD == EF_ARM_ABI_FLOAT_HARD
        )


def _is_linux_i686(executable: str) -> bool:
    with _parse_elf(executable) as f:
        return (
            f is not None
            and f.capacity == EIClass.C32
            and f.encoding == EIData.Lsb
            and f.machine == EMachine.I386
        )


def _have_compatible_abi(executable: str, archs: Sequence[str]) -> bool:
    if "armv7l" in archs:
        return _is_linux_armhf(executable)
    if "i686" in archs:
        return _is_linux_i686(executable)
    allowed_archs = {
        "x86_64",
        "aarch64",
        "ppc64",
        "ppc64le",
        "s390x",
        "loongarch64",
        "riscv64",
    }
    return any(arch in allowed_archs for arch in archs)


# If glibc ever changes its major version, we need to know what the last
# minor version was, so we can build the complete list of all versions.
# For now, guess what the highest minor version might be, assume it will
# be 50 for testing. Once this actually happens, update the dictionary
# with the actual value.
_LAST_GLIBC_MINOR: dict[int, int] = collections.defaultdict(lambda: 50)


class _GLibCVersion(NamedTuple):
    major: int
    minor: int


def _glibc_version_string_confstr() -> str | None:
    """
    Primary implementation of glibc_version_string using os.confstr.
    """
    # os.confstr is quite a bit faster than ctypes.DLL. It's also less likely
    # to be broken or missing. This strategy is used in the standard library
    # platform module.
    # https://github.com/python/cpython/blob/fcf1d003bf4f0100c/Lib/platform.py#L175-L183
    try:
        # Should be a string like "glibc 2.17".
        version_string: str | None = os.confstr("CS_GNU_LIBC_VERSION")
        assert version_string is not None
        _, version = version_string.rsplit()
    except (AssertionError, AttributeError, OSError, ValueError):
        # os.confstr() or CS_GNU_LIBC_VERSION not available (or a bad value)...
        return None
    return version


def _glibc_version_string_ctypes() -> str | None:
    """
    Fallback implementation of glibc_version_string using ctypes.
    """
    try:
        import ctypes
    except ImportError:
        return None

    # ctypes.CDLL(None) internally calls dlopen(NULL), and as the dlopen
    # manpage says, "If filename is NULL, then the returned handle is for the
    # main program". This way we can let the linker do the work to figure out
    # which libc our process is actually using.
    #
    # We must also handle the special case where the executable is not a
    # dynamically linked executable. This can occur when using musl libc,
    # for example. In this situation, dlopen() will error, leading to an
    # OSError. Interestingly, at least in the case of musl, there is no
    # errno set on the OSError. The single string argument used to construct
    # OSError comes from libc itself and is therefore not portable to
    # hard code here. In any case, failure to call dlopen() means we
    # can proceed, so we bail on our attempt.
    try:
        process_namespace = ctypes.CDLL(None)
    except OSError:
        return None

    try:
        gnu_get_libc_version = process_namespace.gnu_get_libc_version
    except AttributeError:
        # Symbol doesn't exist -> therefore, we are not linked to
        # glibc.
        return None

    # Call gnu_get_libc_version, which returns a string like "2.5"
    gnu_get_libc_version.restype = ctypes.c_char_p
    version_str: str = gnu_get_libc_version()
    # py2 / py3 compatibility:
    if not isinstance(version_str, str):
        version_str = version_str.decode("ascii")

    return version_str


def _glibc_version_string() -> str | None:
    """Returns glibc version string, or None if not using glibc."""
    return _glibc_version_string_confstr() or _glibc_version_string_ctypes()


def _parse_glibc_version(version_str: str) -> tuple[int, int]:
    """Parse glibc version.

    We use a regexp instead of str.split because we want to discard any
    random junk that might come after the minor version -- this might happen
    in patched/forked versions of glibc (e.g. Linaro's version of glibc
    uses version strings like "2.20-2014.11"). See gh-3588.
    """
    m = re.match(r"(?P<major>[0-9]+)\.(?P<minor>[0-9]+)", version_str)
    if not m:
        warnings.warn(
            f"Expected glibc version with 2 components major.minor,"
            f" got: {version_str}",
            RuntimeWarning,
        )
        return -1, -1
    return int(m.group("major")), int(m.group("minor"))


@functools.lru_cache
def _get_glibc_version() -> tuple[int, int]:
    version_str = _glibc_version_string()
    if version_str is None:
        return (-1, -1)
    return _parse_glibc_version(version_str)


# From PEP 513, PEP 600
def _is_compatible(arch: str, version: _GLibCVersion) -> bool:
    sys_glibc = _get_glibc_version()
    if sys_glibc < version:
        return False
    # Check for presence of _manylinux module.
    try:
        import _manylinux
    except ImportError:
        return True
    if hasattr(_manylinux, "manylinux_compatible"):
        result = _manylinux.manylinux_compatible(version[0], version[1], arch)
        if result is not None:
            return bool(result)
        return True
    if version == _GLibCVersion(2, 5):
        if hasattr(_manylinux, "manylinux1_compatible"):
            return bool(_manylinux.manylinux1_compatible)
    if version == _GLibCVersion(2, 12):
        if hasattr(_manylinux, "manylinux2010_compatible"):
            return bool(_manylinux.manylinux2010_compatible)
    if version == _GLibCVersion(2, 17):
        if hasattr(_manylinux, "manylinux2014_compatible"):
            return bool(_manylinux.manylinux2014_compatible)
    return True


_LEGACY_MANYLINUX_MAP = {
    # CentOS 7 w/ glibc 2.17 (PEP 599)
    (2, 17): "manylinux2014",
    # CentOS 6 w/ glibc 2.12 (PEP 571)
    (2, 12): "manylinux2010",
    # CentOS 5 w/ glibc 2.5 (PEP 513)
    (2, 5): "manylinux1",
}


def platform_tags(archs: Sequence[str]) -> Iterator[str]:
    """Generate manylinux tags compatible to the current platform.

    :param archs: Sequence of compatible architectures.
        The first one shall be the closest to the actual architecture and be the part of
        platform tag after the ``linux_`` prefix, e.g. ``x86_64``.
        The ``linux_`` prefix is assumed as a prerequisite for the current platform to
        be manylinux-compatible.

    :returns: An iterator of compatible manylinux tags.
    """
    if not _have_compatible_abi(sys.executable, archs):
        return
    # Oldest glibc to be supported regardless of architecture is (2, 17).
    too_old_glibc2 = _GLibCVersion(2, 16)
    if set(archs) & {"x86_64", "i686"}:
        # On x86/i686 also oldest glibc to be supported is (2, 5).
        too_old_glibc2 = _GLibCVersion(2, 4)
    current_glibc = _GLibCVersion(*_get_glibc_version())
    glibc_max_list = [current_glibc]
    # We can assume compatibility across glibc major versions.
    # https://sourceware.org/bugzilla/show_bug.cgi?id=24636
    #
    # Build a list of maximum glibc versions so that we can
    # output the canonical list of all glibc from current_glibc
    # down to too_old_glibc2, including all intermediary versions.
    for glibc_major in range(current_glibc.major - 1, 1, -1):
        glibc_minor = _LAST_GLIBC_MINOR[glibc_major]
        glibc_max_list.append(_GLibCVersion(glibc_major, glibc_minor))
    for arch in archs:
        for glibc_max in glibc_max_list:
            if glibc_max.major == too_old_glibc2.major:
                min_minor = too_old_glibc2.minor
            else:
                # For other glibc major versions oldest supported is (x, 0).
                min_minor = -1
            for glibc_minor in range(glibc_max.minor, min_minor, -1):
                glibc_version = _GLibCVersion(glibc_max.major, glibc_minor)
                tag = "manylinux_{}_{}".format(*glibc_version)
                if _is_compatible(arch, glibc_version):
                    yield f"{tag}_{arch}"
                # Handle the legacy manylinux1, manylinux2010, manylinux2014 tags.
                if glibc_version in _LEGACY_MANYLINUX_MAP:
                    legacy_tag = _LEGACY_MANYLINUX_MAP[glibc_version]
                    if _is_compatible(arch, glibc_version):
                        yield f"{legacy_tag}_{arch}"
```
```bash
./.venv/lib/python3.9/site-packages/packaging/_tokenizer.py
```
```
from __future__ import annotations

import contextlib
import re
from dataclasses import dataclass
from typing import Iterator, NoReturn

from .specifiers import Specifier


@dataclass
class Token:
    name: str
    text: str
    position: int


class ParserSyntaxError(Exception):
    """The provided source text could not be parsed correctly."""

    def __init__(
        self,
        message: str,
        *,
        source: str,
        span: tuple[int, int],
    ) -> None:
        self.span = span
        self.message = message
        self.source = source

        super().__init__()

    def __str__(self) -> str:
        marker = " " * self.span[0] + "~" * (self.span[1] - self.span[0]) + "^"
        return "
    ".join([self.message, self.source, marker])


DEFAULT_RULES: dict[str, str | re.Pattern[str]] = {
    "LEFT_PARENTHESIS": r"\(",
    "RIGHT_PARENTHESIS": r"\)",
    "LEFT_BRACKET": r"\[",
    "RIGHT_BRACKET": r"\]",
    "SEMICOLON": r";",
    "COMMA": r",",
    "QUOTED_STRING": re.compile(
        r"""
            (
                ('[^']*')
                |
                ("[^"]*")
            )
        """,
        re.VERBOSE,
    ),
    "OP": r"(===|==|~=|!=|<=|>=|<|>)",
    "BOOLOP": r"(or|and)",
    "IN": r"in",
    "NOT": r"not",
    "VARIABLE": re.compile(
        r"""
            (
                python_version
                |python_full_version
                |os[._]name
                |sys[._]platform
                |platform_(release|system)
                |platform[._](version|machine|python_implementation)
                |python_implementation
                |implementation_(name|version)
                |extra
            )
        """,
        re.VERBOSE,
    ),
    "SPECIFIER": re.compile(
        Specifier._operator_regex_str + Specifier._version_regex_str,
        re.VERBOSE | re.IGNORECASE,
    ),
    "AT": r"\@",
    "URL": r"[^ 	]+",
    "IDENTIFIER": r"[a-zA-Z0-9][a-zA-Z0-9._-]*",
    "VERSION_PREFIX_TRAIL": r"\.\*",
    "VERSION_LOCAL_LABEL_TRAIL": r"\+[a-z0-9]+(?:[-_\.][a-z0-9]+)*",
    "WS": r"[ 	]+",
    "END": r"$",
}


class Tokenizer:
    """Context-sensitive token parsing.

    Provides methods to examine the input stream to check whether the next token
    matches.
    """

    def __init__(
        self,
        source: str,
        *,
        rules: dict[str, str | re.Pattern[str]],
    ) -> None:
        self.source = source
        self.rules: dict[str, re.Pattern[str]] = {
            name: re.compile(pattern) for name, pattern in rules.items()
        }
        self.next_token: Token | None = None
        self.position = 0

    def consume(self, name: str) -> None:
        """Move beyond provided token name, if at current position."""
        if self.check(name):
            self.read()

    def check(self, name: str, *, peek: bool = False) -> bool:
        """Check whether the next token has the provided name.

        By default, if the check succeeds, the token *must* be read before
        another check. If `peek` is set to `True`, the token is not loaded and
        would need to be checked again.
        """
        assert (
            self.next_token is None
        ), f"Cannot check for {name!r}, already have {self.next_token!r}"
        assert name in self.rules, f"Unknown token name: {name!r}"

        expression = self.rules[name]

        match = expression.match(self.source, self.position)
        if match is None:
            return False
        if not peek:
            self.next_token = Token(name, match[0], self.position)
        return True

    def expect(self, name: str, *, expected: str) -> Token:
        """Expect a certain token name next, failing with a syntax error otherwise.

        The token is *not* read.
        """
        if not self.check(name):
            raise self.raise_syntax_error(f"Expected {expected}")
        return self.read()

    def read(self) -> Token:
        """Consume the next token and return it."""
        token = self.next_token
        assert token is not None

        self.position += len(token.text)
        self.next_token = None

        return token

    def raise_syntax_error(
        self,
        message: str,
        *,
        span_start: int | None = None,
        span_end: int | None = None,
    ) -> NoReturn:
        """Raise ParserSyntaxError at the given position."""
        span = (
            self.position if span_start is None else span_start,
            self.position if span_end is None else span_end,
        )
        raise ParserSyntaxError(
            message,
            source=self.source,
            span=span,
        )

    @contextlib.contextmanager
    def enclosing_tokens(
        self, open_token: str, close_token: str, *, around: str
    ) -> Iterator[None]:
        if self.check(open_token):
            open_position = self.position
            self.read()
        else:
            open_position = None

        yield

        if open_position is None:
            return

        if not self.check(close_token):
            self.raise_syntax_error(
                f"Expected matching {close_token} for {open_token}, after {around}",
                span_start=open_position,
            )

        self.read()
```
```bash
./.venv/lib/python3.9/site-packages/packaging/specifiers.py
```
```
# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.
"""
.. testsetup::

    from packaging.specifiers import Specifier, SpecifierSet, InvalidSpecifier
    from packaging.version import Version
"""

from __future__ import annotations

import abc
import itertools
import re
from typing import Callable, Iterable, Iterator, TypeVar, Union

from .utils import canonicalize_version
from .version import Version

UnparsedVersion = Union[Version, str]
UnparsedVersionVar = TypeVar("UnparsedVersionVar", bound=UnparsedVersion)
CallableOperator = Callable[[Version, str], bool]


def _coerce_version(version: UnparsedVersion) -> Version:
    if not isinstance(version, Version):
        version = Version(version)
    return version


class InvalidSpecifier(ValueError):
    """
    Raised when attempting to create a :class:`Specifier` with a specifier
    string that is invalid.

    >>> Specifier("lolwat")
    Traceback (most recent call last):
        ...
    packaging.specifiers.InvalidSpecifier: Invalid specifier: 'lolwat'
    """


class BaseSpecifier(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __str__(self) -> str:
        """
        Returns the str representation of this Specifier-like object. This
        should be representative of the Specifier itself.
        """

    @abc.abstractmethod
    def __hash__(self) -> int:
        """
        Returns a hash value for this Specifier-like object.
        """

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        """
        Returns a boolean representing whether or not the two Specifier-like
        objects are equal.

        :param other: The other object to check against.
        """

    @property
    @abc.abstractmethod
    def prereleases(self) -> bool | None:
        """Whether or not pre-releases as a whole are allowed.

        This can be set to either ``True`` or ``False`` to explicitly enable or disable
        prereleases or it can be set to ``None`` (the default) to use default semantics.
        """

    @prereleases.setter
    def prereleases(self, value: bool) -> None:
        """Setter for :attr:`prereleases`.

        :param value: The value to set.
        """

    @abc.abstractmethod
    def contains(self, item: str, prereleases: bool | None = None) -> bool:
        """
        Determines if the given item is contained within this specifier.
        """

    @abc.abstractmethod
    def filter(
        self, iterable: Iterable[UnparsedVersionVar], prereleases: bool | None = None
    ) -> Iterator[UnparsedVersionVar]:
        """
        Takes an iterable of items and filters them so that only items which
        are contained within this specifier are allowed in it.
        """


class Specifier(BaseSpecifier):
    """This class abstracts handling of version specifiers.

    .. tip::

        It is generally not required to instantiate this manually. You should instead
        prefer to work with :class:`SpecifierSet` instead, which can parse
        comma-separated version specifiers (which is what package metadata contains).
    """

    _operator_regex_str = r"""
        (?P<operator>(~=|==|!=|<=|>=|<|>|===))
        """
    _version_regex_str = r"""
        (?P<version>
            (?:
                # The identity operators allow for an escape hatch that will
                # do an exact string match of the version you wish to install.
                # This will not be parsed by PEP 440 and we cannot determine
                # any semantic meaning from it. This operator is discouraged
                # but included entirely as an escape hatch.
                (?<====)  # Only match for the identity operator
                \s*
                [^\s;)]*  # The arbitrary version can be just about anything,
                          # we match everything except for whitespace, a
                          # semi-colon for marker support, and a closing paren
                          # since versions can be enclosed in them.
            )
            |
            (?:
                # The (non)equality operators allow for wild card and local
                # versions to be specified so we have to define these two
                # operators separately to enable that.
                (?<===|!=)            # Only match for equals and not equals

                \s*
                v?
                (?:[0-9]+!)?          # epoch
                [0-9]+(?:\.[0-9]+)*   # release

                # You cannot use a wild card and a pre-release, post-release, a dev or
                # local version together so group them with a | and make them optional.
                (?:
                    \.\*  # Wild card syntax of .*
                    |
                    (?:                                  # pre release
                        [-_\.]?
                        (alpha|beta|preview|pre|a|b|c|rc)
                        [-_\.]?
                        [0-9]*
                    )?
                    (?:                                  # post release
                        (?:-[0-9]+)|(?:[-_\.]?(post|rev|r)[-_\.]?[0-9]*)
                    )?
                    (?:[-_\.]?dev[-_\.]?[0-9]*)?         # dev release
                    (?:\+[a-z0-9]+(?:[-_\.][a-z0-9]+)*)? # local
                )?
            )
            |
            (?:
                # The compatible operator requires at least two digits in the
                # release segment.
                (?<=~=)               # Only match for the compatible operator

                \s*
                v?
                (?:[0-9]+!)?          # epoch
                [0-9]+(?:\.[0-9]+)+   # release  (We have a + instead of a *)
                (?:                   # pre release
                    [-_\.]?
                    (alpha|beta|preview|pre|a|b|c|rc)
                    [-_\.]?
                    [0-9]*
                )?
                (?:                                   # post release
                    (?:-[0-9]+)|(?:[-_\.]?(post|rev|r)[-_\.]?[0-9]*)
                )?
                (?:[-_\.]?dev[-_\.]?[0-9]*)?          # dev release
            )
            |
            (?:
                # All other operators only allow a sub set of what the
                # (non)equality operators do. Specifically they do not allow
                # local versions to be specified nor do they allow the prefix
                # matching wild cards.
                (?<!==|!=|~=)         # We have special cases for these
                                      # operators so we want to make sure they
                                      # don't match here.

                \s*
                v?
                (?:[0-9]+!)?          # epoch
                [0-9]+(?:\.[0-9]+)*   # release
                (?:                   # pre release
                    [-_\.]?
                    (alpha|beta|preview|pre|a|b|c|rc)
                    [-_\.]?
                    [0-9]*
                )?
                (?:                                   # post release
                    (?:-[0-9]+)|(?:[-_\.]?(post|rev|r)[-_\.]?[0-9]*)
                )?
                (?:[-_\.]?dev[-_\.]?[0-9]*)?          # dev release
            )
        )
        """

    _regex = re.compile(
        r"^\s*" + _operator_regex_str + _version_regex_str + r"\s*$",
        re.VERBOSE | re.IGNORECASE,
    )

    _operators = {
        "~=": "compatible",
        "==": "equal",
        "!=": "not_equal",
        "<=": "less_than_equal",
        ">=": "greater_than_equal",
        "<": "less_than",
        ">": "greater_than",
        "===": "arbitrary",
    }

    def __init__(self, spec: str = "", prereleases: bool | None = None) -> None:
        """Initialize a Specifier instance.

        :param spec:
            The string representation of a specifier which will be parsed and
            normalized before use.
        :param prereleases:
            This tells the specifier if it should accept prerelease versions if
            applicable or not. The default of ``None`` will autodetect it from the
            given specifiers.
        :raises InvalidSpecifier:
            If the given specifier is invalid (i.e. bad syntax).
        """
        match = self._regex.search(spec)
        if not match:
            raise InvalidSpecifier(f"Invalid specifier: '{spec}'")

        self._spec: tuple[str, str] = (
            match.group("operator").strip(),
            match.group("version").strip(),
        )

        # Store whether or not this Specifier should accept prereleases
        self._prereleases = prereleases

    # https://github.com/python/mypy/pull/13475#pullrequestreview-1079784515
    @property  # type: ignore[override]
    def prereleases(self) -> bool:
        # If there is an explicit prereleases set for this, then we'll just
        # blindly use that.
        if self._prereleases is not None:
            return self._prereleases

        # Look at all of our specifiers and determine if they are inclusive
        # operators, and if they are if they are including an explicit
        # prerelease.
        operator, version = self._spec
        if operator in ["==", ">=", "<=", "~=", "==="]:
            # The == specifier can include a trailing .*, if it does we
            # want to remove before parsing.
            if operator == "==" and version.endswith(".*"):
                version = version[:-2]

            # Parse the version, and if it is a pre-release than this
            # specifier allows pre-releases.
            if Version(version).is_prerelease:
                return True

        return False

    @prereleases.setter
    def prereleases(self, value: bool) -> None:
        self._prereleases = value

    @property
    def operator(self) -> str:
        """The operator of this specifier.

        >>> Specifier("==1.2.3").operator
        '=='
        """
        return self._spec[0]

    @property
    def version(self) -> str:
        """The version of this specifier.

        >>> Specifier("==1.2.3").version
        '1.2.3'
        """
        return self._spec[1]

    def __repr__(self) -> str:
        """A representation of the Specifier that shows all internal state.

        >>> Specifier('>=1.0.0')
        <Specifier('>=1.0.0')>
        >>> Specifier('>=1.0.0', prereleases=False)
        <Specifier('>=1.0.0', prereleases=False)>
        >>> Specifier('>=1.0.0', prereleases=True)
        <Specifier('>=1.0.0', prereleases=True)>
        """
        pre = (
            f", prereleases={self.prereleases!r}"
            if self._prereleases is not None
            else ""
        )

        return f"<{self.__class__.__name__}({str(self)!r}{pre})>"

    def __str__(self) -> str:
        """A string representation of the Specifier that can be round-tripped.

        >>> str(Specifier('>=1.0.0'))
        '>=1.0.0'
        >>> str(Specifier('>=1.0.0', prereleases=False))
        '>=1.0.0'
        """
        return "{}{}".format(*self._spec)

    @property
    def _canonical_spec(self) -> tuple[str, str]:
        canonical_version = canonicalize_version(
            self._spec[1],
            strip_trailing_zero=(self._spec[0] != "~="),
        )
        return self._spec[0], canonical_version

    def __hash__(self) -> int:
        return hash(self._canonical_spec)

    def __eq__(self, other: object) -> bool:
        """Whether or not the two Specifier-like objects are equal.

        :param other: The other object to check against.

        The value of :attr:`prereleases` is ignored.

        >>> Specifier("==1.2.3") == Specifier("== 1.2.3.0")
        True
        >>> (Specifier("==1.2.3", prereleases=False) ==
        ...  Specifier("==1.2.3", prereleases=True))
        True
        >>> Specifier("==1.2.3") == "==1.2.3"
        True
        >>> Specifier("==1.2.3") == Specifier("==1.2.4")
        False
        >>> Specifier("==1.2.3") == Specifier("~=1.2.3")
        False
        """
        if isinstance(other, str):
            try:
                other = self.__class__(str(other))
            except InvalidSpecifier:
                return NotImplemented
        elif not isinstance(other, self.__class__):
            return NotImplemented

        return self._canonical_spec == other._canonical_spec

    def _get_operator(self, op: str) -> CallableOperator:
        operator_callable: CallableOperator = getattr(
            self, f"_compare_{self._operators[op]}"
        )
        return operator_callable

    def _compare_compatible(self, prospective: Version, spec: str) -> bool:
        # Compatible releases have an equivalent combination of >= and ==. That
        # is that ~=2.2 is equivalent to >=2.2,==2.*. This allows us to
        # implement this in terms of the other specifiers instead of
        # implementing it ourselves. The only thing we need to do is construct
        # the other specifiers.

        # We want everything but the last item in the version, but we want to
        # ignore suffix segments.
        prefix = _version_join(
            list(itertools.takewhile(_is_not_suffix, _version_split(spec)))[:-1]
        )

        # Add the prefix notation to the end of our string
        prefix += ".*"

        return self._get_operator(">=")(prospective, spec) and self._get_operator("==")(
            prospective, prefix
        )

    def _compare_equal(self, prospective: Version, spec: str) -> bool:
        # We need special logic to handle prefix matching
        if spec.endswith(".*"):
            # In the case of prefix matching we want to ignore local segment.
            normalized_prospective = canonicalize_version(
                prospective.public, strip_trailing_zero=False
            )
            # Get the normalized version string ignoring the trailing .*
            normalized_spec = canonicalize_version(spec[:-2], strip_trailing_zero=False)
            # Split the spec out by bangs and dots, and pretend that there is
            # an implicit dot in between a release segment and a pre-release segment.
            split_spec = _version_split(normalized_spec)

            # Split the prospective version out by bangs and dots, and pretend
            # that there is an implicit dot in between a release segment and
            # a pre-release segment.
            split_prospective = _version_split(normalized_prospective)

            # 0-pad the prospective version before shortening it to get the correct
            # shortened version.
            padded_prospective, _ = _pad_version(split_prospective, split_spec)

            # Shorten the prospective version to be the same length as the spec
            # so that we can determine if the specifier is a prefix of the
            # prospective version or not.
            shortened_prospective = padded_prospective[: len(split_spec)]

            return shortened_prospective == split_spec
        else:
            # Convert our spec string into a Version
            spec_version = Version(spec)

            # If the specifier does not have a local segment, then we want to
            # act as if the prospective version also does not have a local
            # segment.
            if not spec_version.local:
                prospective = Version(prospective.public)

            return prospective == spec_version

    def _compare_not_equal(self, prospective: Version, spec: str) -> bool:
        return not self._compare_equal(prospective, spec)

    def _compare_less_than_equal(self, prospective: Version, spec: str) -> bool:
        # NB: Local version identifiers are NOT permitted in the version
        # specifier, so local version labels can be universally removed from
        # the prospective version.
        return Version(prospective.public) <= Version(spec)

    def _compare_greater_than_equal(self, prospective: Version, spec: str) -> bool:
        # NB: Local version identifiers are NOT permitted in the version
        # specifier, so local version labels can be universally removed from
        # the prospective version.
        return Version(prospective.public) >= Version(spec)

    def _compare_less_than(self, prospective: Version, spec_str: str) -> bool:
        # Convert our spec to a Version instance, since we'll want to work with
        # it as a version.
        spec = Version(spec_str)

        # Check to see if the prospective version is less than the spec
        # version. If it's not we can short circuit and just return False now
        # instead of doing extra unneeded work.
        if not prospective < spec:
            return False

        # This special case is here so that, unless the specifier itself
        # includes is a pre-release version, that we do not accept pre-release
        # versions for the version mentioned in the specifier (e.g. <3.1 should
        # not match 3.1.dev0, but should match 3.0.dev0).
        if not spec.is_prerelease and prospective.is_prerelease:
            if Version(prospective.base_version) == Version(spec.base_version):
                return False

        # If we've gotten to here, it means that prospective version is both
        # less than the spec version *and* it's not a pre-release of the same
        # version in the spec.
        return True

    def _compare_greater_than(self, prospective: Version, spec_str: str) -> bool:
        # Convert our spec to a Version instance, since we'll want to work with
        # it as a version.
        spec = Version(spec_str)

        # Check to see if the prospective version is greater than the spec
        # version. If it's not we can short circuit and just return False now
        # instead of doing extra unneeded work.
        if not prospective > spec:
            return False

        # This special case is here so that, unless the specifier itself
        # includes is a post-release version, that we do not accept
        # post-release versions for the version mentioned in the specifier
        # (e.g. >3.1 should not match 3.0.post0, but should match 3.2.post0).
        if not spec.is_postrelease and prospective.is_postrelease:
            if Version(prospective.base_version) == Version(spec.base_version):
                return False

        # Ensure that we do not allow a local version of the version mentioned
        # in the specifier, which is technically greater than, to match.
        if prospective.local is not None:
            if Version(prospective.base_version) == Version(spec.base_version):
                return False

        # If we've gotten to here, it means that prospective version is both
        # greater than the spec version *and* it's not a pre-release of the
        # same version in the spec.
        return True

    def _compare_arbitrary(self, prospective: Version, spec: str) -> bool:
        return str(prospective).lower() == str(spec).lower()

    def __contains__(self, item: str | Version) -> bool:
        """Return whether or not the item is contained in this specifier.

        :param item: The item to check for.

        This is used for the ``in`` operator and behaves the same as
        :meth:`contains` with no ``prereleases`` argument passed.

        >>> "1.2.3" in Specifier(">=1.2.3")
        True
        >>> Version("1.2.3") in Specifier(">=1.2.3")
        True
        >>> "1.0.0" in Specifier(">=1.2.3")
        False
        >>> "1.3.0a1" in Specifier(">=1.2.3")
        False
        >>> "1.3.0a1" in Specifier(">=1.2.3", prereleases=True)
        True
        """
        return self.contains(item)

    def contains(self, item: UnparsedVersion, prereleases: bool | None = None) -> bool:
        """Return whether or not the item is contained in this specifier.

        :param item:
            The item to check for, which can be a version string or a
            :class:`Version` instance.
        :param prereleases:
            Whether or not to match prereleases with this Specifier. If set to
            ``None`` (the default), it uses :attr:`prereleases` to determine
            whether or not prereleases are allowed.

        >>> Specifier(">=1.2.3").contains("1.2.3")
        True
        >>> Specifier(">=1.2.3").contains(Version("1.2.3"))
        True
        >>> Specifier(">=1.2.3").contains("1.0.0")
        False
        >>> Specifier(">=1.2.3").contains("1.3.0a1")
        False
        >>> Specifier(">=1.2.3", prereleases=True).contains("1.3.0a1")
        True
        >>> Specifier(">=1.2.3").contains("1.3.0a1", prereleases=True)
        True
        """

        # Determine if prereleases are to be allowed or not.
        if prereleases is None:
            prereleases = self.prereleases

        # Normalize item to a Version, this allows us to have a shortcut for
        # "2.0" in Specifier(">=2")
        normalized_item = _coerce_version(item)

        # Determine if we should be supporting prereleases in this specifier
        # or not, if we do not support prereleases than we can short circuit
        # logic if this version is a prereleases.
        if normalized_item.is_prerelease and not prereleases:
            return False

        # Actually do the comparison to determine if this item is contained
        # within this Specifier or not.
        operator_callable: CallableOperator = self._get_operator(self.operator)
        return operator_callable(normalized_item, self.version)

    def filter(
        self, iterable: Iterable[UnparsedVersionVar], prereleases: bool | None = None
    ) -> Iterator[UnparsedVersionVar]:
        """Filter items in the given iterable, that match the specifier.

        :param iterable:
            An iterable that can contain version strings and :class:`Version` instances.
            The items in the iterable will be filtered according to the specifier.
        :param prereleases:
            Whether or not to allow prereleases in the returned iterator. If set to
            ``None`` (the default), it will be intelligently decide whether to allow
            prereleases or not (based on the :attr:`prereleases` attribute, and
            whether the only versions matching are prereleases).

        This method is smarter than just ``filter(Specifier().contains, [...])``
        because it implements the rule from :pep:`440` that a prerelease item
        SHOULD be accepted if no other versions match the given specifier.

        >>> list(Specifier(">=1.2.3").filter(["1.2", "1.3", "1.5a1"]))
        ['1.3']
        >>> list(Specifier(">=1.2.3").filter(["1.2", "1.2.3", "1.3", Version("1.4")]))
        ['1.2.3', '1.3', <Version('1.4')>]
        >>> list(Specifier(">=1.2.3").filter(["1.2", "1.5a1"]))
        ['1.5a1']
        >>> list(Specifier(">=1.2.3").filter(["1.3", "1.5a1"], prereleases=True))
        ['1.3', '1.5a1']
        >>> list(Specifier(">=1.2.3", prereleases=True).filter(["1.3", "1.5a1"]))
        ['1.3', '1.5a1']
        """

        yielded = False
        found_prereleases = []

        kw = {"prereleases": prereleases if prereleases is not None else True}

        # Attempt to iterate over all the values in the iterable and if any of
        # them match, yield them.
        for version in iterable:
            parsed_version = _coerce_version(version)

            if self.contains(parsed_version, **kw):
                # If our version is a prerelease, and we were not set to allow
                # prereleases, then we'll store it for later in case nothing
                # else matches this specifier.
                if parsed_version.is_prerelease and not (
                    prereleases or self.prereleases
                ):
                    found_prereleases.append(version)
                # Either this is not a prerelease, or we should have been
                # accepting prereleases from the beginning.
                else:
                    yielded = True
                    yield version

        # Now that we've iterated over everything, determine if we've yielded
        # any values, and if we have not and we have any prereleases stored up
        # then we will go ahead and yield the prereleases.
        if not yielded and found_prereleases:
            for version in found_prereleases:
                yield version


_prefix_regex = re.compile(r"^([0-9]+)((?:a|b|c|rc)[0-9]+)$")


def _version_split(version: str) -> list[str]:
    """Split version into components.

    The split components are intended for version comparison. The logic does
    not attempt to retain the original version string, so joining the
    components back with :func:`_version_join` may not produce the original
    version string.
    """
    result: list[str] = []

    epoch, _, rest = version.rpartition("!")
    result.append(epoch or "0")

    for item in rest.split("."):
        match = _prefix_regex.search(item)
        if match:
            result.extend(match.groups())
        else:
            result.append(item)
    return result


def _version_join(components: list[str]) -> str:
    """Join split version components into a version string.

    This function assumes the input came from :func:`_version_split`, where the
    first component must be the epoch (either empty or numeric), and all other
    components numeric.
    """
    epoch, *rest = components
    return f"{epoch}!{'.'.join(rest)}"


def _is_not_suffix(segment: str) -> bool:
    return not any(
        segment.startswith(prefix) for prefix in ("dev", "a", "b", "rc", "post")
    )


def _pad_version(left: list[str], right: list[str]) -> tuple[list[str], list[str]]:
    left_split, right_split = [], []

    # Get the release segment of our versions
    left_split.append(list(itertools.takewhile(lambda x: x.isdigit(), left)))
    right_split.append(list(itertools.takewhile(lambda x: x.isdigit(), right)))

    # Get the rest of our versions
    left_split.append(left[len(left_split[0]) :])
    right_split.append(right[len(right_split[0]) :])

    # Insert our padding
    left_split.insert(1, ["0"] * max(0, len(right_split[0]) - len(left_split[0])))
    right_split.insert(1, ["0"] * max(0, len(left_split[0]) - len(right_split[0])))

    return (
        list(itertools.chain.from_iterable(left_split)),
        list(itertools.chain.from_iterable(right_split)),
    )


class SpecifierSet(BaseSpecifier):
    """This class abstracts handling of a set of version specifiers.

    It can be passed a single specifier (``>=3.0``), a comma-separated list of
    specifiers (``>=3.0,!=3.1``), or no specifier at all.
    """

    def __init__(self, specifiers: str = "", prereleases: bool | None = None) -> None:
        """Initialize a SpecifierSet instance.

        :param specifiers:
            The string representation of a specifier or a comma-separated list of
            specifiers which will be parsed and normalized before use.
        :param prereleases:
            This tells the SpecifierSet if it should accept prerelease versions if
            applicable or not. The default of ``None`` will autodetect it from the
            given specifiers.

        :raises InvalidSpecifier:
            If the given ``specifiers`` are not parseable than this exception will be
            raised.
        """

        # Split on `,` to break each individual specifier into it's own item, and
        # strip each item to remove leading/trailing whitespace.
        split_specifiers = [s.strip() for s in specifiers.split(",") if s.strip()]

        # Make each individual specifier a Specifier and save in a frozen set for later.
        self._specs = frozenset(map(Specifier, split_specifiers))

        # Store our prereleases value so we can use it later to determine if
        # we accept prereleases or not.
        self._prereleases = prereleases

    @property
    def prereleases(self) -> bool | None:
        # If we have been given an explicit prerelease modifier, then we'll
        # pass that through here.
        if self._prereleases is not None:
            return self._prereleases

        # If we don't have any specifiers, and we don't have a forced value,
        # then we'll just return None since we don't know if this should have
        # pre-releases or not.
        if not self._specs:
            return None

        # Otherwise we'll see if any of the given specifiers accept
        # prereleases, if any of them do we'll return True, otherwise False.
        return any(s.prereleases for s in self._specs)

    @prereleases.setter
    def prereleases(self, value: bool) -> None:
        self._prereleases = value

    def __repr__(self) -> str:
        """A representation of the specifier set that shows all internal state.

        Note that the ordering of the individual specifiers within the set may not
        match the input string.

        >>> SpecifierSet('>=1.0.0,!=2.0.0')
        <SpecifierSet('!=2.0.0,>=1.0.0')>
        >>> SpecifierSet('>=1.0.0,!=2.0.0', prereleases=False)
        <SpecifierSet('!=2.0.0,>=1.0.0', prereleases=False)>
        >>> SpecifierSet('>=1.0.0,!=2.0.0', prereleases=True)
        <SpecifierSet('!=2.0.0,>=1.0.0', prereleases=True)>
        """
        pre = (
            f", prereleases={self.prereleases!r}"
            if self._prereleases is not None
            else ""
        )

        return f"<SpecifierSet({str(self)!r}{pre})>"

    def __str__(self) -> str:
        """A string representation of the specifier set that can be round-tripped.

        Note that the ordering of the individual specifiers within the set may not
        match the input string.

        >>> str(SpecifierSet(">=1.0.0,!=1.0.1"))
        '!=1.0.1,>=1.0.0'
        >>> str(SpecifierSet(">=1.0.0,!=1.0.1", prereleases=False))
        '!=1.0.1,>=1.0.0'
        """
        return ",".join(sorted(str(s) for s in self._specs))

    def __hash__(self) -> int:
        return hash(self._specs)

    def __and__(self, other: SpecifierSet | str) -> SpecifierSet:
        """Return a SpecifierSet which is a combination of the two sets.

        :param other: The other object to combine with.

        >>> SpecifierSet(">=1.0.0,!=1.0.1") & '<=2.0.0,!=2.0.1'
        <SpecifierSet('!=1.0.1,!=2.0.1,<=2.0.0,>=1.0.0')>
        >>> SpecifierSet(">=1.0.0,!=1.0.1") & SpecifierSet('<=2.0.0,!=2.0.1')
        <SpecifierSet('!=1.0.1,!=2.0.1,<=2.0.0,>=1.0.0')>
        """
        if isinstance(other, str):
            other = SpecifierSet(other)
        elif not isinstance(other, SpecifierSet):
            return NotImplemented

        specifier = SpecifierSet()
        specifier._specs = frozenset(self._specs | other._specs)

        if self._prereleases is None and other._prereleases is not None:
            specifier._prereleases = other._prereleases
        elif self._prereleases is not None and other._prereleases is None:
            specifier._prereleases = self._prereleases
        elif self._prereleases == other._prereleases:
            specifier._prereleases = self._prereleases
        else:
            raise ValueError(
                "Cannot combine SpecifierSets with True and False prerelease "
                "overrides."
            )

        return specifier

    def __eq__(self, other: object) -> bool:
        """Whether or not the two SpecifierSet-like objects are equal.

        :param other: The other object to check against.

        The value of :attr:`prereleases` is ignored.

        >>> SpecifierSet(">=1.0.0,!=1.0.1") == SpecifierSet(">=1.0.0,!=1.0.1")
        True
        >>> (SpecifierSet(">=1.0.0,!=1.0.1", prereleases=False) ==
        ...  SpecifierSet(">=1.0.0,!=1.0.1", prereleases=True))
        True
        >>> SpecifierSet(">=1.0.0,!=1.0.1") == ">=1.0.0,!=1.0.1"
        True
        >>> SpecifierSet(">=1.0.0,!=1.0.1") == SpecifierSet(">=1.0.0")
        False
        >>> SpecifierSet(">=1.0.0,!=1.0.1") == SpecifierSet(">=1.0.0,!=1.0.2")
        False
        """
        if isinstance(other, (str, Specifier)):
            other = SpecifierSet(str(other))
        elif not isinstance(other, SpecifierSet):
            return NotImplemented

        return self._specs == other._specs

    def __len__(self) -> int:
        """Returns the number of specifiers in this specifier set."""
        return len(self._specs)

    def __iter__(self) -> Iterator[Specifier]:
        """
        Returns an iterator over all the underlying :class:`Specifier` instances
        in this specifier set.

        >>> sorted(SpecifierSet(">=1.0.0,!=1.0.1"), key=str)
        [<Specifier('!=1.0.1')>, <Specifier('>=1.0.0')>]
        """
        return iter(self._specs)

    def __contains__(self, item: UnparsedVersion) -> bool:
        """Return whether or not the item is contained in this specifier.

        :param item: The item to check for.

        This is used for the ``in`` operator and behaves the same as
        :meth:`contains` with no ``prereleases`` argument passed.

        >>> "1.2.3" in SpecifierSet(">=1.0.0,!=1.0.1")
        True
        >>> Version("1.2.3") in SpecifierSet(">=1.0.0,!=1.0.1")
        True
        >>> "1.0.1" in SpecifierSet(">=1.0.0,!=1.0.1")
        False
        >>> "1.3.0a1" in SpecifierSet(">=1.0.0,!=1.0.1")
        False
        >>> "1.3.0a1" in SpecifierSet(">=1.0.0,!=1.0.1", prereleases=True)
        True
        """
        return self.contains(item)

    def contains(
        self,
        item: UnparsedVersion,
        prereleases: bool | None = None,
        installed: bool | None = None,
    ) -> bool:
        """Return whether or not the item is contained in this SpecifierSet.

        :param item:
            The item to check for, which can be a version string or a
            :class:`Version` instance.
        :param prereleases:
            Whether or not to match prereleases with this SpecifierSet. If set to
            ``None`` (the default), it uses :attr:`prereleases` to determine
            whether or not prereleases are allowed.

        >>> SpecifierSet(">=1.0.0,!=1.0.1").contains("1.2.3")
        True
        >>> SpecifierSet(">=1.0.0,!=1.0.1").contains(Version("1.2.3"))
        True
        >>> SpecifierSet(">=1.0.0,!=1.0.1").contains("1.0.1")
        False
        >>> SpecifierSet(">=1.0.0,!=1.0.1").contains("1.3.0a1")
        False
        >>> SpecifierSet(">=1.0.0,!=1.0.1", prereleases=True).contains("1.3.0a1")
        True
        >>> SpecifierSet(">=1.0.0,!=1.0.1").contains("1.3.0a1", prereleases=True)
        True
        """
        # Ensure that our item is a Version instance.
        if not isinstance(item, Version):
            item = Version(item)

        # Determine if we're forcing a prerelease or not, if we're not forcing
        # one for this particular filter call, then we'll use whatever the
        # SpecifierSet thinks for whether or not we should support prereleases.
        if prereleases is None:
            prereleases = self.prereleases

        # We can determine if we're going to allow pre-releases by looking to
        # see if any of the underlying items supports them. If none of them do
        # and this item is a pre-release then we do not allow it and we can
        # short circuit that here.
        # Note: This means that 1.0.dev1 would not be contained in something
        #       like >=1.0.devabc however it would be in >=1.0.debabc,>0.0.dev0
        if not prereleases and item.is_prerelease:
            return False

        if installed and item.is_prerelease:
            item = Version(item.base_version)

        # We simply dispatch to the underlying specs here to make sure that the
        # given version is contained within all of them.
        # Note: This use of all() here means that an empty set of specifiers
        #       will always return True, this is an explicit design decision.
        return all(s.contains(item, prereleases=prereleases) for s in self._specs)

    def filter(
        self, iterable: Iterable[UnparsedVersionVar], prereleases: bool | None = None
    ) -> Iterator[UnparsedVersionVar]:
        """Filter items in the given iterable, that match the specifiers in this set.

        :param iterable:
            An iterable that can contain version strings and :class:`Version` instances.
            The items in the iterable will be filtered according to the specifier.
        :param prereleases:
            Whether or not to allow prereleases in the returned iterator. If set to
            ``None`` (the default), it will be intelligently decide whether to allow
            prereleases or not (based on the :attr:`prereleases` attribute, and
            whether the only versions matching are prereleases).

        This method is smarter than just ``filter(SpecifierSet(...).contains, [...])``
        because it implements the rule from :pep:`440` that a prerelease item
        SHOULD be accepted if no other versions match the given specifier.

        >>> list(SpecifierSet(">=1.2.3").filter(["1.2", "1.3", "1.5a1"]))
        ['1.3']
        >>> list(SpecifierSet(">=1.2.3").filter(["1.2", "1.3", Version("1.4")]))
        ['1.3', <Version('1.4')>]
        >>> list(SpecifierSet(">=1.2.3").filter(["1.2", "1.5a1"]))
        []
        >>> list(SpecifierSet(">=1.2.3").filter(["1.3", "1.5a1"], prereleases=True))
        ['1.3', '1.5a1']
        >>> list(SpecifierSet(">=1.2.3", prereleases=True).filter(["1.3", "1.5a1"]))
        ['1.3', '1.5a1']

        An "empty" SpecifierSet will filter items based on the presence of prerelease
        versions in the set.

        >>> list(SpecifierSet("").filter(["1.3", "1.5a1"]))
        ['1.3']
        >>> list(SpecifierSet("").filter(["1.5a1"]))
        ['1.5a1']
        >>> list(SpecifierSet("", prereleases=True).filter(["1.3", "1.5a1"]))
        ['1.3', '1.5a1']
        >>> list(SpecifierSet("").filter(["1.3", "1.5a1"], prereleases=True))
        ['1.3', '1.5a1']
        """
        # Determine if we're forcing a prerelease or not, if we're not forcing
        # one for this particular filter call, then we'll use whatever the
        # SpecifierSet thinks for whether or not we should support prereleases.
        if prereleases is None:
            prereleases = self.prereleases

        # If we have any specifiers, then we want to wrap our iterable in the
        # filter method for each one, this will act as a logical AND amongst
        # each specifier.
        if self._specs:
            for spec in self._specs:
                iterable = spec.filter(iterable, prereleases=bool(prereleases))
            return iter(iterable)
        # If we do not have any specifiers, then we need to have a rough filter
        # which will filter out any pre-releases, unless there are no final
        # releases.
        else:
            filtered: list[UnparsedVersionVar] = []
            found_prereleases: list[UnparsedVersionVar] = []

            for item in iterable:
                parsed_version = _coerce_version(item)

                # Store any item which is a pre-release for later unless we've
                # already found a final version or we are accepting prereleases
                if parsed_version.is_prerelease and not prereleases:
                    if not filtered:
                        found_prereleases.append(item)
                else:
                    filtered.append(item)

            # If we've found no items except for pre-releases, then we'll go
            # ahead and use the pre-releases
            if not filtered and found_prereleases and prereleases is None:
                return iter(found_prereleases)

            return iter(filtered)
```
```bash
./.venv/lib/python3.9/site-packages/packaging/_elffile.py
```
```
"""
ELF file parser.

This provides a class ``ELFFile`` that parses an ELF executable in a similar
interface to ``ZipFile``. Only the read interface is implemented.

Based on: https://gist.github.com/lyssdod/f51579ae8d93c8657a5564aefc2ffbca
ELF header: https://refspecs.linuxfoundation.org/elf/gabi4+/ch4.eheader.html
"""

from __future__ import annotations

import enum
import os
import struct
from typing import IO


class ELFInvalid(ValueError):
    pass


class EIClass(enum.IntEnum):
    C32 = 1
    C64 = 2


class EIData(enum.IntEnum):
    Lsb = 1
    Msb = 2


class EMachine(enum.IntEnum):
    I386 = 3
    S390 = 22
    Arm = 40
    X8664 = 62
    AArc64 = 183


class ELFFile:
    """
    Representation of an ELF executable.
    """

    def __init__(self, f: IO[bytes]) -> None:
        self._f = f

        try:
            ident = self._read("16B")
        except struct.error:
            raise ELFInvalid("unable to parse identification")
        magic = bytes(ident[:4])
        if magic != b"ELF":
            raise ELFInvalid(f"invalid magic: {magic!r}")

        self.capacity = ident[4]  # Format for program header (bitness).
        self.encoding = ident[5]  # Data structure encoding (endianness).

        try:
            # e_fmt: Format for program header.
            # p_fmt: Format for section header.
            # p_idx: Indexes to find p_type, p_offset, and p_filesz.
            e_fmt, self._p_fmt, self._p_idx = {
                (1, 1): ("<HHIIIIIHHH", "<IIIIIIII", (0, 1, 4)),  # 32-bit LSB.
                (1, 2): (">HHIIIIIHHH", ">IIIIIIII", (0, 1, 4)),  # 32-bit MSB.
                (2, 1): ("<HHIQQQIHHH", "<IIQQQQQQ", (0, 2, 5)),  # 64-bit LSB.
                (2, 2): (">HHIQQQIHHH", ">IIQQQQQQ", (0, 2, 5)),  # 64-bit MSB.
            }[(self.capacity, self.encoding)]
        except KeyError:
            raise ELFInvalid(
                f"unrecognized capacity ({self.capacity}) or "
                f"encoding ({self.encoding})"
            )

        try:
            (
                _,
                self.machine,  # Architecture type.
                _,
                _,
                self._e_phoff,  # Offset of program header.
                _,
                self.flags,  # Processor-specific flags.
                _,
                self._e_phentsize,  # Size of section.
                self._e_phnum,  # Number of sections.
            ) = self._read(e_fmt)
        except struct.error as e:
            raise ELFInvalid("unable to parse machine and section information") from e

    def _read(self, fmt: str) -> tuple[int, ...]:
        return struct.unpack(fmt, self._f.read(struct.calcsize(fmt)))

    @property
    def interpreter(self) -> str | None:
        """
        The path recorded in the ``PT_INTERP`` section header.
        """
        for index in range(self._e_phnum):
            self._f.seek(self._e_phoff + self._e_phentsize * index)
            try:
                data = self._read(self._p_fmt)
            except struct.error:
                continue
            if data[self._p_idx[0]] != 3:  # Not PT_INTERP.
                continue
            self._f.seek(data[self._p_idx[1]])
            return os.fsdecode(self._f.read(data[self._p_idx[2]])).strip(" ")
        return None
```
```bash
./.venv/lib/python3.9/site-packages/pip-24.1.2.dist-info/RECORD
```
```
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/__main__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/__pip-runner__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/build_env.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/cache.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/cli/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/cli/autocompletion.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/cli/base_command.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/cli/cmdoptions.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/cli/command_context.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/cli/index_command.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/cli/main.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/cli/main_parser.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/cli/parser.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/cli/progress_bars.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/cli/req_command.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/cli/spinners.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/cli/status_codes.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/commands/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/commands/cache.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/commands/check.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/commands/completion.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/commands/configuration.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/commands/debug.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/commands/download.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/commands/freeze.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/commands/hash.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/commands/help.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/commands/index.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/commands/inspect.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/commands/install.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/commands/list.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/commands/search.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/commands/show.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/commands/uninstall.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/commands/wheel.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/configuration.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/distributions/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/distributions/base.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/distributions/installed.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/distributions/sdist.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/distributions/wheel.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/exceptions.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/index/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/index/collector.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/index/package_finder.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/index/sources.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/locations/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/locations/_distutils.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/locations/_sysconfig.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/locations/base.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/main.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/metadata/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/metadata/_json.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/metadata/base.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/metadata/importlib/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/metadata/importlib/_compat.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/metadata/importlib/_dists.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/metadata/importlib/_envs.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/metadata/pkg_resources.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/models/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/models/candidate.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/models/direct_url.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/models/format_control.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/models/index.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/models/installation_report.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/models/link.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/models/scheme.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/models/search_scope.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/models/selection_prefs.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/models/target_python.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/models/wheel.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/network/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/network/auth.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/network/cache.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/network/download.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/network/lazy_wheel.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/network/session.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/network/utils.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/network/xmlrpc.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/operations/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/operations/build/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/operations/build/build_tracker.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/operations/build/metadata.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/operations/build/metadata_editable.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/operations/build/metadata_legacy.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/operations/build/wheel.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/operations/build/wheel_editable.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/operations/build/wheel_legacy.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/operations/check.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/operations/freeze.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/operations/install/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/operations/install/editable_legacy.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/operations/install/wheel.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/operations/prepare.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/pyproject.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/req/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/req/constructors.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/req/req_file.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/req/req_install.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/req/req_set.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/req/req_uninstall.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/resolution/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/resolution/base.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/resolution/legacy/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/resolution/legacy/resolver.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/resolution/resolvelib/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/resolution/resolvelib/base.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/resolution/resolvelib/candidates.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/resolution/resolvelib/factory.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/resolution/resolvelib/found_candidates.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/resolution/resolvelib/provider.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/resolution/resolvelib/reporter.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/resolution/resolvelib/requirements.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/resolution/resolvelib/resolver.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/self_outdated_check.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/_jaraco_text.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/_log.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/appdirs.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/compat.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/compatibility_tags.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/datetime.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/deprecation.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/direct_url_helpers.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/egg_link.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/encoding.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/entrypoints.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/filesystem.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/filetypes.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/glibc.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/hashes.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/logging.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/misc.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/packaging.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/setuptools_build.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/subprocess.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/temp_dir.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/unpacking.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/urls.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/virtualenv.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/utils/wheel.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/vcs/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/vcs/bazaar.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/vcs/git.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/vcs/mercurial.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/vcs/subversion.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/vcs/versioncontrol.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_internal/wheel_builder.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/cachecontrol/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/cachecontrol/_cmd.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/cachecontrol/adapter.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/cachecontrol/cache.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/cachecontrol/caches/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/cachecontrol/caches/file_cache.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/cachecontrol/caches/redis_cache.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/cachecontrol/controller.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/cachecontrol/filewrapper.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/cachecontrol/heuristics.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/cachecontrol/serialize.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/cachecontrol/wrapper.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/certifi/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/certifi/__main__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/certifi/core.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/distlib/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/distlib/compat.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/distlib/database.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/distlib/index.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/distlib/locators.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/distlib/manifest.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/distlib/markers.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/distlib/metadata.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/distlib/resources.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/distlib/scripts.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/distlib/util.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/distlib/version.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/distlib/wheel.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/distro/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/distro/__main__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/distro/distro.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/idna/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/idna/codec.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/idna/compat.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/idna/core.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/idna/idnadata.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/idna/intranges.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/idna/package_data.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/idna/uts46data.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/msgpack/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/msgpack/exceptions.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/msgpack/ext.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/msgpack/fallback.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/packaging/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/packaging/_elffile.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/packaging/_manylinux.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/packaging/_musllinux.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/packaging/_parser.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/packaging/_structures.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/packaging/_tokenizer.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/packaging/markers.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/packaging/metadata.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/packaging/requirements.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/packaging/specifiers.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/packaging/tags.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/packaging/utils.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/packaging/version.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pkg_resources/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/platformdirs/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/platformdirs/__main__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/platformdirs/android.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/platformdirs/api.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/platformdirs/macos.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/platformdirs/unix.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/platformdirs/version.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/platformdirs/windows.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/__main__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/cmdline.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/console.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/filter.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/filters/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/formatter.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/formatters/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/formatters/_mapping.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/formatters/bbcode.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/formatters/groff.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/formatters/html.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/formatters/img.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/formatters/irc.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/formatters/latex.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/formatters/other.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/formatters/pangomarkup.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/formatters/rtf.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/formatters/svg.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/formatters/terminal.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/formatters/terminal256.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/lexer.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/lexers/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/lexers/_mapping.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/lexers/python.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/modeline.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/plugin.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/regexopt.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/scanner.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/sphinxext.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/style.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/styles/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/styles/_mapping.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/token.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/unistring.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pygments/util.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pyproject_hooks/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pyproject_hooks/_compat.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pyproject_hooks/_impl.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pyproject_hooks/_in_process/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/requests/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/requests/__version__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/requests/_internal_utils.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/requests/adapters.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/requests/api.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/requests/auth.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/requests/certs.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/requests/compat.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/requests/cookies.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/requests/exceptions.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/requests/help.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/requests/hooks.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/requests/models.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/requests/packages.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/requests/sessions.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/requests/status_codes.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/requests/structures.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/requests/utils.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/resolvelib/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/resolvelib/compat/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/resolvelib/compat/collections_abc.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/resolvelib/providers.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/resolvelib/reporters.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/resolvelib/resolvers.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/resolvelib/structs.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/__main__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/_cell_widths.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/_emoji_codes.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/_emoji_replace.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/_export_format.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/_extension.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/_fileno.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/_inspect.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/_log_render.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/_loop.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/_null_file.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/_palettes.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/_pick.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/_ratio.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/_spinners.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/_stack.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/_timer.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/_win32_console.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/_windows.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/_windows_renderer.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/_wrap.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/abc.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/align.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/ansi.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/bar.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/box.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/cells.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/color.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/color_triplet.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/columns.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/console.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/constrain.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/containers.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/control.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/default_styles.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/diagnose.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/emoji.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/errors.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/file_proxy.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/filesize.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/highlighter.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/json.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/jupyter.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/layout.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/live.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/live_render.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/logging.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/markup.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/measure.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/padding.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/pager.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/palette.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/panel.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/pretty.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/progress.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/progress_bar.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/prompt.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/protocol.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/region.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/repr.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/rule.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/scope.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/screen.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/segment.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/spinner.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/status.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/style.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/styled.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/syntax.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/table.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/terminal_theme.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/text.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/theme.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/themes.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/traceback.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/rich/tree.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/tenacity/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/tenacity/_asyncio.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/tenacity/_utils.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/tenacity/after.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/tenacity/before.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/tenacity/before_sleep.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/tenacity/nap.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/tenacity/retry.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/tenacity/stop.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/tenacity/tornadoweb.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/tenacity/wait.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/tomli/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/tomli/_parser.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/tomli/_re.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/tomli/_types.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/truststore/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/truststore/_api.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/truststore/_macos.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/truststore/_openssl.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/truststore/_ssl_constants.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/truststore/_windows.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/typing_extensions.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/_collections.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/_version.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/connection.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/connectionpool.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/contrib/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/contrib/_appengine_environ.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/contrib/_securetransport/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/contrib/_securetransport/bindings.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/contrib/_securetransport/low_level.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/contrib/appengine.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/contrib/ntlmpool.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/contrib/pyopenssl.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/contrib/securetransport.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/contrib/socks.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/exceptions.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/fields.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/filepost.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/packages/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/packages/backports/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/packages/backports/makefile.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/packages/backports/weakref_finalize.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/packages/six.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/poolmanager.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/request.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/response.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/util/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/util/connection.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/util/proxy.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/util/queue.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/util/request.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/util/response.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/util/retry.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/util/ssl_.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/util/ssl_match_hostname.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/util/ssltransport.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/util/timeout.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/util/url.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pip/_vendor/urllib3/util/wait.cpython-39.pyc,,
../../../bin/pip,sha256=q54VxaDIVFHZMbrR_GjWBVDEv4yNUxcsVp-auGsydBI,264
../../../bin/pip3,sha256=q54VxaDIVFHZMbrR_GjWBVDEv4yNUxcsVp-auGsydBI,264
../../../bin/pip3.9,sha256=q54VxaDIVFHZMbrR_GjWBVDEv4yNUxcsVp-auGsydBI,264
pip-24.1.2.dist-info/AUTHORS.txt,sha256=MkzqpbKoofxeB4_6bAzy7x_Gl-B9GIBRPaYrPWSdFus,10669
pip-24.1.2.dist-info/INSTALLER,sha256=zuuue4knoyJ-UwPPXg8fezS7VCrXJQrAP7zeNuwvFQg,4
pip-24.1.2.dist-info/LICENSE.txt,sha256=Y0MApmnUmurmWxLGxIySTFGkzfPR_whtw0VtyLyqIQQ,1093
pip-24.1.2.dist-info/METADATA,sha256=OFLLNLX7R_It-QfGu_9CNrAwvmg-5UiexwDz-kChfdc,3626
pip-24.1.2.dist-info/RECORD,,
pip-24.1.2.dist-info/REQUESTED,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip-24.1.2.dist-info/WHEEL,sha256=y4mX-SOX4fYIkonsAGA5N0Oy-8_gI4FXw5HNI1xqvWg,91
pip-24.1.2.dist-info/entry_points.txt,sha256=eeIjuzfnfR2PrhbjnbzFU6MnSS70kZLxwaHHq6M-bD0,87
pip-24.1.2.dist-info/top_level.txt,sha256=zuuue4knoyJ-UwPPXg8fezS7VCrXJQrAP7zeNuwvFQg,4
pip/__init__.py,sha256=9QFiOpFNe6kjlpGzvU2X5H_SYqDMLHg7kRWt1gWwUrw,357
pip/__main__.py,sha256=WzbhHXTbSE6gBY19mNN9m4s5o_365LOvTYSgqgbdBhE,854
pip/__pip-runner__.py,sha256=cPPWuJ6NK_k-GzfvlejLFgwzmYUROmpAR6QC3Q-vkXQ,1450
pip/_internal/__init__.py,sha256=MfcoOluDZ8QMCFYal04IqOJ9q6m2V7a0aOsnI-WOxUo,513
pip/_internal/build_env.py,sha256=TLqMeOgGpWbnHvP9piIymV4R2a_rWOWgiB-eOAbVPE8,10374
pip/_internal/cache.py,sha256=Jb698p5PNigRtpW5o26wQNkkUv4MnQ94mc471wL63A0,10369
pip/_internal/cli/__init__.py,sha256=FkHBgpxxb-_gd6r1FjnNhfMOzAUYyXoXKJ6abijfcFU,132
pip/_internal/cli/autocompletion.py,sha256=Lli3Mr6aDNu7ZkJJFFvwD2-hFxNI6Avz8OwMyS5TVrs,6865
pip/_internal/cli/base_command.py,sha256=CNWPhIYFRNPdTDewbtvCl4O-RnyNHLRe6Bfwpds-HV8,8667
pip/_internal/cli/cmdoptions.py,sha256=0XyHY1CQ9tGt05e2BOqVSmSGuVW5g3Udkdgk1M_qQWQ,30066
pip/_internal/cli/command_context.py,sha256=RHgIPwtObh5KhMrd3YZTkl8zbVG-6Okml7YbFX4Ehg0,774
pip/_internal/cli/index_command.py,sha256=GmWL82zpzS4c7yq-2Go5X26BlvdMsSmJewh-3LSimUk,5857
pip/_internal/cli/main.py,sha256=BDZef-bWe9g9Jpr4OVs4dDf-845HJsKw835T7AqEnAc,2817
pip/_internal/cli/main_parser.py,sha256=laDpsuBDl6kyfywp9eMMA9s84jfH2TJJn-vmL0GG90w,4338
pip/_internal/cli/parser.py,sha256=QAkY6s8N-AD7w5D2PQm2Y8C2MIJSv7iuAeNjOMvDBUA,10811
pip/_internal/cli/progress_bars.py,sha256=NedSI8g5-69xK8OoubBetXbkIUu6b11TB0Rsan9Uw28,2714
pip/_internal/cli/req_command.py,sha256=DqeFhmUMs6o6Ev8qawAcOoYNdAZsfyKS0MZI5jsJYwQ,12250
pip/_internal/cli/spinners.py,sha256=hIJ83GerdFgFCdobIA23Jggetegl_uC4Sp586nzFbPE,5118
pip/_internal/cli/status_codes.py,sha256=sEFHUaUJbqv8iArL3HAtcztWZmGOFX01hTesSytDEh0,116
pip/_internal/commands/__init__.py,sha256=5oRO9O3dM2vGuh0bFw4HOVletryrz5HHMmmPWwJrH9U,3882
pip/_internal/commands/cache.py,sha256=xg76_ZFEBC6zoQ3gXLRfMZJft4z2a0RwH4GEFZC6nnU,7944
pip/_internal/commands/check.py,sha256=mLRKTaGDmLuZbZ--kO1nNKoRMYWIsL3fNQ3vm5Fpuks,1684
pip/_internal/commands/completion.py,sha256=HT4lD0bgsflHq2IDgYfiEdp7IGGtE7s6MgI3xn0VQEw,4287
pip/_internal/commands/configuration.py,sha256=n98enwp6y0b5G6fiRQjaZo43FlJKYve_daMhN-4BRNc,9766
pip/_internal/commands/debug.py,sha256=DNDRgE9YsKrbYzU0s3VKi8rHtKF4X13CJ_br_8PUXO0,6797
pip/_internal/commands/download.py,sha256=0qB0nys6ZEPsog451lDsjL5Bx7Z97t-B80oFZKhpzKM,5273
pip/_internal/commands/freeze.py,sha256=2qjQrH9KWi5Roav0CuR7vc7hWm4uOi_0l6tp3ESKDHM,3172
pip/_internal/commands/hash.py,sha256=EVVOuvGtoPEdFi8SNnmdqlCQrhCxV-kJsdwtdcCnXGQ,1703
pip/_internal/commands/help.py,sha256=gcc6QDkcgHMOuAn5UxaZwAStsRBrnGSn_yxjS57JIoM,1132
pip/_internal/commands/index.py,sha256=RAXxmJwFhVb5S1BYzb5ifX3sn9Na8v2CCVYwSMP8pao,4731
pip/_internal/commands/inspect.py,sha256=PGrY9TRTRCM3y5Ml8Bdk8DEOXquWRfscr4DRo1LOTPc,3189
pip/_internal/commands/install.py,sha256=ADWSqa1E1kg0SVCx-I0v8oPn3e1sohGJXFyOkSzeFIA,28997
pip/_internal/commands/list.py,sha256=RgaIV4kN-eMSpgUAXc-6bjnURzl0v3cRE11xr54O9Cg,12771
pip/_internal/commands/search.py,sha256=hSGtIHg26LRe468Ly7oZ6gfd9KbTxBRZAAtJc9Um6S4,5628
pip/_internal/commands/show.py,sha256=IG9L5uo8w6UA4tI_IlmaxLCoNKPa5JNJCljj3NWs0OE,7507
pip/_internal/commands/uninstall.py,sha256=7pOR7enK76gimyxQbzxcG1OsyLXL3DvX939xmM8Fvtg,3892
pip/_internal/commands/wheel.py,sha256=eJRhr_qoNNxWAkkdJCNiQM7CXd4E1_YyQhsqJnBPGGg,6414
pip/_internal/configuration.py,sha256=XkAiBS0hpzsM-LF0Qu5hvPWO_Bs67-oQKRYFBuMbESs,14006
pip/_internal/distributions/__init__.py,sha256=Hq6kt6gXBgjNit5hTTWLAzeCNOKoB-N0pGYSqehrli8,858
pip/_internal/distributions/base.py,sha256=QeB9qvKXDIjLdPBDE5fMgpfGqMMCr-govnuoQnGuiF8,1783
pip/_internal/distributions/installed.py,sha256=QinHFbWAQ8oE0pbD8MFZWkwlnfU1QYTccA1vnhrlYOU,842
pip/_internal/distributions/sdist.py,sha256=PlcP4a6-R6c98XnOM-b6Lkb3rsvh9iG4ok8shaanrzs,6751
pip/_internal/distributions/wheel.py,sha256=THBYfnv7VVt8mYhMYUtH13S1E7FDwtDyDfmUcl8ai0E,1317
pip/_internal/exceptions.py,sha256=6qcW3QgmFVlRxlZvDSLUhSzKJ7_Tedo-lyqWA6NfdAU,25371
pip/_internal/index/__init__.py,sha256=vpt-JeTZefh8a-FC22ZeBSXFVbuBcXSGiILhQZJaNpQ,30
pip/_internal/index/collector.py,sha256=RdPO0JLAlmyBWPAWYHPyRoGjz3GNAeTngCNkbGey_mE,16265
pip/_internal/index/package_finder.py,sha256=XHHQm1Tmw4wC2jYzrDa2lwlx-OGPzF7tThv-Uj1Y7ak,37733
pip/_internal/index/sources.py,sha256=dJegiR9f86kslaAHcv9-R5L_XBf5Rzm_FkyPteDuPxI,8688
pip/_internal/locations/__init__.py,sha256=UaAxeZ_f93FyouuFf4p7SXYF-4WstXuEvd3LbmPCAno,14925
pip/_internal/locations/_distutils.py,sha256=H9ZHK_35rdDV1Qsmi4QeaBULjFT4Mbu6QuoVGkJ6QHI,6009
pip/_internal/locations/_sysconfig.py,sha256=IGzds60qsFneRogC-oeBaY7bEh3lPt_v47kMJChQXsU,7724
pip/_internal/locations/base.py,sha256=RQiPi1d4FVM2Bxk04dQhXZ2PqkeljEL2fZZ9SYqIQ78,2556
pip/_internal/main.py,sha256=r-UnUe8HLo5XFJz8inTcOOTiu_sxNhgHb6VwlGUllOI,340
pip/_internal/metadata/__init__.py,sha256=9pU3W3s-6HtjFuYhWcLTYVmSaziklPv7k2x8p7X1GmA,4339
pip/_internal/metadata/_json.py,sha256=P0cAJrH_mtmMZvlZ16ZXm_-izA4lpr5wy08laICuiaA,2644
pip/_internal/metadata/base.py,sha256=ft0K5XNgI4ETqZnRv2-CtvgYiMOMAeGMAzxT-f6VLJA,25298
pip/_internal/metadata/importlib/__init__.py,sha256=jUUidoxnHcfITHHaAWG1G2i5fdBYklv_uJcjo2x7VYE,135
pip/_internal/metadata/importlib/_compat.py,sha256=GAe_prIfCE4iUylrnr_2dJRlkkBVRUbOidEoID7LPoE,1882
pip/_internal/metadata/importlib/_dists.py,sha256=sB2ehwdqysgFAqNZMrYDw9lVumFanJFw-rZsIzSUo4o,8275
pip/_internal/metadata/importlib/_envs.py,sha256=8AGojbf7Ei-eXmV8cmYMPDqPV_KkqH9oTYHE8OGn5LE,7455
pip/_internal/metadata/pkg_resources.py,sha256=U07ETAINSGeSRBfWUG93E4tZZbaW_f7PGzEqZN0hulc,10542
pip/_internal/models/__init__.py,sha256=3DHUd_qxpPozfzouoqa9g9ts1Czr5qaHfFxbnxriepM,63
pip/_internal/models/candidate.py,sha256=zzgFRuw_kWPjKpGw7LC0ZUMD2CQ2EberUIYs8izjdCA,753
pip/_internal/models/direct_url.py,sha256=uBtY2HHd3TO9cKQJWh0ThvE5FRr-MWRYChRU4IG9HZE,6578
pip/_internal/models/format_control.py,sha256=wtsQqSK9HaUiNxQEuB-C62eVimw6G4_VQFxV9-_KDBE,2486
pip/_internal/models/index.py,sha256=tYnL8oxGi4aSNWur0mG8DAP7rC6yuha_MwJO8xw0crI,1030
pip/_internal/models/installation_report.py,sha256=zRVZoaz-2vsrezj_H3hLOhMZCK9c7TbzWgC-jOalD00,2818
pip/_internal/models/link.py,sha256=jHax9O-9zlSzEwjBCDkx0OXjKXwBDwOuPwn-PsR8dCs,21034
pip/_internal/models/scheme.py,sha256=PakmHJM3e8OOWSZFtfz1Az7f1meONJnkGuQxFlt3wBE,575
pip/_internal/models/search_scope.py,sha256=67NEnsYY84784S-MM7ekQuo9KXLH-7MzFntXjapvAo0,4531
pip/_internal/models/selection_prefs.py,sha256=qaFfDs3ciqoXPg6xx45N1jPLqccLJw4N0s4P0PyHTQ8,2015
pip/_internal/models/target_python.py,sha256=2XaH2rZ5ZF-K5wcJbEMGEl7SqrTToDDNkrtQ2v_v_-Q,4271
pip/_internal/models/wheel.py,sha256=Odc1NVWL5N-i6A3vFa50BfNvCRlGvGa4som60FQM198,3601
pip/_internal/network/__init__.py,sha256=jf6Tt5nV_7zkARBrKojIXItgejvoegVJVKUbhAa5Ioc,50
pip/_internal/network/auth.py,sha256=iRu5LBEMK_3zXmsnWi21r0EKukJbWMum1jmIuL79PeY,20533
pip/_internal/network/cache.py,sha256=48A971qCzKNFvkb57uGEk7-0xaqPS0HWj2711QNTxkU,3935
pip/_internal/network/download.py,sha256=rZrbi6OdY1-2Nkc7AMvJetVmtOMnwVIkEAw615ONBzM,6087
pip/_internal/network/lazy_wheel.py,sha256=2PXVduYZPCPZkkQFe1J1GbfHJWeCU--FXonGyIfw9eU,7638
pip/_internal/network/session.py,sha256=XmanBKjVwPFmh1iJ58q6TDh9xabH37gREuQJ_feuZGA,18741
pip/_internal/network/utils.py,sha256=6A5SrUJEEUHxbGtbscwU2NpCyz-3ztiDlGWHpRRhsJ8,4073
pip/_internal/network/xmlrpc.py,sha256=sAxzOacJ-N1NXGPvap9jC3zuYWSnnv3GXtgR2-E2APA,1838
pip/_internal/operations/__init__.py,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip/_internal/operations/build/__init__.py,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip/_internal/operations/build/build_tracker.py,sha256=-ARW_TcjHCOX7D2NUOGntB4Fgc6b4aolsXkAK6BWL7w,4774
pip/_internal/operations/build/metadata.py,sha256=9S0CUD8U3QqZeXp-Zyt8HxwU90lE4QrnYDgrqZDzBnc,1422
pip/_internal/operations/build/metadata_editable.py,sha256=VLL7LvntKE8qxdhUdEJhcotFzUsOSI8NNS043xULKew,1474
pip/_internal/operations/build/metadata_legacy.py,sha256=8i6i1QZX9m_lKPStEFsHKM0MT4a-CD408JOw99daLmo,2190
pip/_internal/operations/build/wheel.py,sha256=sT12FBLAxDC6wyrDorh8kvcZ1jG5qInCRWzzP-UkJiQ,1075
pip/_internal/operations/build/wheel_editable.py,sha256=yOtoH6zpAkoKYEUtr8FhzrYnkNHQaQBjWQ2HYae1MQg,1417
pip/_internal/operations/build/wheel_legacy.py,sha256=K-6kNhmj-1xDF45ny1yheMerF0ui4EoQCLzEoHh6-tc,3045
pip/_internal/operations/check.py,sha256=Qpw7FwZMG1ZxbZ4sSPnbJ0enzMnXsCKWULq0fS1hvt0,5087
pip/_internal/operations/freeze.py,sha256=V59yEyCSz_YhZuhH09-6aV_zvYBMrS_IxFFNqn2QzlA,9864
pip/_internal/operations/install/__init__.py,sha256=mX7hyD2GNBO2mFGokDQ30r_GXv7Y_PLdtxcUv144e-s,51
pip/_internal/operations/install/editable_legacy.py,sha256=PoEsNEPGbIZ2yQphPsmYTKLOCMs4gv5OcCdzW124NcA,1283
pip/_internal/operations/install/wheel.py,sha256=wshDUAnxuPUBg-prUJ60aqLuW4btb6XHT3bwb3VZchE,27197
pip/_internal/operations/prepare.py,sha256=joWJwPkuqGscQgVNImLK71e9hRapwKvRCM8HclysmvU,28118
pip/_internal/pyproject.py,sha256=4Xszp11xgr126yzG6BbJA0oaQ9WXuhb0jyUb-y_6lPQ,7152
pip/_internal/req/__init__.py,sha256=HxBFtZy_BbCclLgr26waMtpzYdO5T3vxePvpGAXSt5s,2653
pip/_internal/req/constructors.py,sha256=aC9Nc-SESEz57WTodyH46ujupY10pWo2NmTl1v9_tro,18412
pip/_internal/req/req_file.py,sha256=hnC9Oz-trqGQpuDnCVWqwpJkAvtbCsk7-5k0EWVQhlQ,17687
pip/_internal/req/req_install.py,sha256=29LLB4oG6Igi_FeOKZJ_gBt15R1BpGW8FU9Jiq4H9gI,35054
pip/_internal/req/req_set.py,sha256=j3esG0s6SzoVReX9rWn4rpYNtyET_fwxbwJPRimvRxo,2858
pip/_internal/req/req_uninstall.py,sha256=qzDIxJo-OETWqGais7tSMCDcWbATYABT-Tid3ityF0s,23853
pip/_internal/resolution/__init__.py,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip/_internal/resolution/base.py,sha256=qlmh325SBVfvG6Me9gc5Nsh5sdwHBwzHBq6aEXtKsLA,583
pip/_internal/resolution/legacy/__init__.py,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip/_internal/resolution/legacy/resolver.py,sha256=3HZiJBRd1FTN6jQpI4qRO8-TbLYeIbUTS6PFvXnXs2w,24068
pip/_internal/resolution/resolvelib/__init__.py,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip/_internal/resolution/resolvelib/base.py,sha256=DCf669FsqyQY5uqXeePDHQY1e4QO-pBzWH8O0s9-K94,5023
pip/_internal/resolution/resolvelib/candidates.py,sha256=07CBc85ya3J19XqdvUsLQwtVIxiTYq9km9hbTRh0jb0,19823
pip/_internal/resolution/resolvelib/factory.py,sha256=qzNIR_YsC4lpszaSmOmhONCplrf33hPceO8YtAIQrA4,32395
pip/_internal/resolution/resolvelib/found_candidates.py,sha256=9hrTyQqFvl9I7Tji79F1AxHv39Qh1rkJ_7deSHSMfQc,6383
pip/_internal/resolution/resolvelib/provider.py,sha256=bcsFnYvlmtB80cwVdW1fIwgol8ZNr1f1VHyRTkz47SM,9935
pip/_internal/resolution/resolvelib/reporter.py,sha256=YFm9hQvz4DFCbjZeFTQ56hTz3Ac-mDBnHkeNRVvMHLY,3100
pip/_internal/resolution/resolvelib/requirements.py,sha256=7JG4Z72e5Yk4vU0S5ulGvbqTy4FMQGYhY5zQhX9zTtY,8065
pip/_internal/resolution/resolvelib/resolver.py,sha256=nLJOsVMEVi2gQUVJoUFKMZAeu2f7GRMjGMvNSWyz0Bc,12592
pip/_internal/self_outdated_check.py,sha256=t9Zf6aaSXvlodc2JbUNVxImWCoE32p17GKJmyuI-lT8,8356
pip/_internal/utils/__init__.py,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip/_internal/utils/_jaraco_text.py,sha256=M15uUPIh5NpP1tdUGBxRau6q1ZAEtI8-XyLEETscFfE,3350
pip/_internal/utils/_log.py,sha256=-jHLOE_THaZz5BFcCnoSL9EYAtJ0nXem49s9of4jvKw,1015
pip/_internal/utils/appdirs.py,sha256=swgcTKOm3daLeXTW6v5BUS2Ti2RvEnGRQYH_yDXklAo,1665
pip/_internal/utils/compat.py,sha256=ckkFveBiYQjRWjkNsajt_oWPS57tJvE8XxoC4OIYgCY,2399
pip/_internal/utils/compatibility_tags.py,sha256=ydin8QG8BHqYRsPY4OL6cmb44CbqXl1T0xxS97VhHkk,5377
pip/_internal/utils/datetime.py,sha256=m21Y3wAtQc-ji6Veb6k_M5g6A0ZyFI4egchTdnwh-pQ,242
pip/_internal/utils/deprecation.py,sha256=k7Qg_UBAaaTdyq82YVARA6D7RmcGTXGv7fnfcgigj4Q,3707
pip/_internal/utils/direct_url_helpers.py,sha256=r2MRtkVDACv9AGqYODBUC9CjwgtsUU1s68hmgfCJMtA,3196
pip/_internal/utils/egg_link.py,sha256=0FePZoUYKv4RGQ2t6x7w5Z427wbA_Uo3WZnAkrgsuqo,2463
pip/_internal/utils/encoding.py,sha256=qqsXDtiwMIjXMEiIVSaOjwH5YmirCaK-dIzb6-XJsL0,1169
pip/_internal/utils/entrypoints.py,sha256=YlhLTRl2oHBAuqhc-zmL7USS67TPWVHImjeAQHreZTQ,3064
pip/_internal/utils/filesystem.py,sha256=RhMIXUaNVMGjc3rhsDahWQ4MavvEQDdqXqgq-F6fpw8,5122
pip/_internal/utils/filetypes.py,sha256=i8XAQ0eFCog26Fw9yV0Yb1ygAqKYB1w9Cz9n0fj8gZU,716
pip/_internal/utils/glibc.py,sha256=Mesxxgg3BLxheLZx-dSf30b6gKpOgdVXw6W--uHSszQ,3113
pip/_internal/utils/hashes.py,sha256=aLhAlDXeEA_PrjRbfFYy9G6_MKlxdvc7JxUtN5QKP6k,4951
pip/_internal/utils/logging.py,sha256=xSDfIHRfy95-RSHuh1QFXZrrS2Onpa1mMVLDM5_o21s,11602
pip/_internal/utils/misc.py,sha256=PO3qVc98DOSd-2xA9qBMFSThmZjQiDzVDa3dm2-Q3lc,23814
pip/_internal/utils/packaging.py,sha256=5Wm6_x7lKrlqVjPI5MBN_RurcRHwVYoQ7Ksrs84de7s,2108
pip/_internal/utils/setuptools_build.py,sha256=ouXpud-jeS8xPyTPsXJ-m34NPvK5os45otAzdSV_IJE,4435
pip/_internal/utils/subprocess.py,sha256=EsvqSRiSMHF98T8Txmu6NLU3U--MpTTQjtNgKP0P--M,8988
pip/_internal/utils/temp_dir.py,sha256=DUAw22uFruQdK43i2L2K53C-CDjRCPeAsBKJpu-rHQ4,9312
pip/_internal/utils/unpacking.py,sha256=eyDkSsk4nW8ZfiSjNzJduCznpHyaGHVv3ak_LMGsiEM,11951
pip/_internal/utils/urls.py,sha256=qceSOZb5lbNDrHNsv7_S4L4Ytszja5NwPKUMnZHbYnM,1599
pip/_internal/utils/virtualenv.py,sha256=S6f7csYorRpiD6cvn3jISZYc3I8PJC43H5iMFpRAEDU,3456
pip/_internal/utils/wheel.py,sha256=b442jkydFHjXzDy6cMR7MpzWBJ1Q82hR5F33cmcHV3g,4494
pip/_internal/vcs/__init__.py,sha256=UAqvzpbi0VbZo3Ub6skEeZAw-ooIZR-zX_WpCbxyCoU,596
pip/_internal/vcs/bazaar.py,sha256=EKStcQaKpNu0NK4p5Q10Oc4xb3DUxFw024XrJy40bFQ,3528
pip/_internal/vcs/git.py,sha256=3tpc9LQA_J4IVW5r5NvWaaSeDzcmJOrSFZN0J8vIKfU,18177
pip/_internal/vcs/mercurial.py,sha256=oULOhzJ2Uie-06d1omkL-_Gc6meGaUkyogvqG9ZCyPs,5249
pip/_internal/vcs/subversion.py,sha256=ddTugHBqHzV3ebKlU5QXHPN4gUqlyXbOx8q8NgXKvs8,11735
pip/_internal/vcs/versioncontrol.py,sha256=cvf_-hnTAjQLXJ3d17FMNhQfcO1AcKWUF10tfrYyP-c,22440
pip/_internal/wheel_builder.py,sha256=DL3A8LKeRj_ACp11WS5wSgASgPFqeyAeXJKdXfmaWXU,11799
pip/_vendor/__init__.py,sha256=691R7mzHaXjBpSyqx4flnSGjB2xTsNYUx17rbCS8F9c,4850
pip/_vendor/cachecontrol/__init__.py,sha256=GiYoagwPEiJ_xR_lbwWGaoCiPtF_rz4isjfjdDAgHU4,676
pip/_vendor/cachecontrol/_cmd.py,sha256=iist2EpzJvDVIhMAxXq8iFnTBsiZAd6iplxfmNboNyk,1737
pip/_vendor/cachecontrol/adapter.py,sha256=fByO_Pd_EOemjWbuocvBWdN85xT0q_TBm2lxS6vD4fk,6355
pip/_vendor/cachecontrol/cache.py,sha256=OTQj72tUf8C1uEgczdl3Gc8vkldSzsTITKtDGKMx4z8,1952
pip/_vendor/cachecontrol/caches/__init__.py,sha256=dtrrroK5BnADR1GWjCZ19aZ0tFsMfvFBtLQQU1sp_ag,303
pip/_vendor/cachecontrol/caches/file_cache.py,sha256=9AlmmTJc6cslb6k5z_6q0sGPHVrMj8zv-uWy-simmfE,5406
pip/_vendor/cachecontrol/caches/redis_cache.py,sha256=9rmqwtYu_ljVkW6_oLqbC7EaX_a8YT_yLuna-eS0dgo,1386
pip/_vendor/cachecontrol/controller.py,sha256=o-ejGJlBmpKK8QQLyTPJj0t7siU8XVHXuV8MCybCxQ8,18575
pip/_vendor/cachecontrol/filewrapper.py,sha256=STttGmIPBvZzt2b51dUOwoWX5crcMCpKZOisM3f5BNc,4292
pip/_vendor/cachecontrol/heuristics.py,sha256=IYe4QmHERWsMvtxNrp920WeaIsaTTyqLB14DSheSbtY,4834
pip/_vendor/cachecontrol/py.typed,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip/_vendor/cachecontrol/serialize.py,sha256=HQd2IllQ05HzPkVLMXTF2uX5mjEQjDBkxCqUJUODpZk,5163
pip/_vendor/cachecontrol/wrapper.py,sha256=hsGc7g8QGQTT-4f8tgz3AM5qwScg6FO0BSdLSRdEvpU,1417
pip/_vendor/certifi/__init__.py,sha256=ljtEx-EmmPpTe2SOd5Kzsujm_lUD0fKJVnE9gzce320,94
pip/_vendor/certifi/__main__.py,sha256=1k3Cr95vCxxGRGDljrW3wMdpZdL3Nhf0u1n-k2qdsCY,255
pip/_vendor/certifi/cacert.pem,sha256=ejR8qP724p-CtuR4U1WmY1wX-nVeCUD2XxWqj8e9f5I,292541
pip/_vendor/certifi/core.py,sha256=2SRT5rIcQChFDbe37BQa-kULxAgJ8qN6l1jfqTp4HIs,4486
pip/_vendor/certifi/py.typed,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip/_vendor/distlib/__init__.py,sha256=hJKF7FHoqbmGckncDuEINWo_OYkDNiHODtYXSMcvjcc,625
pip/_vendor/distlib/compat.py,sha256=Un-uIBvy02w-D267OG4VEhuddqWgKj9nNkxVltAb75w,41487
pip/_vendor/distlib/database.py,sha256=0V9Qvs0Vrxa2F_-hLWitIyVyRifJ0pCxyOI-kEOBwsA,51965
pip/_vendor/distlib/index.py,sha256=lTbw268rRhj8dw1sib3VZ_0EhSGgoJO3FKJzSFMOaeA,20797
pip/_vendor/distlib/locators.py,sha256=o1r_M86_bRLafSpetmyfX8KRtFu-_Q58abvQrnOSnbA,51767
pip/_vendor/distlib/manifest.py,sha256=3qfmAmVwxRqU1o23AlfXrQGZzh6g_GGzTAP_Hb9C5zQ,14168
pip/_vendor/distlib/markers.py,sha256=n3DfOh1yvZ_8EW7atMyoYeZFXjYla0Nz0itQlojCd0A,5268
pip/_vendor/distlib/metadata.py,sha256=pB9WZ9mBfmQxc9OVIldLS5CjOoQRvKAvUwwQyKwKQtQ,39693
pip/_vendor/distlib/resources.py,sha256=LwbPksc0A1JMbi6XnuPdMBUn83X7BPuFNWqPGEKI698,10820
pip/_vendor/distlib/scripts.py,sha256=8_gP9J7_tlNRicnWmPX4ZiDlP5wTwJKDeeg-8_qXUZU,18780
pip/_vendor/distlib/t32.exe,sha256=a0GV5kCoWsMutvliiCKmIgV98eRZ33wXoS-XrqvJQVs,97792
pip/_vendor/distlib/t64-arm.exe,sha256=68TAa32V504xVBnufojh0PcenpR3U4wAqTqf-MZqbPw,182784
pip/_vendor/distlib/t64.exe,sha256=gaYY8hy4fbkHYTTnA4i26ct8IQZzkBG2pRdy0iyuBrc,108032
pip/_vendor/distlib/util.py,sha256=XSznxEi_i3T20UJuaVc0qXHz5ksGUCW1khYlBprN_QE,67530
pip/_vendor/distlib/version.py,sha256=9pXkduchve_aN7JG6iL9VTYV_kqNSGoc2Dwl8JuySnQ,23747
pip/_vendor/distlib/w32.exe,sha256=R4csx3-OGM9kL4aPIzQKRo5TfmRSHZo6QWyLhDhNBks,91648
pip/_vendor/distlib/w64-arm.exe,sha256=xdyYhKj0WDcVUOCb05blQYvzdYIKMbmJn2SZvzkcey4,168448
pip/_vendor/distlib/w64.exe,sha256=ejGf-rojoBfXseGLpya6bFTFPWRG21X5KvU8J5iU-K0,101888
pip/_vendor/distlib/wheel.py,sha256=FVQCve8u-L0QYk5-YTZc7s4WmNQdvjRWTK08KXzZVX4,43958
pip/_vendor/distro/__init__.py,sha256=2fHjF-SfgPvjyNZ1iHh_wjqWdR_Yo5ODHwZC0jLBPhc,981
pip/_vendor/distro/__main__.py,sha256=bu9d3TifoKciZFcqRBuygV3GSuThnVD_m2IK4cz96Vs,64
pip/_vendor/distro/distro.py,sha256=XqbefacAhDT4zr_trnbA15eY8vdK4GTghgmvUGrEM_4,49430
pip/_vendor/distro/py.typed,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip/_vendor/idna/__init__.py,sha256=KJQN1eQBr8iIK5SKrJ47lXvxG0BJ7Lm38W4zT0v_8lk,849
pip/_vendor/idna/codec.py,sha256=PS6m-XmdST7Wj7J7ulRMakPDt5EBJyYrT3CPtjh-7t4,3426
pip/_vendor/idna/compat.py,sha256=0_sOEUMT4CVw9doD3vyRhX80X19PwqFoUBs7gWsFME4,321
pip/_vendor/idna/core.py,sha256=lyhpoe2vulEaB_65xhXmoKgO-xUqFDvcwxu5hpNNO4E,12663
pip/_vendor/idna/idnadata.py,sha256=dqRwytzkjIHMBa2R1lYvHDwACenZPt8eGVu1Y8UBE-E,78320
pip/_vendor/idna/intranges.py,sha256=YBr4fRYuWH7kTKS2tXlFjM24ZF1Pdvcir-aywniInqg,1881
pip/_vendor/idna/package_data.py,sha256=Tkt0KnIeyIlnHddOaz9WSkkislNgokJAuE-p5GorMqo,21
pip/_vendor/idna/py.typed,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip/_vendor/idna/uts46data.py,sha256=1KuksWqLuccPXm2uyRVkhfiFLNIhM_H2m4azCcnOqEU,206503
pip/_vendor/msgpack/__init__.py,sha256=gsMP7JTECZNUSjvOyIbdhNOkpB9Z8BcGwabVGY2UcdQ,1077
pip/_vendor/msgpack/exceptions.py,sha256=dCTWei8dpkrMsQDcjQk74ATl9HsIBH0ybt8zOPNqMYc,1081
pip/_vendor/msgpack/ext.py,sha256=fKp00BqDLjUtZnPd70Llr138zk8JsCuSpJkkZ5S4dt8,5629
pip/_vendor/msgpack/fallback.py,sha256=wdUWJkWX2gzfRW9BBCTOuIE1Wvrf5PtBtR8ZtY7G_EE,33175
pip/_vendor/packaging/__init__.py,sha256=dtw2bNmWCQ9WnMoK3bk_elL1svSlikXtLpZhCFIB9SE,496
pip/_vendor/packaging/_elffile.py,sha256=_LcJW4YNKywYsl4169B2ukKRqwxjxst_8H0FRVQKlz8,3282
pip/_vendor/packaging/_manylinux.py,sha256=Xo4V0PZz8sbuVCbTni0t1CR0AHeir_7ib4lTmV8scD4,9586
pip/_vendor/packaging/_musllinux.py,sha256=p9ZqNYiOItGee8KcZFeHF_YcdhVwGHdK6r-8lgixvGQ,2694
pip/_vendor/packaging/_parser.py,sha256=s_TvTvDNK0NrM2QB3VKThdWFM4Nc0P6JnkObkl3MjpM,10236
pip/_vendor/packaging/_structures.py,sha256=q3eVNmbWJGG_S0Dit_S3Ao8qQqz_5PYTXFAKBZe5yr4,1431
pip/_vendor/packaging/_tokenizer.py,sha256=J6v5H7Jzvb-g81xp_2QACKwO7LxHQA6ikryMU7zXwN8,5273
pip/_vendor/packaging/markers.py,sha256=dWKSqn5Sp-jDmOG-W3GfLHKjwhf1IsznbT71VlBoB5M,10671
pip/_vendor/packaging/metadata.py,sha256=KINuSkJ12u-SyoKNTy_pHNGAfMUtxNvZ53qA1zAKcKI,32349
pip/_vendor/packaging/py.typed,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip/_vendor/packaging/requirements.py,sha256=gYyRSAdbrIyKDY66ugIDUQjRMvxkH2ALioTmX3tnL6o,2947
pip/_vendor/packaging/specifiers.py,sha256=HfGgfNJRvrzC759gnnoojHyiWs_DYmcw5PEh5jHH-YE,39738
pip/_vendor/packaging/tags.py,sha256=y8EbheOu9WS7s-MebaXMcHMF-jzsA_C1Lz5XRTiSy4w,18883
pip/_vendor/packaging/utils.py,sha256=NAdYUwnlAOpkat_RthavX8a07YuVxgGL_vwrx73GSDM,5287
pip/_vendor/packaging/version.py,sha256=wE4sSVlF-d1H6HFC1vszEe35CwTig_fh4HHIFg95hFE,16210
pip/_vendor/pkg_resources/__init__.py,sha256=jg4dQofVk-8nGUO8gd_tWbtfIV0PWeFEV4y_uwrlCws,108869
pip/_vendor/platformdirs/__init__.py,sha256=FTA6LGNm40GwNZt3gG3uLAacWvf2E_2HTmH0rAALGR8,22285
pip/_vendor/platformdirs/__main__.py,sha256=jBJ8zb7Mpx5ebcqF83xrpO94MaeCpNGHVf9cvDN2JLg,1505
pip/_vendor/platformdirs/android.py,sha256=BqIsAnIw-6aVfxq7oVai4FDT6a0AcGkUwL1joStqxuo,7681
pip/_vendor/platformdirs/api.py,sha256=QBYdUac2eC521ek_y53uD1Dcq-lJX8IgSRVd4InC6uc,8996
pip/_vendor/platformdirs/macos.py,sha256=wftsbsvq6nZ0WORXSiCrZNkRHz_WKuktl0a6mC7MFkI,5580
pip/_vendor/platformdirs/py.typed,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip/_vendor/platformdirs/unix.py,sha256=Cci9Wqt35dAMsg6HT9nRGHSBW5obb0pR3AE1JJnsCXg,10643
pip/_vendor/platformdirs/version.py,sha256=kvsvY0Rd2WGRRrOgeTDKewa3rT0x212Ex5AgbU2NjMk,411
pip/_vendor/platformdirs/windows.py,sha256=IFpiohUBwxPtCzlyKwNtxyW4Jk8haa6W8o59mfrDXVo,10125
pip/_vendor/pygments/__init__.py,sha256=TVGTxny40TqHezz7-4TJ4ehs_m4Dj21jdP24h06vw-M,2983
pip/_vendor/pygments/__main__.py,sha256=es8EKMvXj5yToIfQ-pf3Dv5TnIeeM6sME0LW-n4ecHo,353
pip/_vendor/pygments/cmdline.py,sha256=vblyaGq79OI9SRqeRfpoLCOj7nzpiiw-fz5zb46Y07o,23650
pip/_vendor/pygments/console.py,sha256=2wZ5W-U6TudJD1_NLUwjclMpbomFM91lNv11_60sfGY,1697
pip/_vendor/pygments/filter.py,sha256=j5aLM9a9wSx6eH1oy473oSkJ02hGWNptBlVo4s1g_30,1938
pip/_vendor/pygments/filters/__init__.py,sha256=h_koYkUFo-FFUxjs564JHUAz7O3yJpVwI6fKN3MYzG0,40386
pip/_vendor/pygments/formatter.py,sha256=J9OL9hXLJKZk7moUgKwpjW9HNf4WlJFg_o_-Z_S_tTY,4178
pip/_vendor/pygments/formatters/__init__.py,sha256=1_zM_79hxxurS946tTl5m30Twh8AbzUTtuv-v7oWU_4,5431
pip/_vendor/pygments/formatters/_mapping.py,sha256=1Cw37FuQlNacnxRKmtlPX4nyLoX9_ttko5ZwscNUZZ4,4176
pip/_vendor/pygments/formatters/bbcode.py,sha256=r1b7wzWTJouADDLh-Z11iRi4iQxD0JKJ1qHl6mOYxsA,3314
pip/_vendor/pygments/formatters/groff.py,sha256=xy8Zf3tXOo6MWrXh7yPGWx3lVEkg_DhY4CxmsDb0IVo,5094
pip/_vendor/pygments/formatters/html.py,sha256=iauRmUK7KnA0kDbxQ-C2p1x-bjoWbDPlBqsT9ZPFTUg,35676
pip/_vendor/pygments/formatters/img.py,sha256=bklYds13mYy6mxBJS9aOfR8SEn3BtLcnRb10zuAwD6M,23140
pip/_vendor/pygments/formatters/irc.py,sha256=Ep-m8jd3voFO6Fv57cUGFmz6JVA67IEgyiBOwv0N4a0,4981
pip/_vendor/pygments/formatters/latex.py,sha256=FGzJ-YqSTE8z_voWPdzvLY5Tq8jE_ygjGjM6dXZJ8-k,19351
pip/_vendor/pygments/formatters/other.py,sha256=gPxkk5BdAzWTCgbEHg1lpLi-1F6ZPh5A_aotgLXHnzg,5073
pip/_vendor/pygments/formatters/pangomarkup.py,sha256=6LKnQc8yh49f802bF0sPvbzck4QivMYqqoXAPaYP8uU,2212
pip/_vendor/pygments/formatters/rtf.py,sha256=aA0v_psW6KZI3N18TKDifxeL6mcF8EDXcPXDWI4vhVQ,5014
pip/_vendor/pygments/formatters/svg.py,sha256=dQONWypbzfvzGCDtdp3M_NJawScJvM2DiHbx1k-ww7g,7335
pip/_vendor/pygments/formatters/terminal.py,sha256=FG-rpjRpFmNpiGB4NzIucvxq6sQIXB3HOTo2meTKtrU,4674
pip/_vendor/pygments/formatters/terminal256.py,sha256=13SJ3D5pFdqZ9zROE6HbWnBDwHvOGE8GlsmqGhprRp4,11753
pip/_vendor/pygments/lexer.py,sha256=IHe9eZiKTFzemc1i6qwKcNBZUJ918V2BzREbViwT0cY,35284
pip/_vendor/pygments/lexers/__init__.py,sha256=WD1uIk2EmIMbdy1Wv2UbjqZg5lTvZvpmATS5ZdvLQKo,12161
pip/_vendor/pygments/lexers/_mapping.py,sha256=FMX2ffTEHQGgiwZA9vYSPIAyqOnf2Uw9OiG4GI7wXDs,74926
pip/_vendor/pygments/lexers/python.py,sha256=DzeHBmW1IxQCL7ujXhLSW7AOXlnNcNfrk6JX46iZYbk,53448
pip/_vendor/pygments/modeline.py,sha256=eF2vO4LpOGoPvIKKkbPfnyut8hT4UiebZPpb-BYGQdI,986
pip/_vendor/pygments/plugin.py,sha256=j1Fh310RbV2DQ9nvkmkqvlj38gdyuYKllLnGxbc8sJM,2591
pip/_vendor/pygments/regexopt.py,sha256=jg1ALogcYGU96TQS9isBl6dCrvw5y5--BP_K-uFk_8s,3072
pip/_vendor/pygments/scanner.py,sha256=b_nu5_f3HCgSdp5S_aNRBQ1MSCm4ZjDwec2OmTRickw,3092
pip/_vendor/pygments/sphinxext.py,sha256=XIHxBwMMM2bIaR4XtMH_U8M6H6zpJ-H-xeRsHaeGtD0,7770
pip/_vendor/pygments/style.py,sha256=IR2flUl31IetX-5YJAITUMRRAxk-fTJ3f9nM3D6cKg4,6420
pip/_vendor/pygments/styles/__init__.py,sha256=VMj3B7F6Kf1LeAPTFWF3B8Rt0OZLj_4jZ2WdgC59ooo,2042
pip/_vendor/pygments/styles/_mapping.py,sha256=8nY9bcEF1Zw9Xu0bmqffqYEHHbNZvCQHit2OVlJWHyk,3251
pip/_vendor/pygments/token.py,sha256=DXVQcLULVn05LG63bagiqJd2FH3UzheVUBmdQeXn1U8,6226
pip/_vendor/pygments/unistring.py,sha256=FaUfG14NBJEKLQoY9qj6JYeXrpYcLmKulghdxOGFaOc,63223
pip/_vendor/pygments/util.py,sha256=AEVY0qonyyEMgv4Do2dINrrqUAwUk2XYSqHM650uzek,10230
pip/_vendor/pyproject_hooks/__init__.py,sha256=kCehmy0UaBa9oVMD7ZIZrnswfnP3LXZ5lvnNJAL5JBM,491
pip/_vendor/pyproject_hooks/_compat.py,sha256=by6evrYnqkisiM-MQcvOKs5bgDMzlOSgZqRHNqf04zE,138
pip/_vendor/pyproject_hooks/_impl.py,sha256=61GJxzQip0IInhuO69ZI5GbNQ82XEDUB_1Gg5_KtUoc,11920
pip/_vendor/pyproject_hooks/_in_process/__init__.py,sha256=9gQATptbFkelkIy0OfWFEACzqxXJMQDWCH9rBOAZVwQ,546
pip/_vendor/pyproject_hooks/_in_process/_in_process.py,sha256=m2b34c917IW5o-Q_6TYIHlsK9lSUlNiyrITTUH_zwew,10927
pip/_vendor/requests/__init__.py,sha256=HlB_HzhrzGtfD_aaYUwUh1zWXLZ75_YCLyit75d0Vz8,5057
pip/_vendor/requests/__version__.py,sha256=FVfglgZmNQnmYPXpOohDU58F5EUb_-VnSTaAesS187g,435
pip/_vendor/requests/_internal_utils.py,sha256=nMQymr4hs32TqVo5AbCrmcJEhvPUh7xXlluyqwslLiQ,1495
pip/_vendor/requests/adapters.py,sha256=J7VeVxKBvawbtlX2DERVo05J9BXTcWYLMHNd1Baa-bk,27607
pip/_vendor/requests/api.py,sha256=_Zb9Oa7tzVIizTKwFrPjDEY9ejtm_OnSRERnADxGsQs,6449
pip/_vendor/requests/auth.py,sha256=kF75tqnLctZ9Mf_hm9TZIj4cQWnN5uxRz8oWsx5wmR0,10186
pip/_vendor/requests/certs.py,sha256=PVPooB0jP5hkZEULSCwC074532UFbR2Ptgu0I5zwmCs,575
pip/_vendor/requests/compat.py,sha256=Mo9f9xZpefod8Zm-n9_StJcVTmwSukXR2p3IQyyVXvU,1485
pip/_vendor/requests/cookies.py,sha256=bNi-iqEj4NPZ00-ob-rHvzkvObzN3lEpgw3g6paS3Xw,18590
pip/_vendor/requests/exceptions.py,sha256=D1wqzYWne1mS2rU43tP9CeN1G7QAy7eqL9o1god6Ejw,4272
pip/_vendor/requests/help.py,sha256=hRKaf9u0G7fdwrqMHtF3oG16RKktRf6KiwtSq2Fo1_0,3813
pip/_vendor/requests/hooks.py,sha256=CiuysiHA39V5UfcCBXFIx83IrDpuwfN9RcTUgv28ftQ,733
pip/_vendor/requests/models.py,sha256=x4K4CmH-lC0l2Kb-iPfMN4dRXxHEcbOaEWBL_i09AwI,35483
pip/_vendor/requests/packages.py,sha256=_ZQDCJTJ8SP3kVWunSqBsRZNPzj2c1WFVqbdr08pz3U,1057
pip/_vendor/requests/sessions.py,sha256=ykTI8UWGSltOfH07HKollH7kTBGw4WhiBVaQGmckTw4,30495
pip/_vendor/requests/status_codes.py,sha256=iJUAeA25baTdw-6PfD0eF4qhpINDJRJI-yaMqxs4LEI,4322
pip/_vendor/requests/structures.py,sha256=-IbmhVz06S-5aPSZuUthZ6-6D9XOjRuTXHOabY041XM,2912
pip/_vendor/requests/utils.py,sha256=L79vnFbzJ3SFLKtJwpoWe41Tozi3RlZv94pY1TFIyow,33631
pip/_vendor/resolvelib/__init__.py,sha256=h509TdEcpb5-44JonaU3ex2TM15GVBLjM9CNCPwnTTs,537
pip/_vendor/resolvelib/compat/__init__.py,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip/_vendor/resolvelib/compat/collections_abc.py,sha256=uy8xUZ-NDEw916tugUXm8HgwCGiMO0f-RcdnpkfXfOs,156
pip/_vendor/resolvelib/providers.py,sha256=fuuvVrCetu5gsxPB43ERyjfO8aReS3rFQHpDgiItbs4,5871
pip/_vendor/resolvelib/py.typed,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip/_vendor/resolvelib/reporters.py,sha256=TSbRmWzTc26w0ggsV1bxVpeWDB8QNIre6twYl7GIZBE,1601
pip/_vendor/resolvelib/resolvers.py,sha256=G8rsLZSq64g5VmIq-lB7UcIJ1gjAxIQJmTF4REZleQ0,20511
pip/_vendor/resolvelib/structs.py,sha256=0_1_XO8z_CLhegP3Vpf9VJ3zJcfLm0NOHRM-i0Ykz3o,4963
pip/_vendor/rich/__init__.py,sha256=dRxjIL-SbFVY0q3IjSMrfgBTHrm1LZDgLOygVBwiYZc,6090
pip/_vendor/rich/__main__.py,sha256=eO7Cq8JnrgG8zVoeImiAs92q3hXNMIfp0w5lMsO7Q2Y,8477
pip/_vendor/rich/_cell_widths.py,sha256=fbmeyetEdHjzE_Vx2l1uK7tnPOhMs2X1lJfO3vsKDpA,10209
pip/_vendor/rich/_emoji_codes.py,sha256=hu1VL9nbVdppJrVoijVshRlcRRe_v3dju3Mmd2sKZdY,140235
pip/_vendor/rich/_emoji_replace.py,sha256=n-kcetsEUx2ZUmhQrfeMNc-teeGhpuSQ5F8VPBsyvDo,1064
pip/_vendor/rich/_export_format.py,sha256=RI08pSrm5tBSzPMvnbTqbD9WIalaOoN5d4M1RTmLq1Y,2128
pip/_vendor/rich/_extension.py,sha256=Xt47QacCKwYruzjDi-gOBq724JReDj9Cm9xUi5fr-34,265
pip/_vendor/rich/_fileno.py,sha256=HWZxP5C2ajMbHryvAQZseflVfQoGzsKOHzKGsLD8ynQ,799
pip/_vendor/rich/_inspect.py,sha256=oZJGw31e64dwXSCmrDnvZbwVb1ZKhWfU8wI3VWohjJk,9695
pip/_vendor/rich/_log_render.py,sha256=1ByI0PA1ZpxZY3CGJOK54hjlq4X-Bz_boIjIqCd8Kns,3225
pip/_vendor/rich/_loop.py,sha256=hV_6CLdoPm0va22Wpw4zKqM0RYsz3TZxXj0PoS-9eDQ,1236
pip/_vendor/rich/_null_file.py,sha256=tGSXk_v-IZmbj1GAzHit8A3kYIQMiCpVsCFfsC-_KJ4,1387
pip/_vendor/rich/_palettes.py,sha256=cdev1JQKZ0JvlguV9ipHgznTdnvlIzUFDBb0It2PzjI,7063
pip/_vendor/rich/_pick.py,sha256=evDt8QN4lF5CiwrUIXlOJCntitBCOsI3ZLPEIAVRLJU,423
pip/_vendor/rich/_ratio.py,sha256=Zt58apszI6hAAcXPpgdWKpu3c31UBWebOeR4mbyptvU,5471
pip/_vendor/rich/_spinners.py,sha256=U2r1_g_1zSjsjiUdAESc2iAMc3i4ri_S8PYP6kQ5z1I,19919
pip/_vendor/rich/_stack.py,sha256=-C8OK7rxn3sIUdVwxZBBpeHhIzX0eI-VM3MemYfaXm0,351
pip/_vendor/rich/_timer.py,sha256=zelxbT6oPFZnNrwWPpc1ktUeAT-Vc4fuFcRZLQGLtMI,417
pip/_vendor/rich/_win32_console.py,sha256=P0vxI2fcndym1UU1S37XAzQzQnkyY7YqAKmxm24_gug,22820
pip/_vendor/rich/_windows.py,sha256=aBwaD_S56SbgopIvayVmpk0Y28uwY2C5Bab1wl3Bp-I,1925
pip/_vendor/rich/_windows_renderer.py,sha256=t74ZL3xuDCP3nmTp9pH1L5LiI2cakJuQRQleHCJerlk,2783
pip/_vendor/rich/_wrap.py,sha256=FlSsom5EX0LVkA3KWy34yHnCfLtqX-ZIepXKh-70rpc,3404
pip/_vendor/rich/abc.py,sha256=ON-E-ZqSSheZ88VrKX2M3PXpFbGEUUZPMa_Af0l-4f0,890
pip/_vendor/rich/align.py,sha256=sCUkisXkQfoq-IQPyBELfJ8l7LihZJX3HbH8K7Cie-M,10368
pip/_vendor/rich/ansi.py,sha256=iD6532QYqnBm6hADulKjrV8l8kFJ-9fEVooHJHH3hMg,6906
pip/_vendor/rich/bar.py,sha256=ldbVHOzKJOnflVNuv1xS7g6dLX2E3wMnXkdPbpzJTcs,3263
pip/_vendor/rich/box.py,sha256=nr5fYIUghB_iUCEq6y0Z3LlCT8gFPDrzN9u2kn7tJl4,10831
pip/_vendor/rich/cells.py,sha256=aMmGK4BjXhgE6_JF1ZEGmW3O7mKkE8g84vUnj4Et4To,4780
pip/_vendor/rich/color.py,sha256=bCRATVdRe5IClJ6Hl62de2PKQ_U4i2MZ4ugjUEg7Tao,18223
pip/_vendor/rich/color_triplet.py,sha256=3lhQkdJbvWPoLDO-AnYImAWmJvV5dlgYNCVZ97ORaN4,1054
pip/_vendor/rich/columns.py,sha256=HUX0KcMm9dsKNi11fTbiM_h2iDtl8ySCaVcxlalEzq8,7131
pip/_vendor/rich/console.py,sha256=deFZIubq2M9A2MCsKFAsFQlWDvcOMsGuUA07QkOaHIw,99173
pip/_vendor/rich/constrain.py,sha256=1VIPuC8AgtKWrcncQrjBdYqA3JVWysu6jZo1rrh7c7Q,1288
pip/_vendor/rich/containers.py,sha256=c_56TxcedGYqDepHBMTuZdUIijitAQgnox-Qde0Z1qo,5502
pip/_vendor/rich/control.py,sha256=DSkHTUQLorfSERAKE_oTAEUFefZnZp4bQb4q8rHbKws,6630
pip/_vendor/rich/default_styles.py,sha256=-Fe318kMVI_IwciK5POpThcO0-9DYJ67TZAN6DlmlmM,8082
pip/_vendor/rich/diagnose.py,sha256=an6uouwhKPAlvQhYpNNpGq9EJysfMIOvvCbO3oSoR24,972
pip/_vendor/rich/emoji.py,sha256=omTF9asaAnsM4yLY94eR_9dgRRSm1lHUszX20D1yYCQ,2501
pip/_vendor/rich/errors.py,sha256=5pP3Kc5d4QJ_c0KFsxrfyhjiPVe7J1zOqSFbFAzcV-Y,642
pip/_vendor/rich/file_proxy.py,sha256=Tl9THMDZ-Pk5Wm8sI1gGg_U5DhusmxD-FZ0fUbcU0W0,1683
pip/_vendor/rich/filesize.py,sha256=9fTLAPCAwHmBXdRv7KZU194jSgNrRb6Wx7RIoBgqeKY,2508
pip/_vendor/rich/highlighter.py,sha256=6ZAjUcNhBRajBCo9umFUclyi2xL0-55JL7S0vYGUJu4,9585
pip/_vendor/rich/json.py,sha256=vVEoKdawoJRjAFayPwXkMBPLy7RSTs-f44wSQDR2nJ0,5031
pip/_vendor/rich/jupyter.py,sha256=QyoKoE_8IdCbrtiSHp9TsTSNyTHY0FO5whE7jOTd9UE,3252
pip/_vendor/rich/layout.py,sha256=ajkSFAtEVv9EFTcFs-w4uZfft7nEXhNzL7ZVdgrT5rI,14004
pip/_vendor/rich/live.py,sha256=vUcnJV2LMSK3sQNaILbm0-_B8BpAeiHfcQMAMLfpRe0,14271
pip/_vendor/rich/live_render.py,sha256=zJtB471jGziBtEwxc54x12wEQtH4BuQr1SA8v9kU82w,3666
pip/_vendor/rich/logging.py,sha256=uB-cB-3Q4bmXDLLpbOWkmFviw-Fde39zyMV6tKJ2WHQ,11903
pip/_vendor/rich/markup.py,sha256=3euGKP5s41NCQwaSjTnJxus5iZMHjxpIM0W6fCxra38,8451
pip/_vendor/rich/measure.py,sha256=HmrIJX8sWRTHbgh8MxEay_83VkqNW_70s8aKP5ZcYI8,5305
pip/_vendor/rich/padding.py,sha256=kTFGsdGe0os7tXLnHKpwTI90CXEvrceeZGCshmJy5zw,4970
pip/_vendor/rich/pager.py,sha256=SO_ETBFKbg3n_AgOzXm41Sv36YxXAyI3_R-KOY2_uSc,828
pip/_vendor/rich/palette.py,sha256=lInvR1ODDT2f3UZMfL1grq7dY_pDdKHw4bdUgOGaM4Y,3396
pip/_vendor/rich/panel.py,sha256=2Fd1V7e1kHxlPFIusoHY5T7-Cs0RpkrihgVG9ZVqJ4g,10705
pip/_vendor/rich/pretty.py,sha256=5oIHP_CGWnHEnD0zMdW5qfGC5kHqIKn7zH_eC4crULE,35848
pip/_vendor/rich/progress.py,sha256=P02xi7T2Ua3qq17o83bkshe4c0v_45cg8VyTj6US6Vg,59715
pip/_vendor/rich/progress_bar.py,sha256=L4jw8E6Qb_x-jhOrLVhkuMaPmiAhFIl8jHQbWFrKuR8,8164
pip/_vendor/rich/prompt.py,sha256=wdOn2X8XTJKnLnlw6PoMY7xG4iUPp3ezt4O5gqvpV-E,11304
pip/_vendor/rich/protocol.py,sha256=5hHHDDNHckdk8iWH5zEbi-zuIVSF5hbU2jIo47R7lTE,1391
pip/_vendor/rich/py.typed,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip/_vendor/rich/region.py,sha256=rNT9xZrVZTYIXZC0NYn41CJQwYNbR-KecPOxTgQvB8Y,166
pip/_vendor/rich/repr.py,sha256=5MZJZmONgC6kud-QW-_m1okXwL2aR6u6y-pUcUCJz28,4431
pip/_vendor/rich/rule.py,sha256=0fNaS_aERa3UMRc3T5WMpN_sumtDxfaor2y3of1ftBk,4602
pip/_vendor/rich/scope.py,sha256=TMUU8qo17thyqQCPqjDLYpg_UU1k5qVd-WwiJvnJVas,2843
pip/_vendor/rich/screen.py,sha256=YoeReESUhx74grqb0mSSb9lghhysWmFHYhsbMVQjXO8,1591
pip/_vendor/rich/segment.py,sha256=hU1ueeXqI6YeFa08K9DAjlF2QLxcJY9pwZx7RsXavlk,24246
pip/_vendor/rich/spinner.py,sha256=15koCmF0DQeD8-k28Lpt6X_zJQUlzEhgo_6A6uy47lc,4339
pip/_vendor/rich/status.py,sha256=kkPph3YeAZBo-X-4wPp8gTqZyU466NLwZBA4PZTTewo,4424
pip/_vendor/rich/style.py,sha256=3hiocH_4N8vwRm3-8yFWzM7tSwjjEven69XqWasSQwM,27073
pip/_vendor/rich/styled.py,sha256=eZNnzGrI4ki_54pgY3Oj0T-x3lxdXTYh4_ryDB24wBU,1258
pip/_vendor/rich/syntax.py,sha256=TnZDuOD4DeHFbkaVEAji1gf8qgAlMU9Boe_GksMGCkk,35475
pip/_vendor/rich/table.py,sha256=nGEvAZHF4dy1vT9h9Gj9O5qhSQO3ODAxJv0RY1vnIB8,39680
pip/_vendor/rich/terminal_theme.py,sha256=1j5-ufJfnvlAo5Qsi_ACZiXDmwMXzqgmFByObT9-yJY,3370
pip/_vendor/rich/text.py,sha256=5rQ3zvNrg5UZKNLecbh7fiw9v3HeFulNVtRY_CBDjjE,47312
pip/_vendor/rich/theme.py,sha256=belFJogzA0W0HysQabKaHOc3RWH2ko3fQAJhoN-AFdo,3777
pip/_vendor/rich/themes.py,sha256=0xgTLozfabebYtcJtDdC5QkX5IVUEaviqDUJJh4YVFk,102
pip/_vendor/rich/traceback.py,sha256=CUpxYLjQWIb6vQQ6O72X0hvDV6caryGqU6UweHgOyCY,29601
pip/_vendor/rich/tree.py,sha256=meAOUU6sYnoBEOX2ILrPLY9k5bWrWNQKkaiEFvHinXM,9167
pip/_vendor/tenacity/__init__.py,sha256=ZD4ZvZabfZWjlDvoNZDKki_q2wk2xuE-_DcNDElxrOw,20518
pip/_vendor/tenacity/_asyncio.py,sha256=Qi6wgQsGa9MQibYRy3OXqcDQswIZZ00dLOoSUGN-6o8,3551
pip/_vendor/tenacity/_utils.py,sha256=ubs6a7sxj3JDNRKWCyCU2j5r1CB7rgyONgZzYZq6D_4,2179
pip/_vendor/tenacity/after.py,sha256=S5NCISScPeIrKwIeXRwdJl3kV9Q4nqZfnNPDx6Hf__g,1682
pip/_vendor/tenacity/before.py,sha256=dIZE9gmBTffisfwNkK0F1xFwGPV41u5GK70UY4Pi5Kc,1562
pip/_vendor/tenacity/before_sleep.py,sha256=YmpgN9Y7HGlH97U24vvq_YWb5deaK4_DbiD8ZuFmy-E,2372
pip/_vendor/tenacity/nap.py,sha256=fRWvnz1aIzbIq9Ap3gAkAZgDH6oo5zxMrU6ZOVByq0I,1383
pip/_vendor/tenacity/py.typed,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip/_vendor/tenacity/retry.py,sha256=jrzD_mxA5mSTUEdiYB7SHpxltjhPSYZSnSRATb-ggRc,8746
pip/_vendor/tenacity/stop.py,sha256=YMJs7ZgZfND65PRLqlGB_agpfGXlemx_5Hm4PKnBqpQ,3086
pip/_vendor/tenacity/tornadoweb.py,sha256=po29_F1Mt8qZpsFjX7EVwAT0ydC_NbVia9gVi7R_wXA,2142
pip/_vendor/tenacity/wait.py,sha256=3FcBJoCDgym12_dN6xfK8C1gROY0Hn4NSI2u8xv50uE,8024
pip/_vendor/tomli/__init__.py,sha256=JhUwV66DB1g4Hvt1UQCVMdfCu-IgAV8FXmvDU9onxd4,396
pip/_vendor/tomli/_parser.py,sha256=g9-ENaALS-B8dokYpCuzUFalWlog7T-SIYMjLZSWrtM,22633
pip/_vendor/tomli/_re.py,sha256=dbjg5ChZT23Ka9z9DHOXfdtSpPwUfdgMXnj8NOoly-w,2943
pip/_vendor/tomli/_types.py,sha256=-GTG2VUqkpxwMqzmVO4F7ybKddIbAnuAHXfmWQcTi3Q,254
pip/_vendor/tomli/py.typed,sha256=8PjyZ1aVoQpRVvt71muvuq5qE-jTFZkK-GLHkhdebmc,26
pip/_vendor/truststore/__init__.py,sha256=M-PhuLMIF7gxKXk7tpo2MD7dk6nqG1ae8GXWdNXbMdQ,403
pip/_vendor/truststore/_api.py,sha256=B9JIHipzBIS8pMP_J50-o1DHVZsvKZQUXTB0HQQ_UPg,10461
pip/_vendor/truststore/_macos.py,sha256=VJ24avz5aEGYAs_kWvnGjMJtuIP4xJcYa459UQOQC3M,17608
pip/_vendor/truststore/_openssl.py,sha256=LLUZ7ZGaio-i5dpKKjKCSeSufmn6T8pi9lDcFnvSyq0,2324
pip/_vendor/truststore/_ssl_constants.py,sha256=NUD4fVKdSD02ri7-db0tnO0VqLP9aHuzmStcW7tAl08,1130
pip/_vendor/truststore/_windows.py,sha256=eldNViHNHeY5r3fiBoz_JFGD37atXB9S5yaRoPKEGAA,17891
pip/_vendor/truststore/py.typed,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip/_vendor/typing_extensions.py,sha256=t3bGA8vfcv8alpavDr-UIeaehafE8gWkBJsqTmZOWL8,122341
pip/_vendor/urllib3/__init__.py,sha256=iXLcYiJySn0GNbWOOZDDApgBL1JgP44EZ8i1760S8Mc,3333
pip/_vendor/urllib3/_collections.py,sha256=pyASJJhW7wdOpqJj9QJA8FyGRfr8E8uUUhqUvhF0728,11372
pip/_vendor/urllib3/_version.py,sha256=cuJvnSrWxXGYgQ3-ZRoPMw8-qaN5tpw71jnH1t16dLA,64
pip/_vendor/urllib3/connection.py,sha256=92k9td_y4PEiTIjNufCUa1NzMB3J3w0LEdyokYgXnW8,20300
pip/_vendor/urllib3/connectionpool.py,sha256=Be6q65SR9laoikg-h_jmc_p8OWtEmwgq_Om_Xtig-2M,40285
pip/_vendor/urllib3/contrib/__init__.py,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip/_vendor/urllib3/contrib/_appengine_environ.py,sha256=bDbyOEhW2CKLJcQqAKAyrEHN-aklsyHFKq6vF8ZFsmk,957
pip/_vendor/urllib3/contrib/_securetransport/__init__.py,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip/_vendor/urllib3/contrib/_securetransport/bindings.py,sha256=4Xk64qIkPBt09A5q-RIFUuDhNc9mXilVapm7WnYnzRw,17632
pip/_vendor/urllib3/contrib/_securetransport/low_level.py,sha256=B2JBB2_NRP02xK6DCa1Pa9IuxrPwxzDzZbixQkb7U9M,13922
pip/_vendor/urllib3/contrib/appengine.py,sha256=VR68eAVE137lxTgjBDwCna5UiBZTOKa01Aj_-5BaCz4,11036
pip/_vendor/urllib3/contrib/ntlmpool.py,sha256=NlfkW7WMdW8ziqudopjHoW299og1BTWi0IeIibquFwk,4528
pip/_vendor/urllib3/contrib/pyopenssl.py,sha256=hDJh4MhyY_p-oKlFcYcQaVQRDv6GMmBGuW9yjxyeejM,17081
pip/_vendor/urllib3/contrib/securetransport.py,sha256=Fef1IIUUFHqpevzXiDPbIGkDKchY2FVKeVeLGR1Qq3g,34446
pip/_vendor/urllib3/contrib/socks.py,sha256=aRi9eWXo9ZEb95XUxef4Z21CFlnnjbEiAo9HOseoMt4,7097
pip/_vendor/urllib3/exceptions.py,sha256=0Mnno3KHTNfXRfY7638NufOPkUb6mXOm-Lqj-4x2w8A,8217
pip/_vendor/urllib3/fields.py,sha256=kvLDCg_JmH1lLjUUEY_FLS8UhY7hBvDPuVETbY8mdrM,8579
pip/_vendor/urllib3/filepost.py,sha256=5b_qqgRHVlL7uLtdAYBzBh-GHmU5AfJVt_2N0XS3PeY,2440
pip/_vendor/urllib3/packages/__init__.py,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip/_vendor/urllib3/packages/backports/__init__.py,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pip/_vendor/urllib3/packages/backports/makefile.py,sha256=nbzt3i0agPVP07jqqgjhaYjMmuAi_W5E0EywZivVO8E,1417
pip/_vendor/urllib3/packages/backports/weakref_finalize.py,sha256=tRCal5OAhNSRyb0DhHp-38AtIlCsRP8BxF3NX-6rqIA,5343
pip/_vendor/urllib3/packages/six.py,sha256=b9LM0wBXv7E7SrbCjAm4wwN-hrH-iNxv18LgWNMMKPo,34665
pip/_vendor/urllib3/poolmanager.py,sha256=aWyhXRtNO4JUnCSVVqKTKQd8EXTvUm1VN9pgs2bcONo,19990
pip/_vendor/urllib3/request.py,sha256=YTWFNr7QIwh7E1W9dde9LM77v2VWTJ5V78XuTTw7D1A,6691
pip/_vendor/urllib3/response.py,sha256=fmDJAFkG71uFTn-sVSTh2Iw0WmcXQYqkbRjihvwBjU8,30641
pip/_vendor/urllib3/util/__init__.py,sha256=JEmSmmqqLyaw8P51gUImZh8Gwg9i1zSe-DoqAitn2nc,1155
pip/_vendor/urllib3/util/connection.py,sha256=5Lx2B1PW29KxBn2T0xkN1CBgRBa3gGVJBKoQoRogEVk,4901
pip/_vendor/urllib3/util/proxy.py,sha256=zUvPPCJrp6dOF0N4GAVbOcl6o-4uXKSrGiTkkr5vUS4,1605
pip/_vendor/urllib3/util/queue.py,sha256=nRgX8_eX-_VkvxoX096QWoz8Ps0QHUAExILCY_7PncM,498
pip/_vendor/urllib3/util/request.py,sha256=C0OUt2tcU6LRiQJ7YYNP9GvPrSvl7ziIBekQ-5nlBZk,3997
pip/_vendor/urllib3/util/response.py,sha256=GJpg3Egi9qaJXRwBh5wv-MNuRWan5BIu40oReoxWP28,3510
pip/_vendor/urllib3/util/retry.py,sha256=Z6WEf518eTOXP5jr5QSQ9gqJI0DVYt3Xs3EKnYaTmus,22013
pip/_vendor/urllib3/util/ssl_.py,sha256=X4-AqW91aYPhPx6-xbf66yHFQKbqqfC_5Zt4WkLX1Hc,17177
pip/_vendor/urllib3/util/ssl_match_hostname.py,sha256=Ir4cZVEjmAk8gUAIHWSi7wtOO83UCYABY2xFD1Ql_WA,5758
pip/_vendor/urllib3/util/ssltransport.py,sha256=NA-u5rMTrDFDFC8QzRKUEKMG0561hOD4qBTr3Z4pv6E,6895
pip/_vendor/urllib3/util/timeout.py,sha256=cwq4dMk87mJHSBktK1miYJ-85G-3T3RmT20v7SFCpno,10168
pip/_vendor/urllib3/util/url.py,sha256=lCAE7M5myA8EDdW0sJuyyZhVB9K_j38ljWhHAnFaWoE,14296
pip/_vendor/urllib3/util/wait.py,sha256=fOX0_faozG2P7iVojQoE1mbydweNyTcm-hXEfFrTtLI,5403
pip/_vendor/vendor.txt,sha256=eiYUkiHRU35nedL7Y_FifDuDFVvCktFrR4LQzoQpl7k,346
pip/py.typed,sha256=EBVvvPRTn_eIpz5e5QztSCdrMX7Qwd7VP93RSoIlZ2I,286
```
```bash
./.venv/lib/python3.9/site-packages/pip-24.1.2.dist-info/WHEEL
```
```
Wheel-Version: 1.0
Generator: setuptools (70.2.0)
Root-Is-Purelib: true
Tag: py3-none-any
```
```bash
./.venv/lib/python3.9/site-packages/pip-24.1.2.dist-info/entry_points.txt
```
```
[console_scripts]
pip = pip._internal.cli.main:main
pip3 = pip._internal.cli.main:main
```
```bash
./.venv/lib/python3.9/site-packages/pip-24.1.2.dist-info/top_level.txt
```
```
pip
```
```bash
./.venv/lib/python3.9/site-packages/pip-24.1.2.dist-info/LICENSE.txt
```
```
Copyright (c) 2008-present The pip developers (see AUTHORS.txt file)

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
```bash
./.venv/lib/python3.9/site-packages/pip-24.1.2.dist-info/AUTHORS.txt
```
```
@Switch01
A_Rog
Aakanksha Agrawal
Abhinav Sagar
ABHYUDAY PRATAP SINGH
abs51295
AceGentile
Adam Chainz
Adam Tse
Adam Wentz
admin
Adolfo Ochagav√≠a
Adrien Morison
Agus
ahayrapetyan
Ahilya
AinsworthK
Akash Srivastava
Alan Yee
Albert Tugushev
Albert-Guan
albertg
Alberto Sottile
Aleks Bunin
Ales Erjavec
Alethea Flowers
Alex Gaynor
Alex Gr√∂nholm
Alex Hedges
Alex Loosley
Alex Morega
Alex Stachowiak
Alexander Shtyrov
Alexandre Conrad
Alexey Popravka
Ale≈° Erjavec
Alli
Ami Fischman
Ananya Maiti
Anatoly Techtonik
Anders Kaseorg
Andre Aguiar
Andreas Lutro
Andrei Geacar
Andrew Gaul
Andrew Shymanel
Andrey Bienkowski
Andrey Bulgakov
Andr√©s Delfino
Andy Freeland
Andy Kluger
Ani Hayrapetyan
Aniruddha Basak
Anish Tambe
Anrs Hu
Anthony Sottile
Antoine Musso
Anton Ovchinnikov
Anton Patrushev
Antonio Alvarado Hernandez
Antony Lee
Antti Kaihola
Anubhav Patel
Anudit Nagar
Anuj Godase
AQNOUCH Mohammed
AraHaan
arena
arenasys
Arindam Choudhury
Armin Ronacher
Arnon Yaari
Artem
Arun Babu Neelicattu
Ashley Manton
Ashwin Ramaswami
atse
Atsushi Odagiri
Avinash Karhana
Avner Cohen
Awit (Ah-Wit) Ghirmai
Baptiste Mispelon
Barney Gale
barneygale
Bartek Ogryczak
Bastian Venthur
Ben Bodenmiller
Ben Darnell
Ben Hoyt
Ben Mares
Ben Rosser
Bence Nagy
Benjamin Peterson
Benjamin VanEvery
Benoit Pierre
Berker Peksag
Bernard
Bernard Tyers
Bernardo B. Marques
Bernhard M. Wiedemann
Bertil Hatt
Bhavam Vidyarthi
Blazej Michalik
Bogdan Opanchuk
BorisZZZ
Brad Erickson
Bradley Ayers
Brandon L. Reiss
Brandt Bucher
Brannon Dorsey
Brett Randall
Brett Rosen
Brian Cristante
Brian Rosner
briantracy
BrownTruck
Bruno Oliveira
Bruno Reni√©
Bruno S
Bstrdsmkr
Buck Golemon
burrows
Bussonnier Matthias
bwoodsend
c22
Caleb Martinez
Calvin Smith
Carl Meyer
Carlos Liam
Carol Willing
Carter Thayer
Cass
Chandrasekhar Atina
Chih-Hsuan Yen
Chris Brinker
Chris Hunt
Chris Jerdonek
Chris Kuehl
Chris McDonough
Chris Pawley
Chris Pryer
Chris Wolfe
Christian Clauss
Christian Heimes
Christian Oudard
Christoph Reiter
Christopher Hunt
Christopher Snyder
chrysle
cjc7373
Clark Boylan
Claudio Jolowicz
Clay McClure
Cody
Cody Soyland
Colin Watson
Collin Anderson
Connor Osborn
Cooper Lees
Cooper Ry Lees
Cory Benfield
Cory Wright
Craig Kerstiens
Cristian Sorinel
Cristina
Cristina Mu√±oz
ctg123
Curtis Doty
cytolentino
Daan De Meyer
Dale
Damian
Damian Quiroga
Damian Shaw
Dan Black
Dan Savilonis
Dan Sully
Dane Hillard
daniel
Daniel Collins
Daniel Hahler
Daniel Holth
Daniel Jost
Daniel Katz
Daniel Shaulov
Daniele Esposti
Daniele Nicolodi
Daniele Procida
Daniil Konovalenko
Danny Hermes
Danny McClanahan
Darren Kavanagh
Dav Clark
Dave Abrahams
Dave Jones
David Aguilar
David Black
David Bordeynik
David Caro
David D Lowe
David Evans
David Hewitt
David Linke
David Poggi
David Poznik
David Pursehouse
David Runge
David Tucker
David Wales
Davidovich
ddelange
Deepak Sharma
Deepyaman Datta
Denise Yu
dependabot[bot]
derwolfe
Desetude
Devesh Kumar Singh
devsagul
Diego Caraballo
Diego Ramirez
DiegoCaraballo
Dimitri Merejkowsky
Dimitri Papadopoulos
Dirk Stolle
Dmitry Gladkov
Dmitry Volodin
Domen Ko≈æar
Dominic Davis-Foster
Donald Stufft
Dongweiming
doron zarhi
Dos Moonen
Douglas Thor
DrFeathers
Dustin Ingram
Dwayne Bailey
Ed Morley
Edgar Ram√≠rez
Edgar Ram√≠rez Mondrag√≥n
Ee Durbin
Efflam Lemaillet
efflamlemaillet
Eitan Adler
ekristina
elainechan
Eli Schwartz
Elisha Hollander
Ellen Marie Dash
Emil Burzo
Emil Styrke
Emmanuel Arias
Endoh Takanao
enoch
Erdinc Mutlu
Eric Cousineau
Eric Gillingham
Eric Hanchrow
Eric Hopper
Erik M. Bray
Erik Rose
Erwin Janssen
Eugene Vereshchagin
everdimension
Federico
Felipe Peter
Felix Yan
fiber-space
Filip Kokosi≈Ñski
Filipe La√≠ns
Finn Womack
finnagin
Flavio Amurrio
Florian Briand
Florian Rathgeber
Francesco
Francesco Montesano
Fredrik Orderud
Frost Ming
Gabriel Curio
Gabriel de Perthuis
Garry Polley
gavin
gdanielson
Geoffrey Sneddon
George Song
Georgi Valkov
Georgy Pchelkin
ghost
Giftlin Rajaiah
gizmoguy1
gkdoc
Godefroid Chapelle
Gopinath M
GOTO Hayato
gousaiyang
gpiks
Greg Roodt
Greg Ward
Guilherme Espada
Guillaume Seguin
gutsytechster
Guy Rozendorn
Guy Tuval
gzpan123
Hanjun Kim
Hari Charan
Harsh Vardhan
harupy
Harutaka Kawamura
hauntsaninja
Henrich Hartzer
Henry Schreiner
Herbert Pfennig
Holly Stotelmyer
Honnix
Hsiaoming Yang
Hugo Lopes Tavares
Hugo van Kemenade
Hugues Bruant
Hynek Schlawack
Ian Bicking
Ian Cordasco
Ian Lee
Ian Stapleton Cordasco
Ian Wienand
Igor Kuzmitshov
Igor Sobreira
Ikko Ashimine
Ilan Schnell
Illia Volochii
Ilya Baryshev
Inada Naoki
Ionel Cristian MƒÉrie»ô
Ionel Maries Cristian
Itamar Turner-Trauring
Ivan Pozdeev
J. Nick Koston
Jacob Kim
Jacob Walls
Jaime Sanz
jakirkham
Jakub Kuczys
Jakub Stasiak
Jakub Vysoky
Jakub Wilk
James Cleveland
James Curtin
James Firth
James Gerity
James Polley
Jan Pokorn√Ω
Jannis Leidel
Jarek Potiuk
jarondl
Jason Curtis
Jason R. Coombs
JasonMo
JasonMo1
Jay Graves
Jean Abou Samra
Jean-Christophe Fillion-Robin
Jeff Barber
Jeff Dairiki
Jeff Widman
Jelmer Vernooƒ≥
jenix21
Jeremy Stanley
Jeremy Zafran
Jesse Rittner
Jiashuo Li
Jim Fisher
Jim Garrison
Jiun Bae
Jivan Amara
Joe Bylund
Joe Michelini
John Paton
John Sirois
John T. Wodder II
John-Scott Atlakson
johnthagen
Jon Banafato
Jon Dufresne
Jon Parise
Jonas Nockert
Jonathan Herbert
Joonatan Partanen
Joost Molenaar
Jorge Niedbalski
Joseph Bylund
Joseph Long
Josh Bronson
Josh Hansen
Josh Schneier
Joshua
Juan Luis Cano Rodr√≠guez
Juanjo Baz√°n
Judah Rand
Julian Berman
Julian Gethmann
Julien Demoor
Jussi Kukkonen
jwg4
Jyrki Pulliainen
Kai Chen
Kai Mueller
Kamal Bin Mustafa
kasium
kaustav haldar
keanemind
Keith Maxwell
Kelsey Hightower
Kenneth Belitzky
Kenneth Reitz
Kevin Burke
Kevin Carter
Kevin Frommelt
Kevin R Patterson
Kexuan Sun
Kit Randel
Klaas van Schelven
KOLANICH
konstin
kpinc
Krishna Oza
Kumar McMillan
Kurt McKee
Kyle Persohn
lakshmanaram
Laszlo Kiss-Kollar
Laurent Bristiel
Laurent LAPORTE
Laurie O
Laurie Opperman
layday
Leon Sasson
Lev Givon
Lincoln de Sousa
Lipis
lorddavidiii
Loren Carvalho
Lucas Cimon
Ludovic Gasc
Luis Medel
Lukas Geiger
Lukas Juhrich
Luke Macken
Luo Jiebin
luojiebin
luz.paz
L√°szl√≥ Kiss Koll√°r
M00nL1ght
Marc Abramowitz
Marc Tamlyn
Marcus Smith
Mariatta
Mark Kohler
Mark McLoughlin
Mark Williams
Markus Hametner
Martey Dodoo
Martin Fischer
Martin H√§cker
Martin Pavlasek
Masaki
Masklinn
Matej Stuchlik
Mathew Jennings
Mathieu Bridon
Mathieu Kniewallner
Matt Bacchi
Matt Good
Matt Maker
Matt Robenolt
Matt Wozniski
matthew
Matthew Einhorn
Matthew Feickert
Matthew Gilliard
Matthew Hughes
Matthew Iversen
Matthew Treinish
Matthew Trumbell
Matthew Willson
Matthias Bussonnier
mattip
Maurits van Rees
Max W Chase
Maxim Kurnikov
Maxime Rouyrre
mayeut
mbaluna
mdebi
memoselyk
meowmeowcat
Michael
Michael Aquilina
Michael E. Karpeles
Michael Klich
Michael Mintz
Michael Williamson
michaelpacer
Micha≈Ç G√≥rny
Micka√´l Schoentgen
Miguel Araujo Perez
Mihir Singh
Mike
Mike Hendricks
Min RK
MinRK
Miro Hronƒçok
Monica Baluna
montefra
Monty Taylor
mrKazzila
Muha Ajjan
Nadav Wexler
Nahuel Ambrosini
Nate Coraor
Nate Prewitt
Nathan Houghton
Nathaniel J. Smith
Nehal J Wani
Neil Botelho
Nguy·ªÖn Gia Phong
Nicholas Serra
Nick Coghlan
Nick Stenning
Nick Timkovich
Nicolas Bock
Nicole Harris
Nikhil Benesch
Nikhil Ladha
Nikita Chepanov
Nikolay Korolev
Nipunn Koorapati
Nitesh Sharma
Niyas Sait
Noah
Noah Gorny
Nowell Strite
NtaleGrey
nvdv
OBITORASU
Ofek Lev
ofrinevo
Oliver Freund
Oliver Jeeves
Oliver Mannion
Oliver Tonnhofer
Olivier Girardot
Olivier Grisel
Ollie Rutherfurd
OMOTO Kenji
Omry Yadan
onlinejudge95
Oren Held
Oscar Benjamin
Oz N Tiram
Pachwenko
Patrick Dubroy
Patrick Jenkins
Patrick Lawson
patricktokeeffe
Patrik Kopkan
Paul Ganssle
Paul Kehrer
Paul Moore
Paul Nasrat
Paul Oswald
Paul van der Linden
Paulus Schoutsen
Pavel Safronov
Pavithra Eswaramoorthy
Pawel Jasinski
Pawe≈Ç Szramowski
Pekka Kl√§rck
Peter Gessler
Peter Lis√°k
Peter Shen
Peter Waller
Petr Viktorin
petr-tik
Phaneendra Chiruvella
Phil Elson
Phil Freo
Phil Pennock
Phil Whelan
Philip J√§genstedt
Philip Molloy
Philippe Ombredanne
Pi Delport
Pierre-Yves Rofes
Pieter Degroote
pip
Prabakaran Kumaresshan
Prabhjyotsing Surjit Singh Sodhi
Prabhu Marappan
Pradyun Gedam
Prashant Sharma
Pratik Mallya
pre-commit-ci[bot]
Preet Thakkar
Preston Holmes
Przemek Wrzos
Pulkit Goyal
q0w
Qiangning Hong
Qiming Xu
Quentin Lee
Quentin Pradet
R. David Murray
Rafael Caricio
Ralf Schmitt
Ran Benita
Razzi Abuissa
rdb
Reece Dunham
Remi Rampin
Rene Dudfield
Riccardo Magliocchetti
Riccardo Schirone
Richard Jones
Richard Si
Ricky Ng-Adam
Rishi
RobberPhex
Robert Collins
Robert McGibbon
Robert Pollak
Robert T. McGibbon
robin elisha robinson
Roey Berman
Rohan Jain
Roman Bogorodskiy
Roman Donchenko
Romuald Brunet
ronaudinho
Ronny Pfannschmidt
Rory McCann
Ross Brattain
Roy Wellington ‚Ö£
Ruairidh MacLeod
Russell Keith-Magee
Ryan Shepherd
Ryan Wooden
ryneeverett
S. Guliaev
Sachi King
Salvatore Rinchiera
sandeepkiran-js
Sander Van Balen
Savio Jomton
schlamar
Scott Kitterman
Sean
seanj
Sebastian Jordan
Sebastian Schaetz
Segev Finer
SeongSoo Cho
Sergey Vasilyev
Seth Michael Larson
Seth Woodworth
Shahar Epstein
Shantanu
shenxianpeng
shireenrao
Shivansh-007
Shixian Sheng
Shlomi Fish
Shovan Maity
Simeon Visser
Simon Cross
Simon Pichugin
sinoroc
sinscary
snook92
socketubs
Sorin Sbarnea
Srinivas Nyayapati
Stavros Korokithakis
Stefan Scherfke
Stefano Rivera
Stephan Erb
Stephen Rosen
stepshal
Steve (Gadget) Barnes
Steve Barnes
Steve Dower
Steve Kowalik
Steven Myint
Steven Silvester
stonebig
studioj
St√©phane Bidoul
St√©phane Bidoul (ACSONE)
St√©phane Klein
Sumana Harihareswara
Surbhi Sharma
Sviatoslav Sydorenko
Swat009
Sylvain
Takayuki SHIMIZUKAWA
Taneli Hukkinen
tbeswick
Thiago
Thijs Triemstra
Thomas Fenzl
Thomas Grainger
Thomas Guettler
Thomas Johansson
Thomas Kluyver
Thomas Smith
Thomas VINCENT
Tim D. Smith
Tim Gates
Tim Harder
Tim Heap
tim smith
tinruufu
Tobias Hermann
Tom Forbes
Tom Freudenheim
Tom V
Tomas Hrnciar
Tomas Orsava
Tomer Chachamu
Tommi Enenkel | AnB
Tom√°≈° Hrnƒçiar
Tony Beswick
Tony Narlock
Tony Zhaocheng Tan
TonyBeswick
toonarmycaptain
Toshio Kuratomi
toxinu
Travis Swicegood
Tushar Sadhwani
Tzu-ping Chung
Valentin Haenel
Victor Stinner
victorvpaulo
Vikram - Google
Viktor Sz√©pe
Ville Skytt√§
Vinay Sajip
Vincent Philippon
Vinicyus Macedo
Vipul Kumar
Vitaly Babiy
Vladimir Fokow
Vladimir Rutsky
W. Trevor King
Wil Tan
Wilfred Hughes
William Edwards
William ML Leslie
William T Olson
William Woodruff
Wilson Mo
wim glenn
Winson Luk
Wolfgang Maier
Wu Zhenyu
XAMES3
Xavier Fernandez
Xianpeng Shen
xoviat
xtreak
YAMAMOTO Takashi
Yen Chi Hsuan
Yeray Diaz Diaz
Yoval P
Yu Jian
Yuan Jing Vincent Yan
Yusuke Hayashi
Zearin
Zhiping Deng
ziebam
Zvezdan Petkovic
≈Åukasz Langa
–†–æ–º–∞–Ω –î–æ–Ω—á–µ–Ω–∫–æ
–°–µ–º—ë–Ω –ú–∞—Ä—å—è—Å–∏–Ω
```
```bash
./.venv/lib/python3.9/site-packages/pip-24.1.2.dist-info/REQUESTED
```
```

```
```bash
./.venv/lib/python3.9/site-packages/pip-24.1.2.dist-info/INSTALLER
```
```
pip
```
```bash
./.venv/lib/python3.9/site-packages/pip-24.1.2.dist-info/METADATA
```
```
Metadata-Version: 2.1
Name: pip
Version: 24.1.2
Summary: The PyPA recommended tool for installing Python packages.
Author-email: The pip developers <distutils-sig@python.org>
License: MIT
Project-URL: Homepage, https://pip.pypa.io/
Project-URL: Documentation, https://pip.pypa.io
Project-URL: Source, https://github.com/pypa/pip
Project-URL: Changelog, https://pip.pypa.io/en/stable/news/
Classifier: Development Status :: 5 - Production/Stable
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: MIT License
Classifier: Topic :: Software Development :: Build Tools
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3 :: Only
Classifier: Programming Language :: Python :: 3.8
Classifier: Programming Language :: Python :: 3.9
Classifier: Programming Language :: Python :: 3.10
Classifier: Programming Language :: Python :: 3.11
Classifier: Programming Language :: Python :: 3.12
Classifier: Programming Language :: Python :: Implementation :: CPython
Classifier: Programming Language :: Python :: Implementation :: PyPy
Requires-Python: >=3.8
Description-Content-Type: text/x-rst
License-File: LICENSE.txt
License-File: AUTHORS.txt

pip - The Python Package Installer
==================================

.. |pypi-version| image:: https://img.shields.io/pypi/v/pip.svg
   :target: https://pypi.org/project/pip/
   :alt: PyPI

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/pip
   :target: https://pypi.org/project/pip
   :alt: PyPI - Python Version

.. |docs-badge| image:: https://readthedocs.org/projects/pip/badge/?version=latest
   :target: https://pip.pypa.io/en/latest
   :alt: Documentation

|pypi-version| |python-versions| |docs-badge|

pip is the `package installer`_ for Python. You can use pip to install packages from the `Python Package Index`_ and other indexes.

Please take a look at our documentation for how to install and use pip:

* `Installation`_
* `Usage`_

We release updates regularly, with a new version every 3 months. Find more details in our documentation:

* `Release notes`_
* `Release process`_

If you find bugs, need help, or want to talk to the developers, please use our mailing lists or chat rooms:

* `Issue tracking`_
* `Discourse channel`_
* `User IRC`_

If you want to get involved head over to GitHub to get the source code, look at our development documentation and feel free to jump on the developer mailing lists and chat rooms:

* `GitHub page`_
* `Development documentation`_
* `Development IRC`_

Code of Conduct
---------------

Everyone interacting in the pip project's codebases, issue trackers, chat
rooms, and mailing lists is expected to follow the `PSF Code of Conduct`_.

.. _package installer: https://packaging.python.org/guides/tool-recommendations/
.. _Python Package Index: https://pypi.org
.. _Installation: https://pip.pypa.io/en/stable/installation/
.. _Usage: https://pip.pypa.io/en/stable/
.. _Release notes: https://pip.pypa.io/en/stable/news.html
.. _Release process: https://pip.pypa.io/en/latest/development/release-process/
.. _GitHub page: https://github.com/pypa/pip
.. _Development documentation: https://pip.pypa.io/en/latest/development
.. _Issue tracking: https://github.com/pypa/pip/issues
.. _Discourse channel: https://discuss.python.org/c/packaging
.. _User IRC: https://kiwiirc.com/nextclient/#ircs://irc.libera.chat:+6697/pypa
.. _Development IRC: https://kiwiirc.com/nextclient/#ircs://irc.libera.chat:+6697/pypa-dev
.. _PSF Code of Conduct: https://github.com/pypa/.github/blob/main/CODE_OF_CONDUCT.md
```
```bash
./.venv/lib/python3.9/site-packages/PyYAML-6.0.1.dist-info/RECORD
```
```
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/_yaml/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/yaml/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/yaml/composer.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/yaml/constructor.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/yaml/cyaml.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/yaml/dumper.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/yaml/emitter.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/yaml/error.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/yaml/events.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/yaml/loader.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/yaml/nodes.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/yaml/parser.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/yaml/reader.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/yaml/representer.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/yaml/resolver.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/yaml/scanner.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/yaml/serializer.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/yaml/tokens.cpython-39.pyc,,
PyYAML-6.0.1.dist-info/INSTALLER,sha256=zuuue4knoyJ-UwPPXg8fezS7VCrXJQrAP7zeNuwvFQg,4
PyYAML-6.0.1.dist-info/LICENSE,sha256=jTko-dxEkP1jVwfLiOsmvXZBAqcoKVQwfT5RZ6V36KQ,1101
PyYAML-6.0.1.dist-info/METADATA,sha256=UNNF8-SzzwOKXVo-kV5lXUGH2_wDWMBmGxqISpp5HQk,2058
PyYAML-6.0.1.dist-info/RECORD,,
PyYAML-6.0.1.dist-info/REQUESTED,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
PyYAML-6.0.1.dist-info/WHEEL,sha256=d8sjrkKo8h1ZY8Oxdq-K-58JEo6nLEfNKzkM0CYZtr0,108
PyYAML-6.0.1.dist-info/top_level.txt,sha256=rpj0IVMTisAjh_1vG3Ccf9v5jpCQwAz6cD1IVU5ZdhQ,11
_yaml/__init__.py,sha256=04Ae_5osxahpJHa3XBZUAf4wi6XX32gR8D6X6p64GEA,1402
yaml/__init__.py,sha256=bhl05qSeO-1ZxlSRjGrvl2m9nrXb1n9-GQatTN0Mrqc,12311
yaml/_yaml.cpython-39-darwin.so,sha256=kzFH9vEUWVcU9mnwLz6lWG8d0QRDh1OUP3ztTRyYtRI,378855
yaml/composer.py,sha256=_Ko30Wr6eDWUeUpauUGT3Lcg9QPBnOPVlTnIMRGJ9FM,4883
yaml/constructor.py,sha256=kNgkfaeLUkwQYY_Q6Ff1Tz2XVw_pG1xVE9Ak7z-viLA,28639
yaml/cyaml.py,sha256=6ZrAG9fAYvdVe2FK_w0hmXoG7ZYsoYUwapG8CiC72H0,3851
yaml/dumper.py,sha256=PLctZlYwZLp7XmeUdwRuv4nYOZ2UBnDIUy8-lKfLF-o,2837
yaml/emitter.py,sha256=jghtaU7eFwg31bG0B7RZea_29Adi9CKmXq_QjgQpCkQ,43006
yaml/error.py,sha256=Ah9z-toHJUbE9j-M8YpxgSRM5CgLCcwVzJgLLRF2Fxo,2533
yaml/events.py,sha256=50_TksgQiE4up-lKo_V-nBy-tAIxkIPQxY5qDhKCeHw,2445
yaml/loader.py,sha256=UVa-zIqmkFSCIYq_PgSGm4NSJttHY2Rf_zQ4_b1fHN0,2061
yaml/nodes.py,sha256=gPKNj8pKCdh2d4gr3gIYINnPOaOxGhJAUiYhGRnPE84,1440
yaml/parser.py,sha256=ilWp5vvgoHFGzvOZDItFoGjD6D42nhlZrZyjAwa0oJo,25495
yaml/reader.py,sha256=0dmzirOiDG4Xo41RnuQS7K9rkY3xjHiVasfDMNTqCNw,6794
yaml/representer.py,sha256=IuWP-cAW9sHKEnS0gCqSa894k1Bg4cgTxaDwIcbRQ-Y,14190
yaml/resolver.py,sha256=9L-VYfm4mWHxUD1Vg4X7rjDRK_7VZd6b92wzq7Y2IKY,9004
yaml/scanner.py,sha256=YEM3iLZSaQwXcQRg2l2R4MdT0zGP2F9eHkKGKnHyWQY,51279
yaml/serializer.py,sha256=ChuFgmhU01hj4xgI8GaKv6vfM2Bujwa9i7d2FAHj7cA,4165
yaml/tokens.py,sha256=lTQIzSVw8Mg9wv459-TjiOQe6wVziqaRlqX2_89rp54,2573
```
```bash
./.venv/lib/python3.9/site-packages/PyYAML-6.0.1.dist-info/LICENSE
```
```
Copyright (c) 2017-2021 Ingy d√∂t Net
Copyright (c) 2006-2016 Kirill Simonov

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
```bash
./.venv/lib/python3.9/site-packages/PyYAML-6.0.1.dist-info/WHEEL
```
```
Wheel-Version: 1.0
Generator: bdist_wheel (0.40.0)
Root-Is-Purelib: false
Tag: cp39-cp39-macosx_11_0_arm64
```
```bash
./.venv/lib/python3.9/site-packages/PyYAML-6.0.1.dist-info/top_level.txt
```
```
_yaml
yaml
```
```bash
./.venv/lib/python3.9/site-packages/PyYAML-6.0.1.dist-info/REQUESTED
```
```

```
```bash
./.venv/lib/python3.9/site-packages/PyYAML-6.0.1.dist-info/INSTALLER
```
```
pip
```
```bash
./.venv/lib/python3.9/site-packages/PyYAML-6.0.1.dist-info/METADATA
```
```
Metadata-Version: 2.1
Name: PyYAML
Version: 6.0.1
Summary: YAML parser and emitter for Python
Home-page: https://pyyaml.org/
Download-URL: https://pypi.org/project/PyYAML/
Author: Kirill Simonov
Author-email: xi@resolvent.net
License: MIT
Project-URL: Bug Tracker, https://github.com/yaml/pyyaml/issues
Project-URL: CI, https://github.com/yaml/pyyaml/actions
Project-URL: Documentation, https://pyyaml.org/wiki/PyYAMLDocumentation
Project-URL: Mailing lists, http://lists.sourceforge.net/lists/listinfo/yaml-core
Project-URL: Source Code, https://github.com/yaml/pyyaml
Platform: Any
Classifier: Development Status :: 5 - Production/Stable
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: MIT License
Classifier: Operating System :: OS Independent
Classifier: Programming Language :: Cython
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.6
Classifier: Programming Language :: Python :: 3.7
Classifier: Programming Language :: Python :: 3.8
Classifier: Programming Language :: Python :: 3.9
Classifier: Programming Language :: Python :: 3.10
Classifier: Programming Language :: Python :: 3.11
Classifier: Programming Language :: Python :: Implementation :: CPython
Classifier: Programming Language :: Python :: Implementation :: PyPy
Classifier: Topic :: Software Development :: Libraries :: Python Modules
Classifier: Topic :: Text Processing :: Markup
Requires-Python: >=3.6
License-File: LICENSE

YAML is a data serialization format designed for human readability
and interaction with scripting languages.  PyYAML is a YAML parser
and emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages.  PyYAML
supports standard YAML tags and provides Python-specific tags that
allow to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistence.
```
```bash
./.venv/lib/python3.9/site-packages/dotenv/version.py
```
```
__version__ = "1.0.1"
```
```bash
./.venv/lib/python3.9/site-packages/dotenv/variables.py
```
```
import re
from abc import ABCMeta, abstractmethod
from typing import Iterator, Mapping, Optional, Pattern

_posix_variable: Pattern[str] = re.compile(
    r"""
    \$\{
        (?P<name>[^\}:]*)
        (?::-
            (?P<default>[^\}]*)
        )?
    \}
    """,
    re.VERBOSE,
)


class Atom(metaclass=ABCMeta):
    def __ne__(self, other: object) -> bool:
        result = self.__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        return not result

    @abstractmethod
    def resolve(self, env: Mapping[str, Optional[str]]) -> str: ...


class Literal(Atom):
    def __init__(self, value: str) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"Literal(value={self.value})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.value == other.value

    def __hash__(self) -> int:
        return hash((self.__class__, self.value))

    def resolve(self, env: Mapping[str, Optional[str]]) -> str:
        return self.value


class Variable(Atom):
    def __init__(self, name: str, default: Optional[str]) -> None:
        self.name = name
        self.default = default

    def __repr__(self) -> str:
        return f"Variable(name={self.name}, default={self.default})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.name, self.default) == (other.name, other.default)

    def __hash__(self) -> int:
        return hash((self.__class__, self.name, self.default))

    def resolve(self, env: Mapping[str, Optional[str]]) -> str:
        default = self.default if self.default is not None else ""
        result = env.get(self.name, default)
        return result if result is not None else ""


def parse_variables(value: str) -> Iterator[Atom]:
    cursor = 0

    for match in _posix_variable.finditer(value):
        (start, end) = match.span()
        name = match["name"]
        default = match["default"]

        if start > cursor:
            yield Literal(value=value[cursor:start])

        yield Variable(name=name, default=default)
        cursor = end

    length = len(value)
    if cursor < length:
        yield Literal(value=value[cursor:length])
```
```bash
./.venv/lib/python3.9/site-packages/dotenv/__init__.py
```
```
from typing import Any, Optional

from .main import (dotenv_values, find_dotenv, get_key, load_dotenv, set_key,
                   unset_key)


def load_ipython_extension(ipython: Any) -> None:
    from .ipython import load_ipython_extension
    load_ipython_extension(ipython)


def get_cli_string(
    path: Optional[str] = None,
    action: Optional[str] = None,
    key: Optional[str] = None,
    value: Optional[str] = None,
    quote: Optional[str] = None,
):
    """Returns a string suitable for running as a shell script.

    Useful for converting a arguments passed to a fabric task
    to be passed to a `local` or `run` command.
    """
    command = ['dotenv']
    if quote:
        command.append(f'-q {quote}')
    if path:
        command.append(f'-f {path}')
    if action:
        command.append(action)
        if key:
            command.append(key)
            if value:
                if ' ' in value:
                    command.append(f'"{value}"')
                else:
                    command.append(value)

    return ' '.join(command).strip()


__all__ = ['get_cli_string',
           'load_dotenv',
           'dotenv_values',
           'get_key',
           'set_key',
           'unset_key',
           'find_dotenv',
           'load_ipython_extension']
```
```bash
./.venv/lib/python3.9/site-packages/dotenv/parser.py
```
```
import codecs
import re
from typing import (IO, Iterator, Match, NamedTuple, Optional,  # noqa:F401
                    Pattern, Sequence, Tuple)


def make_regex(string: str, extra_flags: int = 0) -> Pattern[str]:
    return re.compile(string, re.UNICODE | extra_flags)


_newline = make_regex(r"(
|
|
)")
_multiline_whitespace = make_regex(r"\s*", extra_flags=re.MULTILINE)
_whitespace = make_regex(r"[^\S
]*")
_export = make_regex(r"(?:export[^\S
]+)?")
_single_quoted_key = make_regex(r"'([^']+)'")
_unquoted_key = make_regex(r"([^=\#\s]+)")
_equal_sign = make_regex(r"(=[^\S
]*)")
_single_quoted_value = make_regex(r"'((?:\'|[^'])*)'")
_double_quoted_value = make_regex(r'"((?:\"|[^"])*)"')
_unquoted_value = make_regex(r"([^
]*)")
_comment = make_regex(r"(?:[^\S
]*#[^
]*)?")
_end_of_line = make_regex(r"[^\S
]*(?:
|
|
|$)")
_rest_of_line = make_regex(r"[^
]*(?:
|
|
)?")
_double_quote_escapes = make_regex(r"\[\'\"abfnrtv]")
_single_quote_escapes = make_regex(r"\[\']")


class Original(NamedTuple):
    string: str
    line: int


class Binding(NamedTuple):
    key: Optional[str]
    value: Optional[str]
    original: Original
    error: bool


class Position:
    def __init__(self, chars: int, line: int) -> None:
        self.chars = chars
        self.line = line

    @classmethod
    def start(cls) -> "Position":
        return cls(chars=0, line=1)

    def set(self, other: "Position") -> None:
        self.chars = other.chars
        self.line = other.line

    def advance(self, string: str) -> None:
        self.chars += len(string)
        self.line += len(re.findall(_newline, string))


class Error(Exception):
    pass


class Reader:
    def __init__(self, stream: IO[str]) -> None:
        self.string = stream.read()
        self.position = Position.start()
        self.mark = Position.start()

    def has_next(self) -> bool:
        return self.position.chars < len(self.string)

    def set_mark(self) -> None:
        self.mark.set(self.position)

    def get_marked(self) -> Original:
        return Original(
            string=self.string[self.mark.chars:self.position.chars],
            line=self.mark.line,
        )

    def peek(self, count: int) -> str:
        return self.string[self.position.chars:self.position.chars + count]

    def read(self, count: int) -> str:
        result = self.string[self.position.chars:self.position.chars + count]
        if len(result) < count:
            raise Error("read: End of string")
        self.position.advance(result)
        return result

    def read_regex(self, regex: Pattern[str]) -> Sequence[str]:
        match = regex.match(self.string, self.position.chars)
        if match is None:
            raise Error("read_regex: Pattern not found")
        self.position.advance(self.string[match.start():match.end()])
        return match.groups()


def decode_escapes(regex: Pattern[str], string: str) -> str:
    def decode_match(match: Match[str]) -> str:
        return codecs.decode(match.group(0), 'unicode-escape')  # type: ignore

    return regex.sub(decode_match, string)


def parse_key(reader: Reader) -> Optional[str]:
    char = reader.peek(1)
    if char == "#":
        return None
    elif char == "'":
        (key,) = reader.read_regex(_single_quoted_key)
    else:
        (key,) = reader.read_regex(_unquoted_key)
    return key


def parse_unquoted_value(reader: Reader) -> str:
    (part,) = reader.read_regex(_unquoted_value)
    return re.sub(r"\s+#.*", "", part).rstrip()


def parse_value(reader: Reader) -> str:
    char = reader.peek(1)
    if char == u"'":
        (value,) = reader.read_regex(_single_quoted_value)
        return decode_escapes(_single_quote_escapes, value)
    elif char == u'"':
        (value,) = reader.read_regex(_double_quoted_value)
        return decode_escapes(_double_quote_escapes, value)
    elif char in (u"", u"
", u"
"):
        return u""
    else:
        return parse_unquoted_value(reader)


def parse_binding(reader: Reader) -> Binding:
    reader.set_mark()
    try:
        reader.read_regex(_multiline_whitespace)
        if not reader.has_next():
            return Binding(
                key=None,
                value=None,
                original=reader.get_marked(),
                error=False,
            )
        reader.read_regex(_export)
        key = parse_key(reader)
        reader.read_regex(_whitespace)
        if reader.peek(1) == "=":
            reader.read_regex(_equal_sign)
            value: Optional[str] = parse_value(reader)
        else:
            value = None
        reader.read_regex(_comment)
        reader.read_regex(_end_of_line)
        return Binding(
            key=key,
            value=value,
            original=reader.get_marked(),
            error=False,
        )
    except Error:
        reader.read_regex(_rest_of_line)
        return Binding(
            key=None,
            value=None,
            original=reader.get_marked(),
            error=True,
        )


def parse_stream(stream: IO[str]) -> Iterator[Binding]:
    reader = Reader(stream)
    while reader.has_next():
        yield parse_binding(reader)
```
```bash
./.venv/lib/python3.9/site-packages/dotenv/cli.py
```
```
import json
import os
import shlex
import sys
from contextlib import contextmanager
from subprocess import Popen
from typing import Any, Dict, IO, Iterator, List

try:
    import click
except ImportError:
    sys.stderr.write('It seems python-dotenv is not installed with cli option. 
'
                     'Run pip install "python-dotenv[cli]" to fix this.')
    sys.exit(1)

from .main import dotenv_values, set_key, unset_key
from .version import __version__


def enumerate_env():
    """
    Return a path for the ${pwd}/.env file.

    If pwd does not exist, return None.
    """
    try:
        cwd = os.getcwd()
    except FileNotFoundError:
        return None
    path = os.path.join(cwd, '.env')
    return path


@click.group()
@click.option('-f', '--file', default=enumerate_env(),
              type=click.Path(file_okay=True),
              help="Location of the .env file, defaults to .env file in current working directory.")
@click.option('-q', '--quote', default='always',
              type=click.Choice(['always', 'never', 'auto']),
              help="Whether to quote or not the variable values. Default mode is always. This does not affect parsing.")
@click.option('-e', '--export', default=False,
              type=click.BOOL,
              help="Whether to write the dot file as an executable bash script.")
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx: click.Context, file: Any, quote: Any, export: Any) -> None:
    """This script is used to set, get or unset values from a .env file."""
    ctx.obj = {'QUOTE': quote, 'EXPORT': export, 'FILE': file}


@contextmanager
def stream_file(path: os.PathLike) -> Iterator[IO[str]]:
    """
    Open a file and yield the corresponding (decoded) stream.

    Exits with error code 2 if the file cannot be opened.
    """

    try:
        with open(path) as stream:
            yield stream
    except OSError as exc:
        print(f"Error opening env file: {exc}", file=sys.stderr)
        exit(2)


@cli.command()
@click.pass_context
@click.option('--format', default='simple',
              type=click.Choice(['simple', 'json', 'shell', 'export']),
              help="The format in which to display the list. Default format is simple, "
                   "which displays name=value without quotes.")
def list(ctx: click.Context, format: bool) -> None:
    """Display all the stored key/value."""
    file = ctx.obj['FILE']

    with stream_file(file) as stream:
        values = dotenv_values(stream=stream)

    if format == 'json':
        click.echo(json.dumps(values, indent=2, sort_keys=True))
    else:
        prefix = 'export ' if format == 'export' else ''
        for k in sorted(values):
            v = values[k]
            if v is not None:
                if format in ('export', 'shell'):
                    v = shlex.quote(v)
                click.echo(f'{prefix}{k}={v}')


@cli.command()
@click.pass_context
@click.argument('key', required=True)
@click.argument('value', required=True)
def set(ctx: click.Context, key: Any, value: Any) -> None:
    """Store the given key/value."""
    file = ctx.obj['FILE']
    quote = ctx.obj['QUOTE']
    export = ctx.obj['EXPORT']
    success, key, value = set_key(file, key, value, quote, export)
    if success:
        click.echo(f'{key}={value}')
    else:
        exit(1)


@cli.command()
@click.pass_context
@click.argument('key', required=True)
def get(ctx: click.Context, key: Any) -> None:
    """Retrieve the value for the given key."""
    file = ctx.obj['FILE']

    with stream_file(file) as stream:
        values = dotenv_values(stream=stream)

    stored_value = values.get(key)
    if stored_value:
        click.echo(stored_value)
    else:
        exit(1)


@cli.command()
@click.pass_context
@click.argument('key', required=True)
def unset(ctx: click.Context, key: Any) -> None:
    """Removes the given key."""
    file = ctx.obj['FILE']
    quote = ctx.obj['QUOTE']
    success, key = unset_key(file, key, quote)
    if success:
        click.echo(f"Successfully removed {key}")
    else:
        exit(1)


@cli.command(context_settings={'ignore_unknown_options': True})
@click.pass_context
@click.option(
    "--override/--no-override",
    default=True,
    help="Override variables from the environment file with those from the .env file.",
)
@click.argument('commandline', nargs=-1, type=click.UNPROCESSED)
def run(ctx: click.Context, override: bool, commandline: List[str]) -> None:
    """Run command with environment variables present."""
    file = ctx.obj['FILE']
    if not os.path.isfile(file):
        raise click.BadParameter(
            f'Invalid value for \'-f\' "{file}" does not exist.',
            ctx=ctx
        )
    dotenv_as_dict = {
        k: v
        for (k, v) in dotenv_values(file).items()
        if v is not None and (override or k not in os.environ)
    }

    if not commandline:
        click.echo('No command given.')
        exit(1)
    ret = run_command(commandline, dotenv_as_dict)
    exit(ret)


def run_command(command: List[str], env: Dict[str, str]) -> int:
    """Run command in sub process.

    Runs the command in a sub process with the variables from `env`
    added in the current environment variables.

    Parameters
    ----------
    command: List[str]
        The command and it's parameters
    env: Dict
        The additional environment variables

    Returns
    -------
    int
        The return code of the command

    """
    # copy the current environment variables and add the vales from
    # `env`
    cmd_env = os.environ.copy()
    cmd_env.update(env)

    p = Popen(command,
              universal_newlines=True,
              bufsize=0,
              shell=False,
              env=cmd_env)
    _, _ = p.communicate()

    return p.returncode
```
```bash
./.venv/lib/python3.9/site-packages/dotenv/ipython.py
```
```
from IPython.core.magic import Magics, line_magic, magics_class  # type: ignore
from IPython.core.magic_arguments import (argument, magic_arguments,  # type: ignore
                                          parse_argstring)  # type: ignore

from .main import find_dotenv, load_dotenv


@magics_class
class IPythonDotEnv(Magics):

    @magic_arguments()
    @argument(
        '-o', '--override', action='store_true',
        help="Indicate to override existing variables"
    )
    @argument(
        '-v', '--verbose', action='store_true',
        help="Indicate function calls to be verbose"
    )
    @argument('dotenv_path', nargs='?', type=str, default='.env',
              help='Search in increasingly higher folders for the `dotenv_path`')
    @line_magic
    def dotenv(self, line):
        args = parse_argstring(self.dotenv, line)
        # Locate the .env file
        dotenv_path = args.dotenv_path
        try:
            dotenv_path = find_dotenv(dotenv_path, True, True)
        except IOError:
            print("cannot find .env file")
            return

        # Load the .env file
        load_dotenv(dotenv_path, verbose=args.verbose, override=args.override)


def load_ipython_extension(ipython):
    """Register the %dotenv magic."""
    ipython.register_magics(IPythonDotEnv)
```
```bash
./.venv/lib/python3.9/site-packages/dotenv/py.typed
```
```
# Marker file for PEP 561
```
```bash
./.venv/lib/python3.9/site-packages/dotenv/main.py
```
```
import io
import logging
import os
import pathlib
import shutil
import sys
import tempfile
from collections import OrderedDict
from contextlib import contextmanager
from typing import (IO, Dict, Iterable, Iterator, Mapping, Optional, Tuple,
                    Union)

from .parser import Binding, parse_stream
from .variables import parse_variables

# A type alias for a string path to be used for the paths in this file.
# These paths may flow to `open()` and `shutil.move()`; `shutil.move()`
# only accepts string paths, not byte paths or file descriptors. See
# https://github.com/python/typeshed/pull/6832.
StrPath = Union[str, 'os.PathLike[str]']

logger = logging.getLogger(__name__)


def with_warn_for_invalid_lines(mappings: Iterator[Binding]) -> Iterator[Binding]:
    for mapping in mappings:
        if mapping.error:
            logger.warning(
                "Python-dotenv could not parse statement starting at line %s",
                mapping.original.line,
            )
        yield mapping


class DotEnv:
    def __init__(
        self,
        dotenv_path: Optional[StrPath],
        stream: Optional[IO[str]] = None,
        verbose: bool = False,
        encoding: Optional[str] = None,
        interpolate: bool = True,
        override: bool = True,
    ) -> None:
        self.dotenv_path: Optional[StrPath] = dotenv_path
        self.stream: Optional[IO[str]] = stream
        self._dict: Optional[Dict[str, Optional[str]]] = None
        self.verbose: bool = verbose
        self.encoding: Optional[str] = encoding
        self.interpolate: bool = interpolate
        self.override: bool = override

    @contextmanager
    def _get_stream(self) -> Iterator[IO[str]]:
        if self.dotenv_path and os.path.isfile(self.dotenv_path):
            with open(self.dotenv_path, encoding=self.encoding) as stream:
                yield stream
        elif self.stream is not None:
            yield self.stream
        else:
            if self.verbose:
                logger.info(
                    "Python-dotenv could not find configuration file %s.",
                    self.dotenv_path or '.env',
                )
            yield io.StringIO('')

    def dict(self) -> Dict[str, Optional[str]]:
        """Return dotenv as dict"""
        if self._dict:
            return self._dict

        raw_values = self.parse()

        if self.interpolate:
            self._dict = OrderedDict(resolve_variables(raw_values, override=self.override))
        else:
            self._dict = OrderedDict(raw_values)

        return self._dict

    def parse(self) -> Iterator[Tuple[str, Optional[str]]]:
        with self._get_stream() as stream:
            for mapping in with_warn_for_invalid_lines(parse_stream(stream)):
                if mapping.key is not None:
                    yield mapping.key, mapping.value

    def set_as_environment_variables(self) -> bool:
        """
        Load the current dotenv as system environment variable.
        """
        if not self.dict():
            return False

        for k, v in self.dict().items():
            if k in os.environ and not self.override:
                continue
            if v is not None:
                os.environ[k] = v

        return True

    def get(self, key: str) -> Optional[str]:
        """
        """
        data = self.dict()

        if key in data:
            return data[key]

        if self.verbose:
            logger.warning("Key %s not found in %s.", key, self.dotenv_path)

        return None


def get_key(
    dotenv_path: StrPath,
    key_to_get: str,
    encoding: Optional[str] = "utf-8",
) -> Optional[str]:
    """
    Get the value of a given key from the given .env.

    Returns `None` if the key isn't found or doesn't have a value.
    """
    return DotEnv(dotenv_path, verbose=True, encoding=encoding).get(key_to_get)


@contextmanager
def rewrite(
    path: StrPath,
    encoding: Optional[str],
) -> Iterator[Tuple[IO[str], IO[str]]]:
    pathlib.Path(path).touch()

    with tempfile.NamedTemporaryFile(mode="w", encoding=encoding, delete=False) as dest:
        error = None
        try:
            with open(path, encoding=encoding) as source:
                yield (source, dest)
        except BaseException as err:
            error = err

    if error is None:
        shutil.move(dest.name, path)
    else:
        os.unlink(dest.name)
        raise error from None


def set_key(
    dotenv_path: StrPath,
    key_to_set: str,
    value_to_set: str,
    quote_mode: str = "always",
    export: bool = False,
    encoding: Optional[str] = "utf-8",
) -> Tuple[Optional[bool], str, str]:
    """
    Adds or Updates a key/value to the given .env

    If the .env path given doesn't exist, fails instead of risking creating
    an orphan .env somewhere in the filesystem
    """
    if quote_mode not in ("always", "auto", "never"):
        raise ValueError(f"Unknown quote_mode: {quote_mode}")

    quote = (
        quote_mode == "always"
        or (quote_mode == "auto" and not value_to_set.isalnum())
    )

    if quote:
        value_out = "'{}'".format(value_to_set.replace("'", "\'"))
    else:
        value_out = value_to_set
    if export:
        line_out = f'export {key_to_set}={value_out}
'
    else:
        line_out = f"{key_to_set}={value_out}
"

    with rewrite(dotenv_path, encoding=encoding) as (source, dest):
        replaced = False
        missing_newline = False
        for mapping in with_warn_for_invalid_lines(parse_stream(source)):
            if mapping.key == key_to_set:
                dest.write(line_out)
                replaced = True
            else:
                dest.write(mapping.original.string)
                missing_newline = not mapping.original.string.endswith("
")
        if not replaced:
            if missing_newline:
                dest.write("
")
            dest.write(line_out)

    return True, key_to_set, value_to_set


def unset_key(
    dotenv_path: StrPath,
    key_to_unset: str,
    quote_mode: str = "always",
    encoding: Optional[str] = "utf-8",
) -> Tuple[Optional[bool], str]:
    """
    Removes a given key from the given `.env` file.

    If the .env path given doesn't exist, fails.
    If the given key doesn't exist in the .env, fails.
    """
    if not os.path.exists(dotenv_path):
        logger.warning("Can't delete from %s - it doesn't exist.", dotenv_path)
        return None, key_to_unset

    removed = False
    with rewrite(dotenv_path, encoding=encoding) as (source, dest):
        for mapping in with_warn_for_invalid_lines(parse_stream(source)):
            if mapping.key == key_to_unset:
                removed = True
            else:
                dest.write(mapping.original.string)

    if not removed:
        logger.warning("Key %s not removed from %s - key doesn't exist.", key_to_unset, dotenv_path)
        return None, key_to_unset

    return removed, key_to_unset


def resolve_variables(
    values: Iterable[Tuple[str, Optional[str]]],
    override: bool,
) -> Mapping[str, Optional[str]]:
    new_values: Dict[str, Optional[str]] = {}

    for (name, value) in values:
        if value is None:
            result = None
        else:
            atoms = parse_variables(value)
            env: Dict[str, Optional[str]] = {}
            if override:
                env.update(os.environ)  # type: ignore
                env.update(new_values)
            else:
                env.update(new_values)
                env.update(os.environ)  # type: ignore
            result = "".join(atom.resolve(env) for atom in atoms)

        new_values[name] = result

    return new_values


def _walk_to_root(path: str) -> Iterator[str]:
    """
    Yield directories starting from the given directory up to the root
    """
    if not os.path.exists(path):
        raise IOError('Starting path not found')

    if os.path.isfile(path):
        path = os.path.dirname(path)

    last_dir = None
    current_dir = os.path.abspath(path)
    while last_dir != current_dir:
        yield current_dir
        parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
        last_dir, current_dir = current_dir, parent_dir


def find_dotenv(
    filename: str = '.env',
    raise_error_if_not_found: bool = False,
    usecwd: bool = False,
) -> str:
    """
    Search in increasingly higher folders for the given file

    Returns path to the file if found, or an empty string otherwise
    """

    def _is_interactive():
        """ Decide whether this is running in a REPL or IPython notebook """
        try:
            main = __import__('__main__', None, None, fromlist=['__file__'])
        except ModuleNotFoundError:
            return False
        return not hasattr(main, '__file__')

    if usecwd or _is_interactive() or getattr(sys, 'frozen', False):
        # Should work without __file__, e.g. in REPL or IPython notebook.
        path = os.getcwd()
    else:
        # will work for .py files
        frame = sys._getframe()
        current_file = __file__

        while frame.f_code.co_filename == current_file or not os.path.exists(
            frame.f_code.co_filename
        ):
            assert frame.f_back is not None
            frame = frame.f_back
        frame_filename = frame.f_code.co_filename
        path = os.path.dirname(os.path.abspath(frame_filename))

    for dirname in _walk_to_root(path):
        check_path = os.path.join(dirname, filename)
        if os.path.isfile(check_path):
            return check_path

    if raise_error_if_not_found:
        raise IOError('File not found')

    return ''


def load_dotenv(
    dotenv_path: Optional[StrPath] = None,
    stream: Optional[IO[str]] = None,
    verbose: bool = False,
    override: bool = False,
    interpolate: bool = True,
    encoding: Optional[str] = "utf-8",
) -> bool:
    """Parse a .env file and then load all the variables found as environment variables.

    Parameters:
        dotenv_path: Absolute or relative path to .env file.
        stream: Text stream (such as `io.StringIO`) with .env content, used if
            `dotenv_path` is `None`.
        verbose: Whether to output a warning the .env file is missing.
        override: Whether to override the system environment variables with the variables
            from the `.env` file.
        encoding: Encoding to be used to read the file.
    Returns:
        Bool: True if at least one environment variable is set else False

    If both `dotenv_path` and `stream` are `None`, `find_dotenv()` is used to find the
    .env file.
    """
    if dotenv_path is None and stream is None:
        dotenv_path = find_dotenv()

    dotenv = DotEnv(
        dotenv_path=dotenv_path,
        stream=stream,
        verbose=verbose,
        interpolate=interpolate,
        override=override,
        encoding=encoding,
    )
    return dotenv.set_as_environment_variables()


def dotenv_values(
    dotenv_path: Optional[StrPath] = None,
    stream: Optional[IO[str]] = None,
    verbose: bool = False,
    interpolate: bool = True,
    encoding: Optional[str] = "utf-8",
) -> Dict[str, Optional[str]]:
    """
    Parse a .env file and return its content as a dict.

    The returned dict will have `None` values for keys without values in the .env file.
    For example, `foo=bar` results in `{"foo": "bar"}` whereas `foo` alone results in
    `{"foo": None}`

    Parameters:
        dotenv_path: Absolute or relative path to the .env file.
        stream: `StringIO` object with .env content, used if `dotenv_path` is `None`.
        verbose: Whether to output a warning if the .env file is missing.
        encoding: Encoding to be used to read the file.

    If both `dotenv_path` and `stream` are `None`, `find_dotenv()` is used to find the
    .env file.
    """
    if dotenv_path is None and stream is None:
        dotenv_path = find_dotenv()

    return DotEnv(
        dotenv_path=dotenv_path,
        stream=stream,
        verbose=verbose,
        interpolate=interpolate,
        override=True,
        encoding=encoding,
    ).dict()
```
```bash
./.venv/lib/python3.9/site-packages/dotenv/__main__.py
```
```
"""Entry point for cli, enables execution with `python -m dotenv`"""

from .cli import cli

if __name__ == "__main__":
    cli()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_time_periods_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.time_periods_api import TimePeriodsApi  # noqa: E501
from asana.rest import ApiException


class TestTimePeriodsApi(unittest.TestCase):
    """TimePeriodsApi unit test stubs"""

    def setUp(self):
        self.api = TimePeriodsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_time_period(self):
        """Test case for get_time_period

        Get a time period  # noqa: E501
        """
        pass

    def test_get_time_periods(self):
        """Test case for get_time_periods

        Get time periods  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_user_task_lists_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.user_task_lists_api import UserTaskListsApi  # noqa: E501
from asana.rest import ApiException


class TestUserTaskListsApi(unittest.TestCase):
    """UserTaskListsApi unit test stubs"""

    def setUp(self):
        self.api = UserTaskListsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_user_task_list(self):
        """Test case for get_user_task_list

        Get a user task list  # noqa: E501
        """
        pass

    def test_get_user_task_list_for_user(self):
        """Test case for get_user_task_list_for_user

        Get a user's task list  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_workspace_memberships_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.workspace_memberships_api import WorkspaceMembershipsApi  # noqa: E501
from asana.rest import ApiException


class TestWorkspaceMembershipsApi(unittest.TestCase):
    """WorkspaceMembershipsApi unit test stubs"""

    def setUp(self):
        self.api = WorkspaceMembershipsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_workspace_membership(self):
        """Test case for get_workspace_membership

        Get a workspace membership  # noqa: E501
        """
        pass

    def test_get_workspace_memberships_for_user(self):
        """Test case for get_workspace_memberships_for_user

        Get workspace memberships for a user  # noqa: E501
        """
        pass

    def test_get_workspace_memberships_for_workspace(self):
        """Test case for get_workspace_memberships_for_workspace

        Get the workspace memberships for a workspace  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_memberships_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.memberships_api import MembershipsApi  # noqa: E501
from asana.rest import ApiException


class TestMembershipsApi(unittest.TestCase):
    """MembershipsApi unit test stubs"""

    def setUp(self):
        self.api = MembershipsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_membership(self):
        """Test case for create_membership

        Create a membership  # noqa: E501
        """
        pass

    def test_delete_membership(self):
        """Test case for delete_membership

        Delete a membership  # noqa: E501
        """
        pass

    def test_get_membership(self):
        """Test case for get_membership

        Get a membership  # noqa: E501
        """
        pass

    def test_get_memberships(self):
        """Test case for get_memberships

        Get multiple memberships  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_teams_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.teams_api import TeamsApi  # noqa: E501
from asana.rest import ApiException


class TestTeamsApi(unittest.TestCase):
    """TeamsApi unit test stubs"""

    def setUp(self):
        self.api = TeamsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_add_user_for_team(self):
        """Test case for add_user_for_team

        Add a user to a team  # noqa: E501
        """
        pass

    def test_create_team(self):
        """Test case for create_team

        Create a team  # noqa: E501
        """
        pass

    def test_get_team(self):
        """Test case for get_team

        Get a team  # noqa: E501
        """
        pass

    def test_get_teams_for_user(self):
        """Test case for get_teams_for_user

        Get teams for a user  # noqa: E501
        """
        pass

    def test_get_teams_for_workspace(self):
        """Test case for get_teams_for_workspace

        Get teams in a workspace  # noqa: E501
        """
        pass

    def test_remove_user_for_team(self):
        """Test case for remove_user_for_team

        Remove a user from a team  # noqa: E501
        """
        pass

    def test_update_team(self):
        """Test case for update_team

        Update a team  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_audit_log_api_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.audit_log_api_api import AuditLogAPIApi  # noqa: E501
from asana.rest import ApiException


class TestAuditLogAPIApi(unittest.TestCase):
    """AuditLogAPIApi unit test stubs"""

    def setUp(self):
        self.api = AuditLogAPIApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_audit_log_events(self):
        """Test case for get_audit_log_events

        Get audit log events  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_custom_field_settings_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.custom_field_settings_api import CustomFieldSettingsApi  # noqa: E501
from asana.rest import ApiException


class TestCustomFieldSettingsApi(unittest.TestCase):
    """CustomFieldSettingsApi unit test stubs"""

    def setUp(self):
        self.api = CustomFieldSettingsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_custom_field_settings_for_portfolio(self):
        """Test case for get_custom_field_settings_for_portfolio

        Get a portfolio's custom fields  # noqa: E501
        """
        pass

    def test_get_custom_field_settings_for_project(self):
        """Test case for get_custom_field_settings_for_project

        Get a project's custom fields  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_project_briefs_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.project_briefs_api import ProjectBriefsApi  # noqa: E501
from asana.rest import ApiException


class TestProjectBriefsApi(unittest.TestCase):
    """ProjectBriefsApi unit test stubs"""

    def setUp(self):
        self.api = ProjectBriefsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_project_brief(self):
        """Test case for create_project_brief

        Create a project brief  # noqa: E501
        """
        pass

    def test_delete_project_brief(self):
        """Test case for delete_project_brief

        Delete a project brief  # noqa: E501
        """
        pass

    def test_get_project_brief(self):
        """Test case for get_project_brief

        Get a project brief  # noqa: E501
        """
        pass

    def test_update_project_brief(self):
        """Test case for update_project_brief

        Update a project brief  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_project_memberships_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.project_memberships_api import ProjectMembershipsApi  # noqa: E501
from asana.rest import ApiException


class TestProjectMembershipsApi(unittest.TestCase):
    """ProjectMembershipsApi unit test stubs"""

    def setUp(self):
        self.api = ProjectMembershipsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_project_membership(self):
        """Test case for get_project_membership

        Get a project membership  # noqa: E501
        """
        pass

    def test_get_project_memberships_for_project(self):
        """Test case for get_project_memberships_for_project

        Get memberships from a project  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_custom_fields_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.custom_fields_api import CustomFieldsApi  # noqa: E501
from asana.rest import ApiException


class TestCustomFieldsApi(unittest.TestCase):
    """CustomFieldsApi unit test stubs"""

    def setUp(self):
        self.api = CustomFieldsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_custom_field(self):
        """Test case for create_custom_field

        Create a custom field  # noqa: E501
        """
        pass

    def test_create_enum_option_for_custom_field(self):
        """Test case for create_enum_option_for_custom_field

        Create an enum option  # noqa: E501
        """
        pass

    def test_delete_custom_field(self):
        """Test case for delete_custom_field

        Delete a custom field  # noqa: E501
        """
        pass

    def test_get_custom_field(self):
        """Test case for get_custom_field

        Get a custom field  # noqa: E501
        """
        pass

    def test_get_custom_fields_for_workspace(self):
        """Test case for get_custom_fields_for_workspace

        Get a workspace's custom fields  # noqa: E501
        """
        pass

    def test_insert_enum_option_for_custom_field(self):
        """Test case for insert_enum_option_for_custom_field

        Reorder a custom field's enum  # noqa: E501
        """
        pass

    def test_update_custom_field(self):
        """Test case for update_custom_field

        Update a custom field  # noqa: E501
        """
        pass

    def test_update_enum_option(self):
        """Test case for update_enum_option

        Update an enum option  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_sections_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.sections_api import SectionsApi  # noqa: E501
from asana.rest import ApiException


class TestSectionsApi(unittest.TestCase):
    """SectionsApi unit test stubs"""

    def setUp(self):
        self.api = SectionsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_add_task_for_section(self):
        """Test case for add_task_for_section

        Add task to section  # noqa: E501
        """
        pass

    def test_create_section_for_project(self):
        """Test case for create_section_for_project

        Create a section in a project  # noqa: E501
        """
        pass

    def test_delete_section(self):
        """Test case for delete_section

        Delete a section  # noqa: E501
        """
        pass

    def test_get_section(self):
        """Test case for get_section

        Get a section  # noqa: E501
        """
        pass

    def test_get_sections_for_project(self):
        """Test case for get_sections_for_project

        Get sections in a project  # noqa: E501
        """
        pass

    def test_insert_section_for_project(self):
        """Test case for insert_section_for_project

        Move or Insert sections  # noqa: E501
        """
        pass

    def test_update_section(self):
        """Test case for update_section

        Update a section  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_projects_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.projects_api import ProjectsApi  # noqa: E501
from asana.rest import ApiException


class TestProjectsApi(unittest.TestCase):
    """ProjectsApi unit test stubs"""

    def setUp(self):
        self.api = ProjectsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_add_custom_field_setting_for_project(self):
        """Test case for add_custom_field_setting_for_project

        Add a custom field to a project  # noqa: E501
        """
        pass

    def test_add_followers_for_project(self):
        """Test case for add_followers_for_project

        Add followers to a project  # noqa: E501
        """
        pass

    def test_add_members_for_project(self):
        """Test case for add_members_for_project

        Add users to a project  # noqa: E501
        """
        pass

    def test_create_project(self):
        """Test case for create_project

        Create a project  # noqa: E501
        """
        pass

    def test_create_project_for_team(self):
        """Test case for create_project_for_team

        Create a project in a team  # noqa: E501
        """
        pass

    def test_create_project_for_workspace(self):
        """Test case for create_project_for_workspace

        Create a project in a workspace  # noqa: E501
        """
        pass

    def test_delete_project(self):
        """Test case for delete_project

        Delete a project  # noqa: E501
        """
        pass

    def test_duplicate_project(self):
        """Test case for duplicate_project

        Duplicate a project  # noqa: E501
        """
        pass

    def test_get_project(self):
        """Test case for get_project

        Get a project  # noqa: E501
        """
        pass

    def test_get_projects(self):
        """Test case for get_projects

        Get multiple projects  # noqa: E501
        """
        pass

    def test_get_projects_for_task(self):
        """Test case for get_projects_for_task

        Get projects a task is in  # noqa: E501
        """
        pass

    def test_get_projects_for_team(self):
        """Test case for get_projects_for_team

        Get a team's projects  # noqa: E501
        """
        pass

    def test_get_projects_for_workspace(self):
        """Test case for get_projects_for_workspace

        Get all projects in a workspace  # noqa: E501
        """
        pass

    def test_get_task_counts_for_project(self):
        """Test case for get_task_counts_for_project

        Get task count of a project  # noqa: E501
        """
        pass

    def test_project_save_as_template(self):
        """Test case for project_save_as_template

        Create a project template from a project  # noqa: E501
        """
        pass

    def test_remove_custom_field_setting_for_project(self):
        """Test case for remove_custom_field_setting_for_project

        Remove a custom field from a project  # noqa: E501
        """
        pass

    def test_remove_followers_for_project(self):
        """Test case for remove_followers_for_project

        Remove followers from a project  # noqa: E501
        """
        pass

    def test_remove_members_for_project(self):
        """Test case for remove_members_for_project

        Remove users from a project  # noqa: E501
        """
        pass

    def test_update_project(self):
        """Test case for update_project

        Update a project  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_goals_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.goals_api import GoalsApi  # noqa: E501
from asana.rest import ApiException


class TestGoalsApi(unittest.TestCase):
    """GoalsApi unit test stubs"""

    def setUp(self):
        self.api = GoalsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_add_followers(self):
        """Test case for add_followers

        Add a collaborator to a goal  # noqa: E501
        """
        pass

    def test_create_goal(self):
        """Test case for create_goal

        Create a goal  # noqa: E501
        """
        pass

    def test_create_goal_metric(self):
        """Test case for create_goal_metric

        Create a goal metric  # noqa: E501
        """
        pass

    def test_delete_goal(self):
        """Test case for delete_goal

        Delete a goal  # noqa: E501
        """
        pass

    def test_get_goal(self):
        """Test case for get_goal

        Get a goal  # noqa: E501
        """
        pass

    def test_get_goals(self):
        """Test case for get_goals

        Get goals  # noqa: E501
        """
        pass

    def test_get_parent_goals_for_goal(self):
        """Test case for get_parent_goals_for_goal

        Get parent goals from a goal  # noqa: E501
        """
        pass

    def test_remove_followers(self):
        """Test case for remove_followers

        Remove a collaborator from a goal  # noqa: E501
        """
        pass

    def test_update_goal(self):
        """Test case for update_goal

        Update a goal  # noqa: E501
        """
        pass

    def test_update_goal_metric(self):
        """Test case for update_goal_metric

        Update a goal metric  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_task_templates_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.task_templates_api import TaskTemplatesApi  # noqa: E501
from asana.rest import ApiException


class TestTaskTemplatesApi(unittest.TestCase):
    """TaskTemplatesApi unit test stubs"""

    def setUp(self):
        self.api = TaskTemplatesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_task_template(self):
        """Test case for get_task_template

        Get a task template  # noqa: E501
        """
        pass

    def test_get_task_templates(self):
        """Test case for get_task_templates

        Get multiple task templates  # noqa: E501
        """
        pass

    def test_instantiate_task(self):
        """Test case for instantiate_task

        Instantiate a task from a task template  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_portfolio_memberships_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.portfolio_memberships_api import PortfolioMembershipsApi  # noqa: E501
from asana.rest import ApiException


class TestPortfolioMembershipsApi(unittest.TestCase):
    """PortfolioMembershipsApi unit test stubs"""

    def setUp(self):
        self.api = PortfolioMembershipsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_portfolio_membership(self):
        """Test case for get_portfolio_membership

        Get a portfolio membership  # noqa: E501
        """
        pass

    def test_get_portfolio_memberships(self):
        """Test case for get_portfolio_memberships

        Get multiple portfolio memberships  # noqa: E501
        """
        pass

    def test_get_portfolio_memberships_for_portfolio(self):
        """Test case for get_portfolio_memberships_for_portfolio

        Get memberships from a portfolio  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_tasks_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.tasks_api import TasksApi  # noqa: E501
from asana.rest import ApiException


class TestTasksApi(unittest.TestCase):
    """TasksApi unit test stubs"""

    def setUp(self):
        self.api = TasksApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_add_dependencies_for_task(self):
        """Test case for add_dependencies_for_task

        Set dependencies for a task  # noqa: E501
        """
        pass

    def test_add_dependents_for_task(self):
        """Test case for add_dependents_for_task

        Set dependents for a task  # noqa: E501
        """
        pass

    def test_add_followers_for_task(self):
        """Test case for add_followers_for_task

        Add followers to a task  # noqa: E501
        """
        pass

    def test_add_project_for_task(self):
        """Test case for add_project_for_task

        Add a project to a task  # noqa: E501
        """
        pass

    def test_add_tag_for_task(self):
        """Test case for add_tag_for_task

        Add a tag to a task  # noqa: E501
        """
        pass

    def test_create_subtask_for_task(self):
        """Test case for create_subtask_for_task

        Create a subtask  # noqa: E501
        """
        pass

    def test_create_task(self):
        """Test case for create_task

        Create a task  # noqa: E501
        """
        pass

    def test_delete_task(self):
        """Test case for delete_task

        Delete a task  # noqa: E501
        """
        pass

    def test_duplicate_task(self):
        """Test case for duplicate_task

        Duplicate a task  # noqa: E501
        """
        pass

    def test_get_dependencies_for_task(self):
        """Test case for get_dependencies_for_task

        Get dependencies from a task  # noqa: E501
        """
        pass

    def test_get_dependents_for_task(self):
        """Test case for get_dependents_for_task

        Get dependents from a task  # noqa: E501
        """
        pass

    def test_get_subtasks_for_task(self):
        """Test case for get_subtasks_for_task

        Get subtasks from a task  # noqa: E501
        """
        pass

    def test_get_task(self):
        """Test case for get_task

        Get a task  # noqa: E501
        """
        pass

    def test_get_tasks(self):
        """Test case for get_tasks

        Get multiple tasks  # noqa: E501
        """
        pass

    def test_get_tasks_for_project(self):
        """Test case for get_tasks_for_project

        Get tasks from a project  # noqa: E501
        """
        pass

    def test_get_tasks_for_section(self):
        """Test case for get_tasks_for_section

        Get tasks from a section  # noqa: E501
        """
        pass

    def test_get_tasks_for_tag(self):
        """Test case for get_tasks_for_tag

        Get tasks from a tag  # noqa: E501
        """
        pass

    def test_get_tasks_for_user_task_list(self):
        """Test case for get_tasks_for_user_task_list

        Get tasks from a user task list  # noqa: E501
        """
        pass

    def test_remove_dependencies_for_task(self):
        """Test case for remove_dependencies_for_task

        Unlink dependencies from a task  # noqa: E501
        """
        pass

    def test_remove_dependents_for_task(self):
        """Test case for remove_dependents_for_task

        Unlink dependents from a task  # noqa: E501
        """
        pass

    def test_remove_follower_for_task(self):
        """Test case for remove_follower_for_task

        Remove followers from a task  # noqa: E501
        """
        pass

    def test_remove_project_for_task(self):
        """Test case for remove_project_for_task

        Remove a project from a task  # noqa: E501
        """
        pass

    def test_remove_tag_for_task(self):
        """Test case for remove_tag_for_task

        Remove a tag from a task  # noqa: E501
        """
        pass

    def test_search_tasks_for_workspace(self):
        """Test case for search_tasks_for_workspace

        Search tasks in a workspace  # noqa: E501
        """
        pass

    def test_set_parent_for_task(self):
        """Test case for set_parent_for_task

        Set the parent of a task  # noqa: E501
        """
        pass

    def test_update_task(self):
        """Test case for update_task

        Update a task  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_webhooks_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.webhooks_api import WebhooksApi  # noqa: E501
from asana.rest import ApiException


class TestWebhooksApi(unittest.TestCase):
    """WebhooksApi unit test stubs"""

    def setUp(self):
        self.api = WebhooksApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_webhook(self):
        """Test case for create_webhook

        Establish a webhook  # noqa: E501
        """
        pass

    def test_delete_webhook(self):
        """Test case for delete_webhook

        Delete a webhook  # noqa: E501
        """
        pass

    def test_get_webhook(self):
        """Test case for get_webhook

        Get a webhook  # noqa: E501
        """
        pass

    def test_get_webhooks(self):
        """Test case for get_webhooks

        Get multiple webhooks  # noqa: E501
        """
        pass

    def test_update_webhook(self):
        """Test case for update_webhook

        Update a webhook  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_portfolios_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.portfolios_api import PortfoliosApi  # noqa: E501
from asana.rest import ApiException


class TestPortfoliosApi(unittest.TestCase):
    """PortfoliosApi unit test stubs"""

    def setUp(self):
        self.api = PortfoliosApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_add_custom_field_setting_for_portfolio(self):
        """Test case for add_custom_field_setting_for_portfolio

        Add a custom field to a portfolio  # noqa: E501
        """
        pass

    def test_add_item_for_portfolio(self):
        """Test case for add_item_for_portfolio

        Add a portfolio item  # noqa: E501
        """
        pass

    def test_add_members_for_portfolio(self):
        """Test case for add_members_for_portfolio

        Add users to a portfolio  # noqa: E501
        """
        pass

    def test_create_portfolio(self):
        """Test case for create_portfolio

        Create a portfolio  # noqa: E501
        """
        pass

    def test_delete_portfolio(self):
        """Test case for delete_portfolio

        Delete a portfolio  # noqa: E501
        """
        pass

    def test_get_items_for_portfolio(self):
        """Test case for get_items_for_portfolio

        Get portfolio items  # noqa: E501
        """
        pass

    def test_get_portfolio(self):
        """Test case for get_portfolio

        Get a portfolio  # noqa: E501
        """
        pass

    def test_get_portfolios(self):
        """Test case for get_portfolios

        Get multiple portfolios  # noqa: E501
        """
        pass

    def test_remove_custom_field_setting_for_portfolio(self):
        """Test case for remove_custom_field_setting_for_portfolio

        Remove a custom field from a portfolio  # noqa: E501
        """
        pass

    def test_remove_item_for_portfolio(self):
        """Test case for remove_item_for_portfolio

        Remove a portfolio item  # noqa: E501
        """
        pass

    def test_remove_members_for_portfolio(self):
        """Test case for remove_members_for_portfolio

        Remove users from a portfolio  # noqa: E501
        """
        pass

    def test_update_portfolio(self):
        """Test case for update_portfolio

        Update a portfolio  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/__init__.py
```
```
# coding: utf-8
```
```bash
./.venv/lib/python3.9/site-packages/test/test_stories_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.stories_api import StoriesApi  # noqa: E501
from asana.rest import ApiException


class TestStoriesApi(unittest.TestCase):
    """StoriesApi unit test stubs"""

    def setUp(self):
        self.api = StoriesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_story_for_task(self):
        """Test case for create_story_for_task

        Create a story on a task  # noqa: E501
        """
        pass

    def test_delete_story(self):
        """Test case for delete_story

        Delete a story  # noqa: E501
        """
        pass

    def test_get_stories_for_task(self):
        """Test case for get_stories_for_task

        Get stories from a task  # noqa: E501
        """
        pass

    def test_get_story(self):
        """Test case for get_story

        Get a story  # noqa: E501
        """
        pass

    def test_update_story(self):
        """Test case for update_story

        Update a story  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_attachments_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.attachments_api import AttachmentsApi  # noqa: E501
from asana.rest import ApiException


class TestAttachmentsApi(unittest.TestCase):
    """AttachmentsApi unit test stubs"""

    def setUp(self):
        self.api = AttachmentsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_attachment_for_object(self):
        """Test case for create_attachment_for_object

        Upload an attachment  # noqa: E501
        """
        pass

    def test_delete_attachment(self):
        """Test case for delete_attachment

        Delete an attachment  # noqa: E501
        """
        pass

    def test_get_attachment(self):
        """Test case for get_attachment

        Get an attachment  # noqa: E501
        """
        pass

    def test_get_attachments_for_object(self):
        """Test case for get_attachments_for_object

        Get attachments from an object  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_rules_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.rules_api import RulesApi  # noqa: E501
from asana.rest import ApiException


class TestRulesApi(unittest.TestCase):
    """RulesApi unit test stubs"""

    def setUp(self):
        self.api = RulesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_trigger_rule(self):
        """Test case for trigger_rule

        Trigger a rule  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_team_memberships_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.team_memberships_api import TeamMembershipsApi  # noqa: E501
from asana.rest import ApiException


class TestTeamMembershipsApi(unittest.TestCase):
    """TeamMembershipsApi unit test stubs"""

    def setUp(self):
        self.api = TeamMembershipsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_team_membership(self):
        """Test case for get_team_membership

        Get a team membership  # noqa: E501
        """
        pass

    def test_get_team_memberships(self):
        """Test case for get_team_memberships

        Get team memberships  # noqa: E501
        """
        pass

    def test_get_team_memberships_for_team(self):
        """Test case for get_team_memberships_for_team

        Get memberships from a team  # noqa: E501
        """
        pass

    def test_get_team_memberships_for_user(self):
        """Test case for get_team_memberships_for_user

        Get memberships from a user  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_project_templates_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.project_templates_api import ProjectTemplatesApi  # noqa: E501
from asana.rest import ApiException


class TestProjectTemplatesApi(unittest.TestCase):
    """ProjectTemplatesApi unit test stubs"""

    def setUp(self):
        self.api = ProjectTemplatesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_project_template(self):
        """Test case for delete_project_template

        Delete a project template  # noqa: E501
        """
        pass

    def test_get_project_template(self):
        """Test case for get_project_template

        Get a project template  # noqa: E501
        """
        pass

    def test_get_project_templates(self):
        """Test case for get_project_templates

        Get multiple project templates  # noqa: E501
        """
        pass

    def test_get_project_templates_for_team(self):
        """Test case for get_project_templates_for_team

        Get a team's project templates  # noqa: E501
        """
        pass

    def test_instantiate_project(self):
        """Test case for instantiate_project

        Instantiate a project from a project template  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_status_updates_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.status_updates_api import StatusUpdatesApi  # noqa: E501
from asana.rest import ApiException


class TestStatusUpdatesApi(unittest.TestCase):
    """StatusUpdatesApi unit test stubs"""

    def setUp(self):
        self.api = StatusUpdatesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_status_for_object(self):
        """Test case for create_status_for_object

        Create a status update  # noqa: E501
        """
        pass

    def test_delete_status(self):
        """Test case for delete_status

        Delete a status update  # noqa: E501
        """
        pass

    def test_get_status(self):
        """Test case for get_status

        Get a status update  # noqa: E501
        """
        pass

    def test_get_statuses_for_object(self):
        """Test case for get_statuses_for_object

        Get status updates from an object  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_tags_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.tags_api import TagsApi  # noqa: E501
from asana.rest import ApiException


class TestTagsApi(unittest.TestCase):
    """TagsApi unit test stubs"""

    def setUp(self):
        self.api = TagsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_tag(self):
        """Test case for create_tag

        Create a tag  # noqa: E501
        """
        pass

    def test_create_tag_for_workspace(self):
        """Test case for create_tag_for_workspace

        Create a tag in a workspace  # noqa: E501
        """
        pass

    def test_delete_tag(self):
        """Test case for delete_tag

        Delete a tag  # noqa: E501
        """
        pass

    def test_get_tag(self):
        """Test case for get_tag

        Get a tag  # noqa: E501
        """
        pass

    def test_get_tags(self):
        """Test case for get_tags

        Get multiple tags  # noqa: E501
        """
        pass

    def test_get_tags_for_task(self):
        """Test case for get_tags_for_task

        Get a task's tags  # noqa: E501
        """
        pass

    def test_get_tags_for_workspace(self):
        """Test case for get_tags_for_workspace

        Get tags in a workspace  # noqa: E501
        """
        pass

    def test_update_tag(self):
        """Test case for update_tag

        Update a tag  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_jobs_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.jobs_api import JobsApi  # noqa: E501
from asana.rest import ApiException


class TestJobsApi(unittest.TestCase):
    """JobsApi unit test stubs"""

    def setUp(self):
        self.api = JobsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_job(self):
        """Test case for get_job

        Get a job by id  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_project_statuses_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.project_statuses_api import ProjectStatusesApi  # noqa: E501
from asana.rest import ApiException


class TestProjectStatusesApi(unittest.TestCase):
    """ProjectStatusesApi unit test stubs"""

    def setUp(self):
        self.api = ProjectStatusesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_project_status_for_project(self):
        """Test case for create_project_status_for_project

        Create a project status  # noqa: E501
        """
        pass

    def test_delete_project_status(self):
        """Test case for delete_project_status

        Delete a project status  # noqa: E501
        """
        pass

    def test_get_project_status(self):
        """Test case for get_project_status

        Get a project status  # noqa: E501
        """
        pass

    def test_get_project_statuses_for_project(self):
        """Test case for get_project_statuses_for_project

        Get statuses from a project  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_workspaces_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.workspaces_api import WorkspacesApi  # noqa: E501
from asana.rest import ApiException


class TestWorkspacesApi(unittest.TestCase):
    """WorkspacesApi unit test stubs"""

    def setUp(self):
        self.api = WorkspacesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_add_user_for_workspace(self):
        """Test case for add_user_for_workspace

        Add a user to a workspace or organization  # noqa: E501
        """
        pass

    def test_get_workspace(self):
        """Test case for get_workspace

        Get a workspace  # noqa: E501
        """
        pass

    def test_get_workspaces(self):
        """Test case for get_workspaces

        Get multiple workspaces  # noqa: E501
        """
        pass

    def test_remove_user_for_workspace(self):
        """Test case for remove_user_for_workspace

        Remove a user from a workspace or organization  # noqa: E501
        """
        pass

    def test_update_workspace(self):
        """Test case for update_workspace

        Update a workspace  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_time_tracking_entries_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.time_tracking_entries_api import TimeTrackingEntriesApi  # noqa: E501
from asana.rest import ApiException


class TestTimeTrackingEntriesApi(unittest.TestCase):
    """TimeTrackingEntriesApi unit test stubs"""

    def setUp(self):
        self.api = TimeTrackingEntriesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_time_tracking_entry(self):
        """Test case for create_time_tracking_entry

        Create a time tracking entry  # noqa: E501
        """
        pass

    def test_delete_time_tracking_entry(self):
        """Test case for delete_time_tracking_entry

        Delete a time tracking entry  # noqa: E501
        """
        pass

    def test_get_time_tracking_entries_for_task(self):
        """Test case for get_time_tracking_entries_for_task

        Get time tracking entries for a task  # noqa: E501
        """
        pass

    def test_get_time_tracking_entry(self):
        """Test case for get_time_tracking_entry

        Get a time tracking entry  # noqa: E501
        """
        pass

    def test_update_time_tracking_entry(self):
        """Test case for update_time_tracking_entry

        Update a time tracking entry  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_typeahead_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.typeahead_api import TypeaheadApi  # noqa: E501
from asana.rest import ApiException


class TestTypeaheadApi(unittest.TestCase):
    """TypeaheadApi unit test stubs"""

    def setUp(self):
        self.api = TypeaheadApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_typeahead_for_workspace(self):
        """Test case for typeahead_for_workspace

        Get objects via typeahead  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_batch_api_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.batch_api_api import BatchAPIApi  # noqa: E501
from asana.rest import ApiException


class TestBatchAPIApi(unittest.TestCase):
    """BatchAPIApi unit test stubs"""

    def setUp(self):
        self.api = BatchAPIApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_batch_request(self):
        """Test case for create_batch_request

        Submit parallel requests  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_events_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.events_api import EventsApi  # noqa: E501
from asana.rest import ApiException


class TestEventsApi(unittest.TestCase):
    """EventsApi unit test stubs"""

    def setUp(self):
        self.api = EventsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_events(self):
        """Test case for get_events

        Get events on a resource  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_goal_relationships_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.goal_relationships_api import GoalRelationshipsApi  # noqa: E501
from asana.rest import ApiException


class TestGoalRelationshipsApi(unittest.TestCase):
    """GoalRelationshipsApi unit test stubs"""

    def setUp(self):
        self.api = GoalRelationshipsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_add_supporting_relationship(self):
        """Test case for add_supporting_relationship

        Add a supporting goal relationship  # noqa: E501
        """
        pass

    def test_get_goal_relationship(self):
        """Test case for get_goal_relationship

        Get a goal relationship  # noqa: E501
        """
        pass

    def test_get_goal_relationships(self):
        """Test case for get_goal_relationships

        Get goal relationships  # noqa: E501
        """
        pass

    def test_remove_supporting_relationship(self):
        """Test case for remove_supporting_relationship

        Removes a supporting goal relationship  # noqa: E501
        """
        pass

    def test_update_goal_relationship(self):
        """Test case for update_goal_relationship

        Update a goal relationship  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_users_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.users_api import UsersApi  # noqa: E501
from asana.rest import ApiException


class TestUsersApi(unittest.TestCase):
    """UsersApi unit test stubs"""

    def setUp(self):
        self.api = UsersApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_favorites_for_user(self):
        """Test case for get_favorites_for_user

        Get a user's favorites  # noqa: E501
        """
        pass

    def test_get_user(self):
        """Test case for get_user

        Get a user  # noqa: E501
        """
        pass

    def test_get_users(self):
        """Test case for get_users

        Get multiple users  # noqa: E501
        """
        pass

    def test_get_users_for_team(self):
        """Test case for get_users_for_team

        Get users in a team  # noqa: E501
        """
        pass

    def test_get_users_for_workspace(self):
        """Test case for get_users_for_workspace

        Get users in a workspace or organization  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_organization_exports_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.organization_exports_api import OrganizationExportsApi  # noqa: E501
from asana.rest import ApiException


class TestOrganizationExportsApi(unittest.TestCase):
    """OrganizationExportsApi unit test stubs"""

    def setUp(self):
        self.api = OrganizationExportsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_organization_export(self):
        """Test case for create_organization_export

        Create an organization export request  # noqa: E501
        """
        pass

    def test_get_organization_export(self):
        """Test case for get_organization_export

        Get details on an org export request  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/test/test_allocations_api.py
```
```
# coding: utf-8

"""
    Asana

    This is the interface for interacting with the [Asana Platform](https://developers.asana.com). Our API reference is generated from our [OpenAPI spec] (https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml).  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import asana
from asana.api.allocations_api import AllocationsApi  # noqa: E501
from asana.rest import ApiException


class TestAllocationsApi(unittest.TestCase):
    """AllocationsApi unit test stubs"""

    def setUp(self):
        self.api = AllocationsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_allocation(self):
        """Test case for create_allocation

        Create an allocation  # noqa: E501
        """
        pass

    def test_delete_allocation(self):
        """Test case for delete_allocation

        Delete an allocation  # noqa: E501
        """
        pass

    def test_get_allocation(self):
        """Test case for get_allocation

        Get an allocation  # noqa: E501
        """
        pass

    def test_get_allocations(self):
        """Test case for get_allocations

        Get multiple allocations  # noqa: E501
        """
        pass

    def test_update_allocation(self):
        """Test case for update_allocation

        Update an allocation  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
```
```bash
./.venv/lib/python3.9/site-packages/pytest/__init__.py
```
```
# PYTHON_ARGCOMPLETE_OK
"""pytest: unit and functional testing with Python."""

from _pytest import __version__
from _pytest import version_tuple
from _pytest._code import ExceptionInfo
from _pytest.assertion import register_assert_rewrite
from _pytest.cacheprovider import Cache
from _pytest.capture import CaptureFixture
from _pytest.config import cmdline
from _pytest.config import Config
from _pytest.config import console_main
from _pytest.config import ExitCode
from _pytest.config import hookimpl
from _pytest.config import hookspec
from _pytest.config import main
from _pytest.config import PytestPluginManager
from _pytest.config import UsageError
from _pytest.config.argparsing import OptionGroup
from _pytest.config.argparsing import Parser
from _pytest.debugging import pytestPDB as __pytestPDB
from _pytest.doctest import DoctestItem
from _pytest.fixtures import fixture
from _pytest.fixtures import FixtureDef
from _pytest.fixtures import FixtureLookupError
from _pytest.fixtures import FixtureRequest
from _pytest.fixtures import yield_fixture
from _pytest.freeze_support import freeze_includes
from _pytest.legacypath import TempdirFactory
from _pytest.legacypath import Testdir
from _pytest.logging import LogCaptureFixture
from _pytest.main import Dir
from _pytest.main import Session
from _pytest.mark import Mark
from _pytest.mark import MARK_GEN as mark
from _pytest.mark import MarkDecorator
from _pytest.mark import MarkGenerator
from _pytest.mark import param
from _pytest.monkeypatch import MonkeyPatch
from _pytest.nodes import Collector
from _pytest.nodes import Directory
from _pytest.nodes import File
from _pytest.nodes import Item
from _pytest.outcomes import exit
from _pytest.outcomes import fail
from _pytest.outcomes import importorskip
from _pytest.outcomes import skip
from _pytest.outcomes import xfail
from _pytest.pytester import HookRecorder
from _pytest.pytester import LineMatcher
from _pytest.pytester import Pytester
from _pytest.pytester import RecordedHookCall
from _pytest.pytester import RunResult
from _pytest.python import Class
from _pytest.python import Function
from _pytest.python import Metafunc
from _pytest.python import Module
from _pytest.python import Package
from _pytest.python_api import approx
from _pytest.python_api import raises
from _pytest.recwarn import deprecated_call
from _pytest.recwarn import WarningsRecorder
from _pytest.recwarn import warns
from _pytest.reports import CollectReport
from _pytest.reports import TestReport
from _pytest.runner import CallInfo
from _pytest.stash import Stash
from _pytest.stash import StashKey
from _pytest.terminal import TestShortLogReport
from _pytest.tmpdir import TempPathFactory
from _pytest.warning_types import PytestAssertRewriteWarning
from _pytest.warning_types import PytestCacheWarning
from _pytest.warning_types import PytestCollectionWarning
from _pytest.warning_types import PytestConfigWarning
from _pytest.warning_types import PytestDeprecationWarning
from _pytest.warning_types import PytestExperimentalApiWarning
from _pytest.warning_types import PytestRemovedIn9Warning
from _pytest.warning_types import PytestReturnNotNoneWarning
from _pytest.warning_types import PytestUnhandledCoroutineWarning
from _pytest.warning_types import PytestUnhandledThreadExceptionWarning
from _pytest.warning_types import PytestUnknownMarkWarning
from _pytest.warning_types import PytestUnraisableExceptionWarning
from _pytest.warning_types import PytestWarning


set_trace = __pytestPDB.set_trace


__all__ = [
    "__version__",
    "approx",
    "Cache",
    "CallInfo",
    "CaptureFixture",
    "Class",
    "cmdline",
    "Collector",
    "CollectReport",
    "Config",
    "console_main",
    "deprecated_call",
    "Dir",
    "Directory",
    "DoctestItem",
    "exit",
    "ExceptionInfo",
    "ExitCode",
    "fail",
    "File",
    "fixture",
    "FixtureDef",
    "FixtureLookupError",
    "FixtureRequest",
    "freeze_includes",
    "Function",
    "hookimpl",
    "HookRecorder",
    "hookspec",
    "importorskip",
    "Item",
    "LineMatcher",
    "LogCaptureFixture",
    "main",
    "mark",
    "Mark",
    "MarkDecorator",
    "MarkGenerator",
    "Metafunc",
    "Module",
    "MonkeyPatch",
    "OptionGroup",
    "Package",
    "param",
    "Parser",
    "PytestAssertRewriteWarning",
    "PytestCacheWarning",
    "PytestCollectionWarning",
    "PytestConfigWarning",
    "PytestDeprecationWarning",
    "PytestExperimentalApiWarning",
    "PytestRemovedIn9Warning",
    "PytestReturnNotNoneWarning",
    "Pytester",
    "PytestPluginManager",
    "PytestUnhandledCoroutineWarning",
    "PytestUnhandledThreadExceptionWarning",
    "PytestUnknownMarkWarning",
    "PytestUnraisableExceptionWarning",
    "PytestWarning",
    "raises",
    "RecordedHookCall",
    "register_assert_rewrite",
    "RunResult",
    "Session",
    "set_trace",
    "skip",
    "Stash",
    "StashKey",
    "version_tuple",
    "TempdirFactory",
    "TempPathFactory",
    "Testdir",
    "TestReport",
    "TestShortLogReport",
    "UsageError",
    "WarningsRecorder",
    "warns",
    "xfail",
    "yield_fixture",
]
```
```bash
./.venv/lib/python3.9/site-packages/pytest/py.typed
```
```

```
```bash
./.venv/lib/python3.9/site-packages/pytest/__main__.py
```
```
"""The pytest entry point."""

import pytest


if __name__ == "__main__":
    raise SystemExit(pytest.console_main())
```
```bash
./.venv/lib/python3.9/site-packages/pytest_asyncio/_version.py
```
```
# file generated by setuptools_scm
# don't change, don't track in version control
TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Tuple, Union
    VERSION_TUPLE = Tuple[Union[int, str], ...]
else:
    VERSION_TUPLE = object

version: str
__version__: str
__version_tuple__: VERSION_TUPLE
version_tuple: VERSION_TUPLE

__version__ = version = '0.23.7'
__version_tuple__ = version_tuple = (0, 23, 7)
```
```bash
./.venv/lib/python3.9/site-packages/pytest_asyncio/__init__.py
```
```
"""The main point for importing pytest-asyncio items."""

from ._version import version as __version__  # noqa
from .plugin import fixture, is_async_test

__all__ = ("fixture", "is_async_test")
```
```bash
./.venv/lib/python3.9/site-packages/pytest_asyncio/plugin.py
```
```
"""pytest-asyncio implementation."""

import asyncio
import contextlib
import enum
import functools
import inspect
import socket
import warnings
from asyncio import AbstractEventLoopPolicy
from textwrap import dedent
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Dict,
    Generator,
    Iterable,
    Iterator,
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Set,
    Type,
    TypeVar,
    Union,
    overload,
)

import pytest
from pytest import (
    Class,
    Collector,
    Config,
    FixtureRequest,
    Function,
    Item,
    Metafunc,
    Module,
    Package,
    Parser,
    PytestCollectionWarning,
    PytestDeprecationWarning,
    PytestPluginManager,
    Session,
    StashKey,
)

_ScopeName = Literal["session", "package", "module", "class", "function"]
_T = TypeVar("_T")

SimpleFixtureFunction = TypeVar(
    "SimpleFixtureFunction", bound=Callable[..., Awaitable[object]]
)
FactoryFixtureFunction = TypeVar(
    "FactoryFixtureFunction", bound=Callable[..., AsyncIterator[object]]
)
FixtureFunction = Union[SimpleFixtureFunction, FactoryFixtureFunction]
FixtureFunctionMarker = Callable[[FixtureFunction], FixtureFunction]

# https://github.com/pytest-dev/pytest/pull/9510
FixtureDef = Any


class PytestAsyncioError(Exception):
    """Base class for exceptions raised by pytest-asyncio"""


class MultipleEventLoopsRequestedError(PytestAsyncioError):
    """Raised when a test requests multiple asyncio event loops."""


class Mode(str, enum.Enum):
    AUTO = "auto"
    STRICT = "strict"


ASYNCIO_MODE_HELP = """\
'auto' - for automatically handling all async functions by the plugin
'strict' - for autoprocessing disabling (useful if different async frameworks \
should be tested together, e.g. \
both pytest-asyncio and pytest-trio are used in the same project)
"""


def pytest_addoption(parser: Parser, pluginmanager: PytestPluginManager) -> None:
    group = parser.getgroup("asyncio")
    group.addoption(
        "--asyncio-mode",
        dest="asyncio_mode",
        default=None,
        metavar="MODE",
        help=ASYNCIO_MODE_HELP,
    )
    parser.addini(
        "asyncio_mode",
        help="default value for --asyncio-mode",
        default="strict",
    )


@overload
def fixture(
    fixture_function: FixtureFunction,
    *,
    scope: "Union[_ScopeName, Callable[[str, Config], _ScopeName]]" = ...,
    params: Optional[Iterable[object]] = ...,
    autouse: bool = ...,
    ids: Union[
        Iterable[Union[str, float, int, bool, None]],
        Callable[[Any], Optional[object]],
        None,
    ] = ...,
    name: Optional[str] = ...,
) -> FixtureFunction: ...


@overload
def fixture(
    fixture_function: None = ...,
    *,
    scope: "Union[_ScopeName, Callable[[str, Config], _ScopeName]]" = ...,
    params: Optional[Iterable[object]] = ...,
    autouse: bool = ...,
    ids: Union[
        Iterable[Union[str, float, int, bool, None]],
        Callable[[Any], Optional[object]],
        None,
    ] = ...,
    name: Optional[str] = None,
) -> FixtureFunctionMarker: ...


def fixture(
    fixture_function: Optional[FixtureFunction] = None, **kwargs: Any
) -> Union[FixtureFunction, FixtureFunctionMarker]:
    if fixture_function is not None:
        _make_asyncio_fixture_function(fixture_function)
        return pytest.fixture(fixture_function, **kwargs)

    else:

        @functools.wraps(fixture)
        def inner(fixture_function: FixtureFunction) -> FixtureFunction:
            return fixture(fixture_function, **kwargs)

        return inner


def _is_asyncio_fixture_function(obj: Any) -> bool:
    obj = getattr(obj, "__func__", obj)  # instance method maybe?
    return getattr(obj, "_force_asyncio_fixture", False)


def _make_asyncio_fixture_function(obj: Any) -> None:
    if hasattr(obj, "__func__"):
        # instance method, check the function object
        obj = obj.__func__
    obj._force_asyncio_fixture = True


def _is_coroutine_or_asyncgen(obj: Any) -> bool:
    return asyncio.iscoroutinefunction(obj) or inspect.isasyncgenfunction(obj)


def _get_asyncio_mode(config: Config) -> Mode:
    val = config.getoption("asyncio_mode")
    if val is None:
        val = config.getini("asyncio_mode")
    try:
        return Mode(val)
    except ValueError:
        modes = ", ".join(m.value for m in Mode)
        raise pytest.UsageError(
            f"{val!r} is not a valid asyncio_mode. Valid modes: {modes}."
        )


def pytest_configure(config: Config) -> None:
    """Inject documentation."""
    config.addinivalue_line(
        "markers",
        "asyncio: "
        "mark the test as a coroutine, it will be "
        "run using an asyncio event loop",
    )


@pytest.hookimpl(tryfirst=True)
def pytest_report_header(config: Config) -> List[str]:
    """Add asyncio config to pytest header."""
    mode = _get_asyncio_mode(config)
    return [f"asyncio: mode={mode}"]


def _preprocess_async_fixtures(
    collector: Collector,
    processed_fixturedefs: Set[FixtureDef],
) -> None:
    config = collector.config
    asyncio_mode = _get_asyncio_mode(config)
    fixturemanager = config.pluginmanager.get_plugin("funcmanage")
    assert fixturemanager is not None
    for fixtures in fixturemanager._arg2fixturedefs.values():
        for fixturedef in fixtures:
            func = fixturedef.func
            if fixturedef in processed_fixturedefs or not _is_coroutine_or_asyncgen(
                func
            ):
                continue
            if not _is_asyncio_fixture_function(func) and asyncio_mode == Mode.STRICT:
                # Ignore async fixtures without explicit asyncio mark in strict mode
                # This applies to pytest_trio fixtures, for example
                continue
            scope = fixturedef.scope
            if scope == "function":
                event_loop_fixture_id: Optional[str] = "event_loop"
            else:
                event_loop_node = _retrieve_scope_root(collector, scope)
                event_loop_fixture_id = event_loop_node.stash.get(
                    # Type ignored because of non-optimal mypy inference.
                    _event_loop_fixture_id,  # type: ignore[arg-type]
                    None,
                )
            _make_asyncio_fixture_function(func)
            function_signature = inspect.signature(func)
            if "event_loop" in function_signature.parameters:
                warnings.warn(
                    PytestDeprecationWarning(
                        f"{func.__name__} is asynchronous and explicitly "
                        f'requests the "event_loop" fixture. Asynchronous fixtures and '
                        f'test functions should use "asyncio.get_running_loop()" '
                        f"instead."
                    )
                )
            assert event_loop_fixture_id
            _inject_fixture_argnames(
                fixturedef,
                event_loop_fixture_id,
            )
            _synchronize_async_fixture(
                fixturedef,
                event_loop_fixture_id,
            )
            assert _is_asyncio_fixture_function(fixturedef.func)
            processed_fixturedefs.add(fixturedef)


def _inject_fixture_argnames(
    fixturedef: FixtureDef, event_loop_fixture_id: str
) -> None:
    """
    Ensures that `request` and `event_loop` are arguments of the specified fixture.
    """
    to_add = []
    for name in ("request", event_loop_fixture_id):
        if name not in fixturedef.argnames:
            to_add.append(name)
    if to_add:
        fixturedef.argnames += tuple(to_add)


def _synchronize_async_fixture(
    fixturedef: FixtureDef, event_loop_fixture_id: str
) -> None:
    """
    Wraps the fixture function of an async fixture in a synchronous function.
    """
    if inspect.isasyncgenfunction(fixturedef.func):
        _wrap_asyncgen_fixture(fixturedef, event_loop_fixture_id)
    elif inspect.iscoroutinefunction(fixturedef.func):
        _wrap_async_fixture(fixturedef, event_loop_fixture_id)


def _add_kwargs(
    func: Callable[..., Any],
    kwargs: Dict[str, Any],
    event_loop_fixture_id: str,
    event_loop: asyncio.AbstractEventLoop,
    request: FixtureRequest,
) -> Dict[str, Any]:
    sig = inspect.signature(func)
    ret = kwargs.copy()
    if "request" in sig.parameters:
        ret["request"] = request
    if event_loop_fixture_id in sig.parameters:
        ret[event_loop_fixture_id] = event_loop
    return ret


def _perhaps_rebind_fixture_func(
    func: _T, instance: Optional[Any], unittest: bool
) -> _T:
    if instance is not None:
        # The fixture needs to be bound to the actual request.instance
        # so it is bound to the same object as the test method.
        unbound, cls = func, None
        try:
            unbound, cls = func.__func__, type(func.__self__)  # type: ignore
        except AttributeError:
            pass
        # If unittest is true, the fixture is bound unconditionally.
        # otherwise, only if the fixture was bound before to an instance of
        # the same type.
        if unittest or (cls is not None and isinstance(instance, cls)):
            func = unbound.__get__(instance)  # type: ignore
    return func


def _wrap_asyncgen_fixture(fixturedef: FixtureDef, event_loop_fixture_id: str) -> None:
    fixture = fixturedef.func

    @functools.wraps(fixture)
    def _asyncgen_fixture_wrapper(request: FixtureRequest, **kwargs: Any):
        unittest = False if pytest.version_tuple >= (8, 2) else fixturedef.unittest
        func = _perhaps_rebind_fixture_func(fixture, request.instance, unittest)
        event_loop = kwargs.pop(event_loop_fixture_id)
        gen_obj = func(
            **_add_kwargs(func, kwargs, event_loop_fixture_id, event_loop, request)
        )

        async def setup():
            res = await gen_obj.__anext__()
            return res

        def finalizer() -> None:
            """Yield again, to finalize."""

            async def async_finalizer() -> None:
                try:
                    await gen_obj.__anext__()
                except StopAsyncIteration:
                    pass
                else:
                    msg = "Async generator fixture didn't stop."
                    msg += "Yield only once."
                    raise ValueError(msg)

            event_loop.run_until_complete(async_finalizer())

        result = event_loop.run_until_complete(setup())
        request.addfinalizer(finalizer)
        return result

    fixturedef.func = _asyncgen_fixture_wrapper


def _wrap_async_fixture(fixturedef: FixtureDef, event_loop_fixture_id: str) -> None:
    fixture = fixturedef.func

    @functools.wraps(fixture)
    def _async_fixture_wrapper(request: FixtureRequest, **kwargs: Any):
        unittest = False if pytest.version_tuple >= (8, 2) else fixturedef.unittest
        func = _perhaps_rebind_fixture_func(fixture, request.instance, unittest)
        event_loop = kwargs.pop(event_loop_fixture_id)

        async def setup():
            res = await func(
                **_add_kwargs(func, kwargs, event_loop_fixture_id, event_loop, request)
            )
            return res

        return event_loop.run_until_complete(setup())

    fixturedef.func = _async_fixture_wrapper


class PytestAsyncioFunction(Function):
    """Base class for all test functions managed by pytest-asyncio."""

    @classmethod
    def item_subclass_for(
        cls, item: Function, /
    ) -> Union[Type["PytestAsyncioFunction"], None]:
        """
        Returns a subclass of PytestAsyncioFunction if there is a specialized subclass
        for the specified function item.

        Return None if no specialized subclass exists for the specified item.
        """
        for subclass in cls.__subclasses__():
            if subclass._can_substitute(item):
                return subclass
        return None

    @classmethod
    def _from_function(cls, function: Function, /) -> Function:
        """
        Instantiates this specific PytestAsyncioFunction type from the specified
        Function item.
        """
        assert function.get_closest_marker("asyncio")
        subclass_instance = cls.from_parent(
            function.parent,
            name=function.name,
            callspec=getattr(function, "callspec", None),
            callobj=function.obj,
            fixtureinfo=function._fixtureinfo,
            keywords=function.keywords,
            originalname=function.originalname,
        )
        subclass_instance.own_markers.extend(function.own_markers)
        subclassed_function_signature = inspect.signature(subclass_instance.obj)
        if "event_loop" in subclassed_function_signature.parameters:
            subclass_instance.warn(
                PytestDeprecationWarning(
                    f"{subclass_instance.name} is asynchronous and explicitly "
                    f'requests the "event_loop" fixture. Asynchronous fixtures and '
                    f'test functions should use "asyncio.get_running_loop()" instead.'
                )
            )
        return subclass_instance

    @staticmethod
    def _can_substitute(item: Function) -> bool:
        """Returns whether the specified function can be replaced by this class"""
        raise NotImplementedError()


class Coroutine(PytestAsyncioFunction):
    """Pytest item created by a coroutine"""

    @staticmethod
    def _can_substitute(item: Function) -> bool:
        func = item.obj
        return asyncio.iscoroutinefunction(func)

    def runtest(self) -> None:
        self.obj = wrap_in_sync(
            # https://github.com/pytest-dev/pytest-asyncio/issues/596
            self.obj,  # type: ignore[has-type]
        )
        super().runtest()


class AsyncGenerator(PytestAsyncioFunction):
    """Pytest item created by an asynchronous generator"""

    @staticmethod
    def _can_substitute(item: Function) -> bool:
        func = item.obj
        return inspect.isasyncgenfunction(func)

    @classmethod
    def _from_function(cls, function: Function, /) -> Function:
        async_gen_item = super()._from_function(function)
        unsupported_item_type_message = (
            f"Tests based on asynchronous generators are not supported. "
            f"{function.name} will be ignored."
        )
        async_gen_item.warn(PytestCollectionWarning(unsupported_item_type_message))
        async_gen_item.add_marker(
            pytest.mark.xfail(run=False, reason=unsupported_item_type_message)
        )
        return async_gen_item


class AsyncStaticMethod(PytestAsyncioFunction):
    """
    Pytest item that is a coroutine or an asynchronous generator
    decorated with staticmethod
    """

    @staticmethod
    def _can_substitute(item: Function) -> bool:
        func = item.obj
        return isinstance(func, staticmethod) and _is_coroutine_or_asyncgen(
            func.__func__
        )

    def runtest(self) -> None:
        self.obj = wrap_in_sync(
            # https://github.com/pytest-dev/pytest-asyncio/issues/596
            self.obj,  # type: ignore[has-type]
        )
        super().runtest()


class AsyncHypothesisTest(PytestAsyncioFunction):
    """
    Pytest item that is coroutine or an asynchronous generator decorated by
    @hypothesis.given.
    """

    @staticmethod
    def _can_substitute(item: Function) -> bool:
        func = item.obj
        return (
            getattr(func, "is_hypothesis_test", False)  # type: ignore[return-value]
            and getattr(func, "hypothesis", None)
            and asyncio.iscoroutinefunction(func.hypothesis.inner_test)
        )

    def runtest(self) -> None:
        self.obj.hypothesis.inner_test = wrap_in_sync(
            self.obj.hypothesis.inner_test,
        )
        super().runtest()


_HOLDER: Set[FixtureDef] = set()


# The function name needs to start with "pytest_"
# see https://github.com/pytest-dev/pytest/issues/11307
@pytest.hookimpl(specname="pytest_pycollect_makeitem", tryfirst=True)
def pytest_pycollect_makeitem_preprocess_async_fixtures(
    collector: Union[pytest.Module, pytest.Class], name: str, obj: object
) -> Union[
    pytest.Item, pytest.Collector, List[Union[pytest.Item, pytest.Collector]], None
]:
    """A pytest hook to collect asyncio coroutines."""
    if not collector.funcnamefilter(name):
        return None
    _preprocess_async_fixtures(collector, _HOLDER)
    return None


# TODO: #778 Narrow down return type of function when dropping support for pytest 7
# The function name needs to start with "pytest_"
# see https://github.com/pytest-dev/pytest/issues/11307
@pytest.hookimpl(specname="pytest_pycollect_makeitem", hookwrapper=True)
def pytest_pycollect_makeitem_convert_async_functions_to_subclass(
    collector: Union[pytest.Module, pytest.Class], name: str, obj: object
) -> Generator[None, Any, None]:
    """
    Converts coroutines and async generators collected as pytest.Functions
    to AsyncFunction items.
    """
    hook_result = yield
    node_or_list_of_nodes: Union[
        pytest.Item, pytest.Collector, List[Union[pytest.Item, pytest.Collector]], None
    ] = hook_result.get_result()
    if not node_or_list_of_nodes:
        return
    if isinstance(node_or_list_of_nodes, Sequence):
        node_iterator = iter(node_or_list_of_nodes)
    else:
        # Treat single node as a single-element iterable
        node_iterator = iter((node_or_list_of_nodes,))
    updated_node_collection = []
    for node in node_iterator:
        updated_item = node
        if isinstance(node, Function):
            specialized_item_class = PytestAsyncioFunction.item_subclass_for(node)
            if specialized_item_class:
                if _get_asyncio_mode(
                    node.config
                ) == Mode.AUTO and not node.get_closest_marker("asyncio"):
                    node.add_marker("asyncio")
                if node.get_closest_marker("asyncio"):
                    updated_item = specialized_item_class._from_function(node)
        updated_node_collection.append(updated_item)
    hook_result.force_result(updated_node_collection)


_event_loop_fixture_id = StashKey[str]()
_fixture_scope_by_collector_type: Mapping[Type[pytest.Collector], _ScopeName] = {
    Class: "class",
    # Package is a subclass of module and the dict is used in isinstance checks
    # Therefore, the order matters and Package needs to appear before Module
    Package: "package",
    Module: "module",
    Session: "session",
}

# A stack used to push package-scoped loops during collection of a package
# and pop those loops during collection of a Module
__package_loop_stack: List[Union[FixtureFunctionMarker, FixtureFunction]] = []


@pytest.hookimpl
def pytest_collectstart(collector: pytest.Collector) -> None:
    try:
        collector_scope = next(
            scope
            for cls, scope in _fixture_scope_by_collector_type.items()
            if isinstance(collector, cls)
        )
    except StopIteration:
        return
    # Session is not a PyCollector type, so it doesn't have a corresponding
    # "obj" attribute to attach a dynamic fixture function to.
    # However, there's only one session per pytest run, so there's no need to
    # create the fixture dynamically. We can simply define a session-scoped
    # event loop fixture once in the plugin code.
    if collector_scope == "session":
        event_loop_fixture_id = _session_event_loop.__name__
        collector.stash[_event_loop_fixture_id] = event_loop_fixture_id
        return
    # There seem to be issues when a fixture is shadowed by another fixture
    # and both differ in their params.
    # https://github.com/pytest-dev/pytest/issues/2043
    # https://github.com/pytest-dev/pytest/issues/11350
    # As such, we assign a unique name for each event_loop fixture.
    # The fixture name is stored in the collector's Stash, so it can
    # be injected when setting up the test
    event_loop_fixture_id = f"{collector.nodeid}::<event_loop>"
    collector.stash[_event_loop_fixture_id] = event_loop_fixture_id

    @pytest.fixture(
        scope=collector_scope,
        name=event_loop_fixture_id,
    )
    def scoped_event_loop(
        *args,  # Function needs to accept "cls" when collected by pytest.Class
        event_loop_policy,
    ) -> Iterator[asyncio.AbstractEventLoop]:
        new_loop_policy = event_loop_policy
        with _temporary_event_loop_policy(new_loop_policy):
            loop = asyncio.new_event_loop()
            loop.__pytest_asyncio = True  # type: ignore[attr-defined]
            asyncio.set_event_loop(loop)
            yield loop
            loop.close()

    # @pytest.fixture does not register the fixture anywhere, so pytest doesn't
    # know it exists. We work around this by attaching the fixture function to the
    # collected Python object, where it will be picked up by pytest.Class.collect()
    # or pytest.Module.collect(), respectively
    if type(collector) is Package:
        # Packages do not have a corresponding Python object. Therefore, the fixture
        # for the package-scoped event loop is added to a stack. When a module inside
        # the package is collected, the module will attach the fixture to its
        # Python object.
        __package_loop_stack.append(scoped_event_loop)
    elif isinstance(collector, Module):
        # Accessing Module.obj triggers a module import executing module-level
        # statements. A module-level pytest.skip statement raises the "Skipped"
        # OutcomeException or a Collector.CollectError, if the "allow_module_level"
        # kwargs is missing. These cases are handled correctly when they happen inside
        # Collector.collect(), but this hook runs before the actual collect call.
        # Therefore, we monkey patch Module.collect to add the scoped fixture to the
        # module before it runs the actual collection.
        def _patched_collect():
            # If the collected module is a DoctestTextfile, collector.obj is None
            module = collector.obj
            if module is not None:
                module.__pytest_asyncio_scoped_event_loop = scoped_event_loop
                try:
                    package_loop = __package_loop_stack.pop()
                    module.__pytest_asyncio_package_scoped_event_loop = package_loop
                except IndexError:
                    pass
            return collector.__original_collect()

        collector.__original_collect = collector.collect  # type: ignore[attr-defined]
        collector.collect = _patched_collect  # type: ignore[method-assign]
    elif isinstance(collector, Class):
        collector.obj.__pytest_asyncio_scoped_event_loop = scoped_event_loop


@contextlib.contextmanager
def _temporary_event_loop_policy(policy: AbstractEventLoopPolicy) -> Iterator[None]:
    old_loop_policy = asyncio.get_event_loop_policy()
    try:
        old_loop = _get_event_loop_no_warn()
    except RuntimeError:
        old_loop = None
    asyncio.set_event_loop_policy(policy)
    try:
        yield
    finally:
        asyncio.set_event_loop_policy(old_loop_policy)
        # When a test uses both a scoped event loop and the event_loop fixture,
        # the "_provide_clean_event_loop" finalizer of the event_loop fixture
        # will already have installed a fresh event loop, in order to shield
        # subsequent tests from side-effects. We close this loop before restoring
        # the old loop to avoid ResourceWarnings.
        try:
            _get_event_loop_no_warn().close()
        except RuntimeError:
            pass
        asyncio.set_event_loop(old_loop)


_REDEFINED_EVENT_LOOP_FIXTURE_WARNING = dedent(
    """\
    The event_loop fixture provided by pytest-asyncio has been redefined in
    %s:%d
    Replacing the event_loop fixture with a custom implementation is deprecated
    and will lead to errors in the future.
    If you want to request an asyncio event loop with a scope other than function
    scope, use the "scope" argument to the asyncio mark when marking the tests.
    If you want to return different types of event loops, use the event_loop_policy
    fixture.
    """
)


@pytest.hookimpl(tryfirst=True)
def pytest_generate_tests(metafunc: Metafunc) -> None:
    marker = metafunc.definition.get_closest_marker("asyncio")
    if not marker:
        return
    scope = marker.kwargs.get("scope", "function")
    if scope == "function":
        return
    event_loop_node = _retrieve_scope_root(metafunc.definition, scope)
    event_loop_fixture_id = event_loop_node.stash.get(_event_loop_fixture_id, None)

    if event_loop_fixture_id:
        # This specific fixture name may already be in metafunc.argnames, if this
        # test indirectly depends on the fixture. For example, this is the case
        # when the test depends on an async fixture, both of which share the same
        # event loop fixture mark.
        if event_loop_fixture_id in metafunc.fixturenames:
            return
        fixturemanager = metafunc.config.pluginmanager.get_plugin("funcmanage")
        assert fixturemanager is not None
        if "event_loop" in metafunc.fixturenames:
            raise MultipleEventLoopsRequestedError(
                _MULTIPLE_LOOPS_REQUESTED_ERROR.format(
                    test_name=metafunc.definition.nodeid,
                    scope=scope,
                    scoped_loop_node=event_loop_node.nodeid,
                ),
            )
        # Add the scoped event loop fixture to Metafunc's list of fixture names and
        # fixturedefs and leave the actual parametrization to pytest
        # The fixture needs to be appended to avoid messing up the fixture evaluation
        # order
        metafunc.fixturenames.append(event_loop_fixture_id)
        metafunc._arg2fixturedefs[event_loop_fixture_id] = (
            fixturemanager._arg2fixturedefs[event_loop_fixture_id]
        )


# TODO: #778 Narrow down return type of function when dropping support for pytest 7
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(
    fixturedef: FixtureDef,
) -> Generator[None, Any, None]:
    """Adjust the event loop policy when an event loop is produced."""
    if fixturedef.argname == "event_loop":
        # The use of a fixture finalizer is preferred over the
        # pytest_fixture_post_finalizer hook. The fixture finalizer is invoked once
        # for each fixture, whereas the hook may be invoked multiple times for
        # any specific fixture.
        # see https://github.com/pytest-dev/pytest/issues/5848
        _add_finalizers(
            fixturedef,
            _close_event_loop,
            _restore_event_loop_policy(asyncio.get_event_loop_policy()),
            _provide_clean_event_loop,
        )
        outcome = yield
        loop: asyncio.AbstractEventLoop = outcome.get_result()
        # Weird behavior was observed when checking for an attribute of FixtureDef.func
        # Instead, we now check for a special attribute of the returned event loop
        fixture_filename = inspect.getsourcefile(fixturedef.func)
        if not getattr(loop, "__original_fixture_loop", False):
            _, fixture_line_number = inspect.getsourcelines(fixturedef.func)
            warnings.warn(
                _REDEFINED_EVENT_LOOP_FIXTURE_WARNING
                % (fixture_filename, fixture_line_number),
                DeprecationWarning,
            )
        policy = asyncio.get_event_loop_policy()
        try:
            old_loop = _get_event_loop_no_warn(policy)
            is_pytest_asyncio_loop = getattr(old_loop, "__pytest_asyncio", False)
            if old_loop is not loop and not is_pytest_asyncio_loop:
                old_loop.close()
        except RuntimeError:
            # Either the current event loop has been set to None
            # or the loop policy doesn't specify to create new loops
            # or we're not in the main thread
            pass
        policy.set_event_loop(loop)
        return

    yield


def _add_finalizers(fixturedef: FixtureDef, *finalizers: Callable[[], object]) -> None:
    """
    Regsiters the specified fixture finalizers in the fixture.

    Finalizers need to specified in the exact order in which they should be invoked.

    :param fixturedef: Fixture definition which finalizers should be added to
    :param finalizers: Finalizers to be added
    """
    for finalizer in reversed(finalizers):
        fixturedef.addfinalizer(finalizer)


_UNCLOSED_EVENT_LOOP_WARNING = dedent(
    """\
    pytest-asyncio detected an unclosed event loop when tearing down the event_loop
    fixture: %r
    pytest-asyncio will close the event loop for you, but future versions of the
    library will no longer do so. In order to ensure compatibility with future
    versions, please make sure that:
        1. Any custom "event_loop" fixture properly closes the loop after yielding it
        2. The scopes of your custom "event_loop" fixtures do not overlap
        3. Your code does not modify the event loop in async fixtures or tests
    """
)


def _close_event_loop() -> None:
    policy = asyncio.get_event_loop_policy()
    try:
        loop = policy.get_event_loop()
    except RuntimeError:
        loop = None
    if loop is not None:
        if not loop.is_closed():
            warnings.warn(
                _UNCLOSED_EVENT_LOOP_WARNING % loop,
                DeprecationWarning,
            )
        loop.close()


def _restore_event_loop_policy(previous_policy) -> Callable[[], None]:
    def _restore_policy():
        # Close any event loop associated with the old loop policy
        # to avoid ResourceWarnings in the _provide_clean_event_loop finalizer
        try:
            loop = _get_event_loop_no_warn(previous_policy)
        except RuntimeError:
            loop = None
        if loop:
            loop.close()
        asyncio.set_event_loop_policy(previous_policy)

    return _restore_policy


def _provide_clean_event_loop() -> None:
    # At this point, the event loop for the current thread is closed.
    # When a user calls asyncio.get_event_loop(), they will get a closed loop.
    # In order to avoid this side effect from pytest-asyncio, we need to replace
    # the current loop with a fresh one.
    # Note that we cannot set the loop to None, because get_event_loop only creates
    # a new loop, when set_event_loop has not been called.
    policy = asyncio.get_event_loop_policy()
    new_loop = policy.new_event_loop()
    policy.set_event_loop(new_loop)


def _get_event_loop_no_warn(
    policy: Optional[AbstractEventLoopPolicy] = None,
) -> asyncio.AbstractEventLoop:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        if policy is not None:
            return policy.get_event_loop()
        else:
            return asyncio.get_event_loop()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_pyfunc_call(pyfuncitem: Function) -> Optional[object]:
    """
    Pytest hook called before a test case is run.

    Wraps marked tests in a synchronous function
    where the wrapped test coroutine is executed in an event loop.
    """
    if pyfuncitem.get_closest_marker("asyncio") is not None:
        if isinstance(pyfuncitem, PytestAsyncioFunction):
            pass
        else:
            pyfuncitem.warn(
                pytest.PytestWarning(
                    f"The test {pyfuncitem} is marked with '@pytest.mark.asyncio' "
                    "but it is not an async function. "
                    "Please remove the asyncio mark. "
                    "If the test is not marked explicitly, "
                    "check for global marks applied via 'pytestmark'."
                )
            )
    yield


def wrap_in_sync(
    func: Callable[..., Awaitable[Any]],
):
    """Return a sync wrapper around an async function executing it in the
    current event loop."""

    # if the function is already wrapped, we rewrap using the original one
    # not using __wrapped__ because the original function may already be
    # a wrapped one
    raw_func = getattr(func, "_raw_test_func", None)
    if raw_func is not None:
        func = raw_func

    @functools.wraps(func)
    def inner(*args, **kwargs):
        coro = func(*args, **kwargs)
        _loop = _get_event_loop_no_warn()
        task = asyncio.ensure_future(coro, loop=_loop)
        try:
            _loop.run_until_complete(task)
        except BaseException:
            # run_until_complete doesn't get the result from exceptions
            # that are not subclasses of `Exception`. Consume all
            # exceptions to prevent asyncio's warning from logging.
            if task.done() and not task.cancelled():
                task.exception()
            raise

    inner._raw_test_func = func  # type: ignore[attr-defined]
    return inner


_MULTIPLE_LOOPS_REQUESTED_ERROR = dedent(
    """\
        Multiple asyncio event loops with different scopes have been requested
        by {test_name}. The test explicitly requests the event_loop fixture, while
        another event loop with {scope} scope is provided by {scoped_loop_node}.
        Remove "event_loop" from the requested fixture in your test to run the test
        in a {scope}-scoped event loop or remove the scope argument from the "asyncio"
        mark to run the test in a function-scoped event loop.
    """
)


def pytest_runtest_setup(item: pytest.Item) -> None:
    marker = item.get_closest_marker("asyncio")
    if marker is None:
        return
    scope = marker.kwargs.get("scope", "function")
    if scope != "function":
        parent_node = _retrieve_scope_root(item, scope)
        event_loop_fixture_id = parent_node.stash[_event_loop_fixture_id]
    else:
        event_loop_fixture_id = "event_loop"
    fixturenames = item.fixturenames  # type: ignore[attr-defined]
    if event_loop_fixture_id not in fixturenames:
        fixturenames.append(event_loop_fixture_id)
    obj = getattr(item, "obj", None)
    if not getattr(obj, "hypothesis", False) and getattr(
        obj, "is_hypothesis_test", False
    ):
        pytest.fail(
            "test function `%r` is using Hypothesis, but pytest-asyncio "
            "only works with Hypothesis 3.64.0 or later." % item
        )


def _retrieve_scope_root(item: Union[Collector, Item], scope: str) -> Collector:
    node_type_by_scope = {
        "class": Class,
        "module": Module,
        "package": Package,
        "session": Session,
    }
    scope_root_type = node_type_by_scope[scope]
    for node in reversed(item.listchain()):
        if isinstance(node, scope_root_type):
            assert isinstance(node, pytest.Collector)
            return node
    error_message = (
        f"{item.name} is marked to be run in an event loop with scope {scope}, "
        f"but is not part of any {scope}."
    )
    raise pytest.UsageError(error_message)


@pytest.fixture
def event_loop(request: FixtureRequest) -> Iterator[asyncio.AbstractEventLoop]:
    """Create an instance of the default event loop for each test case."""
    new_loop_policy = request.getfixturevalue(event_loop_policy.__name__)
    asyncio.set_event_loop_policy(new_loop_policy)
    loop = asyncio.get_event_loop_policy().new_event_loop()
    # Add a magic value to the event loop, so pytest-asyncio can determine if the
    # event_loop fixture was overridden. Other implementations of event_loop don't
    # set this value.
    # The magic value must be set as part of the function definition, because pytest
    # seems to have multiple instances of the same FixtureDef or fixture function
    loop.__original_fixture_loop = True  # type: ignore[attr-defined]
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def _session_event_loop(
    request: FixtureRequest, event_loop_policy: AbstractEventLoopPolicy
) -> Iterator[asyncio.AbstractEventLoop]:
    new_loop_policy = event_loop_policy
    with _temporary_event_loop_policy(new_loop_policy):
        loop = asyncio.new_event_loop()
        loop.__pytest_asyncio = True  # type: ignore[attr-defined]
        asyncio.set_event_loop(loop)
        yield loop
        loop.close()


@pytest.fixture(scope="session", autouse=True)
def event_loop_policy() -> AbstractEventLoopPolicy:
    """Return an instance of the policy used to create asyncio event loops."""
    return asyncio.get_event_loop_policy()


def is_async_test(item: Item) -> bool:
    """Returns whether a test item is a pytest-asyncio test"""
    return isinstance(item, PytestAsyncioFunction)


def _unused_port(socket_type: int) -> int:
    """Find an unused localhost port from 1024-65535 and return it."""
    with contextlib.closing(socket.socket(type=socket_type)) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@pytest.fixture
def unused_tcp_port() -> int:
    return _unused_port(socket.SOCK_STREAM)


@pytest.fixture
def unused_udp_port() -> int:
    return _unused_port(socket.SOCK_DGRAM)


@pytest.fixture(scope="session")
def unused_tcp_port_factory() -> Callable[[], int]:
    """A factory function, producing different unused TCP ports."""
    produced = set()

    def factory():
        """Return an unused port."""
        port = _unused_port(socket.SOCK_STREAM)

        while port in produced:
            port = _unused_port(socket.SOCK_STREAM)

        produced.add(port)

        return port

    return factory


@pytest.fixture(scope="session")
def unused_udp_port_factory() -> Callable[[], int]:
    """A factory function, producing different unused UDP ports."""
    produced = set()

    def factory():
        """Return an unused port."""
        port = _unused_port(socket.SOCK_DGRAM)

        while port in produced:
            port = _unused_port(socket.SOCK_DGRAM)

        produced.add(port)

        return port

    return factory
```
```bash
./.venv/lib/python3.9/site-packages/pytest_asyncio/py.typed
```
```

```
```bash
./.venv/lib/python3.9/site-packages/six-1.16.0.dist-info/RECORD
```
```
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/six.cpython-39.pyc,,
six-1.16.0.dist-info/INSTALLER,sha256=zuuue4knoyJ-UwPPXg8fezS7VCrXJQrAP7zeNuwvFQg,4
six-1.16.0.dist-info/LICENSE,sha256=i7hQxWWqOJ_cFvOkaWWtI9gq3_YPI5P8J2K2MYXo5sk,1066
six-1.16.0.dist-info/METADATA,sha256=VQcGIFCAEmfZcl77E5riPCN4v2TIsc_qtacnjxKHJoI,1795
six-1.16.0.dist-info/RECORD,,
six-1.16.0.dist-info/WHEEL,sha256=Z-nyYpwrcSqxfdux5Mbn_DQ525iP7J2DG3JgGvOYyTQ,110
six-1.16.0.dist-info/top_level.txt,sha256=_iVH_iYEtEXnD8nYGQYpYFUvkUW9sEO1GYbkeKSAais,4
six.py,sha256=TOOfQi7nFGfMrIvtdr6wX4wyHH8M7aknmuLfo2cBBrM,34549
```
```bash
./.venv/lib/python3.9/site-packages/six-1.16.0.dist-info/LICENSE
```
```
Copyright (c) 2010-2020 Benjamin Peterson

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
```bash
./.venv/lib/python3.9/site-packages/six-1.16.0.dist-info/WHEEL
```
```
Wheel-Version: 1.0
Generator: bdist_wheel (0.36.2)
Root-Is-Purelib: true
Tag: py2-none-any
Tag: py3-none-any
```
```bash
./.venv/lib/python3.9/site-packages/six-1.16.0.dist-info/top_level.txt
```
```
six
```
```bash
./.venv/lib/python3.9/site-packages/six-1.16.0.dist-info/INSTALLER
```
```
pip
```
```bash
./.venv/lib/python3.9/site-packages/six-1.16.0.dist-info/METADATA
```
```
Metadata-Version: 2.1
Name: six
Version: 1.16.0
Summary: Python 2 and 3 compatibility utilities
Home-page: https://github.com/benjaminp/six
Author: Benjamin Peterson
Author-email: benjamin@python.org
License: MIT
Platform: UNKNOWN
Classifier: Development Status :: 5 - Production/Stable
Classifier: Programming Language :: Python :: 2
Classifier: Programming Language :: Python :: 3
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: MIT License
Classifier: Topic :: Software Development :: Libraries
Classifier: Topic :: Utilities
Requires-Python: >=2.7, !=3.0.*, !=3.1.*, !=3.2.*

.. image:: https://img.shields.io/pypi/v/six.svg
   :target: https://pypi.org/project/six/
   :alt: six on PyPI

.. image:: https://travis-ci.org/benjaminp/six.svg?branch=master
   :target: https://travis-ci.org/benjaminp/six
   :alt: six on TravisCI

.. image:: https://readthedocs.org/projects/six/badge/?version=latest
   :target: https://six.readthedocs.io/
   :alt: six's documentation on Read the Docs

.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: https://github.com/benjaminp/six/blob/master/LICENSE
   :alt: MIT License badge

Six is a Python 2 and 3 compatibility library.  It provides utility functions
for smoothing over the differences between the Python versions with the goal of
writing Python code that is compatible on both Python versions.  See the
documentation for more information on what is provided.

Six supports Python 2.7 and 3.3+.  It is contained in only one Python
file, so it can be easily copied into your project. (The copyright and license
notice must be retained.)

Online documentation is at https://six.readthedocs.io/.

Bugs can be reported to https://github.com/benjaminp/six.  The code can also
be found there.
```
```bash
./.venv/lib/python3.9/site-packages/packaging-24.1.dist-info/RECORD
```
```
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/packaging/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/packaging/_elffile.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/packaging/_manylinux.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/packaging/_musllinux.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/packaging/_parser.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/packaging/_structures.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/packaging/_tokenizer.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/packaging/markers.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/packaging/metadata.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/packaging/requirements.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/packaging/specifiers.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/packaging/tags.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/packaging/utils.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/packaging/version.cpython-39.pyc,,
packaging-24.1.dist-info/INSTALLER,sha256=zuuue4knoyJ-UwPPXg8fezS7VCrXJQrAP7zeNuwvFQg,4
packaging-24.1.dist-info/LICENSE,sha256=ytHvW9NA1z4HS6YU0m996spceUDD2MNIUuZcSQlobEg,197
packaging-24.1.dist-info/LICENSE.APACHE,sha256=DVQuDIgE45qn836wDaWnYhSdxoLXgpRRKH4RuTjpRZQ,10174
packaging-24.1.dist-info/LICENSE.BSD,sha256=tw5-m3QvHMb5SLNMFqo5_-zpQZY2S8iP8NIYDwAo-sU,1344
packaging-24.1.dist-info/METADATA,sha256=X3ooO3WnCfzNSBrqQjefCD1POAF1M2WSLmsHMgQlFdk,3204
packaging-24.1.dist-info/RECORD,,
packaging-24.1.dist-info/WHEEL,sha256=EZbGkh7Ie4PoZfRQ8I0ZuP9VklN_TvcZ6DSE5Uar4z4,81
packaging/__init__.py,sha256=dtw2bNmWCQ9WnMoK3bk_elL1svSlikXtLpZhCFIB9SE,496
packaging/_elffile.py,sha256=_LcJW4YNKywYsl4169B2ukKRqwxjxst_8H0FRVQKlz8,3282
packaging/_manylinux.py,sha256=Xo4V0PZz8sbuVCbTni0t1CR0AHeir_7ib4lTmV8scD4,9586
packaging/_musllinux.py,sha256=p9ZqNYiOItGee8KcZFeHF_YcdhVwGHdK6r-8lgixvGQ,2694
packaging/_parser.py,sha256=s_TvTvDNK0NrM2QB3VKThdWFM4Nc0P6JnkObkl3MjpM,10236
packaging/_structures.py,sha256=q3eVNmbWJGG_S0Dit_S3Ao8qQqz_5PYTXFAKBZe5yr4,1431
packaging/_tokenizer.py,sha256=J6v5H7Jzvb-g81xp_2QACKwO7LxHQA6ikryMU7zXwN8,5273
packaging/markers.py,sha256=dWKSqn5Sp-jDmOG-W3GfLHKjwhf1IsznbT71VlBoB5M,10671
packaging/metadata.py,sha256=KINuSkJ12u-SyoKNTy_pHNGAfMUtxNvZ53qA1zAKcKI,32349
packaging/py.typed,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
packaging/requirements.py,sha256=gYyRSAdbrIyKDY66ugIDUQjRMvxkH2ALioTmX3tnL6o,2947
packaging/specifiers.py,sha256=rjpc3hoJuunRIT6DdH7gLTnQ5j5QKSuWjoTC5sdHtHI,39714
packaging/tags.py,sha256=y8EbheOu9WS7s-MebaXMcHMF-jzsA_C1Lz5XRTiSy4w,18883
packaging/utils.py,sha256=NAdYUwnlAOpkat_RthavX8a07YuVxgGL_vwrx73GSDM,5287
packaging/version.py,sha256=V0H3SOj_8werrvorrb6QDLRhlcqSErNTTkCvvfszhDI,16198
```
```bash
./.venv/lib/python3.9/site-packages/packaging-24.1.dist-info/LICENSE
```
```
This software is made available under the terms of *either* of the licenses
found in LICENSE.APACHE or LICENSE.BSD. Contributions to this software is made
under the terms of *both* these licenses.
```
```bash
./.venv/lib/python3.9/site-packages/packaging-24.1.dist-info/LICENSE.APACHE
```
```

                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS
```
```bash
./.venv/lib/python3.9/site-packages/packaging-24.1.dist-info/WHEEL
```
```
Wheel-Version: 1.0
Generator: flit 3.9.0
Root-Is-Purelib: true
Tag: py3-none-any
```
```bash
./.venv/lib/python3.9/site-packages/packaging-24.1.dist-info/LICENSE.BSD
```
```
Copyright (c) Donald Stufft and individual contributors.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
```bash
./.venv/lib/python3.9/site-packages/packaging-24.1.dist-info/INSTALLER
```
```
pip
```
```bash
./.venv/lib/python3.9/site-packages/packaging-24.1.dist-info/METADATA
```
```
Metadata-Version: 2.1
Name: packaging
Version: 24.1
Summary: Core utilities for Python packages
Author-email: Donald Stufft <donald@stufft.io>
Requires-Python: >=3.8
Description-Content-Type: text/x-rst
Classifier: Development Status :: 5 - Production/Stable
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: Apache Software License
Classifier: License :: OSI Approved :: BSD License
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3 :: Only
Classifier: Programming Language :: Python :: 3.8
Classifier: Programming Language :: Python :: 3.9
Classifier: Programming Language :: Python :: 3.10
Classifier: Programming Language :: Python :: 3.11
Classifier: Programming Language :: Python :: 3.12
Classifier: Programming Language :: Python :: 3.13
Classifier: Programming Language :: Python :: Implementation :: CPython
Classifier: Programming Language :: Python :: Implementation :: PyPy
Classifier: Typing :: Typed
Project-URL: Documentation, https://packaging.pypa.io/
Project-URL: Source, https://github.com/pypa/packaging

packaging
=========

.. start-intro

Reusable core utilities for various Python Packaging
`interoperability specifications <https://packaging.python.org/specifications/>`_.

This library provides utilities that implement the interoperability
specifications which have clearly one correct behaviour (eg: :pep:`440`)
or benefit greatly from having a single shared implementation (eg: :pep:`425`).

.. end-intro

The ``packaging`` project includes the following: version handling, specifiers,
markers, requirements, tags, utilities.

Documentation
-------------

The `documentation`_ provides information and the API for the following:

- Version Handling
- Specifiers
- Markers
- Requirements
- Tags
- Utilities

Installation
------------

Use ``pip`` to install these utilities::

    pip install packaging

The ``packaging`` library uses calendar-based versioning (``YY.N``).

Discussion
----------

If you run into bugs, you can file them in our `issue tracker`_.

You can also join ``#pypa`` on Freenode to ask questions or get involved.


.. _`documentation`: https://packaging.pypa.io/
.. _`issue tracker`: https://github.com/pypa/packaging/issues


Code of Conduct
---------------

Everyone interacting in the packaging project's codebases, issue trackers, chat
rooms, and mailing lists is expected to follow the `PSF Code of Conduct`_.

.. _PSF Code of Conduct: https://github.com/pypa/.github/blob/main/CODE_OF_CONDUCT.md

Contributing
------------

The ``CONTRIBUTING.rst`` file outlines how to contribute to this project as
well as how to report a potential security issue. The documentation for this
project also covers information about `project development`_ and `security`_.

.. _`project development`: https://packaging.pypa.io/en/latest/development/
.. _`security`: https://packaging.pypa.io/en/latest/security/

Project History
---------------

Please review the ``CHANGELOG.rst`` file or the `Changelog documentation`_ for
recent changes and project history.

.. _`Changelog documentation`: https://packaging.pypa.io/en/latest/changelog/
```
```bash
./.venv/lib/python3.9/site-packages/pytz-2024.1.dist-info/zip-safe
```
```

```
```bash
./.venv/lib/python3.9/site-packages/pytz-2024.1.dist-info/RECORD
```
```
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pytz/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pytz/exceptions.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pytz/lazy.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pytz/reference.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pytz/tzfile.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/pytz/tzinfo.cpython-39.pyc,,
pytz-2024.1.dist-info/INSTALLER,sha256=zuuue4knoyJ-UwPPXg8fezS7VCrXJQrAP7zeNuwvFQg,4
pytz-2024.1.dist-info/LICENSE.txt,sha256=vosaN-vibFkqkPbA6zMQOn84POL010mMCvmlJpkKB7g,1088
pytz-2024.1.dist-info/METADATA,sha256=2mOz3YzpRCJtu0iklrKsUm8a8BmJglIL_qqGhhduPJk,22325
pytz-2024.1.dist-info/RECORD,,
pytz-2024.1.dist-info/REQUESTED,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
pytz-2024.1.dist-info/WHEEL,sha256=z9j0xAa_JmUKMpmz72K0ZGALSM_n-wQVmGbleXx2VHg,110
pytz-2024.1.dist-info/top_level.txt,sha256=6xRYlt934v1yHb1JIrXgHyGxn3cqACvd-yE8ski_kcc,5
pytz-2024.1.dist-info/zip-safe,sha256=AbpHGcgLb-kRsJGnwFEktk7uzpZOCcBY74-YBdrKVGs,1
pytz/__init__.py,sha256=RZJJJ1W2RyP9fllsMNO4w-yjJRpIazWJ9fvj5telYig,35101
pytz/exceptions.py,sha256=434ZcuLlpLQY9mWoGq7zJMV1TyiYvVgpKBU1qZkbDjM,1571
pytz/lazy.py,sha256=toeR5uDWKBj6ezsUZ4elNP6CEMtK7CO2jS9A30nsFbo,5404
pytz/reference.py,sha256=zUtCki7JFEmrzrjNsfMD7YL0lWDxynKc1Ubo4iXSs74,3778
pytz/tzfile.py,sha256=K2y7pZs4vydpZVftrfAA_-hgw17y1Szc7z_QCse6udU,4723
pytz/tzinfo.py,sha256=XfaVOoO3KsCvtUYaCd0fvgBXWZ8tgevGYUoBh_uiE60,19340
pytz/zoneinfo/Africa/Abidjan,sha256=0u-sTl8j2IyV1ywdtCgHFw9S9D3ZiiBa9akqkbny2Zc,148
pytz/zoneinfo/Africa/Accra,sha256=0u-sTl8j2IyV1ywdtCgHFw9S9D3ZiiBa9akqkbny2Zc,148
pytz/zoneinfo/Africa/Addis_Ababa,sha256=yJsuJTqJJqbOz37_NOS_zbf-JNr_IthHGMMN7sDqSWg,265
pytz/zoneinfo/Africa/Algiers,sha256=vaFpjNVCwObnbfu82rOQzdJvN6nVgmpXpQ1aqzfzsqY,735
pytz/zoneinfo/Africa/Asmara,sha256=yJsuJTqJJqbOz37_NOS_zbf-JNr_IthHGMMN7sDqSWg,265
pytz/zoneinfo/Africa/Asmera,sha256=yJsuJTqJJqbOz37_NOS_zbf-JNr_IthHGMMN7sDqSWg,265
pytz/zoneinfo/Africa/Bamako,sha256=0u-sTl8j2IyV1ywdtCgHFw9S9D3ZiiBa9akqkbny2Zc,148
pytz/zoneinfo/Africa/Bangui,sha256=z_6wKCzL1_ug5JP_hneh5abdUZeIUELkN_ladz-ESEY,235
pytz/zoneinfo/Africa/Banjul,sha256=0u-sTl8j2IyV1ywdtCgHFw9S9D3ZiiBa9akqkbny2Zc,148
pytz/zoneinfo/Africa/Bissau,sha256=IjuxDP6EZiDHFvl_bHS6NN7sdRxLKXllooBC829poak,194
pytz/zoneinfo/Africa/Blantyre,sha256=k_GelVHViGiuWCB1LSyTpIYSTDZEY9yclInQRY-LxoI,149
pytz/zoneinfo/Africa/Brazzaville,sha256=z_6wKCzL1_ug5JP_hneh5abdUZeIUELkN_ladz-ESEY,235
pytz/zoneinfo/Africa/Bujumbura,sha256=k_GelVHViGiuWCB1LSyTpIYSTDZEY9yclInQRY-LxoI,149
pytz/zoneinfo/Africa/Cairo,sha256=Lft-GCLQhaSJm9VqUmsEFoHIS1Vhfa7pFJn9GZCpifs,2399
pytz/zoneinfo/Africa/Casablanca,sha256=4RqVbw_F3ZucopIC2ivAJ8WDwj5wRODAB67tBpdXcgA,2429
pytz/zoneinfo/Africa/Ceuta,sha256=Cw-2_nFDGbN8WqIsVpcauyZooWX8j3Kmx2PnC0fHut8,2052
pytz/zoneinfo/Africa/Conakry,sha256=0u-sTl8j2IyV1ywdtCgHFw9S9D3ZiiBa9akqkbny2Zc,148
pytz/zoneinfo/Africa/Dakar,sha256=0u-sTl8j2IyV1ywdtCgHFw9S9D3ZiiBa9akqkbny2Zc,148
pytz/zoneinfo/Africa/Dar_es_Salaam,sha256=yJsuJTqJJqbOz37_NOS_zbf-JNr_IthHGMMN7sDqSWg,265
pytz/zoneinfo/Africa/Djibouti,sha256=yJsuJTqJJqbOz37_NOS_zbf-JNr_IthHGMMN7sDqSWg,265
pytz/zoneinfo/Africa/Douala,sha256=z_6wKCzL1_ug5JP_hneh5abdUZeIUELkN_ladz-ESEY,235
pytz/zoneinfo/Africa/El_Aaiun,sha256=UWCCqQLJxd8qsTYw82kz9W1suwW5TRgnZw31sDWDz20,2295
pytz/zoneinfo/Africa/Freetown,sha256=0u-sTl8j2IyV1ywdtCgHFw9S9D3ZiiBa9akqkbny2Zc,148
pytz/zoneinfo/Africa/Gaborone,sha256=k_GelVHViGiuWCB1LSyTpIYSTDZEY9yclInQRY-LxoI,149
pytz/zoneinfo/Africa/Harare,sha256=k_GelVHViGiuWCB1LSyTpIYSTDZEY9yclInQRY-LxoI,149
pytz/zoneinfo/Africa/Johannesburg,sha256=bBvMdSZo53WFowiuhUO9C8zY6BOGViboCb-U8_49l34,246
pytz/zoneinfo/Africa/Juba,sha256=UVnIqEPJwHLTMC-r5qZQHNv9opoYVsKdq-ta_5XUw_Q,679
pytz/zoneinfo/Africa/Kampala,sha256=yJsuJTqJJqbOz37_NOS_zbf-JNr_IthHGMMN7sDqSWg,265
pytz/zoneinfo/Africa/Khartoum,sha256=MYWDoJ3AcCItZdApoeOgtWWDDxquwTon5v5TOGP70-o,679
pytz/zoneinfo/Africa/Kigali,sha256=k_GelVHViGiuWCB1LSyTpIYSTDZEY9yclInQRY-LxoI,149
pytz/zoneinfo/Africa/Kinshasa,sha256=z_6wKCzL1_ug5JP_hneh5abdUZeIUELkN_ladz-ESEY,235
pytz/zoneinfo/Africa/Lagos,sha256=z_6wKCzL1_ug5JP_hneh5abdUZeIUELkN_ladz-ESEY,235
pytz/zoneinfo/Africa/Libreville,sha256=z_6wKCzL1_ug5JP_hneh5abdUZeIUELkN_ladz-ESEY,235
pytz/zoneinfo/Africa/Lome,sha256=0u-sTl8j2IyV1ywdtCgHFw9S9D3ZiiBa9akqkbny2Zc,148
pytz/zoneinfo/Africa/Luanda,sha256=z_6wKCzL1_ug5JP_hneh5abdUZeIUELkN_ladz-ESEY,235
pytz/zoneinfo/Africa/Lubumbashi,sha256=k_GelVHViGiuWCB1LSyTpIYSTDZEY9yclInQRY-LxoI,149
pytz/zoneinfo/Africa/Lusaka,sha256=k_GelVHViGiuWCB1LSyTpIYSTDZEY9yclInQRY-LxoI,149
pytz/zoneinfo/Africa/Malabo,sha256=z_6wKCzL1_ug5JP_hneh5abdUZeIUELkN_ladz-ESEY,235
pytz/zoneinfo/Africa/Maputo,sha256=k_GelVHViGiuWCB1LSyTpIYSTDZEY9yclInQRY-LxoI,149
pytz/zoneinfo/Africa/Maseru,sha256=bBvMdSZo53WFowiuhUO9C8zY6BOGViboCb-U8_49l34,246
pytz/zoneinfo/Africa/Mbabane,sha256=bBvMdSZo53WFowiuhUO9C8zY6BOGViboCb-U8_49l34,246
pytz/zoneinfo/Africa/Mogadishu,sha256=yJsuJTqJJqbOz37_NOS_zbf-JNr_IthHGMMN7sDqSWg,265
pytz/zoneinfo/Africa/Monrovia,sha256=-VsJW5cU4KdvfgYaQVv4lcuzmaKIVFMd42nO6RXOBdU,208
pytz/zoneinfo/Africa/Nairobi,sha256=yJsuJTqJJqbOz37_NOS_zbf-JNr_IthHGMMN7sDqSWg,265
pytz/zoneinfo/Africa/Ndjamena,sha256=8T3A0Zm9Gj0Bvm6rd88t3GAXKiKdGUfHlIqYlkYI0KM,199
pytz/zoneinfo/Africa/Niamey,sha256=z_6wKCzL1_ug5JP_hneh5abdUZeIUELkN_ladz-ESEY,235
pytz/zoneinfo/Africa/Nouakchott,sha256=0u-sTl8j2IyV1ywdtCgHFw9S9D3ZiiBa9akqkbny2Zc,148
pytz/zoneinfo/Africa/Ouagadougou,sha256=0u-sTl8j2IyV1ywdtCgHFw9S9D3ZiiBa9akqkbny2Zc,148
pytz/zoneinfo/Africa/Porto-Novo,sha256=z_6wKCzL1_ug5JP_hneh5abdUZeIUELkN_ladz-ESEY,235
pytz/zoneinfo/Africa/Sao_Tome,sha256=MdjxpQ268uzJ7Zx1ZroFUtRUwqsJ6F_yY3AYV9FXw1I,254
pytz/zoneinfo/Africa/Timbuktu,sha256=0u-sTl8j2IyV1ywdtCgHFw9S9D3ZiiBa9akqkbny2Zc,148
pytz/zoneinfo/Africa/Tripoli,sha256=W1dptGD70T7ppGoo0fczFQeDiIp0nultLNPV66MwB2c,625
pytz/zoneinfo/Africa/Tunis,sha256=OFVMEM4eYT2Ez0beuhEUCTSIpcFldWxsV2uEoTZIUNI,689
pytz/zoneinfo/Africa/Windhoek,sha256=xuhvudrMH4alnVmouSTQI8YL8F_HbgsF2EQ7AZKzuHs,955
pytz/zoneinfo/America/Adak,sha256=IB1DhwJQAKbhPJ9jHLf8zW5Dad7HIkBS-dhv64E1OlM,2356
pytz/zoneinfo/America/Anchorage,sha256=oZA1NSPS2BWdymYpnCHFO8BlYVS-ll5KLg2Ez9CbETs,2371
pytz/zoneinfo/America/Anguilla,sha256=hJHlV_-AGoMGUWuMpZRv9fLmghrzFHfrR9fRkcxaZJc,246
pytz/zoneinfo/America/Antigua,sha256=hJHlV_-AGoMGUWuMpZRv9fLmghrzFHfrR9fRkcxaZJc,246
pytz/zoneinfo/America/Araguaina,sha256=G6v9wYFZ8EB4WQfIsqRbbiiKd2b27j7Zt5dFjBbzx2o,870
pytz/zoneinfo/America/Argentina/Buenos_Aires,sha256=JmU8lBwmy29gR6OmeytvFdMRx6ObJKnYNHmLyMmXX2M,1062
pytz/zoneinfo/America/Argentina/Catamarca,sha256=uMCJXXGYmNESHVvj5RYBZ0McrOdE14hwm17l25MgRW0,1062
pytz/zoneinfo/America/Argentina/ComodRivadavia,sha256=uMCJXXGYmNESHVvj5RYBZ0McrOdE14hwm17l25MgRW0,1062
pytz/zoneinfo/America/Argentina/Cordoba,sha256=uniNihhMHnr4XK4WpwiPUnrAT0YPmvzqB6f0hRLtXvY,1062
pytz/zoneinfo/America/Argentina/Jujuy,sha256=PGmAehypCxj0XCenCSWqylDIPbKLK0DlrwJK_24D590,1034
pytz/zoneinfo/America/Argentina/La_Rioja,sha256=Um6XoVXhsr62ad1mWuebe6NY0ZHauBdR9tMGDgqCOHg,1076
pytz/zoneinfo/America/Argentina/Mendoza,sha256=xcOVtvRyVYFAU90y2QYwpyQhpMLyAp7-Fxvku4kgl0c,1062
pytz/zoneinfo/America/Argentina/Rio_Gallegos,sha256=F9ZKR4o8gLHX7QBuIjMapGIdmzJxpqwbouPgZ5MqDpY,1062
pytz/zoneinfo/America/Argentina/Salta,sha256=h1KYrDNIapvDkYhi1PaB8WD1qWOe4vhhgDJWDCGV4jc,1034
pytz/zoneinfo/America/Argentina/San_Juan,sha256=AI2GltA80mPNzhHxYycuEwIbO1ANXyIqBQZMpjqKqdQ,1076
pytz/zoneinfo/America/Argentina/San_Luis,sha256=2ItGRcLVK2wx8MyJsHbIBBeAkU4B-MN5x1ZxNyZ7UJE,1088
pytz/zoneinfo/America/Argentina/Tucuman,sha256=twO-FqtNJV8XOzWTvFQ-xnEcWCoDUHY3gpVIG0Mzbf8,1090
pytz/zoneinfo/America/Argentina/Ushuaia,sha256=A6IbpVlY9IIPoSKMFRR9DMROdwXUSDc2HsASueOSnqo,1062
pytz/zoneinfo/America/Aruba,sha256=hJHlV_-AGoMGUWuMpZRv9fLmghrzFHfrR9fRkcxaZJc,246
pytz/zoneinfo/America/Asuncion,sha256=V8wwkUoNqyj0C-fUSADpU7HU8H3Qkr3jNPJ4SLsGUIc,2030
pytz/zoneinfo/America/Atikokan,sha256=kayA_pdpMcSQ0FjIzotdcf-m1JYfbKE-qcFT8LC8zqA,182
pytz/zoneinfo/America/Atka,sha256=IB1DhwJQAKbhPJ9jHLf8zW5Dad7HIkBS-dhv64E1OlM,2356
pytz/zoneinfo/America/Bahia,sha256=qi7dA6FofDhLxVMmd2L8bK3HeaQnc9X-jiijwyfhs3g,1010
pytz/zoneinfo/America/Bahia_Banderas,sha256=L6iHYbA1Us1pljllFLEIAHW4ZaZhFKoG2Zr8TT5aY38,1152
pytz/zoneinfo/America/Barbados,sha256=ima-Qrrhazu4Qfvu2Z0-e6E-GTiYknuJBu6c2yVG9LE,436
pytz/zoneinfo/America/Belem,sha256=aZMUgtFDdHNISpqyQRYbmS2IBD-BAS3CaJnhu6onLCY,562
pytz/zoneinfo/America/Belize,sha256=pkfLY2KfPchbeJa1pWcXmWAwp4ZlRvxWLVezXnrbkws,1614
pytz/zoneinfo/America/Blanc-Sablon,sha256=hJHlV_-AGoMGUWuMpZRv9fLmghrzFHfrR9fRkcxaZJc,246
pytz/zoneinfo/America/Boa_Vista,sha256=dMtaG11kGlJrgJJgGWEDZZAmnO_HfT3L4X8pI72LLFY,618
pytz/zoneinfo/America/Bogota,sha256=Z1ernZZGQxulE8KFWHYWcM3SV1jn2_QEc1Q0OJzHRak,232
pytz/zoneinfo/America/Boise,sha256=7HQsNPJiUheQgFz5kVLvTnf5xhXAYaeANqDskxKz2Vs,2410
pytz/zoneinfo/America/Buenos_Aires,sha256=JmU8lBwmy29gR6OmeytvFdMRx6ObJKnYNHmLyMmXX2M,1062
pytz/zoneinfo/America/Cambridge_Bay,sha256=_4xRlX3WdVpEcqoT6myD7NeTCXnn9OYk_iH006bwULo,2254
pytz/zoneinfo/America/Campo_Grande,sha256=gINiXg5i2e6Rh2Nbo2bFqhPAJL4F4cAqGnBankXTDXw,1430
pytz/zoneinfo/America/Cancun,sha256=lI4ZtiBtxKqNHvU47vRSwc5-GDl8JOdC2A6oc9s8iIo,834
pytz/zoneinfo/America/Caracas,sha256=mUNMFdDzZLav_ePA1ocBdmqVBierkeEszTIFpNCm5J0,250
pytz/zoneinfo/America/Catamarca,sha256=uMCJXXGYmNESHVvj5RYBZ0McrOdE14hwm17l25MgRW0,1062
pytz/zoneinfo/America/Cayenne,sha256=4k7Iv1woX4atqePKrcvMQD2Vk9Tmma7rW_AW_R62pCc,184
pytz/zoneinfo/America/Cayman,sha256=kayA_pdpMcSQ0FjIzotdcf-m1JYfbKE-qcFT8LC8zqA,182
pytz/zoneinfo/America/Chicago,sha256=_roybr6I6sIAF6cYdIxGxoRpoef153Fty48dQ6bm9oY,3592
pytz/zoneinfo/America/Chihuahua,sha256=ZAlPSsUfT3VGp1VdibnHIf-QsdEIqHuzX15wu2P2YQk,1102
pytz/zoneinfo/America/Ciudad_Juarez,sha256=OQstyPrMxx3nNEbzgDhq_W0mK49-ApNMK7_6p-6dJ64,1538
pytz/zoneinfo/America/Coral_Harbour,sha256=kayA_pdpMcSQ0FjIzotdcf-m1JYfbKE-qcFT8LC8zqA,182
pytz/zoneinfo/America/Cordoba,sha256=uniNihhMHnr4XK4WpwiPUnrAT0YPmvzqB6f0hRLtXvY,1062
pytz/zoneinfo/America/Costa_Rica,sha256=74rYa6lrgIkyls9PkHo8SCYl9oOqiuG5S7MWdnJelP4,316
pytz/zoneinfo/America/Creston,sha256=illz0sYuLL8lIPK0Tkou6dL0Vck_D0W_3rRTOvFYRmQ,360
pytz/zoneinfo/America/Cuiaba,sha256=GRJqkhRXNsOUcgjZddQxRIJdRYaw9pM_YLWbun88dkg,1402
pytz/zoneinfo/America/Curacao,sha256=hJHlV_-AGoMGUWuMpZRv9fLmghrzFHfrR9fRkcxaZJc,246
pytz/zoneinfo/America/Danmarkshavn,sha256=YRZAfUCoVtaL1L-MYMYMH1wyOaVQnfUo_gFnvMXSuzw,698
pytz/zoneinfo/America/Dawson,sha256=rAHhyuMuyjf_eyA2SBG76MRBf_fj_xi5FAuiWVQgJhw,1614
pytz/zoneinfo/America/Dawson_Creek,sha256=aJXCyP4j3ggE4wGCN-LrS9hpD_5zWHzQTeSAKTWEPUM,1050
pytz/zoneinfo/America/Denver,sha256=MugZwApDs8NI9TnXANQlUE8guNBowWQY0m-ptpPndck,2460
pytz/zoneinfo/America/Detroit,sha256=hecz8yqY2Cj5B61G3gLZdAVZvRgK9l0P90c_gN-uD5g,2230
pytz/zoneinfo/America/Dominica,sha256=hJHlV_-AGoMGUWuMpZRv9fLmghrzFHfrR9fRkcxaZJc,246
pytz/zoneinfo/America/Edmonton,sha256=-TkIfc3QlvaCf0p8COZ43Y1HRBAl-nARUi-JdXeK1vE,2332
pytz/zoneinfo/America/Eirunepe,sha256=j5eExkjFaqtC-D8XK0rGzoF9yEgbSlTbPqVG9WKhEa8,642
pytz/zoneinfo/America/El_Salvador,sha256=gvGN8Lkj-sGm2_rs8OUjAMf1oMtKp2Xes6UfWT0WqgU,224
pytz/zoneinfo/America/Ensenada,sha256=57-Q9LSTNuTidz-lOTwDysmlCoeFUXSecvVVqNWburQ,2374
pytz/zoneinfo/America/Fort_Nelson,sha256=erfODr3DrSpz65kAdO7Ts2dGbZxvddEP6gx4BX3y2J0,2240
pytz/zoneinfo/America/Fort_Wayne,sha256=kNKy9Kj9ICsiYYfCCbAggzMA7exf-GpGPMxoXocHUyw,1682
pytz/zoneinfo/America/Fortaleza,sha256=rjiSB0q1cBuMDOM9orW_uwe5UOLBwTlfjFotwOYe1mU,702
pytz/zoneinfo/America/Glace_Bay,sha256=G8DGLGCapH_aYCF_OhaL5Qonf7FOAgAPwelO5htCWBc,2192
pytz/zoneinfo/America/Godthab,sha256=KGXrMN-YkYpVCgLdpcfwMFQ77EsRAGsjUCG3yAUvVfw,1889
pytz/zoneinfo/America/Goose_Bay,sha256=JgaLueghSvX2g725FOfIgpgvsqxZGykWOhAZWGpQZRY,3210
pytz/zoneinfo/America/Grand_Turk,sha256=4YOFEPK60Bel2_fCsY6vSZxUcMJKjiKtyOf_Q0khEwU,1834
pytz/zoneinfo/America/Grenada,sha256=hJHlV_-AGoMGUWuMpZRv9fLmghrzFHfrR9fRkcxaZJc,246
pytz/zoneinfo/America/Guadeloupe,sha256=hJHlV_-AGoMGUWuMpZRv9fLmghrzFHfrR9fRkcxaZJc,246
pytz/zoneinfo/America/Guatemala,sha256=dugUgCd6QY52yHkHuUP4jRWzo5x439IQigaYCvEF46Q,280
pytz/zoneinfo/America/Guayaquil,sha256=j2UuIo-4RgSOlTNfu77mhZ92waNTeKFSvmoVemJooT0,232
pytz/zoneinfo/America/Guyana,sha256=R0bOvCRDC8SRIexmhsduPdHbbRPwI2GviD9otExiUrk,248
pytz/zoneinfo/America/Halifax,sha256=TZpmc5PwWoLfTfQoQ_b3U17BE2iVKSeNkR0Ho8mbTn8,3424
pytz/zoneinfo/America/Havana,sha256=HUQeAuKBsEkI5SLZjqynXICOUVOajkKzKH5r-Ov5Odc,2416
pytz/zoneinfo/America/Hermosillo,sha256=WnlVBpVBG8ONnz0wpxteXmuvSzOGwSlAisvDd1GtKYA,456
pytz/zoneinfo/America/Indiana/Indianapolis,sha256=kNKy9Kj9ICsiYYfCCbAggzMA7exf-GpGPMxoXocHUyw,1682
pytz/zoneinfo/America/Indiana/Knox,sha256=CsvZ5BKw2qVav3x_F8CU9taJdDk7jX41Cfsqms6jXV8,2444
pytz/zoneinfo/America/Indiana/Marengo,sha256=f3tQ-lgMSUA7nvn64pXhKtJL7mWzGajoCega5MEJSbI,1738
pytz/zoneinfo/America/Indiana/Petersburg,sha256=A88OHuM0Rg3iMLHjKgXq_d2jZCdVSytUQs-9W0KcFyQ,1920
pytz/zoneinfo/America/Indiana/Tell_City,sha256=4dWqAr9Y2BXfL4pAQk-81c3gGl2cNdHXOD7_wJhhhn8,1700
pytz/zoneinfo/America/Indiana/Vevay,sha256=H7VR2G-_sD_C5Rm4P3g1iRC1FWCPg4m0MGD3P1PLzsk,1430
pytz/zoneinfo/America/Indiana/Vincennes,sha256=62mAxT7APFCaoygflnEzdOpe-fuW1yObI6m6EUUcS7A,1710
pytz/zoneinfo/America/Indiana/Winamac,sha256=aZGM2jR8CH9BHSUq7XygiweDd6dorXLPXg246XsbR6s,1794
pytz/zoneinfo/America/Indianapolis,sha256=kNKy9Kj9ICsiYYfCCbAggzMA7exf-GpGPMxoXocHUyw,1682
pytz/zoneinfo/America/Inuvik,sha256=6J-mapDnrk9A1LtswoE34tqSy_ufedcEBNxixkrEjIo,2074
pytz/zoneinfo/America/Iqaluit,sha256=feOnxAN0N0r-M1qlkrA4JMyawoc0tqae0iiBCPDAs4k,2202
pytz/zoneinfo/America/Jamaica,sha256=wlagieUPRf5-beie-h7QsONbNzjGsm8vMs8uf28pw28,482
pytz/zoneinfo/America/Jujuy,sha256=PGmAehypCxj0XCenCSWqylDIPbKLK0DlrwJK_24D590,1034
pytz/zoneinfo/America/Juneau,sha256=k7hxb0aGRnfnE-DBi3LkcjAzRPyAf0_Hw0vVFfjGeb0,2353
pytz/zoneinfo/America/Kentucky/Louisville,sha256=tP072xV_n_vIQjxxcJ77AGeGj6yL1KPpn3fwids9g1U,2788
pytz/zoneinfo/America/Kentucky/Monticello,sha256=LtdyCo85BrXQs6rlH61Ym-8KqWHH6PwAOjD0QxhIdzM,2368
pytz/zoneinfo/America/Knox_IN,sha256=CsvZ5BKw2qVav3x_F8CU9taJdDk7jX41Cfsqms6jXV8,2444
pytz/zoneinfo/America/Kralendijk,sha256=hJHlV_-AGoMGUWuMpZRv9fLmghrzFHfrR9fRkcxaZJc,246
pytz/zoneinfo/America/La_Paz,sha256=hqfD8LQHupdZhji2e93_9pOQAT-R7muzzjP0nyfbFXY,218
pytz/zoneinfo/America/Lima,sha256=HHgTnDUnCZzibvL0MrG8qyOuvjmYYw3e3R5VbnxMZs8,392
pytz/zoneinfo/America/Los_Angeles,sha256=aJd7ua1tGG_vxser02AQpm4wAI3LLTdgh6QcSYYecmg,2852
pytz/zoneinfo/America/Louisville,sha256=tP072xV_n_vIQjxxcJ77AGeGj6yL1KPpn3fwids9g1U,2788
pytz/zoneinfo/America/Lower_Princes,sha256=hJHlV_-AGoMGUWuMpZRv9fLmghrzFHfrR9fRkcxaZJc,246
pytz/zoneinfo/America/Maceio,sha256=3R5DlSe32kQDmoSVIWpcyk2o7qohr-rliwqDSGFIMyQ,730
pytz/zoneinfo/America/Managua,sha256=xBzF01AHn2E2fD8Qdy-DHFe36UqoeNpKPfChduBKWdk,430
pytz/zoneinfo/America/Manaus,sha256=F6RLOOeOi9lymZiQmQ9pR8tFpPZ6EguNdPfOc6BhXDE,590
pytz/zoneinfo/America/Marigot,sha256=hJHlV_-AGoMGUWuMpZRv9fLmghrzFHfrR9fRkcxaZJc,246
pytz/zoneinfo/America/Martinique,sha256=fMs80kOU2YFvC0f9y2eje97JeAtTYBamXrnlTunNLzQ,232
pytz/zoneinfo/America/Matamoros,sha256=fq-PqdmZrQ98UsFmHA9ivjBZv5GEBRTOuLQ5Cu5ajW8,1418
pytz/zoneinfo/America/Mazatlan,sha256=RQQVwlEVHRp2X-c_0hJ46y54abTlqUuLkyrUUicyc5g,1128
pytz/zoneinfo/America/Mendoza,sha256=xcOVtvRyVYFAU90y2QYwpyQhpMLyAp7-Fxvku4kgl0c,1062
pytz/zoneinfo/America/Menominee,sha256=Arv9WLbfhNcpRsUjHDU757BEdwlp08Gt30AixG3gZ04,2274
pytz/zoneinfo/America/Merida,sha256=ORJCGiO2mXG-kk5ZZGro1MNuKqRnJx6HJlvoezTMM90,1004
pytz/zoneinfo/America/Metlakatla,sha256=twmieGTVY2V-U8nFxqvx7asYv8GVjeWdLtrOI7UApVI,1423
pytz/zoneinfo/America/Mexico_City,sha256=A5MlfDUZ4O1-jMTRt0WPem7qqcW0Nrslls1hlc8C4-Q,1222
pytz/zoneinfo/America/Miquelon,sha256=l5txBJYe9HTRZlILcbSL_HNDYrjUb0ouecNy7QEkg9c,1652
pytz/zoneinfo/America/Moncton,sha256=Wmv-bk9aKKcWWzOpc1UFu67HOfwaIk2Wmh3LgqGctys,3154
pytz/zoneinfo/America/Monterrey,sha256=vKBLVjG0bNVDI07M4WwOVv2KbrYJVNTLmc19iM2CvTU,980
pytz/zoneinfo/America/Montevideo,sha256=dQEBE4mjZPtyRjKXK6Z-bMHJdFqpwhIzxDH4x04rKYk,1496
pytz/zoneinfo/America/Montreal,sha256=pYehoWB0Ofe6woPhgV8r26-5ZJpFPRjgbC5E5pltiI8,3494
pytz/zoneinfo/America/Montserrat,sha256=hJHlV_-AGoMGUWuMpZRv9fLmghrzFHfrR9fRkcxaZJc,246
pytz/zoneinfo/America/Nassau,sha256=pYehoWB0Ofe6woPhgV8r26-5ZJpFPRjgbC5E5pltiI8,3494
pytz/zoneinfo/America/New_York,sha256=6e0H177gx2qdRC0JHvHwFmj-58TyYBTAqGixn-bBipU,3552
pytz/zoneinfo/America/Nipigon,sha256=pYehoWB0Ofe6woPhgV8r26-5ZJpFPRjgbC5E5pltiI8,3494
pytz/zoneinfo/America/Nome,sha256=2izM3-P-PqJ9za6MdhzFfMvPFNq7Gim69tAvEwPeY2s,2367
pytz/zoneinfo/America/Noronha,sha256=feeRAijQqKylZgqe84nKhsFLycT5zIBm7mLIvdyGw4w,702
pytz/zoneinfo/America/North_Dakota/Beulah,sha256=qtgbqNu8M3AkHF2n-_oSps1pYT4SxgclbkkPKbXaBHs,2396
pytz/zoneinfo/America/North_Dakota/Center,sha256=9ZWbK9YKkquULyBUFS3Lr_idxbt7V7y4W4EO0Kn20sw,2396
pytz/zoneinfo/America/North_Dakota/New_Salem,sha256=DH_bsQfuUnK2obdb06KgisO4XLqht12BXdrgUsZZveg,2396
pytz/zoneinfo/America/Nuuk,sha256=KGXrMN-YkYpVCgLdpcfwMFQ77EsRAGsjUCG3yAUvVfw,1889
pytz/zoneinfo/America/Ojinaga,sha256=9catgEQ2SD7qfuvTMxs15Cdd9SKaUy-svEzPBFw2Q3Q,1524
pytz/zoneinfo/America/Panama,sha256=kayA_pdpMcSQ0FjIzotdcf-m1JYfbKE-qcFT8LC8zqA,182
pytz/zoneinfo/America/Pangnirtung,sha256=feOnxAN0N0r-M1qlkrA4JMyawoc0tqae0iiBCPDAs4k,2202
pytz/zoneinfo/America/Paramaribo,sha256=Z7UZvNlgd-qEUHjEPYXIkLNTgjMcCzk9EfUUEmUyd7M,248
pytz/zoneinfo/America/Phoenix,sha256=illz0sYuLL8lIPK0Tkou6dL0Vck_D0W_3rRTOvFYRmQ,360
pytz/zoneinfo/America/Port-au-Prince,sha256=09ZAJd4IOiMpfdpUuF1U44R_hRt6BvpAkFXOnYO9yOM,1434
pytz/zoneinfo/America/Port_of_Spain,sha256=hJHlV_-AGoMGUWuMpZRv9fLmghrzFHfrR9fRkcxaZJc,246
pytz/zoneinfo/America/Porto_Acre,sha256=0gpJUl46hQbp0P6Xj1S0NArIWeAryuuDXjsldvB5GHE,614
pytz/zoneinfo/America/Porto_Velho,sha256=uSMV2hZWj-VyBhFBwC950wcThfN3jq6KlycESmQTLOA,562
pytz/zoneinfo/America/Puerto_Rico,sha256=hJHlV_-AGoMGUWuMpZRv9fLmghrzFHfrR9fRkcxaZJc,246
pytz/zoneinfo/America/Punta_Arenas,sha256=tR5uIf1351AWFqrqNtmXnhQWnKREmJaZqKBzaWRVMTQ,1902
pytz/zoneinfo/America/Rainy_River,sha256=7P-_YQrneFcon7QKSTOnkiGjEppFDn3Z48MJ1qq8VBw,2868
pytz/zoneinfo/America/Rankin_Inlet,sha256=nXgqjL3O2BV0em-Xk8qVRRZb_X0yQmHE6vmSSvI9Kzc,2066
pytz/zoneinfo/America/Recife,sha256=bJ_HE0-JFio4-owpZ0pLO8U3ai0fiGu8QHL0DexLiLc,702
pytz/zoneinfo/America/Regina,sha256=yjqT08pHbICYe83H8JmtaDBvCFqRv7Tfze3Y8xuXukw,980
pytz/zoneinfo/America/Resolute,sha256=CnMU2dBI-63vt8-J0Q1Ropx-8b9pRCLjhvrycMIedGg,2066
pytz/zoneinfo/America/Rio_Branco,sha256=0gpJUl46hQbp0P6Xj1S0NArIWeAryuuDXjsldvB5GHE,614
pytz/zoneinfo/America/Rosario,sha256=uniNihhMHnr4XK4WpwiPUnrAT0YPmvzqB6f0hRLtXvY,1062
pytz/zoneinfo/America/Santa_Isabel,sha256=57-Q9LSTNuTidz-lOTwDysmlCoeFUXSecvVVqNWburQ,2374
pytz/zoneinfo/America/Santarem,sha256=VmZP9S5pPucFxyqAOV908EmWXQZvgCgWLmlJJTUl0LE,588
pytz/zoneinfo/America/Santiago,sha256=0CDw13dCMUsoquMupoJgupkzAUNhDK6E0lVxURA7osA,2515
pytz/zoneinfo/America/Santo_Domingo,sha256=DKtaEj8fQ92ybITTWU4Bm160S9pzJmUVbjaWRnenxU4,458
pytz/zoneinfo/America/Sao_Paulo,sha256=BMBnRO4_4HjvO4t3njjrMGZr-ZPmegkvyvL8KPY6ZM4,1430
pytz/zoneinfo/America/Scoresbysund,sha256=K-qkiMCCFgOe8ccPMABA-lDjc9vb6wpluBOCVfiBdLI,1935
pytz/zoneinfo/America/Shiprock,sha256=MugZwApDs8NI9TnXANQlUE8guNBowWQY0m-ptpPndck,2460
pytz/zoneinfo/America/Sitka,sha256=aiS7Fk37hZpzZ9VkeJQeF-BqTLRC1QOTCgMAJwT8UxA,2329
pytz/zoneinfo/America/St_Barthelemy,sha256=hJHlV_-AGoMGUWuMpZRv9fLmghrzFHfrR9fRkcxaZJc,246
pytz/zoneinfo/America/St_Johns,sha256=r1-17uKv27eZ3JsVkw_DLZQbo6wvjuuVu7C2pDsmOgI,3655
pytz/zoneinfo/America/St_Kitts,sha256=hJHlV_-AGoMGUWuMpZRv9fLmghrzFHfrR9fRkcxaZJc,246
pytz/zoneinfo/America/St_Lucia,sha256=hJHlV_-AGoMGUWuMpZRv9fLmghrzFHfrR9fRkcxaZJc,246
pytz/zoneinfo/America/St_Thomas,sha256=hJHlV_-AGoMGUWuMpZRv9fLmghrzFHfrR9fRkcxaZJc,246
pytz/zoneinfo/America/St_Vincent,sha256=hJHlV_-AGoMGUWuMpZRv9fLmghrzFHfrR9fRkcxaZJc,246
pytz/zoneinfo/America/Swift_Current,sha256=RRKOF7vZC8VvYxD8PP4J1_hUPayKBP7Lu80avRkfPDY,560
pytz/zoneinfo/America/Tegucigalpa,sha256=EzOz7ntTlreMq69JZ2CcAb8Ps98V9bUMN480tpPIyw4,252
pytz/zoneinfo/America/Thule,sha256=8xuPRaZU8RgO5ECqFYHYmnHioc81sBOailkVu8Y02i8,1502
pytz/zoneinfo/America/Thunder_Bay,sha256=pYehoWB0Ofe6woPhgV8r26-5ZJpFPRjgbC5E5pltiI8,3494
pytz/zoneinfo/America/Tijuana,sha256=57-Q9LSTNuTidz-lOTwDysmlCoeFUXSecvVVqNWburQ,2374
pytz/zoneinfo/America/Toronto,sha256=pYehoWB0Ofe6woPhgV8r26-5ZJpFPRjgbC5E5pltiI8,3494
pytz/zoneinfo/America/Tortola,sha256=hJHlV_-AGoMGUWuMpZRv9fLmghrzFHfrR9fRkcxaZJc,246
pytz/zoneinfo/America/Vancouver,sha256=sknKH0jSPWam-DHfM35qXs8Nam7d5TFlkUI9Sgxryyg,2892
pytz/zoneinfo/America/Virgin,sha256=hJHlV_-AGoMGUWuMpZRv9fLmghrzFHfrR9fRkcxaZJc,246
pytz/zoneinfo/America/Whitehorse,sha256=TrR6PCnYG-mSClBMohqlP8qnYhXMUsydI-L-quXFxyM,1614
pytz/zoneinfo/America/Winnipeg,sha256=7P-_YQrneFcon7QKSTOnkiGjEppFDn3Z48MJ1qq8VBw,2868
pytz/zoneinfo/America/Yakutat,sha256=tFwnKbvwhyyn4LNTAn5ye_JWDdxjCerNDt7oOwUwO2M,2305
pytz/zoneinfo/America/Yellowknife,sha256=-TkIfc3QlvaCf0p8COZ43Y1HRBAl-nARUi-JdXeK1vE,2332
pytz/zoneinfo/Antarctica/Casey,sha256=VeaLOxTfDyjfGXq5Ul95JEIMXNWHSW-0N3yOoS7VK-c,423
pytz/zoneinfo/Antarctica/Davis,sha256=XB12dEq0Q-3XkzBNTNC7G1fzH-WxxctIuZqI3zp8ypI,283
pytz/zoneinfo/Antarctica/DumontDUrville,sha256=nB36HBWZTdh3TlP0DLFNz1KRQ0aHIfHbp7LC4Urp9fA,172
pytz/zoneinfo/Antarctica/Macquarie,sha256=ie7RlaU8RHTorVVj-MX8StKMqx_oXf4UH2PUqpzcwe0,2260
pytz/zoneinfo/Antarctica/Mawson,sha256=EjIFbqRdr2ZJBaI1XvoWRptnnW1LFrlhydxDDuIQjSI,185
pytz/zoneinfo/Antarctica/McMurdo,sha256=gADjoyPo_QISQU6UJrAgcHp3HDaMoOFRdH-d23uBSyc,2437
pytz/zoneinfo/Antarctica/Palmer,sha256=HTZY0M8td7oUx5REPgRCHuqKg5V3fjJEi4lYBNL4Etg,1404
pytz/zoneinfo/Antarctica/Rothera,sha256=_9NY-f8vkozQYrjbUHP5YjcICg0-LuyA9PnIeK123RU,150
pytz/zoneinfo/Antarctica/South_Pole,sha256=gADjoyPo_QISQU6UJrAgcHp3HDaMoOFRdH-d23uBSyc,2437
pytz/zoneinfo/Antarctica/Syowa,sha256=oCKH7uafN8R1o-ijXGoT5U1JZxwvoLzJu_2Cqyi2hUM,151
pytz/zoneinfo/Antarctica/Troll,sha256=fjcYppwr1FnjEssee-RLgGOANzoUyfjse-RGK46PR2E,1148
pytz/zoneinfo/Antarctica/Vostok,sha256=KfftwdzK6PkMDz0d-D3z4HKIBgY9KqsqHnTnqsPMrUg,213
pytz/zoneinfo/Arctic/Longyearbyen,sha256=XuR19xoPwaMvrrhJ-MOcbnqmbW1B7HQrl7OnQ2s7BwE,2298
pytz/zoneinfo/Asia/Aden,sha256=oCKH7uafN8R1o-ijXGoT5U1JZxwvoLzJu_2Cqyi2hUM,151
pytz/zoneinfo/Asia/Almaty,sha256=lPLWXk2f1mWYRQZFkIrq_5HkhocsUBis0M-yhdDHcBQ,983
pytz/zoneinfo/Asia/Amman,sha256=Qv4cXXw7KBQWE882cgj0kjQ3wh1vpV1orJ2v2Jjxr2U,1433
pytz/zoneinfo/Asia/Anadyr,sha256=WqKnHo5IHSWZ08d2sS5ytHtv0MQMoczP3W9zbDDrbYU,1174
pytz/zoneinfo/Asia/Aqtau,sha256=4n654FZtDssXSfhQszjZG5OmtbE2zo1KbiWcYrFJg00,969
pytz/zoneinfo/Asia/Aqtobe,sha256=1oFHTb-ybcTqLXm0r1ZOVgdYMTHlGoNs-Pgvux50d3E,997
pytz/zoneinfo/Asia/Ashgabat,sha256=-sfGnRumio7_Bs8w9YH4xRDWgjB3wBeW7c0C56Qqk64,605
pytz/zoneinfo/Asia/Ashkhabad,sha256=-sfGnRumio7_Bs8w9YH4xRDWgjB3wBeW7c0C56Qqk64,605
pytz/zoneinfo/Asia/Atyrau,sha256=_U8COUIE9nG_HKddZE1Q0sPuz3rMwfjwmfnVDY_vSmg,977
pytz/zoneinfo/Asia/Baghdad,sha256=S-plKI4zCLqI0idGABEk3oRTazNyrIj2T98-EtWtZD8,969
pytz/zoneinfo/Asia/Bahrain,sha256=wklGY3WPGp-z1OUwb_KOHzRTwBndt1RfDg9Uttt36G4,185
pytz/zoneinfo/Asia/Baku,sha256=6_hq98SGG0j0JA8qYx96WcIMZSLW4w460QXh_OM_ccg,1213
pytz/zoneinfo/Asia/Bangkok,sha256=hf_5PVegQcFSS60CjS80C7h-TGOrfQ4ncm83N8VmZkk,185
pytz/zoneinfo/Asia/Barnaul,sha256=3zeUimLTMrIZE0vX6XHFvB3MoqExoVbE5CSm6GV0zf0,1207
pytz/zoneinfo/Asia/Beirut,sha256=_Z_2ZAg_iL9vU51JDB8CB04uXBDrf1kLIis-JnXaS2o,2154
pytz/zoneinfo/Asia/Bishkek,sha256=IOoUyjABILCkXu1rjCIqSwAufRYFklc5YAC4jdhVw6Q,969
pytz/zoneinfo/Asia/Brunei,sha256=D5qtyWJ_SM8bTQeJJIYhqqojxlVKbrFC1EYMDU9GzXQ,469
pytz/zoneinfo/Asia/Calcutta,sha256=6Qw0EDbLcgMgDik8s7UTJn4QSjmllPNeGVJU5rwKF88,285
pytz/zoneinfo/Asia/Chita,sha256=LbSlS23swFkANUScg8zkNR0imANWNfOIaYd39HbLdIQ,1207
pytz/zoneinfo/Asia/Choibalsan,sha256=atm7FmPwZGsftLM7vS1LltjcdaDC-DSg1cIdP2MF17I,935
pytz/zoneinfo/Asia/Chongqing,sha256=ZP_C5DqUQ1oEPAQNHTr36S0DGtx453N68YYbqk7u8-Y,561
pytz/zoneinfo/Asia/Chungking,sha256=ZP_C5DqUQ1oEPAQNHTr36S0DGtx453N68YYbqk7u8-Y,561
pytz/zoneinfo/Asia/Colombo,sha256=w52L7bgT4m5hcgRuevIPY83xytfkBmkLhnKMwp16KsY,358
pytz/zoneinfo/Asia/Dacca,sha256=-xulJ2KVhvKp6rlZLMydpw7oXVirk-riEH-181xPE54,323
pytz/zoneinfo/Asia/Damascus,sha256=EthGheaHWmy5IrLCc9NmM3jvASQFHt8TsBF07I1tgbg,1873
pytz/zoneinfo/Asia/Dhaka,sha256=-xulJ2KVhvKp6rlZLMydpw7oXVirk-riEH-181xPE54,323
pytz/zoneinfo/Asia/Dili,sha256=0mUs0Utk-uW9deZV3cBUTpfWMgFvl0DyN29JuKvKMyw,213
pytz/zoneinfo/Asia/Dubai,sha256=pmdhPhaJRwKwONvxiZNGeFSICjlWzyY9JlFHv-H9upY,151
pytz/zoneinfo/Asia/Dushanbe,sha256=koYnnYWuFsBXd1vJfZsGdpwnbFHEwvkGBmSrrx3KIss,577
pytz/zoneinfo/Asia/Famagusta,sha256=CFrcygd8ude5x6OEtfM_Dw0KYHoxpPPzq46KoHVxjjc,2028
pytz/zoneinfo/Asia/Gaza,sha256=t0YxcUQL53VNKnKbKijn0OE_MaryEynonabse-iTtzs,3844
pytz/zoneinfo/Asia/Harbin,sha256=ZP_C5DqUQ1oEPAQNHTr36S0DGtx453N68YYbqk7u8-Y,561
pytz/zoneinfo/Asia/Hebron,sha256=6Y0USHKx-xoCxCr_WpCuM3olP1vUGnzrcnGiyQFcqdQ,3872
pytz/zoneinfo/Asia/Ho_Chi_Minh,sha256=Lnv1vpUNAXBo8v0b9d9AQpy-AEyO5Qa2Ig0PvDkjrmU,337
pytz/zoneinfo/Asia/Hong_Kong,sha256=al_O4kPlq5JpgkLYjEaZzrcgiiLul9NC0R5B69JVWhc,1233
pytz/zoneinfo/Asia/Hovd,sha256=Zn4PLGlD-URJDsbChor5bqWTzuAil2tbrGJW0j5TLbs,877
pytz/zoneinfo/Asia/Irkutsk,sha256=IVuoXCwdeI-KIUfFkEt6yBjqYP3V9GTrF-_WLnffFzk,1229
pytz/zoneinfo/Asia/Istanbul,sha256=Jk4wjndDta_uLWc8W1dWdjbavJJbsL5ROTmZboVnGKU,1933
pytz/zoneinfo/Asia/Jakarta,sha256=TvEzBvSzfzFCdOsMAZ0QgR95JA5xf3kAZONhy5gEXRE,383
pytz/zoneinfo/Asia/Jayapura,sha256=ihzUd-L8HUVqG-Na10MyPE-YYwjVFj-xerqjTN4EJZs,221
pytz/zoneinfo/Asia/Jerusalem,sha256=JUuWQmW5Tha0pJjw61Q5aN7CX0z4D7ops9OOSnda6Dc,2388
pytz/zoneinfo/Asia/Kabul,sha256=JZEbo8bSj_L7HnXUm2gAUlNlCvJlRJhFkSHCg5o3ggk,194
pytz/zoneinfo/Asia/Kamchatka,sha256=KY1PlJvRSNkY_5hyJBxj5DDweeYVQaBK05ZgL3kdcCY,1152
pytz/zoneinfo/Asia/Karachi,sha256=iB-mWMTXUyfBwAkZdz8_UmEw0xsgxIub-KNI7akzhkk,379
pytz/zoneinfo/Asia/Kashgar,sha256=F1ZOdZZDsVHwDJinksR-hjcqPzqOljvdreZIWFulJxY,151
pytz/zoneinfo/Asia/Kathmandu,sha256=_RsfeSWbCr8kM4YRJi7Xv6hAEiHW14IFhsXsfhbPjoM,198
pytz/zoneinfo/Asia/Katmandu,sha256=_RsfeSWbCr8kM4YRJi7Xv6hAEiHW14IFhsXsfhbPjoM,198
pytz/zoneinfo/Asia/Khandyga,sha256=bKfmw6k5qYDQsEHG3Mv-VYis3YhCeV7qijDxfxQNn_g,1257
pytz/zoneinfo/Asia/Kolkata,sha256=6Qw0EDbLcgMgDik8s7UTJn4QSjmllPNeGVJU5rwKF88,285
pytz/zoneinfo/Asia/Krasnoyarsk,sha256=D5KE_1wWSD2YdixDy8n3LBNaAlE1_y3TWXw6NrxFKKA,1193
pytz/zoneinfo/Asia/Kuala_Lumpur,sha256=XmeVImeqcJ8hJzm7TjAti1nWJAxawOqq7jIzDnHX2hI,401
pytz/zoneinfo/Asia/Kuching,sha256=D5qtyWJ_SM8bTQeJJIYhqqojxlVKbrFC1EYMDU9GzXQ,469
pytz/zoneinfo/Asia/Kuwait,sha256=oCKH7uafN8R1o-ijXGoT5U1JZxwvoLzJu_2Cqyi2hUM,151
pytz/zoneinfo/Asia/Macao,sha256=MvAkRyRsrA2r052ItlyF5bh2FheRjI0jPwg0uIiH2Yk,1227
pytz/zoneinfo/Asia/Macau,sha256=MvAkRyRsrA2r052ItlyF5bh2FheRjI0jPwg0uIiH2Yk,1227
pytz/zoneinfo/Asia/Magadan,sha256=HccEEXBQvMmLoC_JE-zP_MlLAZ1WmNLQLfM3tJt55M4,1208
pytz/zoneinfo/Asia/Makassar,sha256=OhJtCqSTEU-u5n0opBVO5Bu-wQzcYPy9S_6aAhJXgOw,254
pytz/zoneinfo/Asia/Manila,sha256=ujfq0kl1EhxcYSOrG-FS750aNaYUt1TT4bFuK4EcL_c,328
pytz/zoneinfo/Asia/Muscat,sha256=pmdhPhaJRwKwONvxiZNGeFSICjlWzyY9JlFHv-H9upY,151
pytz/zoneinfo/Asia/Nicosia,sha256=0Unm0IFT7HyGeQ7F3vTa_-klfysCgrulqFO6BD1plZU,2002
pytz/zoneinfo/Asia/Novokuznetsk,sha256=pyxxtSUtYDeVmFk0Cg-F33laZS0iKtde9_GJnL9f0KM,1151
pytz/zoneinfo/Asia/Novosibirsk,sha256=5K2-Gx15ThlHfolyW85S5zREtAcMjeHBYWK4E8x2LdY,1207
pytz/zoneinfo/Asia/Omsk,sha256=HyXIWItJXBKVHUzWcQPi1Mmd6ZLmZk-QhRUo9Kv2XOI,1193
pytz/zoneinfo/Asia/Oral,sha256=WQT4qRmC9RI_ll8zB9FvkAL8ezGb8qoqWd75GTlC7kQ,991
pytz/zoneinfo/Asia/Phnom_Penh,sha256=hf_5PVegQcFSS60CjS80C7h-TGOrfQ4ncm83N8VmZkk,185
pytz/zoneinfo/Asia/Pontianak,sha256=inOXwuKtjKv1z_eliPZSIqjSt6whtuxhPeG1YpjU_BQ,353
pytz/zoneinfo/Asia/Pyongyang,sha256=_-g3GnDAtfDX4XAktXH9jFouLUDmOovnjoOfvRpUDsE,237
pytz/zoneinfo/Asia/Qatar,sha256=wklGY3WPGp-z1OUwb_KOHzRTwBndt1RfDg9Uttt36G4,185
pytz/zoneinfo/Asia/Qostanay,sha256=HIjln8QIPNRU6MkWzyPi6vDrjlmVZ4XzFxcUHtXMi7s,1025
pytz/zoneinfo/Asia/Qyzylorda,sha256=JZLNN6NuLkqaWEeVaCZiW_gL6BrIFL9lr65iK7myVPg,1011
pytz/zoneinfo/Asia/Rangoon,sha256=_YHASq4Z5YcUILIdhEzg27CGLzarUHPDHs1Dj0QgNGM,254
pytz/zoneinfo/Asia/Riyadh,sha256=oCKH7uafN8R1o-ijXGoT5U1JZxwvoLzJu_2Cqyi2hUM,151
pytz/zoneinfo/Asia/Saigon,sha256=Lnv1vpUNAXBo8v0b9d9AQpy-AEyO5Qa2Ig0PvDkjrmU,337
pytz/zoneinfo/Asia/Sakhalin,sha256=xzAor82ihAe-yXEwC6OWiMzo9b6Z-oQl39NIkU5Hhbs,1188
pytz/zoneinfo/Asia/Samarkand,sha256=zJKSRt3lEvd6Qvg9b49QAyO4cTJyVnTKyPYcyudpHxk,563
pytz/zoneinfo/Asia/Seoul,sha256=LI9LsV3XcJC0l-KoQf8zI-y7rk-du57erS-N2Ptdi7Q,617
pytz/zoneinfo/Asia/Shanghai,sha256=ZP_C5DqUQ1oEPAQNHTr36S0DGtx453N68YYbqk7u8-Y,561
pytz/zoneinfo/Asia/Singapore,sha256=XmeVImeqcJ8hJzm7TjAti1nWJAxawOqq7jIzDnHX2hI,401
pytz/zoneinfo/Asia/Srednekolymsk,sha256=efaaT8iFHrcccp-VZKNMvtTuPLNjG5V9JH5KKHhH3SI,1194
pytz/zoneinfo/Asia/Taipei,sha256=DMmQwOpPql25ue3Nf8vAKKT4em06D1Z9rHbLIitxixk,761
pytz/zoneinfo/Asia/Tashkent,sha256=apRPy251fSRy_ixsg3BOZNmUbHdO86P5-PdgC1Xws7U,577
pytz/zoneinfo/Asia/Tbilisi,sha256=zQ-2bVq5_USUSbwN6q0qvWjD-HXkKaH4ifMVq1lEeIM,1021
pytz/zoneinfo/Asia/Tehran,sha256=LQMch2TMA4wI23SQzoIrlZh0_KceXQegurwxCZ5YDlY,1248
pytz/zoneinfo/Asia/Tel_Aviv,sha256=JUuWQmW5Tha0pJjw61Q5aN7CX0z4D7ops9OOSnda6Dc,2388
pytz/zoneinfo/Asia/Thimbu,sha256=G2nTQVEMmKlWt0B74_fUAL7KQ3YAu__J6HciiYs2IyU,189
pytz/zoneinfo/Asia/Thimphu,sha256=G2nTQVEMmKlWt0B74_fUAL7KQ3YAu__J6HciiYs2IyU,189
pytz/zoneinfo/Asia/Tokyo,sha256=oCueZgRNxcNcX3ZGdif9y6Su4cyVhga4XHdwlcrYLOs,309
pytz/zoneinfo/Asia/Tomsk,sha256=cr0ULZgWBnQfzDiJeYmqpA7Xo5QRzurvrHsrbZsnhOQ,1207
pytz/zoneinfo/Asia/Ujung_Pandang,sha256=OhJtCqSTEU-u5n0opBVO5Bu-wQzcYPy9S_6aAhJXgOw,254
pytz/zoneinfo/Asia/Ulaanbaatar,sha256=qUkXRsTc_u7B90JxULSu7yzKbGtGfKcfEFIasGPC2ec,877
pytz/zoneinfo/Asia/Ulan_Bator,sha256=qUkXRsTc_u7B90JxULSu7yzKbGtGfKcfEFIasGPC2ec,877
pytz/zoneinfo/Asia/Urumqi,sha256=F1ZOdZZDsVHwDJinksR-hjcqPzqOljvdreZIWFulJxY,151
pytz/zoneinfo/Asia/Ust-Nera,sha256=zsG8kgnw0Fcs5N2WwNTVmvWkTlpwf7Oo8y68HcXjYyw,1238
pytz/zoneinfo/Asia/Vientiane,sha256=hf_5PVegQcFSS60CjS80C7h-TGOrfQ4ncm83N8VmZkk,185
pytz/zoneinfo/Asia/Vladivostok,sha256=XMQLMh5SPbI6C4R3UO4KhbnG4hWVkHNedzCQeqxFk6A,1194
pytz/zoneinfo/Asia/Yakutsk,sha256=PPNrRGgg9jefOUM-6M8XqaIm-ElfmRZSWAtSGKLzNXQ,1193
pytz/zoneinfo/Asia/Yangon,sha256=_YHASq4Z5YcUILIdhEzg27CGLzarUHPDHs1Dj0QgNGM,254
pytz/zoneinfo/Asia/Yekaterinburg,sha256=4NyEW6Xjr4UsWPh63HIPI4G6GT_tVG1Xkgc2xbwGjzA,1229
pytz/zoneinfo/Asia/Yerevan,sha256=FM0pUA4NbTWBb_CsJ5KCLVrLoNmad7njBKqFrJBDoxE,1137
pytz/zoneinfo/Atlantic/Azores,sha256=NyNrE2YIwL9yVddpECcYWwci5JzrfjxiIXP7RP0MrL8,3498
pytz/zoneinfo/Atlantic/Bermuda,sha256=LNGKfMsnYvwImjTyzXrLhMOHHDu7qI67RbYNKvvI15I,2396
pytz/zoneinfo/Atlantic/Canary,sha256=ymK9ufqphvNjDK3hzikN4GfkcR3QeCBiPKyVc6FjlbA,1897
pytz/zoneinfo/Atlantic/Cape_Verde,sha256=o92pLdLFX_b9vUiq3rNpca4tupIO3dx9rNrnPcA8474,256
pytz/zoneinfo/Atlantic/Faeroe,sha256=NibdZPZtapnYR_myIZnMdTaSKGsOBGgujj0_T2NvAzs,1815
pytz/zoneinfo/Atlantic/Faroe,sha256=NibdZPZtapnYR_myIZnMdTaSKGsOBGgujj0_T2NvAzs,1815
pytz/zoneinfo/Atlantic/Jan_Mayen,sha256=XuR19xoPwaMvrrhJ-MOcbnqmbW1B7HQrl7OnQ2s7BwE,2298
pytz/zoneinfo/Atlantic/Madeira,sha256=21Zcy0xRqDN3oY8jmjjO-LI7aC3G9mcS9ytaYg0g7ik,3503
pytz/zoneinfo/Atlantic/Reykjavik,sha256=0u-sTl8j2IyV1ywdtCgHFw9S9D3ZiiBa9akqkbny2Zc,148
pytz/zoneinfo/Atlantic/South_Georgia,sha256=I9SAcPPumy6Xf9P7dg2aE16oxwDIqyKFqinJTC-XsgM,150
pytz/zoneinfo/Atlantic/St_Helena,sha256=0u-sTl8j2IyV1ywdtCgHFw9S9D3ZiiBa9akqkbny2Zc,148
pytz/zoneinfo/Atlantic/Stanley,sha256=siEjXTAuTum_4XGtS98MBE34XW_5xgXShEX5OMnSFjo,1200
pytz/zoneinfo/Australia/ACT,sha256=QsOFdYWxbbL4_9R7oZ-qYPRzNA3o1P6TIOp76GFgWQY,2190
pytz/zoneinfo/Australia/Adelaide,sha256=ld2EbxU75oVgmPe703z-I6aqLg0Kmv62ZcCGzkT5R20,2208
pytz/zoneinfo/Australia/Brisbane,sha256=eW6Qzze2t0-speJmmvt1JMzbkSadIKdE84XHc7JUtGc,419
pytz/zoneinfo/Australia/Broken_Hill,sha256=3k_3ljTvS5GSfo7Xh6w71UgR3aAwYPBsnCJ-mlEYCqQ,2229
pytz/zoneinfo/Australia/Canberra,sha256=QsOFdYWxbbL4_9R7oZ-qYPRzNA3o1P6TIOp76GFgWQY,2190
pytz/zoneinfo/Australia/Currie,sha256=GLQSzgIfsWxOvmKOrhpfofWqINQf6h36NYy3mcq6gcg,2358
pytz/zoneinfo/Australia/Darwin,sha256=fn0IZhIW98FAnzLig-_GBtW5LA54jajdeeUzg4tCGvo,325
pytz/zoneinfo/Australia/Eucla,sha256=i1-XGG8I6E0dXIdWGF4DlkfDLWhiAxJ_3gMpt-nm_u4,456
pytz/zoneinfo/Australia/Hobart,sha256=GLQSzgIfsWxOvmKOrhpfofWqINQf6h36NYy3mcq6gcg,2358
pytz/zoneinfo/Australia/LHI,sha256=oyPFQzmRqWPrSXt9pNHQmEi_PvX11k2clknziOS6ud8,1846
pytz/zoneinfo/Australia/Lindeman,sha256=xM6Udx22oLNoLR1Y7GQhHOYov8nw3xQNqgc_NVQ2JK4,475
pytz/zoneinfo/Australia/Lord_Howe,sha256=oyPFQzmRqWPrSXt9pNHQmEi_PvX11k2clknziOS6ud8,1846
pytz/zoneinfo/Australia/Melbourne,sha256=lvx_MQcunMc6u2smIrl8X427bLsXvjkgpCSdjYCTNBM,2190
pytz/zoneinfo/Australia/NSW,sha256=QsOFdYWxbbL4_9R7oZ-qYPRzNA3o1P6TIOp76GFgWQY,2190
pytz/zoneinfo/Australia/North,sha256=fn0IZhIW98FAnzLig-_GBtW5LA54jajdeeUzg4tCGvo,325
pytz/zoneinfo/Australia/Perth,sha256=Al1DOUh4U_ofMUQSeVlzSyD3x7SUjP9dchSaBUGmeWg,446
pytz/zoneinfo/Australia/Queensland,sha256=eW6Qzze2t0-speJmmvt1JMzbkSadIKdE84XHc7JUtGc,419
pytz/zoneinfo/Australia/South,sha256=ld2EbxU75oVgmPe703z-I6aqLg0Kmv62ZcCGzkT5R20,2208
pytz/zoneinfo/Australia/Sydney,sha256=QsOFdYWxbbL4_9R7oZ-qYPRzNA3o1P6TIOp76GFgWQY,2190
pytz/zoneinfo/Australia/Tasmania,sha256=GLQSzgIfsWxOvmKOrhpfofWqINQf6h36NYy3mcq6gcg,2358
pytz/zoneinfo/Australia/Victoria,sha256=lvx_MQcunMc6u2smIrl8X427bLsXvjkgpCSdjYCTNBM,2190
pytz/zoneinfo/Australia/West,sha256=Al1DOUh4U_ofMUQSeVlzSyD3x7SUjP9dchSaBUGmeWg,446
pytz/zoneinfo/Australia/Yancowinna,sha256=3k_3ljTvS5GSfo7Xh6w71UgR3aAwYPBsnCJ-mlEYCqQ,2229
pytz/zoneinfo/Brazil/Acre,sha256=0gpJUl46hQbp0P6Xj1S0NArIWeAryuuDXjsldvB5GHE,614
pytz/zoneinfo/Brazil/DeNoronha,sha256=feeRAijQqKylZgqe84nKhsFLycT5zIBm7mLIvdyGw4w,702
pytz/zoneinfo/Brazil/East,sha256=BMBnRO4_4HjvO4t3njjrMGZr-ZPmegkvyvL8KPY6ZM4,1430
pytz/zoneinfo/Brazil/West,sha256=F6RLOOeOi9lymZiQmQ9pR8tFpPZ6EguNdPfOc6BhXDE,590
pytz/zoneinfo/CET,sha256=o4omkrM_IsITxooUo8krM921XfBdvRs9JhwGXGd-Ypg,2094
pytz/zoneinfo/CST6CDT,sha256=WGbtZ1FwjRX6Jeo_TCXKsfeDs4V9uhXGJfcnLJhk3s0,2310
pytz/zoneinfo/Canada/Atlantic,sha256=TZpmc5PwWoLfTfQoQ_b3U17BE2iVKSeNkR0Ho8mbTn8,3424
pytz/zoneinfo/Canada/Central,sha256=7P-_YQrneFcon7QKSTOnkiGjEppFDn3Z48MJ1qq8VBw,2868
pytz/zoneinfo/Canada/Eastern,sha256=pYehoWB0Ofe6woPhgV8r26-5ZJpFPRjgbC5E5pltiI8,3494
pytz/zoneinfo/Canada/Mountain,sha256=-TkIfc3QlvaCf0p8COZ43Y1HRBAl-nARUi-JdXeK1vE,2332
pytz/zoneinfo/Canada/Newfoundland,sha256=r1-17uKv27eZ3JsVkw_DLZQbo6wvjuuVu7C2pDsmOgI,3655
pytz/zoneinfo/Canada/Pacific,sha256=sknKH0jSPWam-DHfM35qXs8Nam7d5TFlkUI9Sgxryyg,2892
pytz/zoneinfo/Canada/Saskatchewan,sha256=yjqT08pHbICYe83H8JmtaDBvCFqRv7Tfze3Y8xuXukw,980
pytz/zoneinfo/Canada/Yukon,sha256=TrR6PCnYG-mSClBMohqlP8qnYhXMUsydI-L-quXFxyM,1614
pytz/zoneinfo/Chile/Continental,sha256=0CDw13dCMUsoquMupoJgupkzAUNhDK6E0lVxURA7osA,2515
pytz/zoneinfo/Chile/EasterIsland,sha256=QbubBs_xQlvKweAnurhyHjIK4ji77Gh4G-usXul6XVM,2219
pytz/zoneinfo/Cuba,sha256=HUQeAuKBsEkI5SLZjqynXICOUVOajkKzKH5r-Ov5Odc,2416
pytz/zoneinfo/EET,sha256=gGVsW5-qnI7ty8vqVK1ADWhunrvAT8kUC79GUf-_7G8,1908
pytz/zoneinfo/EST,sha256=uKE_VPKfxGyYEsyqV_DdE2MW55vs_qUioOdIn5Goobc,114
pytz/zoneinfo/EST5EDT,sha256=fwzEMT1jgnY2dDjd0EqDl26_7LC-oF48Bd4ng5311H0,2310
pytz/zoneinfo/Egypt,sha256=Lft-GCLQhaSJm9VqUmsEFoHIS1Vhfa7pFJn9GZCpifs,2399
pytz/zoneinfo/Eire,sha256=QOjSocO1cihNo59vQkWxvIFPRSxE9apz0KARVx1czEM,3492
pytz/zoneinfo/Etc/GMT,sha256=bZ83iIPAefhsA4elVHqSxEmGnYBuB94QCEqwTwJJAY0,114
pytz/zoneinfo/Etc/GMT+0,sha256=bZ83iIPAefhsA4elVHqSxEmGnYBuB94QCEqwTwJJAY0,114
pytz/zoneinfo/Etc/GMT+1,sha256=1Qzl2X9rQ_RXEf11yH09wQZCr_ph6UdFP7E0yu9s-IQ,116
pytz/zoneinfo/Etc/GMT+10,sha256=JEQyQyQlkC0o6ZTdeVjZhCIOh6cK5TF7H00Pkls-sUI,117
pytz/zoneinfo/Etc/GMT+11,sha256=tWvcvYMFCaE60nJVvDrrov7stJvs1KQYOyrhl3dzcUs,117
pytz/zoneinfo/Etc/GMT+12,sha256=b70HEhErq8IJmq8x7cOZy4eR__3fq5uHHpjvPBEHqMA,117
pytz/zoneinfo/Etc/GMT+2,sha256=T6Ep5zhslBKbYaECFUB6gUKh3iTZPyMoW1kjhonxrUo,116
pytz/zoneinfo/Etc/GMT+3,sha256=QGoYrE04bUJ-OzL37dt2MZT5FxWNLpJDPVXgJbstYZA,116
pytz/zoneinfo/Etc/GMT+4,sha256=RWrkNki-wV7X-coe0VvufBe6LrWVpkPJgia5QQYEnBo,116
pytz/zoneinfo/Etc/GMT+5,sha256=oRmeC41dgYXT-zzyZIRKXN9IvdL2Da5nTuwmG2_prIA,116
pytz/zoneinfo/Etc/GMT+6,sha256=d6dAnwiejyFI2n7AzFlFW0aFAT6zYNEjBIEG0uu0sbQ,116
pytz/zoneinfo/Etc/GMT+7,sha256=TqjYbzd0YHpx1wisFg08J19wTpg6ztJLLongZY_lozs,116
pytz/zoneinfo/Etc/GMT+8,sha256=th_8bIMmYgRPCesBrbmBhRr0jQO7whd70LiY9HfwJyk,116
pytz/zoneinfo/Etc/GMT+9,sha256=Qq5E6iUS7JMJIymT7YoqlI8MtqtVy0mr9t6zWFtWc9Y,116
pytz/zoneinfo/Etc/GMT-0,sha256=bZ83iIPAefhsA4elVHqSxEmGnYBuB94QCEqwTwJJAY0,114
pytz/zoneinfo/Etc/GMT-1,sha256=73F1eU8uAQGP3mcoB2q99CjfManGFHk3fefljp9pYC4,117
pytz/zoneinfo/Etc/GMT-10,sha256=fKWWNwLBOp1OkKjtc1w9LIXJR1mTTD-JdvYflRy1IrU,118
pytz/zoneinfo/Etc/GMT-11,sha256=D2S79n6psa9t9_2vj5wIrFpHH2OJLcCKP6vtwzFZINY,118
pytz/zoneinfo/Etc/GMT-12,sha256=me4V6lmWI8gSr8H7N41WAD0Eww1anh_EF34Qr9UoSnI,118
pytz/zoneinfo/Etc/GMT-13,sha256=xbmbG1BQA6Dlpa_iUwEGyJxW4a3t6lmawdPKAE8vbR8,118
pytz/zoneinfo/Etc/GMT-14,sha256=PpXoREBh02qFpvxVMj2pV9IAzSQvBE7XPvnN9qSZ-Kc,118
pytz/zoneinfo/Etc/GMT-2,sha256=ve6hWLdeuiLhqagaWLqMD6HNybS1chRwjudfTZ2bYBE,117
pytz/zoneinfo/Etc/GMT-3,sha256=N77jILanuLDVkLsdujXZSu-dsHiwN5MIpwh7fMUifso,117
pytz/zoneinfo/Etc/GMT-4,sha256=LSko5fVHqPl5zfwjGqkbMa_OFnvtpT6o_4xYxNz9n5o,117
pytz/zoneinfo/Etc/GMT-5,sha256=uLaSR5Mb18HRTsAA5SveY9PAJ97dO8QzIWqNXe3wZb4,117
pytz/zoneinfo/Etc/GMT-6,sha256=JSN-RUAphJ50fpIv7cYC6unrtrz9S1Wma-piDHlGe7c,117
pytz/zoneinfo/Etc/GMT-7,sha256=vVAOF8xU9T9ESnw68c0SFXpcvkoopaiwTR0zbefHHSU,117
pytz/zoneinfo/Etc/GMT-8,sha256=S7xFQbFMpiDZy4v5L4D9fCrjRIzzoLC5p8Se23xi7us,117
pytz/zoneinfo/Etc/GMT-9,sha256=I5vHNmUK-Yyg_S1skFN44VGVzBgktjFgVQiDIKO4aMI,117
pytz/zoneinfo/Etc/GMT0,sha256=bZ83iIPAefhsA4elVHqSxEmGnYBuB94QCEqwTwJJAY0,114
pytz/zoneinfo/Etc/Greenwich,sha256=bZ83iIPAefhsA4elVHqSxEmGnYBuB94QCEqwTwJJAY0,114
pytz/zoneinfo/Etc/UCT,sha256=i4WEZ5GrLIpUY8g6W-PAQ-JXDXRIQ01BOYlp7Ufj5vI,114
pytz/zoneinfo/Etc/UTC,sha256=i4WEZ5GrLIpUY8g6W-PAQ-JXDXRIQ01BOYlp7Ufj5vI,114
pytz/zoneinfo/Etc/Universal,sha256=i4WEZ5GrLIpUY8g6W-PAQ-JXDXRIQ01BOYlp7Ufj5vI,114
pytz/zoneinfo/Etc/Zulu,sha256=i4WEZ5GrLIpUY8g6W-PAQ-JXDXRIQ01BOYlp7Ufj5vI,114
pytz/zoneinfo/Europe/Amsterdam,sha256=gS9Vrrbozend9HhuFetCVrIegs9fXSjaG60X2UVwysA,2933
pytz/zoneinfo/Europe/Andorra,sha256=gTB5jCQmvIw3JJi1_vAcOYuhtzPBR6RXUx9gVV6p6ug,1742
pytz/zoneinfo/Europe/Astrakhan,sha256=ZeGDZjwVVRoeR-J642zEnN26BPL58ViTJLbwnk7pLXk,1151
pytz/zoneinfo/Europe/Athens,sha256=XDY-FBUddRyQHN8GxQLZ4awjuOlWlzlUdjv7OdXFNzA,2262
pytz/zoneinfo/Europe/Belfast,sha256=yFSVBw3KQmh99qHD7ngKJ8vLgvGER1Dqb2QoM6RNKbQ,3664
pytz/zoneinfo/Europe/Belgrade,sha256=OpWtsGFWBE_S-mYoQcAmjCta9HwbGQANnSmVY9OHCTo,1920
pytz/zoneinfo/Europe/Berlin,sha256=XuR19xoPwaMvrrhJ-MOcbnqmbW1B7HQrl7OnQ2s7BwE,2298
pytz/zoneinfo/Europe/Bratislava,sha256=G9fdhUXmzx651BnyZ6V7AOYIV9EV5aMJMm44eJaLLZw,2301
pytz/zoneinfo/Europe/Brussels,sha256=gS9Vrrbozend9HhuFetCVrIegs9fXSjaG60X2UVwysA,2933
pytz/zoneinfo/Europe/Bucharest,sha256=nfg6-bU2D6DMEWb9EMIBR5kxnNsbDSx0UKfHH_ZzqFc,2184
pytz/zoneinfo/Europe/Budapest,sha256=lNwqxWciBvw9ei81VQwIKHbC_ZDJjpgHU6HFg4wCUkY,2368
pytz/zoneinfo/Europe/Busingen,sha256=K5QY7Ujj2VUchKR4bhhb0hgdAJhmwED71ykXDQOGKe8,1909
pytz/zoneinfo/Europe/Chisinau,sha256=p1J_rqFE13pL8cpBRrEFe-teCI8f0fKK4uTUy_4diF4,2390
pytz/zoneinfo/Europe/Copenhagen,sha256=XuR19xoPwaMvrrhJ-MOcbnqmbW1B7HQrl7OnQ2s7BwE,2298
pytz/zoneinfo/Europe/Dublin,sha256=QOjSocO1cihNo59vQkWxvIFPRSxE9apz0KARVx1czEM,3492
pytz/zoneinfo/Europe/Gibraltar,sha256=a87WpaBlvxI4gAU9OpQOkN8VUJbirVWYf-VfFLTIoS4,3068
pytz/zoneinfo/Europe/Guernsey,sha256=yFSVBw3KQmh99qHD7ngKJ8vLgvGER1Dqb2QoM6RNKbQ,3664
pytz/zoneinfo/Europe/Helsinki,sha256=GEkB7LsVhmegt7YuuWheCDvDGC7b7Nw9bTdDGS9qkJc,1900
pytz/zoneinfo/Europe/Isle_of_Man,sha256=yFSVBw3KQmh99qHD7ngKJ8vLgvGER1Dqb2QoM6RNKbQ,3664
pytz/zoneinfo/Europe/Istanbul,sha256=Jk4wjndDta_uLWc8W1dWdjbavJJbsL5ROTmZboVnGKU,1933
pytz/zoneinfo/Europe/Jersey,sha256=yFSVBw3KQmh99qHD7ngKJ8vLgvGER1Dqb2QoM6RNKbQ,3664
pytz/zoneinfo/Europe/Kaliningrad,sha256=s7GXSe1YvMcs7AiUhHNTA6I4nAOQn_Kmz_ZqJYO-LMM,1493
pytz/zoneinfo/Europe/Kiev,sha256=-wrpG9jPuIKFP1NgBVvnxsMRf9L_h5z3J6Q3jj1AwNM,2120
pytz/zoneinfo/Europe/Kirov,sha256=P7T2Zf5Eo6o4L4Dbg_BfiFjUgTj0dQXlrwY-QZ1eBVk,1185
pytz/zoneinfo/Europe/Kyiv,sha256=-wrpG9jPuIKFP1NgBVvnxsMRf9L_h5z3J6Q3jj1AwNM,2120
pytz/zoneinfo/Europe/Lisbon,sha256=mpUpxGexMhbOBImDLSQs5-GAk7pm7tg4qYW044Kkle0,3497
pytz/zoneinfo/Europe/Ljubljana,sha256=OpWtsGFWBE_S-mYoQcAmjCta9HwbGQANnSmVY9OHCTo,1920
pytz/zoneinfo/Europe/London,sha256=yFSVBw3KQmh99qHD7ngKJ8vLgvGER1Dqb2QoM6RNKbQ,3664
pytz/zoneinfo/Europe/Luxembourg,sha256=gS9Vrrbozend9HhuFetCVrIegs9fXSjaG60X2UVwysA,2933
pytz/zoneinfo/Europe/Madrid,sha256=mkLX03rW3t0tmzKBIPe_noUvaFDErwC6_5ZPZZsWHOo,2614
pytz/zoneinfo/Europe/Malta,sha256=EhKcbPL47765tWAiQ57cusaK2TaIQqZCgtJoEZs3Ud0,2620
pytz/zoneinfo/Europe/Mariehamn,sha256=GEkB7LsVhmegt7YuuWheCDvDGC7b7Nw9bTdDGS9qkJc,1900
pytz/zoneinfo/Europe/Minsk,sha256=KgPm0fHycntgd3xbTmmDl4O13Xh_9e2zUnd8XFSU29o,1307
pytz/zoneinfo/Europe/Monaco,sha256=q3ehSIot1GZ6TyMHIjbg0oRf4ghAXuwbSDSYVim6evg,2962
pytz/zoneinfo/Europe/Moscow,sha256=KmkofRcj6T8Ph28PJChm8JVp13uRvef6TZ0GuPzUiDw,1535
pytz/zoneinfo/Europe/Nicosia,sha256=0Unm0IFT7HyGeQ7F3vTa_-klfysCgrulqFO6BD1plZU,2002
pytz/zoneinfo/Europe/Oslo,sha256=XuR19xoPwaMvrrhJ-MOcbnqmbW1B7HQrl7OnQ2s7BwE,2298
pytz/zoneinfo/Europe/Paris,sha256=q3ehSIot1GZ6TyMHIjbg0oRf4ghAXuwbSDSYVim6evg,2962
pytz/zoneinfo/Europe/Podgorica,sha256=OpWtsGFWBE_S-mYoQcAmjCta9HwbGQANnSmVY9OHCTo,1920
pytz/zoneinfo/Europe/Prague,sha256=G9fdhUXmzx651BnyZ6V7AOYIV9EV5aMJMm44eJaLLZw,2301
pytz/zoneinfo/Europe/Riga,sha256=hJ2_0m1taW9IuA-hMyP5n-WX7YOrR0heKszJhgljRWk,2198
pytz/zoneinfo/Europe/Rome,sha256=1a3oLMSiMpSbh9QxV8hLLDVbZqash89iUO1urYC1AY8,2641
pytz/zoneinfo/Europe/Samara,sha256=nXL0IxbT6qu10CNuaDHxx4W1OaAnaaKTtIJ9N9URMoU,1201
pytz/zoneinfo/Europe/San_Marino,sha256=1a3oLMSiMpSbh9QxV8hLLDVbZqash89iUO1urYC1AY8,2641
pytz/zoneinfo/Europe/Sarajevo,sha256=OpWtsGFWBE_S-mYoQcAmjCta9HwbGQANnSmVY9OHCTo,1920
pytz/zoneinfo/Europe/Saratov,sha256=ygwjvXN13TgaWxjg6ysWEnHWNxwrVtkEbrk8t9bzVVw,1169
pytz/zoneinfo/Europe/Simferopol,sha256=tzl7xdNVSZprNCul4YE5LSpoR9JoujmOq8VbbB8wHic,1469
pytz/zoneinfo/Europe/Skopje,sha256=OpWtsGFWBE_S-mYoQcAmjCta9HwbGQANnSmVY9OHCTo,1920
pytz/zoneinfo/Europe/Sofia,sha256=hCQKXfMNrnA5xHNw_uzTjKzVw4-Bvsq5oGO4yUCv5tY,2077
pytz/zoneinfo/Europe/Stockholm,sha256=XuR19xoPwaMvrrhJ-MOcbnqmbW1B7HQrl7OnQ2s7BwE,2298
pytz/zoneinfo/Europe/Tallinn,sha256=4a6JC0aIpMzqIV7O35zoG0LLJwkQq5AoXZ2ivkic6-w,2148
pytz/zoneinfo/Europe/Tirane,sha256=ztlZyCS9WCXeVW8nBun3Tyi5HUY0EtFbiBbEc1gucuw,2084
pytz/zoneinfo/Europe/Tiraspol,sha256=p1J_rqFE13pL8cpBRrEFe-teCI8f0fKK4uTUy_4diF4,2390
pytz/zoneinfo/Europe/Ulyanovsk,sha256=c8Ad5p7CKj_1cCA7lVRpcPqbQXGYaX83cuu6uIFx-Bg,1253
pytz/zoneinfo/Europe/Uzhgorod,sha256=-wrpG9jPuIKFP1NgBVvnxsMRf9L_h5z3J6Q3jj1AwNM,2120
pytz/zoneinfo/Europe/Vaduz,sha256=K5QY7Ujj2VUchKR4bhhb0hgdAJhmwED71ykXDQOGKe8,1909
pytz/zoneinfo/Europe/Vatican,sha256=1a3oLMSiMpSbh9QxV8hLLDVbZqash89iUO1urYC1AY8,2641
pytz/zoneinfo/Europe/Vienna,sha256=ZmI3kADE6bnrJEccqh73XXBY36L1G4DkpiTQImtNrUk,2200
pytz/zoneinfo/Europe/Vilnius,sha256=UFzRX3orCTB8d9IzlxJPy5eUA2oBPuCu1UJl-2D7C3U,2162
pytz/zoneinfo/Europe/Volgograd,sha256=RgFvt7mzZ-TtIKL9BVHmoNZLIeLIuiDdXeY10g2_vks,1193
pytz/zoneinfo/Europe/Warsaw,sha256=TiLDPbeVF0ckgLVEkaSeDaKZ8wctdJDOl_HE_Wd5rKs,2654
pytz/zoneinfo/Europe/Zagreb,sha256=OpWtsGFWBE_S-mYoQcAmjCta9HwbGQANnSmVY9OHCTo,1920
pytz/zoneinfo/Europe/Zaporozhye,sha256=-wrpG9jPuIKFP1NgBVvnxsMRf9L_h5z3J6Q3jj1AwNM,2120
pytz/zoneinfo/Europe/Zurich,sha256=K5QY7Ujj2VUchKR4bhhb0hgdAJhmwED71ykXDQOGKe8,1909
pytz/zoneinfo/Factory,sha256=aFFlKx93HXoJoF4SSuTlD8cZtJA-ne5oKzAa6eX2V4k,116
pytz/zoneinfo/GB,sha256=yFSVBw3KQmh99qHD7ngKJ8vLgvGER1Dqb2QoM6RNKbQ,3664
pytz/zoneinfo/GB-Eire,sha256=yFSVBw3KQmh99qHD7ngKJ8vLgvGER1Dqb2QoM6RNKbQ,3664
pytz/zoneinfo/GMT,sha256=bZ83iIPAefhsA4elVHqSxEmGnYBuB94QCEqwTwJJAY0,114
pytz/zoneinfo/GMT+0,sha256=bZ83iIPAefhsA4elVHqSxEmGnYBuB94QCEqwTwJJAY0,114
pytz/zoneinfo/GMT-0,sha256=bZ83iIPAefhsA4elVHqSxEmGnYBuB94QCEqwTwJJAY0,114
pytz/zoneinfo/GMT0,sha256=bZ83iIPAefhsA4elVHqSxEmGnYBuB94QCEqwTwJJAY0,114
pytz/zoneinfo/Greenwich,sha256=bZ83iIPAefhsA4elVHqSxEmGnYBuB94QCEqwTwJJAY0,114
pytz/zoneinfo/HST,sha256=1YkCncvgL9Z5CmUo4Vk8VbQmgA7ZAQ0PtE37j1yOli8,115
pytz/zoneinfo/Hongkong,sha256=al_O4kPlq5JpgkLYjEaZzrcgiiLul9NC0R5B69JVWhc,1233
pytz/zoneinfo/Iceland,sha256=0u-sTl8j2IyV1ywdtCgHFw9S9D3ZiiBa9akqkbny2Zc,148
pytz/zoneinfo/Indian/Antananarivo,sha256=yJsuJTqJJqbOz37_NOS_zbf-JNr_IthHGMMN7sDqSWg,265
pytz/zoneinfo/Indian/Chagos,sha256=2errXzKdFIcpU0L-XRhSHxhNabIzbI5lXV3Pq6lt40Y,185
pytz/zoneinfo/Indian/Christmas,sha256=hf_5PVegQcFSS60CjS80C7h-TGOrfQ4ncm83N8VmZkk,185
pytz/zoneinfo/Indian/Cocos,sha256=_YHASq4Z5YcUILIdhEzg27CGLzarUHPDHs1Dj0QgNGM,254
pytz/zoneinfo/Indian/Comoro,sha256=yJsuJTqJJqbOz37_NOS_zbf-JNr_IthHGMMN7sDqSWg,265
pytz/zoneinfo/Indian/Kerguelen,sha256=F73ffVfBoUoHre0-DwsiQrYJcLpPOW-JJGk3n88lM5U,185
pytz/zoneinfo/Indian/Mahe,sha256=pmdhPhaJRwKwONvxiZNGeFSICjlWzyY9JlFHv-H9upY,151
pytz/zoneinfo/Indian/Maldives,sha256=F73ffVfBoUoHre0-DwsiQrYJcLpPOW-JJGk3n88lM5U,185
pytz/zoneinfo/Indian/Mauritius,sha256=Znqrc1chimlciJsYBOl0NvIHnrNdCxncGxWczq1PBeI,227
pytz/zoneinfo/Indian/Mayotte,sha256=yJsuJTqJJqbOz37_NOS_zbf-JNr_IthHGMMN7sDqSWg,265
pytz/zoneinfo/Indian/Reunion,sha256=pmdhPhaJRwKwONvxiZNGeFSICjlWzyY9JlFHv-H9upY,151
pytz/zoneinfo/Iran,sha256=LQMch2TMA4wI23SQzoIrlZh0_KceXQegurwxCZ5YDlY,1248
pytz/zoneinfo/Israel,sha256=JUuWQmW5Tha0pJjw61Q5aN7CX0z4D7ops9OOSnda6Dc,2388
pytz/zoneinfo/Jamaica,sha256=wlagieUPRf5-beie-h7QsONbNzjGsm8vMs8uf28pw28,482
pytz/zoneinfo/Japan,sha256=oCueZgRNxcNcX3ZGdif9y6Su4cyVhga4XHdwlcrYLOs,309
pytz/zoneinfo/Kwajalein,sha256=TmZ_0f-ySQ-saBAlRXV0f49Itwne51VBXn6rWcrWqHQ,302
pytz/zoneinfo/Libya,sha256=W1dptGD70T7ppGoo0fczFQeDiIp0nultLNPV66MwB2c,625
pytz/zoneinfo/MET,sha256=i3CKSuP4N_PAj7o-Cbk8zPEdFs0CWWBCAfg2JXDx5V8,2094
pytz/zoneinfo/MST,sha256=6IQwvtT12Bz1pTiqFuoVxNY-4ViS7ZrYHo5nPWwzKPw,114
pytz/zoneinfo/MST7MDT,sha256=910Ek32FKoSyZWY_H19VHaVvqb-JsvnWTOOHvhrKsE0,2310
pytz/zoneinfo/Mexico/BajaNorte,sha256=57-Q9LSTNuTidz-lOTwDysmlCoeFUXSecvVVqNWburQ,2374
pytz/zoneinfo/Mexico/BajaSur,sha256=RQQVwlEVHRp2X-c_0hJ46y54abTlqUuLkyrUUicyc5g,1128
pytz/zoneinfo/Mexico/General,sha256=A5MlfDUZ4O1-jMTRt0WPem7qqcW0Nrslls1hlc8C4-Q,1222
pytz/zoneinfo/NZ,sha256=gADjoyPo_QISQU6UJrAgcHp3HDaMoOFRdH-d23uBSyc,2437
pytz/zoneinfo/NZ-CHAT,sha256=xhexVc5lfJ_qAv2d3HrII6lfRSxKZYBAjY2zpYkCGE8,2054
pytz/zoneinfo/Navajo,sha256=MugZwApDs8NI9TnXANQlUE8guNBowWQY0m-ptpPndck,2460
pytz/zoneinfo/PRC,sha256=ZP_C5DqUQ1oEPAQNHTr36S0DGtx453N68YYbqk7u8-Y,561
pytz/zoneinfo/PST8PDT,sha256=Q7TCLkE69a6g7mPoPAkqhg-0dStyiAC0jVlM72KG_R8,2310
pytz/zoneinfo/Pacific/Apia,sha256=M3QKsp75Q7H1X3aeE_9ZqQli9aEkNCCQctZQ5sEKu00,598
pytz/zoneinfo/Pacific/Auckland,sha256=gADjoyPo_QISQU6UJrAgcHp3HDaMoOFRdH-d23uBSyc,2437
pytz/zoneinfo/Pacific/Bougainville,sha256=hWE86eXnNx-vABbp7-YSIqWyecHPMIWLftVloAoPhL8,254
pytz/zoneinfo/Pacific/Chatham,sha256=xhexVc5lfJ_qAv2d3HrII6lfRSxKZYBAjY2zpYkCGE8,2054
pytz/zoneinfo/Pacific/Chuuk,sha256=nB36HBWZTdh3TlP0DLFNz1KRQ0aHIfHbp7LC4Urp9fA,172
pytz/zoneinfo/Pacific/Easter,sha256=QbubBs_xQlvKweAnurhyHjIK4ji77Gh4G-usXul6XVM,2219
pytz/zoneinfo/Pacific/Efate,sha256=oSxNcQYx5-1FU2_yHzHI-hT-dMJcPxzy4XmdI1UxXAo,524
pytz/zoneinfo/Pacific/Enderbury,sha256=HNTAKrsH_R2W3QRlKcmNld5KcXdP0ygXCjEovc1i-6Q,220
pytz/zoneinfo/Pacific/Fakaofo,sha256=qOodpTMKjztvZIXVLe_f_kZ6WcHl9fCLE9ZsyvdFKLI,186
pytz/zoneinfo/Pacific/Fiji,sha256=jB5FbOsCnHVQQ2ohPiWEQUPhG6JybB3Nog3qT6WJQ0I,564
pytz/zoneinfo/Pacific/Funafuti,sha256=UyaKimsR8LjgL8Z2g65I0HTvr3tMZuA2wUeBB6_Zp9c,152
pytz/zoneinfo/Pacific/Galapagos,sha256=_GJUYOjSiIjoNBO2qdq23isLMJ4NCVk3DKIRGeDc8BA,224
pytz/zoneinfo/Pacific/Gambier,sha256=gAS7gr1HH_re0uYnL6eWo5KGJ-B5QaiM8mV2cY5mQxE,150
pytz/zoneinfo/Pacific/Guadalcanal,sha256=M4kTWqaSQaV1AMhyLSvmwoBJF7X9icrILbvQJwp940g,152
pytz/zoneinfo/Pacific/Guam,sha256=Ex9znmf6rNfGze6gNpZJCMr1TT4rkl2SnrhecrdJufI,494
pytz/zoneinfo/Pacific/Honolulu,sha256=fwPRv1Jk56sCOi75uZfd_Iy2k2aSQHx3B2K5xUlSPzM,329
pytz/zoneinfo/Pacific/Johnston,sha256=fwPRv1Jk56sCOi75uZfd_Iy2k2aSQHx3B2K5xUlSPzM,329
pytz/zoneinfo/Pacific/Kanton,sha256=HNTAKrsH_R2W3QRlKcmNld5KcXdP0ygXCjEovc1i-6Q,220
pytz/zoneinfo/Pacific/Kiritimati,sha256=hYk1Ooz-Lj1PuZCbNV2WJIvOLtCwSwq2u63cb1Z-3NQ,224
pytz/zoneinfo/Pacific/Kosrae,sha256=Q0jrb4zeDrd61bU4V8TqjMc0Iep8rWZyZqJ0uqsunxs,337
pytz/zoneinfo/Pacific/Kwajalein,sha256=TmZ_0f-ySQ-saBAlRXV0f49Itwne51VBXn6rWcrWqHQ,302
pytz/zoneinfo/Pacific/Majuro,sha256=UyaKimsR8LjgL8Z2g65I0HTvr3tMZuA2wUeBB6_Zp9c,152
pytz/zoneinfo/Pacific/Marquesas,sha256=FTxPJTWtk48LVb3N2U64KLpLsmvu0DQBubTCg-dvyGM,159
pytz/zoneinfo/Pacific/Midway,sha256=fCYrYphYY6rUfxOw712y5cyRe104AC3pouqD3bCINFg,175
pytz/zoneinfo/Pacific/Nauru,sha256=9ASKgLHB-8nsTEK1ApzfTH0yQtbNAmGX-JI7uHZiqnA,238
pytz/zoneinfo/Pacific/Niue,sha256=OllXxukncR7a-SMmdFox5az1xpIPMhbahQhtObmpuDM,189
pytz/zoneinfo/Pacific/Norfolk,sha256=DMdX1Bm18lzNuiCWzwfeHUMRGXPS8v5AWnh-_EX_AZw,866
pytz/zoneinfo/Pacific/Noumea,sha256=tkHxxnxsXTOqz3YzWi0mkhTCIONzg-W7EpSRMdPjKdQ,290
pytz/zoneinfo/Pacific/Pago_Pago,sha256=fCYrYphYY6rUfxOw712y5cyRe104AC3pouqD3bCINFg,175
pytz/zoneinfo/Pacific/Palau,sha256=aN2HbT0reqwKrtLKDK9M2zb0d0ikdNlTrrntVxdH66o,166
pytz/zoneinfo/Pacific/Pitcairn,sha256=U4jAUuvsRNoy8XrPa16YpcXCcqHJY0u6JvCNgPEWO1c,188
pytz/zoneinfo/Pacific/Pohnpei,sha256=M4kTWqaSQaV1AMhyLSvmwoBJF7X9icrILbvQJwp940g,152
pytz/zoneinfo/Pacific/Ponape,sha256=M4kTWqaSQaV1AMhyLSvmwoBJF7X9icrILbvQJwp940g,152
pytz/zoneinfo/Pacific/Port_Moresby,sha256=nB36HBWZTdh3TlP0DLFNz1KRQ0aHIfHbp7LC4Urp9fA,172
pytz/zoneinfo/Pacific/Rarotonga,sha256=wPEsoXbyDnuhfzkgLvUqhSzrMx_FD42uAPluSPMh3Bc,589
pytz/zoneinfo/Pacific/Saipan,sha256=Ex9znmf6rNfGze6gNpZJCMr1TT4rkl2SnrhecrdJufI,494
pytz/zoneinfo/Pacific/Samoa,sha256=fCYrYphYY6rUfxOw712y5cyRe104AC3pouqD3bCINFg,175
pytz/zoneinfo/Pacific/Tahiti,sha256=BRff9G3E-iWKhOWR1Wu02Z0iMgjrwDXV-XNrqItXdTY,151
pytz/zoneinfo/Pacific/Tarawa,sha256=UyaKimsR8LjgL8Z2g65I0HTvr3tMZuA2wUeBB6_Zp9c,152
pytz/zoneinfo/Pacific/Tongatapu,sha256=OppBZqTAZib9HY7U9AC-JavO7m6NxPGUtUfPQAl9oBY,358
pytz/zoneinfo/Pacific/Truk,sha256=nB36HBWZTdh3TlP0DLFNz1KRQ0aHIfHbp7LC4Urp9fA,172
pytz/zoneinfo/Pacific/Wake,sha256=UyaKimsR8LjgL8Z2g65I0HTvr3tMZuA2wUeBB6_Zp9c,152
pytz/zoneinfo/Pacific/Wallis,sha256=UyaKimsR8LjgL8Z2g65I0HTvr3tMZuA2wUeBB6_Zp9c,152
pytz/zoneinfo/Pacific/Yap,sha256=nB36HBWZTdh3TlP0DLFNz1KRQ0aHIfHbp7LC4Urp9fA,172
pytz/zoneinfo/Poland,sha256=TiLDPbeVF0ckgLVEkaSeDaKZ8wctdJDOl_HE_Wd5rKs,2654
pytz/zoneinfo/Portugal,sha256=mpUpxGexMhbOBImDLSQs5-GAk7pm7tg4qYW044Kkle0,3497
pytz/zoneinfo/ROC,sha256=DMmQwOpPql25ue3Nf8vAKKT4em06D1Z9rHbLIitxixk,761
pytz/zoneinfo/ROK,sha256=LI9LsV3XcJC0l-KoQf8zI-y7rk-du57erS-N2Ptdi7Q,617
pytz/zoneinfo/Singapore,sha256=XmeVImeqcJ8hJzm7TjAti1nWJAxawOqq7jIzDnHX2hI,401
pytz/zoneinfo/Turkey,sha256=Jk4wjndDta_uLWc8W1dWdjbavJJbsL5ROTmZboVnGKU,1933
pytz/zoneinfo/UCT,sha256=i4WEZ5GrLIpUY8g6W-PAQ-JXDXRIQ01BOYlp7Ufj5vI,114
pytz/zoneinfo/US/Alaska,sha256=oZA1NSPS2BWdymYpnCHFO8BlYVS-ll5KLg2Ez9CbETs,2371
pytz/zoneinfo/US/Aleutian,sha256=IB1DhwJQAKbhPJ9jHLf8zW5Dad7HIkBS-dhv64E1OlM,2356
pytz/zoneinfo/US/Arizona,sha256=illz0sYuLL8lIPK0Tkou6dL0Vck_D0W_3rRTOvFYRmQ,360
pytz/zoneinfo/US/Central,sha256=_roybr6I6sIAF6cYdIxGxoRpoef153Fty48dQ6bm9oY,3592
pytz/zoneinfo/US/East-Indiana,sha256=kNKy9Kj9ICsiYYfCCbAggzMA7exf-GpGPMxoXocHUyw,1682
pytz/zoneinfo/US/Eastern,sha256=6e0H177gx2qdRC0JHvHwFmj-58TyYBTAqGixn-bBipU,3552
pytz/zoneinfo/US/Hawaii,sha256=fwPRv1Jk56sCOi75uZfd_Iy2k2aSQHx3B2K5xUlSPzM,329
pytz/zoneinfo/US/Indiana-Starke,sha256=CsvZ5BKw2qVav3x_F8CU9taJdDk7jX41Cfsqms6jXV8,2444
pytz/zoneinfo/US/Michigan,sha256=hecz8yqY2Cj5B61G3gLZdAVZvRgK9l0P90c_gN-uD5g,2230
pytz/zoneinfo/US/Mountain,sha256=MugZwApDs8NI9TnXANQlUE8guNBowWQY0m-ptpPndck,2460
pytz/zoneinfo/US/Pacific,sha256=aJd7ua1tGG_vxser02AQpm4wAI3LLTdgh6QcSYYecmg,2852
pytz/zoneinfo/US/Samoa,sha256=fCYrYphYY6rUfxOw712y5cyRe104AC3pouqD3bCINFg,175
pytz/zoneinfo/UTC,sha256=i4WEZ5GrLIpUY8g6W-PAQ-JXDXRIQ01BOYlp7Ufj5vI,114
pytz/zoneinfo/Universal,sha256=i4WEZ5GrLIpUY8g6W-PAQ-JXDXRIQ01BOYlp7Ufj5vI,114
pytz/zoneinfo/W-SU,sha256=KmkofRcj6T8Ph28PJChm8JVp13uRvef6TZ0GuPzUiDw,1535
pytz/zoneinfo/WET,sha256=Sc0l03EfVs_aIi17I4KyZJFkwiAHat5BgpjuuFDhgQ0,1905
pytz/zoneinfo/Zulu,sha256=i4WEZ5GrLIpUY8g6W-PAQ-JXDXRIQ01BOYlp7Ufj5vI,114
pytz/zoneinfo/iso3166.tab,sha256=oBpdFY8x1GrY5vjMKgbGQYEGgqk5fUYDIPaNVCG2XnE,4791
pytz/zoneinfo/leapseconds,sha256=fjC39Eu3wB6I4g7x_VL7HzvDVbiKbLUjfQAEgo7442I,3257
pytz/zoneinfo/tzdata.zi,sha256=8PWtzwDNZfLJU8Wa6Ktci7tg9V5mpvh26Vb0P8jBU0w,109390
pytz/zoneinfo/zone.tab,sha256=qSLfeCWE3tsCDIIQbr71DMkmCUXTIUEgNZgfN-60d-Y,18846
pytz/zoneinfo/zone1970.tab,sha256=FJErvL9wggoFluO2WceYn8ZQ-nA9A073Lub1x2Pzg40,17582
pytz/zoneinfo/zonenow.tab,sha256=YoPd7huhHsKlJliOO-eMIBE5-bHBKpbfjkSJQFAto6I,8311
```
```bash
./.venv/lib/python3.9/site-packages/pytz-2024.1.dist-info/WHEEL
```
```
Wheel-Version: 1.0
Generator: bdist_wheel (0.37.1)
Root-Is-Purelib: true
Tag: py2-none-any
Tag: py3-none-any
```
```bash
./.venv/lib/python3.9/site-packages/pytz-2024.1.dist-info/top_level.txt
```
```
pytz
```
```bash
./.venv/lib/python3.9/site-packages/pytz-2024.1.dist-info/LICENSE.txt
```
```
Copyright (c) 2003-2019 Stuart Bishop <stuart@stuartbishop.net>

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
```
```bash
./.venv/lib/python3.9/site-packages/pytz-2024.1.dist-info/REQUESTED
```
```

```
```bash
./.venv/lib/python3.9/site-packages/pytz-2024.1.dist-info/INSTALLER
```
```
pip
```
```bash
./.venv/lib/python3.9/site-packages/pytz-2024.1.dist-info/METADATA
```
```
Metadata-Version: 2.1
Name: pytz
Version: 2024.1
Summary: World timezone definitions, modern and historical
Home-page: http://pythonhosted.org/pytz
Author: Stuart Bishop
Author-email: stuart@stuartbishop.net
Maintainer: Stuart Bishop
Maintainer-email: stuart@stuartbishop.net
License: MIT
Download-URL: https://pypi.org/project/pytz/
Keywords: timezone,tzinfo,datetime,olson,time
Platform: Independent
Classifier: Development Status :: 6 - Mature
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: MIT License
Classifier: Natural Language :: English
Classifier: Operating System :: OS Independent
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 2
Classifier: Programming Language :: Python :: 2.4
Classifier: Programming Language :: Python :: 2.5
Classifier: Programming Language :: Python :: 2.6
Classifier: Programming Language :: Python :: 2.7
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.1
Classifier: Programming Language :: Python :: 3.2
Classifier: Programming Language :: Python :: 3.3
Classifier: Programming Language :: Python :: 3.4
Classifier: Programming Language :: Python :: 3.5
Classifier: Programming Language :: Python :: 3.6
Classifier: Programming Language :: Python :: 3.7
Classifier: Programming Language :: Python :: 3.8
Classifier: Programming Language :: Python :: 3.9
Classifier: Programming Language :: Python :: 3.10
Classifier: Programming Language :: Python :: 3.11
Classifier: Programming Language :: Python :: 3.12
Classifier: Topic :: Software Development :: Libraries :: Python Modules
License-File: LICENSE.txt

pytz - World Timezone Definitions for Python
============================================

:Author: Stuart Bishop <stuart@stuartbishop.net>

Introduction
~~~~~~~~~~~~

pytz brings the Olson tz database into Python. This library allows
accurate and cross platform timezone calculations using Python 2.4
or higher. It also solves the issue of ambiguous times at the end
of daylight saving time, which you can read more about in the Python
Library Reference (``datetime.tzinfo``).

Almost all of the Olson timezones are supported.

.. note::

    Projects using Python 3.9 or later should be using the support
    now included as part of the standard library, and third party
    packages work with it such as `tzdata <https://pypi.org/project/tzdata/>`_.
    pytz offers no advantages beyond backwards compatibility with
    code written for earlier versions of Python.

.. note::

    This library differs from the documented Python API for
    tzinfo implementations; if you want to create local wallclock
    times you need to use the ``localize()`` method documented in this
    document. In addition, if you perform date arithmetic on local
    times that cross DST boundaries, the result may be in an incorrect
    timezone (ie. subtract 1 minute from 2002-10-27 1:00 EST and you get
    2002-10-27 0:59 EST instead of the correct 2002-10-27 1:59 EDT). A
    ``normalize()`` method is provided to correct this. Unfortunately these
    issues cannot be resolved without modifying the Python datetime
    implementation (see PEP-431).


Installation
~~~~~~~~~~~~

This package can either be installed using ``pip`` or from a tarball using the
standard Python distutils.

If you are installing using ``pip``, you don't need to download anything as the
latest version will be downloaded for you from PyPI::

    pip install pytz

If you are installing from a tarball, run the following command as an
administrative user::

    python setup.py install


pytz for Enterprise
~~~~~~~~~~~~~~~~~~~

Available as part of the Tidelift Subscription.

The maintainers of pytz and thousands of other packages are working with Tidelift to deliver commercial support and maintenance for the open source dependencies you use to build your applications. Save time, reduce risk, and improve code health, while paying the maintainers of the exact dependencies you use. `Learn more. <https://tidelift.com/subscription/pkg/pypi-pytz?utm_source=pypi-pytz&utm_medium=referral&utm_campaign=enterprise&utm_term=repo>`_.


Example & Usage
~~~~~~~~~~~~~~~

Localized times and date arithmetic
-----------------------------------

>>> from datetime import datetime, timedelta
>>> from pytz import timezone
>>> import pytz
>>> utc = pytz.utc
>>> utc.zone
'UTC'
>>> eastern = timezone('US/Eastern')
>>> eastern.zone
'US/Eastern'
>>> amsterdam = timezone('Europe/Amsterdam')
>>> fmt = '%Y-%m-%d %H:%M:%S %Z%z'

This library only supports two ways of building a localized time. The
first is to use the ``localize()`` method provided by the pytz library.
This is used to localize a naive datetime (datetime with no timezone
information):

>>> loc_dt = eastern.localize(datetime(2002, 10, 27, 6, 0, 0))
>>> print(loc_dt.strftime(fmt))
2002-10-27 06:00:00 EST-0500

The second way of building a localized time is by converting an existing
localized time using the standard ``astimezone()`` method:

>>> ams_dt = loc_dt.astimezone(amsterdam)
>>> ams_dt.strftime(fmt)
'2002-10-27 12:00:00 CET+0100'

Unfortunately using the tzinfo argument of the standard datetime
constructors ''does not work'' with pytz for many timezones.

>>> datetime(2002, 10, 27, 12, 0, 0, tzinfo=amsterdam).strftime(fmt)  # /!\ Does not work this way!
'2002-10-27 12:00:00 LMT+0018'

It is safe for timezones without daylight saving transitions though, such
as UTC:

>>> datetime(2002, 10, 27, 12, 0, 0, tzinfo=pytz.utc).strftime(fmt)  # /!\ Not recommended except for UTC
'2002-10-27 12:00:00 UTC+0000'

The preferred way of dealing with times is to always work in UTC,
converting to localtime only when generating output to be read
by humans.

>>> utc_dt = datetime(2002, 10, 27, 6, 0, 0, tzinfo=utc)
>>> loc_dt = utc_dt.astimezone(eastern)
>>> loc_dt.strftime(fmt)
'2002-10-27 01:00:00 EST-0500'

This library also allows you to do date arithmetic using local
times, although it is more complicated than working in UTC as you
need to use the ``normalize()`` method to handle daylight saving time
and other timezone transitions. In this example, ``loc_dt`` is set
to the instant when daylight saving time ends in the US/Eastern
timezone.

>>> before = loc_dt - timedelta(minutes=10)
>>> before.strftime(fmt)
'2002-10-27 00:50:00 EST-0500'
>>> eastern.normalize(before).strftime(fmt)
'2002-10-27 01:50:00 EDT-0400'
>>> after = eastern.normalize(before + timedelta(minutes=20))
>>> after.strftime(fmt)
'2002-10-27 01:10:00 EST-0500'

Creating local times is also tricky, and the reason why working with
local times is not recommended. Unfortunately, you cannot just pass
a ``tzinfo`` argument when constructing a datetime (see the next
section for more details)

>>> dt = datetime(2002, 10, 27, 1, 30, 0)
>>> dt1 = eastern.localize(dt, is_dst=True)
>>> dt1.strftime(fmt)
'2002-10-27 01:30:00 EDT-0400'
>>> dt2 = eastern.localize(dt, is_dst=False)
>>> dt2.strftime(fmt)
'2002-10-27 01:30:00 EST-0500'

Converting between timezones is more easily done, using the
standard astimezone method.

>>> utc_dt = datetime.fromtimestamp(1143408899, tz=utc)
>>> utc_dt.strftime(fmt)
'2006-03-26 21:34:59 UTC+0000'
>>> au_tz = timezone('Australia/Sydney')
>>> au_dt = utc_dt.astimezone(au_tz)
>>> au_dt.strftime(fmt)
'2006-03-27 08:34:59 AEDT+1100'
>>> utc_dt2 = au_dt.astimezone(utc)
>>> utc_dt2.strftime(fmt)
'2006-03-26 21:34:59 UTC+0000'
>>> utc_dt == utc_dt2
True

You can take shortcuts when dealing with the UTC side of timezone
conversions. ``normalize()`` and ``localize()`` are not really
necessary when there are no daylight saving time transitions to
deal with.

>>> utc_dt = datetime.fromtimestamp(1143408899, tz=utc)
>>> utc_dt.strftime(fmt)
'2006-03-26 21:34:59 UTC+0000'
>>> au_tz = timezone('Australia/Sydney')
>>> au_dt = au_tz.normalize(utc_dt.astimezone(au_tz))
>>> au_dt.strftime(fmt)
'2006-03-27 08:34:59 AEDT+1100'
>>> utc_dt2 = au_dt.astimezone(utc)
>>> utc_dt2.strftime(fmt)
'2006-03-26 21:34:59 UTC+0000'


``tzinfo`` API
--------------

The ``tzinfo`` instances returned by the ``timezone()`` function have
been extended to cope with ambiguous times by adding an ``is_dst``
parameter to the ``utcoffset()``, ``dst()`` && ``tzname()`` methods.

>>> tz = timezone('America/St_Johns')

>>> normal = datetime(2009, 9, 1)
>>> ambiguous = datetime(2009, 10, 31, 23, 30)

The ``is_dst`` parameter is ignored for most timestamps. It is only used
during DST transition ambiguous periods to resolve that ambiguity.

>>> print(tz.utcoffset(normal, is_dst=True))
-1 day, 21:30:00
>>> print(tz.dst(normal, is_dst=True))
1:00:00
>>> tz.tzname(normal, is_dst=True)
'NDT'

>>> print(tz.utcoffset(ambiguous, is_dst=True))
-1 day, 21:30:00
>>> print(tz.dst(ambiguous, is_dst=True))
1:00:00
>>> tz.tzname(ambiguous, is_dst=True)
'NDT'

>>> print(tz.utcoffset(normal, is_dst=False))
-1 day, 21:30:00
>>> tz.dst(normal, is_dst=False).seconds
3600
>>> tz.tzname(normal, is_dst=False)
'NDT'

>>> print(tz.utcoffset(ambiguous, is_dst=False))
-1 day, 20:30:00
>>> tz.dst(ambiguous, is_dst=False)
datetime.timedelta(0)
>>> tz.tzname(ambiguous, is_dst=False)
'NST'

If ``is_dst`` is not specified, ambiguous timestamps will raise
an ``pytz.exceptions.AmbiguousTimeError`` exception.

>>> print(tz.utcoffset(normal))
-1 day, 21:30:00
>>> print(tz.dst(normal))
1:00:00
>>> tz.tzname(normal)
'NDT'

>>> import pytz.exceptions
>>> try:
...     tz.utcoffset(ambiguous)
... except pytz.exceptions.AmbiguousTimeError:
...     print('pytz.exceptions.AmbiguousTimeError: %s' % ambiguous)
pytz.exceptions.AmbiguousTimeError: 2009-10-31 23:30:00
>>> try:
...     tz.dst(ambiguous)
... except pytz.exceptions.AmbiguousTimeError:
...     print('pytz.exceptions.AmbiguousTimeError: %s' % ambiguous)
pytz.exceptions.AmbiguousTimeError: 2009-10-31 23:30:00
>>> try:
...     tz.tzname(ambiguous)
... except pytz.exceptions.AmbiguousTimeError:
...     print('pytz.exceptions.AmbiguousTimeError: %s' % ambiguous)
pytz.exceptions.AmbiguousTimeError: 2009-10-31 23:30:00


Problems with Localtime
~~~~~~~~~~~~~~~~~~~~~~~

The major problem we have to deal with is that certain datetimes
may occur twice in a year. For example, in the US/Eastern timezone
on the last Sunday morning in October, the following sequence
happens:

    - 01:00 EDT occurs
    - 1 hour later, instead of 2:00am the clock is turned back 1 hour
      and 01:00 happens again (this time 01:00 EST)

In fact, every instant between 01:00 and 02:00 occurs twice. This means
that if you try and create a time in the 'US/Eastern' timezone
the standard datetime syntax, there is no way to specify if you meant
before of after the end-of-daylight-saving-time transition. Using the
pytz custom syntax, the best you can do is make an educated guess:

>>> loc_dt = eastern.localize(datetime(2002, 10, 27, 1, 30, 00))
>>> loc_dt.strftime(fmt)
'2002-10-27 01:30:00 EST-0500'

As you can see, the system has chosen one for you and there is a 50%
chance of it being out by one hour. For some applications, this does
not matter. However, if you are trying to schedule meetings with people
in different timezones or analyze log files it is not acceptable.

The best and simplest solution is to stick with using UTC.  The pytz
package encourages using UTC for internal timezone representation by
including a special UTC implementation based on the standard Python
reference implementation in the Python documentation.

The UTC timezone unpickles to be the same instance, and pickles to a
smaller size than other pytz tzinfo instances.  The UTC implementation
can be obtained as pytz.utc, pytz.UTC, or pytz.timezone('UTC').

>>> import pickle, pytz
>>> dt = datetime(2005, 3, 1, 14, 13, 21, tzinfo=utc)
>>> naive = dt.replace(tzinfo=None)
>>> p = pickle.dumps(dt, 1)
>>> naive_p = pickle.dumps(naive, 1)
>>> len(p) - len(naive_p)
17
>>> new = pickle.loads(p)
>>> new == dt
True
>>> new is dt
False
>>> new.tzinfo is dt.tzinfo
True
>>> pytz.utc is pytz.UTC is pytz.timezone('UTC')
True

Note that some other timezones are commonly thought of as the same (GMT,
Greenwich, Universal, etc.). The definition of UTC is distinct from these
other timezones, and they are not equivalent. For this reason, they will
not compare the same in Python.

>>> utc == pytz.timezone('GMT')
False

See the section `What is UTC`_, below.

If you insist on working with local times, this library provides a
facility for constructing them unambiguously:

>>> loc_dt = datetime(2002, 10, 27, 1, 30, 00)
>>> est_dt = eastern.localize(loc_dt, is_dst=True)
>>> edt_dt = eastern.localize(loc_dt, is_dst=False)
>>> print(est_dt.strftime(fmt) + ' / ' + edt_dt.strftime(fmt))
2002-10-27 01:30:00 EDT-0400 / 2002-10-27 01:30:00 EST-0500

If you pass None as the is_dst flag to localize(), pytz will refuse to
guess and raise exceptions if you try to build ambiguous or non-existent
times.

For example, 1:30am on 27th Oct 2002 happened twice in the US/Eastern
timezone when the clocks where put back at the end of Daylight Saving
Time:

>>> dt = datetime(2002, 10, 27, 1, 30, 00)
>>> try:
...     eastern.localize(dt, is_dst=None)
... except pytz.exceptions.AmbiguousTimeError:
...     print('pytz.exceptions.AmbiguousTimeError: %s' % dt)
pytz.exceptions.AmbiguousTimeError: 2002-10-27 01:30:00

Similarly, 2:30am on 7th April 2002 never happened at all in the
US/Eastern timezone, as the clocks where put forward at 2:00am skipping
the entire hour:

>>> dt = datetime(2002, 4, 7, 2, 30, 00)
>>> try:
...     eastern.localize(dt, is_dst=None)
... except pytz.exceptions.NonExistentTimeError:
...     print('pytz.exceptions.NonExistentTimeError: %s' % dt)
pytz.exceptions.NonExistentTimeError: 2002-04-07 02:30:00

Both of these exceptions share a common base class to make error handling
easier:

>>> isinstance(pytz.AmbiguousTimeError(), pytz.InvalidTimeError)
True
>>> isinstance(pytz.NonExistentTimeError(), pytz.InvalidTimeError)
True


A special case is where countries change their timezone definitions
with no daylight savings time switch. For example, in 1915 Warsaw
switched from Warsaw time to Central European time with no daylight savings
transition. So at the stroke of midnight on August 5th 1915 the clocks
were wound back 24 minutes creating an ambiguous time period that cannot
be specified without referring to the timezone abbreviation or the
actual UTC offset. In this case midnight happened twice, neither time
during a daylight saving time period. pytz handles this transition by
treating the ambiguous period before the switch as daylight savings
time, and the ambiguous period after as standard time.


>>> warsaw = pytz.timezone('Europe/Warsaw')
>>> amb_dt1 = warsaw.localize(datetime(1915, 8, 4, 23, 59, 59), is_dst=True)
>>> amb_dt1.strftime(fmt)
'1915-08-04 23:59:59 WMT+0124'
>>> amb_dt2 = warsaw.localize(datetime(1915, 8, 4, 23, 59, 59), is_dst=False)
>>> amb_dt2.strftime(fmt)
'1915-08-04 23:59:59 CET+0100'
>>> switch_dt = warsaw.localize(datetime(1915, 8, 5, 00, 00, 00), is_dst=False)
>>> switch_dt.strftime(fmt)
'1915-08-05 00:00:00 CET+0100'
>>> str(switch_dt - amb_dt1)
'0:24:01'
>>> str(switch_dt - amb_dt2)
'0:00:01'

The best way of creating a time during an ambiguous time period is
by converting from another timezone such as UTC:

>>> utc_dt = datetime(1915, 8, 4, 22, 36, tzinfo=pytz.utc)
>>> utc_dt.astimezone(warsaw).strftime(fmt)
'1915-08-04 23:36:00 CET+0100'

The standard Python way of handling all these ambiguities is not to
handle them, such as demonstrated in this example using the US/Eastern
timezone definition from the Python documentation (Note that this
implementation only works for dates between 1987 and 2006 - it is
included for tests only!):

>>> from pytz.reference import Eastern # pytz.reference only for tests
>>> dt = datetime(2002, 10, 27, 0, 30, tzinfo=Eastern)
>>> str(dt)
'2002-10-27 00:30:00-04:00'
>>> str(dt + timedelta(hours=1))
'2002-10-27 01:30:00-05:00'
>>> str(dt + timedelta(hours=2))
'2002-10-27 02:30:00-05:00'
>>> str(dt + timedelta(hours=3))
'2002-10-27 03:30:00-05:00'

Notice the first two results? At first glance you might think they are
correct, but taking the UTC offset into account you find that they are
actually two hours appart instead of the 1 hour we asked for.

>>> from pytz.reference import UTC # pytz.reference only for tests
>>> str(dt.astimezone(UTC))
'2002-10-27 04:30:00+00:00'
>>> str((dt + timedelta(hours=1)).astimezone(UTC))
'2002-10-27 06:30:00+00:00'


Country Information
~~~~~~~~~~~~~~~~~~~

A mechanism is provided to access the timezones commonly in use
for a particular country, looked up using the ISO 3166 country code.
It returns a list of strings that can be used to retrieve the relevant
tzinfo instance using ``pytz.timezone()``:

>>> print(' '.join(pytz.country_timezones['nz']))
Pacific/Auckland Pacific/Chatham

The Olson database comes with a ISO 3166 country code to English country
name mapping that pytz exposes as a dictionary:

>>> print(pytz.country_names['nz'])
New Zealand


What is UTC
~~~~~~~~~~~

'UTC' is `Coordinated Universal Time`_. It is a successor to, but distinct
from, Greenwich Mean Time (GMT) and the various definitions of Universal
Time. UTC is now the worldwide standard for regulating clocks and time
measurement.

All other timezones are defined relative to UTC, and include offsets like
UTC+0800 - hours to add or subtract from UTC to derive the local time. No
daylight saving time occurs in UTC, making it a useful timezone to perform
date arithmetic without worrying about the confusion and ambiguities caused
by daylight saving time transitions, your country changing its timezone, or
mobile computers that roam through multiple timezones.

..  _Coordinated Universal Time: https://en.wikipedia.org/wiki/Coordinated_Universal_Time


Helpers
~~~~~~~

There are two lists of timezones provided.

``all_timezones`` is the exhaustive list of the timezone names that can
be used.

>>> from pytz import all_timezones
>>> len(all_timezones) >= 500
True
>>> 'Etc/Greenwich' in all_timezones
True

``common_timezones`` is a list of useful, current timezones. It doesn't
contain deprecated zones or historical zones, except for a few I've
deemed in common usage, such as US/Eastern (open a bug report if you
think other timezones are deserving of being included here). It is also
a sequence of strings.

>>> from pytz import common_timezones
>>> len(common_timezones) < len(all_timezones)
True
>>> 'Etc/Greenwich' in common_timezones
False
>>> 'Australia/Melbourne' in common_timezones
True
>>> 'US/Eastern' in common_timezones
True
>>> 'Canada/Eastern' in common_timezones
True
>>> 'Australia/Yancowinna' in all_timezones
True
>>> 'Australia/Yancowinna' in common_timezones
False

Both ``common_timezones`` and ``all_timezones`` are alphabetically
sorted:

>>> common_timezones_dupe = common_timezones[:]
>>> common_timezones_dupe.sort()
>>> common_timezones == common_timezones_dupe
True
>>> all_timezones_dupe = all_timezones[:]
>>> all_timezones_dupe.sort()
>>> all_timezones == all_timezones_dupe
True

``all_timezones`` and ``common_timezones`` are also available as sets.

>>> from pytz import all_timezones_set, common_timezones_set
>>> 'US/Eastern' in all_timezones_set
True
>>> 'US/Eastern' in common_timezones_set
True
>>> 'Australia/Victoria' in common_timezones_set
False

You can also retrieve lists of timezones used by particular countries
using the ``country_timezones()`` function. It requires an ISO-3166
two letter country code.

>>> from pytz import country_timezones
>>> print(' '.join(country_timezones('ch')))
Europe/Zurich
>>> print(' '.join(country_timezones('CH')))
Europe/Zurich


Internationalization - i18n/l10n
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pytz is an interface to the IANA database, which uses ASCII names. The `Unicode  Consortium's Unicode Locales (CLDR) <http://cldr.unicode.org>`_
project provides translations. Python packages such as
`Babel <https://babel.pocoo.org/en/latest/api/dates.html#timezone-functionality>`_
and Thomas Khyn's `l18n <https://pypi.org/project/l18n/>`_ package can be used
to access these translations from Python.


License
~~~~~~~

MIT license.

This code is also available as part of Zope 3 under the Zope Public
License,  Version 2.1 (ZPL).

I'm happy to relicense this code if necessary for inclusion in other
open source projects.


Latest Versions
~~~~~~~~~~~~~~~

This package will be updated after releases of the Olson timezone
database.  The latest version can be downloaded from the `Python Package
Index <https://pypi.org/project/pytz/>`_.  The code that is used
to generate this distribution is hosted on Github and available
using git::

    git clone https://github.com/stub42/pytz.git

Announcements of new releases are made on
`Launchpad <https://launchpad.net/pytz>`_, and the
`Atom feed <http://feeds.launchpad.net/pytz/announcements.atom>`_
hosted there.


Bugs, Feature Requests & Patches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bugs should be reported on `Github <https://github.com/stub42/pytz/issues>`_.
Feature requests are unlikely to be considered, and efforts instead directed
to timezone support now built into Python or packages that work with it.


Security Issues
~~~~~~~~~~~~~~~

Reports about security issues can be made via `Tidelift <https://tidelift.com/security>`_.


Issues & Limitations
~~~~~~~~~~~~~~~~~~~~

- This project is in maintenance mode. Projects using Python 3.9 or later
  are best served by using the timezone functionaly now included in core
  Python and packages that work with it such as `tzdata <https://pypi.org/project/tzdata/>`_.

- Offsets from UTC are rounded to the nearest whole minute, so timezones
  such as Europe/Amsterdam pre 1937 will be up to 30 seconds out. This
  was a limitation of the Python datetime library.

- If you think a timezone definition is incorrect, I probably can't fix
  it. pytz is a direct translation of the Olson timezone database, and
  changes to the timezone definitions need to be made to this source.
  If you find errors they should be reported to the time zone mailing
  list, linked from http://www.iana.org/time-zones.


Further Reading
~~~~~~~~~~~~~~~

More info than you want to know about timezones:
https://data.iana.org/time-zones/tz-link.html


Contact
~~~~~~~

Stuart Bishop <stuart@stuartbishop.net>
```
```bash
./.venv/lib/python3.9/site-packages/iniconfig-2.0.0.dist-info/RECORD
```
```
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/iniconfig/__init__.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/iniconfig/_parse.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/iniconfig/_version.cpython-39.pyc,,
../../../../../../Library/Caches/com.apple.python/Users/sumeet/projects/LLMContextProviders/.venv/lib/python3.9/site-packages/iniconfig/exceptions.cpython-39.pyc,,
iniconfig-2.0.0.dist-info/INSTALLER,sha256=zuuue4knoyJ-UwPPXg8fezS7VCrXJQrAP7zeNuwvFQg,4
iniconfig-2.0.0.dist-info/METADATA,sha256=2KcBd5DEFiZclO-ruP_qzN71qcTL0hNsCw5MCDIPN6I,2599
iniconfig-2.0.0.dist-info/RECORD,,
iniconfig-2.0.0.dist-info/WHEEL,sha256=hKi7AIIx6qfnsRbr087vpeJnrVUuDokDHZacPPMW7-Y,87
iniconfig-2.0.0.dist-info/licenses/LICENSE,sha256=KvaAw570k_uCgwNW0dPfGstaBgM8ui3sehniHKp3qGY,1061
iniconfig/__init__.py,sha256=ALJSNenAgTD7RNj820NggEQuyaZp2QseTCThGJPavk0,5473
iniconfig/_parse.py,sha256=OWGLbmE8GjxcoMWTvnGbck1RoNsTm5bt5ficIRZqWJ8,2436
iniconfig/_version.py,sha256=WM8rOXoL5t25aMQJp4qbU2XP09nrDtmDnrAGhHSk0Wk,160
iniconfig/exceptions.py,sha256=3V2JS5rndwiYUh84PNYS_1zd8H8IB-Rar81ARAA7E9s,501
iniconfig/py.typed,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
```
```bash
./.venv/lib/python3.9/site-packages/iniconfig-2.0.0.dist-info/licenses/LICENSE
```
```

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:
     
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
 
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
```
```bash
./.venv/lib/python3.9/site-packages/iniconfig-2.0.0.dist-info/WHEEL
```
```
Wheel-Version: 1.0
Generator: hatchling 1.12.2
Root-Is-Purelib: true
Tag: py3-none-any
```
```bash
./.venv/lib/python3.9/site-packages/iniconfig-2.0.0.dist-info/INSTALLER
```
```
pip
```
```bash
./.venv/lib/python3.9/site-packages/iniconfig-2.0.0.dist-info/METADATA
```
```
Metadata-Version: 2.1
Name: iniconfig
Version: 2.0.0
Summary: brain-dead simple config-ini parsing
Project-URL: Homepage, https://github.com/pytest-dev/iniconfig
Author-email: Ronny Pfannschmidt <opensource@ronnypfannschmidt.de>, Holger Krekel <holger.krekel@gmail.com>
License-Expression: MIT
License-File: LICENSE
Classifier: Development Status :: 4 - Beta
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: MIT License
Classifier: Operating System :: MacOS :: MacOS X
Classifier: Operating System :: Microsoft :: Windows
Classifier: Operating System :: POSIX
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3 :: Only
Classifier: Programming Language :: Python :: 3.7
Classifier: Programming Language :: Python :: 3.8
Classifier: Programming Language :: Python :: 3.9
Classifier: Programming Language :: Python :: 3.10
Classifier: Programming Language :: Python :: 3.11
Classifier: Topic :: Software Development :: Libraries
Classifier: Topic :: Utilities
Requires-Python: >=3.7
Description-Content-Type: text/x-rst

iniconfig: brain-dead simple parsing of ini files
=======================================================

iniconfig is a small and simple INI-file parser module
having a unique set of features:

* maintains order of sections and entries
* supports multi-line values with or without line-continuations
* supports "#" comments everywhere
* raises errors with proper line-numbers
* no bells and whistles like automatic substitutions
* iniconfig raises an Error if two sections have the same name.

If you encounter issues or have feature wishes please report them to:

    https://github.com/RonnyPfannschmidt/iniconfig/issues

Basic Example
===================================

If you have an ini file like this:

.. code-block:: ini

    # content of example.ini
    [section1] # comment
    name1=value1  # comment
    name1b=value1,value2  # comment

    [section2]
    name2=
        line1
        line2

then you can do:

.. code-block:: pycon

    >>> import iniconfig
    >>> ini = iniconfig.IniConfig("example.ini")
    >>> ini['section1']['name1'] # raises KeyError if not exists
    'value1'
    >>> ini.get('section1', 'name1b', [], lambda x: x.split(","))
    ['value1', 'value2']
    >>> ini.get('section1', 'notexist', [], lambda x: x.split(","))
    []
    >>> [x.name for x in list(ini)]
    ['section1', 'section2']
    >>> list(list(ini)[0].items())
    [('name1', 'value1'), ('name1b', 'value1,value2')]
    >>> 'section1' in ini
    True
    >>> 'inexistendsection' in ini
    False
```
```bash
./.venv/lib/python3.9/site-packages/pytz/zoneinfo/Indian/Mauritius
```
```
TZif2âòÌ@€r0Iñ‡IŒè–5ËFP8@LMT+05+04TZif2ˇˇˇˇâòÌ@€r0Iñ‡IŒè–5ËFP8@LMT+05+04
<+04>-4
```
```bash
./.venv/lib/python3.9/site-packages/pytz/zoneinfo/Indian/Chagos
```
```
TZif2â~˜ú0Ê›∞C‰FPT`LMT+05+06TZif2ˇˇˇˇâ~˜ú0Ê›∞C‰FPT`LMT+05+06
<+06>-6
```
```bash
./.venv/lib/python3.9/site-packages/pytz/zoneinfo/Indian/Mayotte
```
```
TZif2ãˇ—¸±Ó⁄X¥«‡–¡Ì≠XÃlz‘"Ñ#(*0
&¨*0
LMT+0230EAT+0245TZif2ˇˇˇˇãˇ—¸ˇˇˇˇ±Ó⁄Xˇˇˇˇ¥«‡–ˇˇˇˇ¡Ì≠XˇˇˇˇÃlz‘"Ñ#(*0
&¨*0
LMT+0230EAT+0245
EAT-3
```
```bash
./.venv/lib/python3.9/site-packages/pytz/zoneinfo/Indian/Christmas
```
```
TZif2Ä¢jgƒ^<^<bpLMTBMT+07TZif2ˇˇˇˇV∂Öƒˇˇˇˇ¢jgƒ^<^<bpLMTBMT+07
<+07>-7
```
```bash
./.venv/lib/python3.9/site-packages/pytz/zoneinfo/Indian/Cocos
```
```
TZif2Ä°ÚsQÀÚ¸—ögZ/Z/[h~ê[hLMTRMT+0630+09TZif2ˇˇˇˇV∂â—ˇˇˇˇ°ÚsQˇˇˇˇÀÚ¸ˇˇˇˇ—ögZ/Z/[h~ê[hLMTRMT+0630+09
<+0630>-6:30
```
```bash
./.venv/lib/python3.9/site-packages/pytz/zoneinfo/Indian/Maldives
```
```
TZif2ÄÌ/√òDËDËFPLMTMMT+05TZif2ˇˇˇˇV∂üˇˇˇˇÌ/√òDËDËFPLMTMMT+05
<+05>-5
```
```bash
./.venv/lib/python3.9/site-packages/pytz/zoneinfo/Indian/Comoro
```
```
TZif2ãˇ—¸±Ó⁄X¥«‡–¡Ì≠XÃlz‘"Ñ#(*0
&¨*0
LMT+0230EAT+0245TZif2ˇˇˇˇãˇ—¸ˇˇˇˇ±Ó⁄Xˇˇˇˇ¥«‡–ˇˇˇˇ¡Ì≠XˇˇˇˇÃlz‘"Ñ#(*0
&¨*0
LMT+0230EAT+0245
EAT-3
```
```bash
./.venv/lib/python3.9/site-packages/pytz/zoneinfo/Indian/Reunion
```
```
TZif2°Úô®3ÿ8@LMT+04TZif2ˇˇˇˇ°Úô®3ÿ8@LMT+04
<+04>-4
```
```bash
./.venv/lib/python3.9/site-packages/pytz/zoneinfo/Indian/Mahe
```
```
TZif2°Úô®3ÿ8@LMT+04TZif2ˇˇˇˇ°Úô®3ÿ8@LMT+04
<+04>-4
```
```bash
./.venv/lib/python3.9/site-packages/pytz/zoneinfo/Indian/Kerguelen
```
```
TZif2ÄÌ/√òDËDËFPLMTMMT+05TZif2ˇˇˇˇV∂üˇˇˇˇÌ/√òDËDËFPLMTMMT+05
<+05>-5
```
```bash
./.venv/lib/python3.9/site-packages/pytz/zoneinfo/Indian/Antananarivo
```
```
TZif2ãˇ—¸±Ó⁄X¥«‡–¡Ì≠XÃlz‘"Ñ#(*0
&¨*0
LMT+0230EAT+0245TZif2ˇˇˇˇãˇ—¸ˇˇˇˇ±Ó⁄Xˇˇˇˇ¥«‡–ˇˇˇˇ¡Ì≠XˇˇˇˇÃlz‘"Ñ#(*0
&¨*0
LMT+0230EAT+0245
EAT-3
```
```bash
./.venv/lib/python3.9/site-packages/pytz/zoneinfo/Atlantic/Faroe
```
```
TZif2s
ãm§X#Îê‹êÕêÛæê„Øê”†ê√ëêºΩ¨Æúüåê|Å lr!