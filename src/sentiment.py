import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def ensure_vader_downloaded():
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        nltk.download('vader_lexicon')

def compute_vader_sentiment(text: str) -> float:
    """Return compound VADER sentiment in [-1, 1]."""
    if not isinstance(text, str) or not text.strip():
        return 0.0
    ensure_vader_downloaded()
    sia = SentimentIntensityAnalyzer()
    return float(sia.polarity_scores(text)['compound'])
