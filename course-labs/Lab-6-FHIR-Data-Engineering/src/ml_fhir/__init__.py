import importlib.metadata
from importlib.metadata import PackageNotFoundError

try:
    __version__ = importlib.metadata.version("ml_fhir")
except PackageNotFoundError:
    __version__ = None
