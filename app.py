from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import random
import re

app = Flask(__name__)

# Configuration
QUOTES_FILE = 'quotes.json'
DAILY_STOIC_URL = 'https://x.com/dailystoic'

def load_quotes():
    """Load quotes from JSON file"""
    if os.path.exists(QUOTES_FILE):
        with open(QUOTES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_quotes(quotes):
    """Save quotes to JSON file"""
    with open(QUOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)

def scrape_daily_stoic_quotes():
    """Scrape quotes from Daily Stoic Twitter account"""
    try:
        # Since we can't directly scrape Twitter/X, we'll use a mock approach
        # In a real implementation, you'd use Twitter API or a scraping service
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # For demo purposes, we'll add some sample stoic quotes
        sample_quotes = [
            {
                "text": "The obstacle is the way.",
                "author": "Marcus Aurelius",
                "source": "Daily Stoic",
                "date_added": datetime.now().isoformat()
            },
            {
                "text": "You have power over your mind - not outside events. Realize this, and you will find strength.",
                "author": "Marcus Aurelius",
                "source": "Daily Stoic", 
                "date_added": datetime.now().isoformat()
            },
            {
                "text": "It is not death that a man should fear, but he should fear never beginning to live.",
                "author": "Marcus Aurelius",
                "source": "Daily Stoic",
                "date_added": datetime.now().isoformat()
            },
            {
                "text": "The best revenge is not to be like your enemy.",
                "author": "Marcus Aurelius",
                "source": "Daily Stoic",
                "date_added": datetime.now().isoformat()
            },
            {
                "text": "Waste no more time arguing what a good man should be. Be one.",
                "author": "Marcus Aurelius",
                "source": "Daily Stoic",
                "date_added": datetime.now().isoformat()
            }
        ]
        
        return sample_quotes
        
    except Exception as e:
        print(f"Error scraping quotes: {e}")
        return []

@app.route('/')
def index():
    """Main page with quote management UI"""
    quotes = load_quotes()
    return render_template('index.html', quotes=quotes)

@app.route('/api/quotes')
def get_quotes():
    """API endpoint to get all quotes"""
    quotes = load_quotes()
    return jsonify(quotes)

@app.route('/api/quotes/random')
def get_random_quote():
    """API endpoint to get a random quote"""
    quotes = load_quotes()
    if quotes:
        return jsonify(random.choice(quotes))
    return jsonify({"error": "No quotes available"}), 404

@app.route('/api/quotes', methods=['POST'])
def add_quote():
    """API endpoint to add a new quote"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "Quote text is required"}), 400
    
    quote = {
        "id": len(load_quotes()) + 1,
        "text": data['text'],
        "author": data.get('author', 'Unknown'),
        "source": data.get('source', 'Custom'),
        "date_added": datetime.now().isoformat()
    }
    
    quotes = load_quotes()
    quotes.append(quote)
    save_quotes(quotes)
    
    return jsonify(quote), 201

@app.route('/api/scrape', methods=['POST'])
def scrape_quotes():
    """API endpoint to scrape quotes from Daily Stoic"""
    new_quotes = scrape_daily_stoic_quotes()
    quotes = load_quotes()
    
    # Add new quotes that don't already exist
    existing_texts = {q['text'] for q in quotes}
    added_count = 0
    
    for quote in new_quotes:
        if quote['text'] not in existing_texts:
            quote['id'] = len(quotes) + added_count + 1
            quotes.append(quote)
            added_count += 1
    
    save_quotes(quotes)
    
    return jsonify({
        "message": f"Added {added_count} new quotes",
        "total_quotes": len(quotes)
    })

@app.route('/trmnl/markup')
def trmnl_markup():
    """TRMNL plugin markup endpoint"""
    quotes = load_quotes()
    if quotes:
        quote = random.choice(quotes)
    else:
        quote = {
            "text": "No quotes available. Add some quotes to get started!",
            "author": "System",
            "source": "Default"
        }
    
    return render_template('trmnl_markup.liquid', quote=quote)

@app.route('/trmnl/install')
def trmnl_install():
    """TRMNL plugin installation endpoint"""
    return jsonify({
        "status": "success",
        "message": "Quote plugin installed successfully"
    })

@app.route('/trmnl/uninstall')
def trmnl_uninstall():
    """TRMNL plugin uninstallation endpoint"""
    return jsonify({
        "status": "success", 
        "message": "Quote plugin uninstalled successfully"
    })

@app.route('/trmnl/webhook/install', methods=['POST'])
def webhook_install():
    """Handle TRMNL installation webhook"""
    try:
        data = request.get_json()
        print(f"Installation webhook received: {data}")
        
        # Log the installation event
        # In a real implementation, you might want to store this in a database
        
        return jsonify({
            "status": "success",
            "message": "Installation webhook processed"
        })
    except Exception as e:
        print(f"Error processing installation webhook: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to process installation webhook"
        }), 500

@app.route('/trmnl/webhook/uninstall', methods=['POST'])
def webhook_uninstall():
    """Handle TRMNL uninstallation webhook"""
    try:
        data = request.get_json()
        print(f"Uninstallation webhook received: {data}")
        
        # Log the uninstallation event
        # In a real implementation, you might want to clean up user data
        
        return jsonify({
            "status": "success",
            "message": "Uninstallation webhook processed"
        })
    except Exception as e:
        print(f"Error processing uninstallation webhook: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to process uninstallation webhook"
        }), 500

@app.route('/trmnl/manage')
def trmnl_manage():
    """TRMNL plugin management page"""
    quotes = load_quotes()
    return render_template('manage.html', quotes=quotes)

if __name__ == '__main__':
    # Initialize with some sample quotes if none exist
    quotes = load_quotes()
    if not quotes:
        sample_quotes = scrape_daily_stoic_quotes()
        save_quotes(sample_quotes)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
