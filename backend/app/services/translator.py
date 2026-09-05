import os
import json

_translations = {}

def load_translations(lang: str) -> dict:
    """Loads and caches translation dictionary for the given language."""
    lang = (lang or "en").lower()
    if lang in _translations:
        return _translations[lang]
        
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file_path = os.path.join(base_dir, "translations", f"{lang}.json")
    
    if not os.path.exists(file_path):
        # Fallback if specific file is not found
        if lang != "en":
            return load_translations("en")
        return {}
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            _translations[lang] = json.load(f)
    except Exception as e:
        print(f"[Translator] Error loading translations for {lang}: {e}")
        _translations[lang] = {}
        
    return _translations[lang]

def translate(key: str, category: str, lang: str = "en") -> str:
    """
    Translates a key in a category (e.g., 'crops', 'diseases', 'severity', 'ui') to the target language.
    Falls back to English if key is missing, then returns the key itself.
    """
    if not key:
        return ""
        
    lang = (lang or "en").lower()
    data = load_translations(lang)
    cat_data = data.get(category, {})
    
    if key in cat_data:
        return cat_data[key]
        
    # Fallback to English if target language doesn't have the translation
    if lang != "en":
        en_data = load_translations("en")
        en_cat = en_data.get(category, {})
        if key in en_cat:
            return en_cat[key]
            
    return key
