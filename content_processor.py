import re
import json
from datetime import datetime
from config import Config

class ContentProcessor:
    def __init__(self):
        self.emoji_pattern = re.compile(r'[^\w\s]')
        self.remove_pattern = re.compile(r'^.*Жми на .*$', re.MULTILINE | re.IGNORECASE)

    def process_text_entities(self, text_entities):
        """Convert Telegram text entities to HTML"""
        if not text_entities:
            return ""

        html_parts = []
        for entity in text_entities:
            text = entity.get('text', '')
            entity_type = entity.get('type', 'plain')

            if entity_type == 'bold':
                html_parts.append(f'<strong>{text}</strong>')
            elif entity_type == 'italic':
                html_parts.append(f'<em>{text}</em>')
            elif entity_type == 'code':
                html_parts.append(f'<code>{text}</code>')
            elif entity_type == 'pre':
                html_parts.append(f'<pre>{text}</pre>')
            elif entity_type == 'link':
                url = entity.get('href', text)
                html_parts.append(f'<a href="{url}">{text}</a>')
            elif entity_type == 'plain':
                html_parts.append(text)
            else:
                html_parts.append(text)

        return ''.join(html_parts)

    def process_mixed_text_content(self, text_content):
        """Process mixed text content (strings and objects)"""
        if not text_content:
            return ""

        html_parts = []
        for item in text_content:
            if isinstance(item, dict):
                # Handle entity object
                text = item.get('text', '')
                entity_type = item.get('type', 'plain')

                if entity_type == 'bold':
                    html_parts.append(f'<strong>{text}</strong>')
                elif entity_type == 'italic':
                    html_parts.append(f'<em>{text}</em>')
                elif entity_type == 'code':
                    html_parts.append(f'<code>{text}</code>')
                elif entity_type == 'pre':
                    html_parts.append(f'<pre>{text}</pre>')
                elif entity_type == 'link':
                    url = item.get('href', text)
                    html_parts.append(f'<a href="{url}">{text}</a>')
                elif entity_type == 'plain':
                    html_parts.append(text)
                else:
                    html_parts.append(text)
            else:
                # Handle plain string
                html_parts.append(str(item))

        return ''.join(html_parts)

    def clean_text(self, text):
        """Clean text by removing unwanted patterns"""
        if not text:
            return ""

        # Remove lines with "Жми на " and emojis
        if Config.REMOVE_EMOJI_LINES:
            lines = text.split('\n')
            cleaned_lines = []

            for line in lines:
                # Skip lines that contain "Жми" patterns and have emojis
                if (('Жми на ' in line or 'Жми сердечко' in line or 'Жми молнию' in line) and
                    self.emoji_pattern.search(line)):
                    continue
                cleaned_lines.append(line)

            text = '\n'.join(cleaned_lines)

        return text.strip()

    def remove_title_from_content(self, content, title):
        """Remove the title from the beginning of content to avoid duplication"""
        if not content or not title:
            return content

        # Clean title for comparison (remove HTML tags)
        clean_title = re.sub(r'<[^>]+>', '', title).strip()

        # Split content into lines
        lines = content.split('\n')

        # Find and remove the line that matches the title
        for i, line in enumerate(lines):
            clean_line = re.sub(r'<[^>]+>', '', line).strip()
            if clean_line == clean_title:
                # Remove this line and any empty lines that follow
                lines = lines[i+1:]
                # Remove leading empty lines
                while lines and not lines[0].strip():
                    lines = lines[1:]
                break

        return '\n'.join(lines).strip()

    def extract_title(self, content, max_length=100):
        """Extract title from content"""
        if not content:
            return "Post"

                # Get the first line only
        lines = content.split('\n')
        if not lines:
            return "Post"

        # Find the first non-empty line
        first_line = None
        first_line_index = 0
        for i, line in enumerate(lines):
            if line.strip():
                first_line = line.strip()
                first_line_index = i
                break

        if not first_line:
            return "Post"

        # Skip if first line is a list item
        if first_line.startswith('-') or first_line.startswith('—') or first_line.startswith('•'):
            # Try to find the next non-empty line that could be a title
            for line in lines[first_line_index + 1:]:
                line = line.strip()
                if line and len(line) <= max_length and not line.startswith('http'):
                    # Skip list items
                    if line.startswith('-') or line.startswith('—') or line.startswith('•'):
                        continue
                    # Remove HTML tags for title
                    clean_title = re.sub(r'<[^>]+>', '', line)
                    # Remove trailing dots and clean up
                    clean_title = clean_title.rstrip('.')
                    return clean_title[:max_length]
        else:
            # First line is not a list item, use it as title
            if len(first_line) <= max_length and not first_line.startswith('http'):
                # Remove HTML tags for title
                clean_title = re.sub(r'<[^>]+>', '', first_line)
                # Remove trailing dots and clean up
                clean_title = clean_title.rstrip('.')
                return clean_title[:max_length]

        # Fallback: use first meaningful text
        clean_content = re.sub(r'<[^>]+>', '', content)
        words = clean_content.split()[:5]
        fallback_title = ' '.join(words)[:max_length]
        # Remove trailing dots from fallback title too
        return fallback_title.rstrip('.')

    def analyze_content(self, content):
        """Analyze content to determine categories and tags"""
        if not content:
            return [], []

        content_lower = content.lower()
        categories = []
        tags = []

        # Check for categories (now simple list)
        for category in Config.CATEGORIES:
            if category.lower() in content_lower:
                categories.append(category)

        # Check for tags
        for tag in Config.TAGS:
            if tag.lower() in content_lower:
                tags.append(tag)

        return categories, tags

    def format_date(self, date_string):
        """Format date for WordPress"""
        try:
            # Parse Telegram date format
            dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return dt.isoformat()
        except:
            return None

    def process_message(self, message):
        """Process a single Telegram message"""
        # Skip system messages
        if message.get('type') == 'service':
            return None

        # Skip messages without text
        if not message.get('text'):
            return None

        # Process text content
        text_content = message.get('text', '')
        if isinstance(text_content, list):
            # Handle mixed array format (strings and objects)
            processed_content = self.process_mixed_text_content(text_content)
        else:
            # Handle plain text format
            processed_content = text_content

        # Clean the content
        cleaned_content = self.clean_text(processed_content)
        if not cleaned_content:
            return None

        # Extract title
        title = self.extract_title(cleaned_content)

        # Remove title from content to avoid duplication
        content_without_title = self.remove_title_from_content(cleaned_content, title)

        # Analyze content for categories and tags
        categories, tags = self.analyze_content(content_without_title)

        # Process date
        date = self.format_date(message.get('date', ''))

        # Process photo if present
        photo_path = None
        if message.get('photo'):
            photo_filename = message['photo']
            # Remove 'photos/' prefix if it's already in the filename
            if photo_filename.startswith('photos/'):
                photo_filename = photo_filename[7:]  # Remove 'photos/' prefix
            photo_path = f"{Config.PHOTOS_DIR}/{photo_filename}"

        return {
            'id': message.get('id'),
            'title': title,
            'content': content_without_title,
            'date': date,
            'categories': categories,
            'tags': tags,
            'photo_path': photo_path,
            'original_message': message
        }