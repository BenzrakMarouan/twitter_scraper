from langdetect import detect, LangDetectException
import stopwordsiso as stopwords
import re

def preprocess_text(text):
    # Detect language
    try:
        lang = detect(text)
    except LangDetectException:
        lang = 'en'  # Default to English if detection fails

    # Tokenize and remove stop words
    words = re.findall(r'\b\w+\b', text.lower())
    filtered_words = [word for word in words if word not in stopwords.stopwords(lang)]

    # Reconstruct the sentence
    filtered_text = ' '.join(filtered_words)
    return filtered_text, lang
