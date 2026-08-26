"""
AIRecommendationService
------------------------
Abstraction layer reserved for future AI-powered features (AI resume
analysis, AI career recommendations, AI roadmap generation, job
description analysis, AI career assistant, resume improvement
suggestions).

The current, deterministic version of SkillGap AI does NOT call any
external AI API and does not require one to function. This class
exists so a future AI provider (e.g. an LLM API) can be plugged in
without changing the rest of the application.
"""


class AIRecommendationService:
    def __init__(self, provider=None):
        # provider: an object implementing .generate(prompt) -> str
        # Left as None until an AI provider is configured.
        self.provider = provider

    def is_enabled(self):
        return self.provider is not None

    def suggest_career_advice(self, analysis):
        """Placeholder for future AI-generated career advice.

        Returns None when no provider is configured so callers can
        gracefully fall back to the deterministic roadmap/analysis only.
        """
        if not self.is_enabled():
            return None
        # Future implementation would call self.provider.generate(...)
        return None
