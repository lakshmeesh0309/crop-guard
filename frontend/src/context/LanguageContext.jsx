import React, { createContext, useContext, useState, useEffect } from 'react';
import en from '../translations/en.json';
import hi from '../translations/hi.json';
import te from '../translations/te.json';

const LanguageContext = createContext();

const translations = { en, hi, te };

export const LanguageProvider = ({ children }) => {
  const [lang, setLangState] = useState(() => {
    return localStorage.getItem('cropguard_lang') || 'en';
  });

  const setLang = (newLang) => {
    if (translations[newLang]) {
      setLangState(newLang);
    }
  };

  useEffect(() => {
    localStorage.setItem('cropguard_lang', lang);
  }, [lang]);

  /**
   * Translates a dot-notated key. E.g. t("dashboard.welcome", { name: "User" })
   */
  const t = (key, replacements = {}) => {
    const keys = key.split('.');
    
    // Resolve in active language
    let resolved = translations[lang];
    for (const k of keys) {
      if (resolved && resolved[k] !== undefined) {
        resolved = resolved[k];
      } else {
        resolved = null;
        break;
      }
    }
    
    // Fallback to English if not found
    if (!resolved && lang !== 'en') {
      resolved = translations['en'];
      for (const k of keys) {
        if (resolved && resolved[k] !== undefined) {
          resolved = resolved[k];
        } else {
          resolved = null;
          break;
        }
      }
    }
    
    // Final fallback to the key string
    if (!resolved) {
      return keys[keys.length - 1];
    }
    
    // Apply string replacements
    if (typeof resolved === 'string') {
      let result = resolved;
      Object.entries(replacements).forEach(([param, value]) => {
        result = result.replace(`{${param}}`, value);
      });
      return result;
    }
    
    return resolved;
  };

  return (
    <LanguageContext.Provider value={{ lang, setLang, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => useContext(LanguageContext);
