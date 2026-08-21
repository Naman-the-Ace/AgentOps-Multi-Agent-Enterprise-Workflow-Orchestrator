"""Workflow template marketplace — discover, validate, install templates."""

from agentops.marketplace.registry import (
    TemplateManifest,
    TemplateRegistry,
    get_registry,
)

__all__ = ["TemplateManifest", "TemplateRegistry", "get_registry"]
