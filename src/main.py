import importlib
import os

class ShortL:
    _available_services = None
    @staticmethod
    def shortener(service):
        if ShortL._available_services is None:
            ShortL._available_services = [f.replace('.py', '') for f in os.listdir(os.path.join(os.path.dirname(__file__), 'providers')) if f.endswith('.py')]
        provider_module_name = f"providers.{service}"
        try:
            provider_module = importlib.import_module(provider_module_name)
            for name, obj in provider_module.__dict__.items():
                if name.endswith("Shortener") and callable(obj):
                    return obj()
            raise ValueError(f"No valid shortener class found in module: {provider_module_name}")
        except ModuleNotFoundError:
             available_services = ", ".join(ShortL._available_services)
             raise ValueError(f"Service '{service}' not found. Available services: {available_services}")


if __name__ == '__main__':
    shortener = ShortL.shortener("ulvis")
    print(shortener.shorten("https://www.example.com"))
