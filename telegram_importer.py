import json
import os
import sys
from pathlib import Path
from wordpress_api import WordPressAPI
from content_processor import ContentProcessor
from config import Config

class TelegramImporter:
    def __init__(self):
        self.wp_api = WordPressAPI()
        self.processor = ContentProcessor()
        self.categories_cache = {}
        self.tags_cache = {}

    def load_export_data(self):
        """Load Telegram export data from JSON file"""
        export_file = os.path.join(Config.EXPORT_DIR, 'result.json')

        if not os.path.exists(export_file):
            raise FileNotFoundError(f"Export file not found: {export_file}")

        with open(export_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data.get('messages', [])

    def ensure_categories_exist(self, category_names):
        """Ensure all categories exist in WordPress"""
        if not category_names:
            return []

        # Get existing categories
        if not self.categories_cache:
            existing_categories = self.wp_api.get_categories()
            self.categories_cache = {cat['name'].lower(): cat['id'] for cat in existing_categories}

        category_ids = []
        for category_name in category_names:
            category_lower = category_name.lower()

            if category_lower not in self.categories_cache:
                # Create new category
                try:
                    new_category = self.wp_api.create_category(category_name)
                    self.categories_cache[category_lower] = new_category['id']
                    print(f"Created category: {category_name}")
                except Exception as e:
                    print(f"Error creating category {category_name}: {e}")
                    continue

            category_ids.append(self.categories_cache[category_lower])

        return category_ids

    def ensure_tags_exist(self, tag_names):
        """Ensure all tags exist in WordPress"""
        if not tag_names:
            return []

        # Get existing tags
        if not self.tags_cache:
            existing_tags = self.wp_api.get_tags()
            self.tags_cache = {tag['name'].lower(): tag['id'] for tag in existing_tags}

        tag_ids = []
        for tag_name in tag_names:
            tag_lower = tag_name.lower()

            if tag_lower not in self.tags_cache:
                # Create new tag
                try:
                    new_tag = self.wp_api.create_tag(tag_name)
                    self.tags_cache[tag_lower] = new_tag['id']
                    print(f"Created tag: {tag_name}")
                except Exception as e:
                    print(f"Error creating tag {tag_name}: {e}")
                    continue

            tag_ids.append(self.tags_cache[tag_lower])

        return tag_ids

    def upload_photo(self, photo_path):
        """Upload photo to WordPress and return media ID"""
        if not photo_path or not os.path.exists(photo_path):
            return None

        try:
            media = self.wp_api.upload_media(photo_path)
            print(f"Uploaded photo: {os.path.basename(photo_path)}")
            return media['id']
        except Exception as e:
            print(f"Error uploading photo {photo_path}: {e}")
            return None

    def create_post(self, processed_message):
        """Create a WordPress post from processed message"""
        try:
            # Upload photo if present
            featured_media_id = None
            if processed_message['photo_path']:
                featured_media_id = self.upload_photo(processed_message['photo_path'])

            # Ensure categories and tags exist
            category_ids = self.ensure_categories_exist(processed_message['categories'])
            tag_ids = self.ensure_tags_exist(processed_message['tags'])

            # Create the post
            post = self.wp_api.create_post(
                title=processed_message['title'],
                content=processed_message['content'],
                date=processed_message['date'],
                categories=category_ids,
                tags=tag_ids,
                featured_media_id=featured_media_id
            )

            print(f"Created post: {processed_message['title']} (ID: {post['id']})")
            return post

        except Exception as e:
            print(f"Error creating post '{processed_message['title']}': {e}")
            return None

    def import_messages(self, messages, start_index=0, batch_size=None):
        """Import messages to WordPress"""
        if batch_size is None:
            batch_size = Config.BATCH_SIZE

        processed_count = 0
        created_count = 0

        for i, message in enumerate(messages[start_index:], start_index):
            # Process the message
            processed_message = self.processor.process_message(message)

            if processed_message:
                processed_count += 1

                # Create the post
                post = self.create_post(processed_message)
                if post:
                    created_count += 1

                # Check if we should stop for batch processing
                if batch_size > 0 and processed_count >= batch_size:
                    print(f"Batch complete. Processed {processed_count} messages, created {created_count} posts.")
                    return i + 1  # Return next index to start from

        print(f"Import complete. Processed {processed_count} messages, created {created_count} posts.")
        return len(messages)

    def run(self, start_index=0, batch_size=None):
        """Run the import process"""
        print("Starting Telegram to WordPress import...")

        try:
            # Load export data
            messages = self.load_export_data()
            print(f"Loaded {len(messages)} messages from export")

            # Import messages
            next_index = self.import_messages(messages, start_index, batch_size)

            print(f"Import completed. Next index: {next_index}")
            return next_index

        except Exception as e:
            print(f"Import failed: {e}")
            return start_index

def main():
    """Main function for command line usage"""
    importer = TelegramImporter()

    # Parse command line arguments
    start_index = 0
    batch_size = None

    if len(sys.argv) > 1:
        try:
            start_index = int(sys.argv[1])
        except ValueError:
            print("Invalid start index. Using 0.")

    if len(sys.argv) > 2:
        try:
            batch_size = int(sys.argv[2])
        except ValueError:
            print("Invalid batch size. Using default.")

    # Run import
    next_index = importer.run(start_index, batch_size)

    if batch_size and batch_size > 0:
        print(f"To continue, run: python telegram_importer.py {next_index} {batch_size}")

if __name__ == "__main__":
    main()