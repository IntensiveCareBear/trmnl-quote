from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import random
import re
import threading
import time

app = Flask(__name__)

# Configuration
QUOTES_FILE = os.getenv('QUOTES_FILE_PATH', 'quotes.json')
DAILY_STOIC_URL = 'https://x.com/dailystoic'
REFRESH_INTERVAL_MINUTES = int(os.getenv('REFRESH_INTERVAL_MINUTES', '30'))
TRMNL_WEBHOOK_URL = 'https://usetrmnl.com/api/custom_plugins/f4e72e60-c2d1-481d-b55a-11e3dcf33682'

def load_quotes():
    """Load quotes from JSON file"""
    if os.path.exists(QUOTES_FILE):
        try:
            with open(QUOTES_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except (json.JSONDecodeError, ValueError):
            # If file is corrupted or empty, return empty list
            return []
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
        "author": data.get('author', 'Unknown') or 'Unknown',
        "source": data.get('source', 'Custom') or 'Custom',
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
    try:
        quotes = load_quotes()
        if quotes:
            quote = random.choice(quotes)
        else:
            quote = {
                "text": "No quotes available. Add some quotes to get started!",
                "author": "System",
                "source": "Default"
            }
        
        return render_template('trmnl_markup.html', 
                             quote=quote, 
                             refresh_interval_minutes=REFRESH_INTERVAL_MINUTES)
    except Exception as e:
        print(f"Error in trmnl_markup: {e}")
        # Return a simple fallback response
        return f"""
        <div style="width: 800px; height: 600px; background: #667eea; color: white; display: flex; align-items: center; justify-content: center; font-family: Arial, sans-serif;">
            <div style="text-align: center;">
                <h1>TRMNL Quote Plugin</h1>
                <p>Error loading quotes. Please check the application logs.</p>
                <p>Refresh interval: {REFRESH_INTERVAL_MINUTES} minutes</p>
            </div>
        </div>
        """

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

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    quotes = load_quotes()
    return jsonify({
        "status": "healthy",
        "quotes_count": len(quotes),
        "refresh_interval_minutes": REFRESH_INTERVAL_MINUTES,
        "quotes_file": QUOTES_FILE,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/debug/quotes')
def debug_quotes():
    """Debug endpoint to see all quotes with their sources"""
    quotes = load_quotes()
    return jsonify({
        "total_quotes": len(quotes),
        "quotes": quotes,
        "sources": list(set([q.get('source', 'No Source') for q in quotes])),
        "custom_count": len([q for q in quotes if q.get('source', 'Custom') != 'Daily Stoic']),
        "daily_stoic_count": len([q for q in quotes if q.get('source', '') == 'Daily Stoic'])
    })

@app.route('/api/webhook/test', methods=['POST'])
def test_webhook():
    """Manually trigger webhook to TRMNL for testing"""
    try:
        send_quote_to_trmnl()
        return jsonify({
            "status": "success",
            "message": "Webhook sent to TRMNL"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to send webhook: {str(e)}"
        }), 500

@app.route('/api/webhook/debug', methods=['GET'])
def debug_webhook():
    """Debug webhook configuration and test"""
    quotes = load_quotes()
    if quotes:
        quote = random.choice(quotes)
        payload = {
            "merge_variables": {
                "text": quote['text'],
                "author": quote['author'],
                "source": quote['source'],
                "timestamp": datetime.now().isoformat()
            }
        }
        
        # Test if TRMNL webhook is accessible
        try:
            test_response = requests.get(TRMNL_WEBHOOK_URL, timeout=5)
            webhook_accessible = True
            webhook_status = test_response.status_code
        except Exception as e:
            webhook_accessible = False
            webhook_status = str(e)
        
        return jsonify({
            "webhook_url": TRMNL_WEBHOOK_URL,
            "webhook_accessible": webhook_accessible,
            "webhook_status": webhook_status,
            "sample_payload": payload,
            "quotes_count": len(quotes),
            "refresh_interval_minutes": REFRESH_INTERVAL_MINUTES
        })
    else:
        return jsonify({"error": "No quotes available"}), 404

def send_quote_to_trmnl():
    """Send a random quote to TRMNL webhook"""
    try:
        quotes = load_quotes()
        if quotes:
            quote = random.choice(quotes)
            
            # Prepare the data for TRMNL - nested in merge_variables
            payload = {
                "merge_variables": {
                    "text": quote['text'],
                    "author": quote['author'],
                    "source": quote['source'],
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            print(f"📤 Sending quote to TRMNL: {quote['text'][:50]}...")
            print(f"📤 Payload: {payload}")
            
            # Send to TRMNL webhook
            print(f"🌐 Making request to: {TRMNL_WEBHOOK_URL}")
            response = requests.post(
                TRMNL_WEBHOOK_URL,
                json=payload,
                timeout=5,  # Reduced timeout
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"📥 TRMNL Response Status: {response.status_code}")
            print(f"📥 TRMNL Response Body: {response.text}")
            
            if response.status_code == 200:
                print(f"✅ Quote sent to TRMNL successfully!")
            else:
                print(f"❌ Failed to send quote: {response.status_code} - {response.text}")
                
    except Exception as e:
        print(f"❌ Error sending quote to TRMNL: {e}")

def webhook_scheduler():
    """Run webhook sender every 30 minutes"""
    while True:
        send_quote_to_trmnl()
        time.sleep(REFRESH_INTERVAL_MINUTES * 60)  # Convert minutes to seconds

def initialize_quotes():
    """Initialize quotes file with sample data if empty"""
    quotes = load_quotes()
    if not quotes:
        print("No quotes found, initializing with sample quotes...")
        sample_quotes = scrape_daily_stoic_quotes()
        save_quotes(sample_quotes)
        print(f"Initialized with {len(sample_quotes)} sample quotes")
    else:
        print(f"Loaded {len(quotes)} existing quotes")

if __name__ == '__main__':
    # Initialize with some sample quotes if none exist
    initialize_quotes()
    
    # Start webhook scheduler in background thread
    scheduler_thread = threading.Thread(target=webhook_scheduler, daemon=True)
    scheduler_thread.start()
    print(f"🚀 Started webhook scheduler - sending quotes every {REFRESH_INTERVAL_MINUTES} minutes")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
