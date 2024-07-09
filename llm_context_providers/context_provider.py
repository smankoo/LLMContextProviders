from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

class Status(Enum):
    FRESH = "fresh"
    STALE = "stale"
    FETCHING = "fetching"
    INDEXING = "indexing"

class ContextProvider(ABC):
    _registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry[cls.__name__] = cls

    def __init__(self):
        self.status = Status.STALE
        self.last_updated = None
        self.context_info = None

    @classmethod
    def get_provider_class(cls, name):
        return cls._registry.get(name)

    @abstractmethod
    async def fetch_context_async(self, full_fetch: bool = False):
        pass

    def fetch_context(self, full_fetch: bool = False):
        import asyncio
        asyncio.run(self.fetch_context_async(full_fetch))

    def provide_status(self):
        return {
            'status': self.status.value,
            'last_updated': self.last_updated
        }

    def update_status(self, status: Status):
        self.status = status
        self.last_updated = datetime.now()

    @abstractmethod
    def get_context(self):
        return self.context_info

    @abstractmethod
    async def index_context(self):
        pass

    @abstractmethod
    async def search_index(self, query: str):
        pass

    @abstractmethod
    def load_from_index(self, search_results):
        pass
