# TRMNL Quote Plugin

A beautiful plugin for TRMNL devices that displays inspirational quotes from Daily Stoic and custom sources. Perfect for daily motivation and inspiration on your TRMNL OG device.

## Features

- 📱 **TRMNL OG Support**: Optimized for 800x600 resolution
- 🎨 **Beautiful UI**: Gradient backgrounds with glass-morphism effects
- 📚 **Daily Stoic Integration**: Scrape quotes from @dailystoic Twitter account
- ✏️ **Custom Quotes**: Add your own inspirational quotes
- 🔄 **Auto-refresh**: Automatic quote rotation every 30 seconds
- 🌐 **Web Management**: Easy-to-use web interface for quote management
- 🐳 **Docker Ready**: Containerized for easy deployment

## Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone <your-repo-url>
cd trmnl-quote
```

2. Start the service:
```bash
docker-compose up -d
```

3. Access the management interface:
   - Open http://localhost:5000 in your browser
   - Add custom quotes or scrape Daily Stoic quotes
   - Preview the TRMNL display at http://localhost:5000/trmnl/markup

### Manual Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

## Plugin Configuration for TRMNL

When creating your plugin on TRMNL, use these URLs:

- **Installation URL**: `https://your-domain.com/trmnl/install`
- **Installation Success Webhook URL**: `https://your-domain.com/trmnl/webhook/install`
- **Plugin Management URL**: `https://your-domain.com/trmnl/manage`
- **Plugin Markup URL**: `https://your-domain.com/trmnl/markup`
- **Uninstallation Webhook URL**: `https://your-domain.com/trmnl/webhook/uninstall`

## API Endpoints

### Quote Management
- `GET /api/quotes` - Get all quotes
- `GET /api/quotes/random` - Get a random quote
- `POST /api/quotes` - Add a new quote
- `POST /api/scrape` - Scrape Daily Stoic quotes

### TRMNL Plugin Endpoints
- `GET /trmnl/markup` - TRMNL device markup (Liquid template)
- `GET /trmnl/install` - Plugin installation
- `GET /trmnl/uninstall` - Plugin uninstallation
- `GET /trmnl/manage` - Plugin management interface

## Customization

### Adding Custom Quotes

Use the web interface at `/` or make a POST request to `/api/quotes`:

```json
{
  "text": "Your inspirational quote here",
  "author": "Author Name",
  "source": "Source Name"
}
```

### Modifying the Display

The TRMNL display template is located at `templates/trmnl_markup.liquid`. You can customize:

- Colors and gradients
- Typography and spacing
- Layout and positioning
- Animation effects

### Scraping Configuration

The Daily Stoic scraping is currently using sample quotes. To implement real scraping:

1. Set up Twitter API access
2. Modify the `scrape_daily_stoic_quotes()` function in `app.py`
3. Add proper error handling and rate limiting

## Deployment

### Production Deployment

1. Set up a domain and SSL certificate
2. Update the plugin configuration URLs
3. Deploy using Docker Compose:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables

- `FLASK_ENV=production` - Set to production mode
- `FLASK_APP=app.py` - Flask application entry point

## File Structure

```
trmnl-quote/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── plugin-config.json    # TRMNL plugin configuration
├── templates/
│   ├── trmnl_markup.liquid  # TRMNL device template
│   ├── index.html           # Management interface
│   └── manage.html          # Plugin management
└── README.md             # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the TRMNL documentation
- Join the TRMNL community

## Changelog

### v1.0.0
- Initial release
- Daily Stoic quote integration
- Custom quote management
- TRMNL OG device support
- Web management interface
- Docker deployment support