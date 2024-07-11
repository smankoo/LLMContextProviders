Sure, here is the revised README with a more focused quick start section and a separate section demonstrating the full functionality:

---

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

## Quick Start

Create an `app.py` file with the following content to quickly get started:

```python
import yaml
from llm_context_providers import ContextManager

# Load configuration from YAML file
def load_config(config_file='config.yml'):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

# Fetch contexts synchronously and print the combined context
def main_sync(config):
    manager = ContextManager(config['context_providers'])
    manager.fetch_contexts()
    context = manager.get_combined_context()
    print("Sync Fetch Context (All):\n", context)

if __name__ == "__main__":
    config = load_config()
    main_sync(config)
```

Run the application:

```bash
python app.py
```

## Full Functionality

### Asynchronous and Specific Context Fetching

Update your `app.py` to demonstrate the full functionality, including asynchronous and specific context fetching:

```python
import yaml
import asyncio
from llm_context_providers import ContextManager

# Load configuration from YAML file
def load_config(config_file='config.yml'):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

# Fetch contexts asynchronously and print the combined context
async def main_async(config):
    manager = ContextManager(config['context_providers'])
    await manager.fetch_contexts_async()
    context = manager.get_combined_context()
    print("Async Fetch Context (All):\n", context)

# Fetch specific context asynchronously and print the combined context
async def main_async_specific(config):
    manager = ContextManager(config['context_providers'])
    await manager.fetch_contexts_async(providers=['asana'])
    context = manager.get_combined_context(providers=['asana'])
    print("Async Fetch Context (Specific):\n", context)

# Fetch contexts synchronously and print the combined context
def main_sync(config):
    manager = ContextManager(config['context_providers'])
    manager.fetch_contexts()
    context = manager.get_combined_context()
    print("Sync Fetch Context (All):\n", context)

# Fetch specific context synchronously and print the combined context
def main_sync_specific(config):
    manager = ContextManager(config['context_providers'])
    manager.fetch_contexts(providers=['asana'])
    context = manager.get_combined_context(providers=['asana'])
    print("Sync Fetch Context (Specific):\n", context)

if __name__ == "__main__":
    config = load_config()

    print("Running Async Fetch (All):")
    asyncio.run(main_async(config))

    print("\nRunning Async Fetch (Specific):")
    asyncio.run(main_async_specific(config))

    print("\nRunning Sync Fetch (All):")
    main_sync(config)

    print("\nRunning Sync Fetch (Specific):")
    main_sync_specific(config)
```

Run the application:

```bash
python app.py
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

## Contributing

Contributions are welcome! Please create a pull request or raise an issue to discuss your ideas.

## License

This project is licensed under the MIT License.

---

This revised README provides a clear and concise guide for developers to quickly get started with using the package, along with a separate section for demonstrating the full functionality.