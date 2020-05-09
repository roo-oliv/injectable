"""
Custom exceptions raised by injectable.
"""
from injectable.errors.autowiring_error import AutowiringError
from injectable.errors.injection_error import InjectionError

__all__ = [
    "AutowiringError",
    "InjectionError",
]
