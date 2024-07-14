import yaml
import asyncio
from llm_context_providers import ContextManager

def load_config(config_file='config.yml'):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

async def main_async(config):
    manager = ContextManager(config)
    await manager.fetch_contexts_async()
    context = manager.get_combined_context()
    print("Async Fetch Context (All):\n", context)

async def main_async_specific(config):
    manager = ContextManager(config)
    await manager.fetch_contexts_async(providers=['asana'])
    context = manager.get_combined_context(providers=['asana'])
    print("Async Fetch Context (Specific):\n", context)

def main_sync(config):
    manager = ContextManager(config)
    manager.fetch_contexts()
    context = manager.get_combined_context()
    print("Sync Fetch Context (All):\n", context)

def main_sync_specific(config):
    manager = ContextManager(config)
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
