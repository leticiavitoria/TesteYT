"""
Core components do sistema de análise vetorial.
"""

from .vector_analyzer import AdaptiveVectorAnalyzer
from .pattern_discovery import PatternDiscoveryEngine
from .similarity_search import SimilaritySearchEngine

__all__ = [
    'AdaptiveVectorAnalyzer',
    'PatternDiscoveryEngine',
    'SimilaritySearchEngine'
]
