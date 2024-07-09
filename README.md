# LLM Context Providers

LLM Context Providers package for extracting context from various sources like Asana, Quip, OneNote, Outlook Calendar, and more.

## Installation

```bash
pip install LLMContextProviders
```

## Configuration

Create a `config.yml` file in the root of your project directory with the following content:

```yaml
context_providers:
  asana:
    enabled: true
    project_id: "your_project_id"
  # Add other context providers here
```

Create a `.env` file in the root of your project directory to store sensitive information:

```
ASANA_PERSONAL_ACCESS_TOKEN=your_asana_personal_access_token
QUIP_ACCESS_TOKEN=your_quip_access_token
ONENOTE_CLIENT_ID=your_onenote_client_id
ONENOTE_CLIENT_SECRET=your_onenote_client_secret
OUTLOOK_CLIENT_ID=your_outlook_client_id
OUTLOOK_CLIENT_SECRET=your_outlook_client_secret
```

Ensure that the `.env` file is listed in your `.gitignore` to prevent it from being tracked by Git:

```bash
echo ".env" >> .gitignore
```

## Usage

### Asynchronous Fetching

#### Fetching All Providers

```python
from llm_context_providers import ContextManager
import asyncio

async def main_async():
    manager = ContextManager(config_file='config.yml')
    await manager.fetch_contexts_async()
    context = manager.get_combined_context()
    print("Async Fetch Context (All):\n", context)

if __name__ == "__main__":
    asyncio.run(main_async())
```

#### Fetching Specific Providers

```python
from llm_context_providers import ContextManager
import asyncio

async def main_async_specific():
    manager = ContextManager(config_file='config.yml')
    await manager.fetch_contexts_async(providers=['asana'])
    context = manager.get_combined_context(providers=['asana'])
    print("Async Fetch Context (Specific):\n", context)

if __name__ == "__main__":
    asyncio.run(main_async_specific())
```

### Synchronous Fetching

#### Fetching All Providers

```python
from llm_context_providers import ContextManager

def main_sync():
    manager = ContextManager(config_file='config.yml')
    manager.fetch_contexts()
    context = manager.get_combined_context()
    print("Sync Fetch Context (All):\n", context)

if __name__ == "__main__":
    main_sync()
```

#### Fetching Specific Providers

```python
from llm_context_providers import ContextManager

def main_sync_specific():
    manager = ContextManager(config_file='config.yml')
    manager.fetch_contexts(providers=['asana'])
    context = manager.get_combined_context(providers=['asana'])
    print("Sync Fetch Context (Specific):\n", context)

if __name__ == "__main__":
    main_sync_specific()
```

## Development

### Setting Up for Development

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/LLMContextProviders.git
cd LLMContextProviders
```

2. **Set Up a Virtual Environment and Install Dependencies**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
pip install -r requirements.txt
pip install -e .
```

3. **Create a Configuration File**

Create a `config.yml` file in the root of your project directory with the appropriate settings for your context providers.

4. **Create a .env File**

Create a `.env` file in the root of your project directory with the credentials for your context providers.

5. **Run Tests**

```bash
pytest
```

### Running the Test App

Create a `test_app.py` file:

```python
# test_app.py
from llm_context_providers import ContextManager
import asyncio

async def main_async():
    manager = ContextManager(config_file='config.yml')
    await manager.fetch_contexts_async()
    context = manager.get_combined_context()
    print("Async Fetch Context (All):\n", context)

async def main_async_specific():
    manager = ContextManager(config_file='config.yml')
    await manager.fetch_contexts_async(providers=['asana'])
    context = manager.get_combined_context(providers=['asana'])
    print("Async Fetch Context (Specific):\n", context)

def main_sync():
    manager = ContextManager(config_file='config.yml')
    manager.fetch_contexts()
    context = manager.get_combined_context()
    print("Sync Fetch Context (All):\n", context)

def main_sync_specific():
    manager = ContextManager(config_file='config.yml')
    manager.fetch_contexts(providers=['asana'])
    context = manager.get_combined_context(providers=['asana'])
    print("Sync Fetch Context (Specific):\n", context)

if __name__ == "__main__":
    print("Testing Async Fetch (All):")
    asyncio.run(main_async())
    print("\nTesting Async Fetch (Specific):")
    asyncio.run(main_async_specific())
    print("\nTesting Sync Fetch (All):")
    main_sync()
    print("\nTesting Sync Fetch (Specific):")
    main_sync_specific()
```

Run the test app:

```bash
python test_app.py
```

## License

MIT License
