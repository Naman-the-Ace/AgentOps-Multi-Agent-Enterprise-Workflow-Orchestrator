"""Opt-in anonymous telemetry — minimal, PII-clean, webhook-agnostic."""

from agentops.telemetry.emitter import (
    TelemetryEmitter,
    emit,
    get_emitter,
)

__all__ = ["TelemetryEmitter", "emit", "get_emitter"]
