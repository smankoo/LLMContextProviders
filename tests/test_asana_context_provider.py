import pytest
from unittest.mock import patch, MagicMock
from llm_context_providers import AsanaContextProvider

@pytest.mark.asyncio
async def test_fetch_context_async():
    provider = AsanaContextProvider(personal_access_token="dummy_token", project_id="dummy_project")

    with patch('llm_context_providers.asana_context_provider.projects_api.get_project') as mock_get_project,          patch('llm_context_providers.asana_context_provider.tasks_api.get_tasks_for_project') as mock_get_tasks_for_project,          patch('llm_context_providers.asana_context_provider.tasks_api.get_task') as mock_get_task,          patch('llm_context_providers.asana_context_provider.stories_api.get_stories_for_task') as mock_get_stories_for_task:

        mock_project = MagicMock()
        mock_project.return_value = {
            'name': 'Test Project',
            'gid': '12345',
            'created_at': '2023-07-08T00:00:00Z',
            'modified_at': '2023-07-08T00:00:00Z',
            'owner': {'name': 'Owner Name'},
            'notes': 'Project notes',
            'start_on': '2023-07-08',
            'due_on': '2023-07-08'
        }
        mock_get_project.return_value = mock_project.return_value

        mock_tasks = MagicMock()
        mock_tasks.return_value = [{
            'name': 'Test Task',
            'gid': '123',
            'created_at': '2023-07-08T00:00:00Z',
            'modified_at': '2023-07-08T00:00:00Z',
            'completed': False,
            'assignee': {'name': 'Assignee Name'},
            'due_on': '2023-07-08',
            'notes': 'Task notes'
        }]
        mock_get_tasks_for_project.return_value = mock_tasks.return_value

        mock_task = MagicMock()
        mock_task.return_value = {
            'name': 'Test Task',
            'gid': '123',
            'created_at': '2023-07-08T00:00:00Z',
            'modified_at': '2023-07-08T00:00:00Z',
            'completed': False,
            'assignee': {'name': 'Assignee Name'},
            'due_on': '2023-07-08',
            'notes': 'Task notes'
        }
        mock_get_task.return_value = mock_task.return_value

        mock_stories = MagicMock()
        mock_stories.return_value = [{
            'created_at': '2023-07-08T00:00:00Z',
            'created_by': {'name': 'Creator Name'},
            'text': 'Story text'
        }]
        mock_get_stories_for_task.return_value = mock_stories.return_value

        await provider.fetch_context_async()
        context = provider.get_context()

        assert context is not None
        assert provider.provide_status()['status'] == 'fresh'

def test_fetch_context_sync():
    provider = AsanaContextProvider(personal_access_token="dummy_token", project_id="dummy_project")

    with patch('llm_context_providers.asana_context_provider.projects_api.get_project') as mock_get_project,          patch('llm_context_providers.asana_context_provider.tasks_api.get_tasks_for_project') as mock_get_tasks_for_project,          patch('llm_context_providers.asana_context_provider.tasks_api.get_task') as mock_get_task,          patch('llm_context_providers.asana_context_provider.stories_api.get_stories_for_task') as mock_get_stories_for_task:

        mock_project = MagicMock()
        mock_project.return_value = {
            'name': 'Test Project',
            'gid': '12345',
            'created_at': '2023-07-08T00:00:00Z',
            'modified_at': '2023-07-08T00:00:00Z',
            'owner': {'name': 'Owner Name'},
            'notes': 'Project notes',
            'start_on': '2023-07-08',
            'due_on': '2023-07-08'
        }
        mock_get_project.return_value = mock_project.return_value

        mock_tasks = MagicMock()
        mock_tasks.return_value = [{
            'name': 'Test Task',
            'gid': '123',
            'created_at': '2023-07-08T00:00:00Z',
            'modified_at': '2023-07-08T00:00:00Z',
            'completed': False,
            'assignee': {'name': 'Assignee Name'},
            'due_on': '2023-07-08',
            'notes': 'Task notes'
        }]
        mock_get_tasks_for_project.return_value = mock_tasks.return_value

        mock_task = MagicMock()
        mock_task.return_value = {
            'name': 'Test Task',
            'gid': '123',
            'created_at': '2023-07-08T00:00:00Z',
            'modified_at': '2023-07-08T00:00:00Z',
            'completed': False,
            'assignee': {'name': 'Assignee Name'},
            'due_on': '2023-07-08',
            'notes': 'Task notes'
        }
        mock_get_task.return_value = mock_task.return_value

        mock_stories = MagicMock()
        mock_stories.return_value = [{
            'created_at': '2023-07-08T00:00:00Z',
            'created_by': {'name': 'Creator Name'},
            'text': 'Story text'
        }]
        mock_get_stories_for_task.return_value = mock_stories.return_value

        provider.fetch_context()
        context = provider.get_context()

        assert context is not None
        assert provider.provide_status()['status'] == 'fresh'
