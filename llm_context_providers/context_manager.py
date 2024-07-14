import os
from dotenv import load_dotenv
from .context_provider import ContextProvider
from copy import deepcopy

class ContextManager:
    def __init__(self, config):
        load_dotenv()
        self.global_config = config.get('global', {})
        self.context_providers_config = config.get('context_providers', {})
        self.context_providers = self.initialize_providers()

    def initialize_providers(self):
        providers = {}
        for provider_name, provider_config in self.context_providers_config.items():
            if provider_config.get('enabled', False):
                provider_class = ContextProvider.get_provider_class(f"{provider_name.capitalize()}ContextProvider")
                if provider_class:
                    # Pass a copy of the config to avoid mutating the original
                    config_copy = deepcopy(provider_config)
                    config_copy.pop('enabled', None)
                    # Add global configuration to the context provider's configuration
                    config_copy.update(self.global_config)
                    providers[provider_name] = provider_class(**config_copy)
                else:
                    print(f"Warning: No context provider class found for {provider_name}")
        return providers

    async def fetch_contexts_async(self, providers=None):
        providers = providers or self.context_providers.keys()
        for provider_name in providers:
            if provider_name in self.context_providers:
                try:
                    await self.context_providers[provider_name].fetch_context_async()
                except ValueError as e:
                    print(f"Error in {provider_name} context provider: {e}")

    def fetch_contexts(self, providers=None):
        providers = providers or self.context_providers.keys()
        for provider_name in providers:
            if provider_name in self.context_providers:
                try:
                    self.context_providers[provider_name].fetch_context()
                except ValueError as e:
                    print(f"Error in {provider_name} context provider: {e}")

    def get_combined_context(self, providers=None):
        providers = providers or self.context_providers.keys()
        combined_context = ""
        for provider_name in providers:
            if provider_name in self.context_providers:
                context = self.context_providers[provider_name].get_context()
                if context:
                    combined_context += context + "\n"
        return combined_context

    def get_status(self, providers=None):
        providers = providers or self.context_providers.keys()
        status = {}
        for provider_name in providers:
            if provider_name in self.context_providers:
                status[provider_name] = self.context_providers[provider_name].provide_status()
        return status
