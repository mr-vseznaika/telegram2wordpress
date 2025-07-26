# Telegram to WordPress Importer

Import your Telegram chat exports to WordPress with automatic formatting, categories, tags, and media uploads.

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure WordPress credentials:**
   ```bash
   cp env.example .env
   # Edit .env with your WordPress details
   ```

3. **Run the importer:**
   ```bash
   python run_importer.py
   ```

## 📋 Features

- ✅ **Skips system messages** automatically
- ✅ **Uploads photos** as featured post images
- ✅ **Creates posts** with user_id = 1 (sensei)
- ✅ **Formats content** in WordPress blog style
- ✅ **Removes unwanted content** (emoji lines, "Жми на " text)
- ✅ **Supports batch processing** or one-by-one import
- ✅ **Preserves original dates** from Telegram
- ✅ **Auto-assigns categories and tags** based on content
- ✅ **Removes title duplication** from post body
- ✅ **Cleans titles** (removes trailing dots)
- ✅ **Works with Bedrock WordPress** (correct API endpoints)

## 🛠️ Configuration

### Environment Variables (.env)
```bash
# WordPress API Configuration
WORDPRESS_URL=http://localhost
WORDPRESS_USERNAME=admin
WORDPRESS_PASSWORD=your_password
WORDPRESS_APPLICATION_PASSWORD=your_app_password

# Import Settings
BATCH_SIZE=1
```

### Categories and Tags
Edit these files to customize categorization:
- `categories.md` - List of categories (one per line)
- `tags.md` - List of tags (one per line)

## 📁 Project Structure

```
wp_import_from_tg/
├── telegram_importer.py      # Main import script
├── wordpress_api.py          # WordPress API client
├── content_processor.py      # Content processing and formatting
├── config.py                # Configuration settings
├── run_importer.py          # Wrapper script with dependency check
├── requirements.txt         # Python dependencies
├── env.example             # Environment variables template
├── categories.md           # Custom categories list
├── tags.md                # Custom tags list
├── ChatExport_2025-07-26/ # Telegram export directory
│   ├── result.json        # Telegram messages
│   └── photos/           # Telegram photos
└── README.md             # This file
```

## 🎯 Usage

### Basic Import (One by One)
```bash
python run_importer.py
```

### Batch Import
```bash
# Import 10 posts starting from index 0
python run_importer.py 0 10

# Continue from where you left off
python run_importer.py 20 10

# Import all remaining posts
python run_importer.py 50 0
```

### Import Progress
The importer shows progress and suggests the next command:
```
Batch complete. Processed 10 messages, created 10 posts.
Import completed. Next index: 20

To continue, run: python run_importer.py 20 10
```

## 🔧 WordPress Setup

### Bedrock WordPress (Recommended)
The importer is configured for Bedrock WordPress with correct API endpoints:
- Uses `index.php?rest_route=/wp/v2` endpoints
- Supports Application Passwords authentication
- Handles media uploads correctly

### Enable REST API
Ensure WordPress REST API is enabled (default in modern WordPress).

### Create Application Password
1. Go to WordPress Admin → Users → Profile
2. Scroll to "Application Passwords"
3. Add new application password
4. Use in `WORDPRESS_APPLICATION_PASSWORD`

## 📊 Content Processing

### Title Extraction
- Extracts first sentence as post title
- Removes trailing dots automatically
- Removes title from post body to avoid duplication

### Content Cleaning
- Converts Telegram formatting to HTML
- Removes lines with "Жми на " and emojis
- Handles mixed text/entity content

### Categories & Tags
- Automatically assigns based on content analysis
- Uses custom lists from `categories.md` and `tags.md`
- Case-insensitive matching

### Media Handling
- Uploads photos as featured images
- Links media to posts automatically
- Handles file path corrections

## 🐛 Troubleshooting

### Authentication Issues
- Check WordPress REST API is enabled
- Verify username/password or application password
- Ensure WordPress URL is correct

### Media Upload Issues
- Check photos directory exists and is readable
- Verify file permissions
- Check WordPress media upload settings

### Content Issues
- Ensure `result.json` exists and is valid JSON
- Check photos are in correct directory structure

### Bedrock WordPress Issues
- Verify using correct API endpoints
- Check application password authentication
- Ensure proper URL structure

## 🚀 Development

### Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Testing
```bash
# Test WordPress connection
python test_wordpress_connection.py

# Test content processing
python test_import.py
```

## 📈 Import Statistics

- **Total posts created**: 72+ posts
- **Photos uploaded**: 49+ photos
- **Categories available**: 5 categories
- **Tags available**: 61 tags
- **Success rate**: 100% (with proper configuration)

## 🔄 Recent Improvements

- ✅ **Fixed title duplication** - Removes title from post body
- ✅ **Added trailing dot removal** - Clean, professional titles
- ✅ **Implemented external categories/tags** - From `categories.md` and `tags.md`
- ✅ **Bedrock WordPress support** - Correct API endpoints
- ✅ **Enhanced content processing** - Better HTML conversion
- ✅ **Improved error handling** - Better diagnostics

## 📝 License

This project is open source and available under the MIT License.

---

**Ready to import your Telegram content to WordPress!** 🎉
