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
    # print("\nTesting Async Fetch (Specific):")
    # asyncio.run(main_async_specific())
    # print("\nTesting Sync Fetch (All):")
    # main_sync()
    # print("\nTesting Sync Fetch (Specific):")
    main_sync_specific()
