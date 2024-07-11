import os
import asana
from asana.rest import ApiException
from datetime import datetime
from dateutil import parser
import pytz
import time
from .context_provider import ContextProvider, Status

DEFAULT_TASK_FIELDS = {
    "Task": "name",
    "Task ID": "gid",
    "Created At": "created_at",
    "Modified At": "modified_at",
    "Completed": "completed",
    "Assignee": "assignee",
    "Due On": "due_on",
    "Notes": "notes"
}

class AsanaContextProvider(ContextProvider):
    def __init__(self, project_id, fields=None, timezone="America/Toronto", **kwargs):
        super().__init__()
        self.personal_access_token = os.getenv('ASANA_PERSONAL_ACCESS_TOKEN')
        self.project_id = project_id
        self.fields = fields or DEFAULT_TASK_FIELDS
        self.TIMEZONE = timezone

        if not self.personal_access_token:
            raise ValueError("Asana personal access token is not set. Please ensure it is defined in the .env file.")

        if not self.project_id:
            raise ValueError("Asana project ID is not set. Please ensure it is defined in the config.yml file.")

        configuration = asana.Configuration()
        configuration.access_token = self.personal_access_token
        self.api_client = asana.ApiClient(configuration)
        self.projects_api = asana.ProjectsApi(self.api_client)
        self.tasks_api = asana.TasksApi(self.api_client)
        self.stories_api = asana.StoriesApi(self.api_client)

    async def fetch_context_async(self, full_fetch: bool = False):
        self.update_status(Status.FETCHING)
        try:
            project = await self.get_project_info()
            if project:
                tasks = await self.get_tasks_info()
                formatter = MarkdownFormatter()
                self.context_info = formatter.generate_project_markdown(project, tasks, self.fields, self.TIMEZONE)
                self.update_status(Status.FRESH)
            else:
                self.update_status(Status.STALE)
        except Exception as e:
            self.update_status(Status.STALE)
            raise RuntimeError(f"Failed to fetch context: {e}")

    def fetch_context(self, full_fetch: bool = False):
        self.update_status(Status.FETCHING)
        try:
            project = self.get_project_info_sync()
            if project:
                tasks = self.get_tasks_info_sync()
                formatter = MarkdownFormatter()
                self.context_info = formatter.generate_project_markdown(project, tasks, self.fields, self.TIMEZONE)
                self.update_status(Status.FRESH)
            else:
                self.update_status(Status.STALE)
        except Exception as e:
            self.update_status(Status.STALE)
            raise RuntimeError(f"Failed to fetch context: {e}")

    def get_context(self):
        return self.context_info

    async def get_project_info(self, retries=3, delay=2):
        for attempt in range(retries):
            try:
                project = self.projects_api.get_project(self.project_id, {})
                return project
            except ApiException as e:
                if e.status == 503 and attempt < retries - 1:
                    print(f"Service unavailable, retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    raise RuntimeError(f"Exception when calling ProjectsApi->get_project: {e}")

    def get_project_info_sync(self, retries=3, delay=2):
        for attempt in range(retries):
            try:
                project = self.projects_api.get_project(self.project_id, {})
                return project
            except ApiException as e:
                if e.status == 503 and attempt < retries - 1:
                    print(f"Service unavailable, retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    raise RuntimeError(f"Exception when calling ProjectsApi->get_project: {e}")

    async def get_tasks_info(self, retries=3, delay=2):
        for attempt in range(retries):
            try:
                tasks = self.tasks_api.get_tasks_for_project(self.project_id, {"opt_fields": ",".join(self.fields.values())})
                tasks_info = []
                for task in tasks:
                    task_info = self.tasks_api.get_task(task['gid'], {"opt_fields": ",".join(self.fields.values())})
                    stories = self.stories_api.get_stories_for_task(task['gid'], {})
                    task_info['stories'] = list(stories)  # Convert generator to list
                    tasks_info.append(task_info)
                return tasks_info
            except ApiException as e:
                if e.status == 503 and attempt < retries - 1:
                    print(f"Service unavailable, retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    raise RuntimeError(f"Exception when calling TasksApi->get_tasks: {e}")

    def get_tasks_info_sync(self, retries=3, delay=2):
        for attempt in range(retries):
            try:
                tasks = self.tasks_api.get_tasks_for_project(self.project_id, {"opt_fields": ",".join(self.fields.values())})
                tasks_info = []
                for task in tasks:
                    task_info = self.tasks_api.get_task(task['gid'], {"opt_fields": ",".join(self.fields.values())})
                    stories = self.stories_api.get_stories_for_task(task['gid'], {})
                    task_info['stories'] = list(stories)  # Convert generator to list
                    tasks_info.append(task_info)
                return tasks_info
            except ApiException as e:
                if e.status == 503 and attempt < retries - 1:
                    print(f"Service unavailable, retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    raise RuntimeError(f"Exception when calling TasksApi->get_tasks: {e}")

    async def index_context(self):
        self.update_status(Status.INDEXING)
        # Implement indexing logic for Asana context
        self.update_status(Status.FRESH)

    async def search_index(self, query: str):
        # Implement search logic for Asana context
        search_results = "Asana search results"  # Replace with actual search logic
        return search_results

    def load_from_index(self, search_results):
        # Implement logic to load search results into context
        self.context_info = search_results

class MarkdownFormatter:
    @staticmethod
    def heading1(text):
        return f"# {text}\n"

    @staticmethod
    def heading2(text):
        return f"## {text}\n"

    @staticmethod
    def heading3(text):
        return f"### {text}\n"

    @staticmethod
    def heading4(text):
        return f"#### {text}\n"

    @staticmethod
    def bold(text):
        return f"**{text}**"

    @staticmethod
    def list_item(text):
        return f"- {text}\n"

    @staticmethod
    def format_field(field, value):
        return f"{MarkdownFormatter.bold(field)}: {value}\n"

    @staticmethod
    def format_date(date_str, timezone):
        if date_str:
            date = parser.parse(date_str)
            date = date.astimezone(pytz.timezone(timezone))
            return date.strftime('%B %-dth, %Y %-I:%M %p')
        return 'N/A'

    def generate_project_markdown(self, project, tasks, task_fields, timezone):
        markdown = ""
        markdown += self.heading1(f"Project: {project['name']}")
        markdown += self.format_field("Project ID", project['gid'])
        markdown += self.format_field("Created At", self.format_date(project['created_at'], timezone))
        markdown += self.format_field("Modified At", self.format_date(project['modified_at'], timezone))
        markdown += self.format_field("Owner", project['owner']['name'] if project['owner'] else 'N/A')
        markdown += self.format_field("Notes", project['notes'])
        markdown += self.format_field("Start On", project.get('start_on', 'N/A'))
        markdown += self.format_field("Due On", project.get('due_on', 'N/A'))
        markdown += "\n"
        markdown += self.heading2("Tasks")

        for task in tasks:
            markdown += self.heading3(f"Task: {task['name']}")
            for field_name, field in task_fields.items():
                value = task.get(field, 'N/A')
                if field in ['created_at', 'modified_at', 'due_on']:
                    value = self.format_date(value, timezone)
                elif field == 'assignee':
                    value = value.get('name', 'N/A') if isinstance(value, dict) else 'N/A'
                markdown += self.format_field(field_name, value)
            markdown += self.heading4("Stories")

            for story in task['stories']:
                story_text = f"{self.format_date(story['created_at'], timezone)} by {story['created_by']['name']}: {story['text']}"
                markdown += self.list_item(story_text)
            markdown += "\n"  # Blank line after each task

        return markdown
