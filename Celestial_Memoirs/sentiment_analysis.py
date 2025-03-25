import os
from typing import Literal, Optional
from groq import Groq

class SentimentAnalyzer:
    """A class to analyze text sentiment using Groq's LLM API."""
    
    def __init__(self):
        """
        Initialize the sentiment analyzer with Groq API credentials.
        
        Args:
            api_key: Groq API key. If not provided, will look for GROQ_API_KEY environment variable.
        """
        self.api_key = os.environ.get("GROQ_API_KEY") 
        if not self.api_key:
            raise ValueError("Groq API key must be provided or set as GROQ_API_KEY environment variable")
        
        self.client = Groq(api_key=self.api_key)
    
    def analyze_sentiment(self, text: str) -> Literal["Happy", "Sad", "Neutral"]:
        """
        Analyze the sentiment of the given text using Groq's LLM.
        
        Args:
            text: The text to analyze
            
        Returns:
            One of "Happy", "Sad", or "Neutral"
        
        Raises:
            Exception: If there's an error communicating with the Groq API
        """
        try:
            prompt = f"""Analyze the sentiment of the following text and respond with exactly one word - either 'Happy', 'Sad', or 'Neutral':
            
            Text: {text}
            
            Sentiment:"""
            
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="mixtral-8x7b-32768",  # You can also use other available models
                temperature=0,  # Use 0 for more consistent results
                max_tokens=1    # We only need one word
            )
            
            sentiment = response.choices[0].message.content.strip()
            
            # Ensure we get one of our expected values
            if sentiment.lower() not in ["happy", "sad", "neutral"]:
                return "Neutral"  # Default to neutral if we get an unexpected response
                
            return sentiment.capitalize()
            
        except Exception as e:
            raise Exception(f"Error analyzing sentiment: {str(e)}")

# Example usage
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    
    # Example texts
    texts = [
        "I love this product! It's amazing!",
        "This is the worst experience ever.",
        "The weather is quite normal today."
    ]
    
    for text in texts:
        sentiment = analyzer.analyze_sentiment(text)
        print(f"Text: {text}")
        print(f"Sentiment: {sentiment}\n")
