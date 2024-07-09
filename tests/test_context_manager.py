import pytest
from unittest.mock import patch, MagicMock
from llm_context_providers import ContextManager

@pytest.mark.asyncio
async def test_fetch_all_contexts_async():
    with patch('llm_context_providers.context_manager.AsanaContextProvider') as MockAsana:
        mock_asana = MockAsana.return_value
        mock_asana.fetch_context_async = MagicMock()

        manager = ContextManager(config_file='llm_context_providers/config.yml')
        await manager.fetch_all_contexts_async()

        mock_asana.fetch_context_async.assert_called_once()

def test_fetch_all_contexts():
    with patch('llm_context_providers.context_manager.AsanaContextProvider') as MockAsana:
        mock_asana = MockAsana.return_value
        mock_asana.fetch_context = MagicMock()

        manager = ContextManager(config_file='llm_context_providers/config.yml')
        manager.fetch_all_contexts()

        mock_asana.fetch_context.assert_called_once()
