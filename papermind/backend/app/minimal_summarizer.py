# app/minimal_summarizer.py
import nltk
import re
from typing import List
from collections import Counter
import math

class MinimalSummarizer:
    """Ultra-lightweight extractive summarizer without ML models"""
    
    def __init__(self):
        """Initialize with NLTK data"""
        try:
            # Download required NLTK data (small)
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            from nltk.corpus import stopwords
            from nltk.tokenize import sent_tokenize, word_tokenize
            self.stopwords = set(stopwords.words('english'))
            self.sent_tokenize = sent_tokenize
            self.word_tokenize = word_tokenize
        except:
            # Fallback if NLTK fails
            self.stopwords = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
            self.sent_tokenize = lambda x: re.split(r'[.!?]+', x)
            self.word_tokenize = lambda x: re.findall(r'\b\w+\b', x.lower())
    
    def extractive_summarize(self, text: str, num_sentences: int = 3) -> str:
        """Create extractive summary using TF-IDF-like scoring"""
        # Clean and preprocess text
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Split into sentences
        sentences = self.sent_tokenize(text)
        if len(sentences) <= num_sentences:
            return text
        
        # Calculate word frequencies
        word_freq = {}
        for sentence in sentences:
            words = self.word_tokenize(sentence.lower())
            for word in words:
                if word not in self.stopwords and len(word) > 2:
                    word_freq[word] = word_freq.get(word, 0) + 1
        
        # Score sentences based on word frequencies
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            words = self.word_tokenize(sentence.lower())
            score = 0
            word_count = 0
            for word in words:
                if word in word_freq:
                    score += word_freq[word]
                    word_count += 1
            
            if word_count > 0:
                sentence_scores[i] = score / word_count
            else:
                sentence_scores[i] = 0
        
        # Get top sentences
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
        top_sentences = sorted([idx for idx, score in top_sentences])  # Maintain order
        
        # Create summary
        summary_sentences = [sentences[idx] for idx in top_sentences]
        return ' '.join(summary_sentences)
    
    def abstractive_summary(self, text: str, style: str = "academic") -> str:
        """Simple rule-based abstractive summary"""
        # Extract key information
        sentences = self.sent_tokenize(text)
        
        # Find sentences with key academic indicators
        key_indicators = {
            'academic': ['results', 'conclusion', 'findings', 'analysis', 'study', 'research', 'data', 'significant'],
            'brief': ['main', 'key', 'important', 'primary', 'essential'],
            'detailed': ['method', 'approach', 'technique', 'process', 'implementation']
        }
        
        indicators = key_indicators.get(style, key_indicators['academic'])
        
        # Score sentences by key indicators
        scored_sentences = []
        for sentence in sentences:
            score = sum(1 for indicator in indicators if indicator.lower() in sentence.lower())
            scored_sentences.append((sentence, score))
        
        # Sort by score and take top sentences
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        
        if style == "brief":
            num_sentences = min(2, len(scored_sentences))
        elif style == "detailed":
            num_sentences = min(5, len(scored_sentences))
        else:  # academic
            num_sentences = min(3, len(scored_sentences))
        
        summary = ' '.join([sent[0] for sent in scored_sentences[:num_sentences]])
        
        # If no high-scoring sentences, fall back to extractive
        if not summary.strip():
            summary = self.extractive_summarize(text, num_sentences)
        
        return summary

def summarize_text_minimal(text: str, style: str = "academic") -> str:
    """Minimal summarization function"""
    summarizer = MinimalSummarizer()
    return summarizer.abstractive_summary(text, style)
