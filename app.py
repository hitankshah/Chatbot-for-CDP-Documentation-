from flask import Flask, request, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util
import re
import logging
import time
from urllib.parse import urljoin
import torch
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='.')

# Get port from environment variable (Render will set this)
port = int(os.environ.get('PORT', 5000))

# Load model with error handling
try:
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    model = None

documentation_urls = {
    "Segment": {
        "main": "https://segment.com/docs/connections/spec/",
        "sub_pages": [
            "https://segment.com/docs/connections/sources/catalog/libraries/server/http-api/",
            "https://segment.com/docs/connections/destinations/catalog/",
            "https://segment.com/docs/privacy/gdpr/"
        ]
    },
    "mParticle": {
        "main": "https://docs.mparticle.com/developers/quickstart/web/overview/",
        "sub_pages": [
            "https://docs.mparticle.com/developers/client-sdks/web/event-tracking/",
            "https://docs.mparticle.com/guides/personalization/audiences/overview/"
        ]
    },
    "Lytics": {
        "main": "https://docs.lytics.com/docs/developer-quickstart",
        "sub_pages": [
            "https://docs.lytics.com/docs/developer-quickstart-2-content-setup"
        ]
    },
    "Zeotap": {
        "main": "https://docs.zeotap.com/home/en-us/",
        "sub_pages": []
    }
}

# Cache configuration
doc_cache = {}
last_fetch_time = None
CACHE_DURATION = 3600  # 1 hour cache duration

def fetch_page_content(url, headers=None):
    if not headers:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for element in soup(['script', 'style', 'nav', 'header', 'footer']):
                element.decompose()
            
            content = []
            for elem in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li']):
                text = elem.get_text().strip()
                if text and len(text) > 20:  # Filter out very short segments
                    content.append(text)
            
            return ' '.join(content)
        
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
            if attempt == max_retries - 1:
                return ""
            time.sleep(1)  
def fetch_documentation():
    global last_fetch_time, doc_cache
    
    if last_fetch_time and time.time() - last_fetch_time < CACHE_DURATION:
        return doc_cache
    
    new_cache = {}
    for cdp, urls in documentation_urls.items():
        logger.info(f"Fetching documentation for {cdp}")
        content = []
        
        main_content = fetch_page_content(urls['main'])
        if main_content:
            content.append(main_content)
        
        for sub_url in urls['sub_pages']:
            sub_content = fetch_page_content(sub_url)
            if sub_content:
                content.append(sub_content)
        
        if content:
            new_cache[cdp] = ' '.join(content)
        else:
            logger.warning(f"No content fetched for {cdp}")
            new_cache[cdp] = doc_cache.get(cdp, "")  
    
    doc_cache = new_cache
    last_fetch_time = time.time()
    return doc_cache

def search_documentation(query, docs):
    """Search through documentation using sentence embeddings"""
    try:
        results = {}
        if not model:
            return {"error": "Model not loaded properly"}
            
        # Encode the query
        query_embedding = model.encode(query, convert_to_tensor=True)
        
        for cdp, content in docs.items():
            if not content:
                continue
                
            # Split content into manageable chunks
            sentences = [s.strip() for s in re.split(r'[.!?]+', content) if len(s.strip()) > 30]
            
            if not sentences:
                continue
                
            # Encode sentences
            sentence_embeddings = model.encode(sentences, convert_to_tensor=True)
            
            # Calculate similarity scores
            similarities = util.pytorch_cos_sim(query_embedding, sentence_embeddings)
            
            # Get top 2 matches
            top_k = min(2, len(sentences))
            best_matches = torch.topk(similarities[0], k=top_k)
            
            # Combine the best matching sentences
            matched_sentences = [sentences[idx] for idx in best_matches.indices]
            results[cdp] = " ".join(matched_sentences)
        
        return results
    except Exception as e:
        logger.error(f"Error in search: {e}")
        return {"error": str(e)}

@app.route('/')
def serve_ui():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        user_query = request.json.get('query', '').strip()
        if not user_query:
            return jsonify({"response": "Please enter a question."})

        if not user_query.lower().startswith('how') and "compare" not in user_query.lower():
            return jsonify({
                "response": "Please ask a question starting with 'How' or include 'compare' in your query."
            })

        # Fetch or use cached documentation
        docs = fetch_documentation()
        
        if "compare" in user_query.lower():
            # Handle comparison queries
            cdps_mentioned = [cdp for cdp in documentation_urls.keys() 
                              if cdp.lower() in user_query.lower()]
            
            if len(cdps_mentioned) < 2:
                return jsonify({
                    "response": "Please specify at least two CDPs to compare."
                })
            
            results = search_documentation(user_query, {cdp: docs[cdp] for cdp in cdps_mentioned})
            
            if "error" in results:
                return jsonify({"response": f"Error performing comparison: {results['error']}"})
            
            response = "Comparison Results:\n\n"
            for cdp, result in results.items():
                response += f"{cdp}:\n{result}\n\n"
            
        else:
            # Handle "how" questions
            results = search_documentation(user_query, docs)
            
            if "error" in results:
                return jsonify({"response": f"Error finding answer: {results['error']}"})
            
            response = "Here's what I found:\n\n"
            for cdp, result in results.items():
                if result.strip():  
                    response += f"{cdp}:\n{result}\n\n"

        return jsonify({"response": response if response.strip() else "Sorry, I couldn't find relevant information for your query."})

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({
            "response": "An error occurred while processing your request. Please try again."
        })

if __name__ == '__main__':
    # Run the app on the specified port
    app.run(host='0.0.0.0', port=port)