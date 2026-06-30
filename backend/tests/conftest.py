"""Shared fixtures for backend tests."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import pytest
from backend.core.sympy_engine import SympyEngine
from backend.core.lean_bridge import LeanBridge
from backend.core.llm_engine import LLMEngine


@pytest.fixture
def sympy_engine():
    e = SympyEngine()
    e.reset_session()
    return e


@pytest.fixture
def lean_bridge():
    return LeanBridge()


@pytest.fixture
def llm_engine():
    return LLMEngine()
