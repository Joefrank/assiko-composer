
import json
from pathlib import Path

class Translator:
    def __init__(self, root="translations", default_language="enGB"):
        self.languages = {}
        self.default_language = default_language

        root = Path(root)

        for lang_dir in root.iterdir():
            if not lang_dir.is_dir():
                continue

            translations = {}

            for file in lang_dir.glob("*.json"):
                with open(file, encoding="utf-8") as f:
                    translations.update(json.load(f))

            self.languages[lang_dir.name] = translations

    def t(self, key, lang=None):
        if lang is None:
            lang = self.default_language

        return self.languages.get(lang, {}).get(
            key,
            self.languages[lang].get(key, key)
        )