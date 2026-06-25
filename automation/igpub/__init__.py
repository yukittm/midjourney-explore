"""igpub — headless core for the IG publish pipeline.

No I/O assumptions in the domain/validation layer, so a CLI today and a UI later are both
thin callers of the same core (see automation/ig-publish-pipeline.md §Extensibility).
"""

__version__ = "0.1.0"
