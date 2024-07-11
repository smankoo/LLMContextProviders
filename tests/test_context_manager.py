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
