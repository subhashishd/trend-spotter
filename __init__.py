# This file makes trend_spotter a Python package

"""Trend Spotter package initialization."""

__version__ = "0.1.0"
__author__ = "Your Name"

# Import and expose the root_agent for ADK discovery
# Only import when not running tests to avoid import issues
try:
    from agent import root_agent  # noqa: F401
except ImportError:
    # During testing or when dependencies aren't available,
    # skip the import to allow basic package functionality
    pass
