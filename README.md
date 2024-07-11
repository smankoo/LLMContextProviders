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
    print("Async Fetch Context:\n", context)

asyncio.run(fetch_async())
```

### Fetching Context Synchronously

```python
manager.fetch_contexts()
context = manager.get_combined_context()
print("Sync Fetch Context:\n", context)
```

### Fetching Specific Context Providers

#### Asynchronously

```python
async def fetch_specific_async():
    await manager.fetch_contexts_async(providers=['asana'])
    context = manager.get_combined_context(providers=['asana'])
    print("Async Fetch Specific Context:\n", context)

asyncio.run(fetch_specific_async())
```

#### Synchronously

```python
manager.fetch_contexts(providers=['asana'])
context = manager.get_combined_context(providers=['asana'])
print("Sync Fetch Specific Context:\n", context)
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
    print("Async Fetch Context (All):\n", context)

async def main_async_specific(config):
    manager = ContextManager(config['context_providers'])
    await manager.fetch_contexts_async(providers=['asana'])
    context = manager.get_combined_context(providers=['asana'])
    print("Async Fetch Context (Specific):\n", context)

def main_sync(config):
    manager = ContextManager(config['context_providers'])
    manager.fetch_contexts()
    context = manager.get_combined_context()
    print("Sync Fetch Context (All):\n", context)

def main_sync_specific(config):
    manager = ContextManager(config['context_providers'])
    manager.fetch_contexts(providers=['asana'])
    context = manager.get_combined_context(providers=['asana'])
    print("Sync Fetch Context (Specific):\n", context)

if __name__ == "__main__":
    config = load_config()

    print("Testing Async Fetch (All):")
    asyncio.run(main_async(config))

    print("\nTesting Async Fetch (Specific):")
    asyncio.run(main_async_specific(config))

    print("\nTesting Sync Fetch (All):")
    main_sync(config)

    print("\nTesting Sync Fetch (Specific):")
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
