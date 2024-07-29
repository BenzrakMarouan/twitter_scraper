from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from langdetect import detect, LangDetectException
from preprocessing import preprocess_text

def analyze_sentiment(text):
    # Preprocess text and detect language
    try:
        filtered_text, lang = preprocess_text(text)
    except LangDetectException:
        filtered_text, lang = text, 'en'  # Default to English if detection fails

    # Use VADER for English
    if lang == 'en':
        analyzer = SentimentIntensityAnalyzer()
        sentiment = analyzer.polarity_scores(filtered_text)
        return sentiment['compound']  # Return the compound score as a measure of sentiment
    
    # Use TextBlob for other languages
    else:
        blob = TextBlob(filtered_text)
        try:
            if lang != 'en':
                blob = blob.translate(to='en')
            sentiment = blob.sentiment.polarity
        except Exception as e:
            # If translation or sentiment analysis fails, return neutral sentiment
            sentiment = 0.0
        return sentiment
