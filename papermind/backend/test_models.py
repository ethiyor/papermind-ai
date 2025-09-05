#!/usr/bin/env python3
"""
Test different summarization models to find the best one for academic papers
"""
import sys
import os
from pathlib import Path
import time

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.summarizer_utils import summarize_text, get_available_models, PaperMindSummarizer

# Sample academic text for testing
ACADEMIC_TEXT = """
Machine learning has revolutionized the field of artificial intelligence by enabling computers to learn and make decisions without explicit programming. This paradigm shift has led to significant advancements in various domains including computer vision, natural language processing, and robotics. Deep learning, a subset of machine learning, utilizes neural networks with multiple hidden layers to model and understand complex patterns in data.

The success of deep learning can be attributed to several factors: the availability of large datasets, increased computational power through GPUs, and algorithmic improvements. Convolutional Neural Networks (CNNs) have shown remarkable performance in image recognition tasks, achieving human-level accuracy in many cases. Recurrent Neural Networks (RNNs) and their variants, such as Long Short-Term Memory (LSTM) networks, have been instrumental in processing sequential data.

Recent developments in transformer architectures have further pushed the boundaries of what's possible in natural language understanding. Models like BERT, GPT, and T5 have demonstrated exceptional capabilities in language comprehension and generation. These models leverage attention mechanisms to focus on relevant parts of the input sequence, enabling them to capture long-range dependencies effectively.

The applications of machine learning extend beyond traditional computer science domains. In healthcare, machine learning algorithms assist in medical diagnosis, drug discovery, and personalized treatment plans. In finance, they power algorithmic trading, fraud detection, and credit scoring systems. The automotive industry has embraced machine learning for autonomous driving systems, while e-commerce platforms use it for recommendation systems and supply chain optimization.

Despite these successes, machine learning faces several challenges. The lack of interpretability in deep learning models, often referred to as the "black box" problem, raises concerns about trust and accountability. Bias in training data can lead to unfair or discriminatory outcomes. Additionally, the computational requirements for training large models raise environmental concerns due to high energy consumption.

Future research directions include developing more efficient algorithms, improving model interpretability, and addressing ethical considerations. Federated learning offers a promising approach to train models while preserving privacy. Quantum machine learning explores the potential of quantum computing to solve problems that are intractable for classical computers.
"""

def test_model_performance():
    """Test all available models and compare their performance"""
    models = get_available_models()
    print("Testing Summarization Models for Academic Text")
    print("=" * 60)
    print(f"Original text length: {len(ACADEMIC_TEXT)} characters")
    print(f"Word count: {len(ACADEMIC_TEXT.split())} words")
    print()
    
    results = {}
    
    for model_name, model_id in models.items():
        print(f"Testing {model_name} ({model_id})...")
        print("-" * 40)
        
        try:
            start_time = time.time()
            
            # Test with academic style
            summary = summarize_text(ACADEMIC_TEXT, model=model_name, style="academic")
            
            end_time = time.time()
            duration = end_time - start_time
            
            results[model_name] = {
                'summary': summary,
                'length': len(summary),
                'word_count': len(summary.split()),
                'duration': duration,
                'success': True
            }
            
            print(f"✓ Success! Duration: {duration:.2f}s")
            print(f"Summary length: {len(summary)} chars, {len(summary.split())} words")
            print(f"Summary: {summary[:150]}...")
            print()
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results[model_name] = {
                'error': str(e),
                'success': False
            }
            print()
    
    return results

def analyze_results(results):
    """Analyze and rank the model results"""
    print("ANALYSIS RESULTS")
    print("=" * 60)
    
    successful_models = {k: v for k, v in results.items() if v.get('success', False)}
    
    if not successful_models:
        print("❌ No models worked successfully!")
        return
    
    print("✅ Successful Models:")
    print()
    
    # Sort by performance criteria
    sorted_models = sorted(
        successful_models.items(),
        key=lambda x: (
            -len(x[1]['summary']),  # Longer summaries first (more informative)
            x[1]['duration']        # Then by speed (faster is better)
        )
    )
    
    for i, (model_name, data) in enumerate(sorted_models, 1):
        print(f"{i}. {model_name.upper()}")
        print(f"   Summary quality: {data['word_count']} words")
        print(f"   Speed: {data['duration']:.2f} seconds")
        print(f"   Summary: {data['summary'][:100]}...")
        print()
    
    # Recommendation
    best_model = sorted_models[0]
    print("RECOMMENDATION:")
    print(f"🏆 Best model for academic papers: {best_model[0].upper()}")
    print(f"   Reasons: {best_model[1]['word_count']} words in {best_model[1]['duration']:.2f}s")

def test_different_styles():
    """Test different summarization styles with the best model"""
    print("TESTING DIFFERENT SUMMARIZATION STYLES")
    print("=" * 60)
    
    styles = ["academic", "brief", "detailed"]
    
    for style in styles:
        print(f"Testing {style} style...")
        print("-" * 30)
        
        try:
            summary = summarize_text(ACADEMIC_TEXT, model="bart", style=style)
            print(f"✓ {style.capitalize()} summary ({len(summary.split())} words):")
            print(f"   {summary[:200]}...")
            print()
        except Exception as e:
            print(f"❌ Error with {style} style: {e}")
            print()

if __name__ == "__main__":
    print("PaperMind AI - Summarization Model Evaluation")
    print("=" * 60)
    
    # Test all models
    results = test_model_performance()
    
    # Analyze results
    analyze_results(results)
    
    # Test different styles
    test_different_styles()
    
    print("CONCLUSION:")
    print("The system is working with multiple model options.")
    print("BART is generally the most reliable for academic text.")
    print("You can switch models using the 'model' parameter in API calls.")
