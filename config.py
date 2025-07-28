import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # WordPress API Configuration
    WORDPRESS_URL = os.getenv('WORDPRESS_URL', 'http://localhost')
    WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME', 'sensei')
    WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD', '')
    WORDPRESS_APPLICATION_PASSWORD = os.getenv('WORDPRESS_APPLICATION_PASSWORD', '')

    # Import Settings
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', '1'))  # Process 1 by 1 or batch
    SKIP_SYSTEM_MESSAGES = True
    REMOVE_EMOJI_LINES = True  # Remove lines with "Жми на " and emojis

    # Content Processing
    DEFAULT_AUTHOR_ID = 1
    DEFAULT_STATUS = 'publish'

    # File paths - can be overridden by environment variable or command line
    EXPORT_DIR = os.getenv('EXPORT_DIR', 'ChatExport_2025-07-27')
    PHOTOS_DIR = os.path.join(EXPORT_DIR, 'photos')

    @classmethod
    def set_export_dir(cls, export_dir):
        """Update export directory and recalculate photos directory"""
        cls.EXPORT_DIR = export_dir
        cls.PHOTOS_DIR = os.path.join(export_dir, 'photos')

    # Load categories and tags from external files
    @staticmethod
    def load_categories():
        try:
            with open('categories.md', 'r', encoding='utf-8') as f:
                categories = [line.strip() for line in f if line.strip()]
            return categories
        except FileNotFoundError:
            return ['Продукт', 'Разработка', 'Команда', 'Маркетинг', 'Рефлексия']

    @staticmethod
    def load_tags():
        try:
            with open('tags.md', 'r', encoding='utf-8') as f:
                tags = [line.strip() for line in f if line.strip()]
            return tags
        except FileNotFoundError:
            return [
                'агентство', 'результат', 'seo', 'разработчики', 'пользователь',
                'лендинг', 'wordpress', 'ux', 'gitlab', 'стартап', 'дизайн',
                'найм', 'реклама', 'docker', 'ценность', 'php', 'nginx',
                'тестирование', 'ci/cd', 'email', 'react', 'laravel', 'контент',
                'конверсия', 'ошибка', 'приоритеты', 'devops', 'sentry', 'crm',
                'аналитика', 'vue', 'переговоры', 'менторство', 'продуктивность',
                'мышление', 'фокус', 'рост', 'релиз', 'мониторинг', 'grafana',
                'posthog', 'онбординг', 'финансы', 'фриланс', 'коммуникация',
                'фаундер', 'юзабилити', 'mvp', 'собеседование', 'rest api',
                'бэкап', 'позиционирование', 'интеграция', 'веб-студия',
                'презентация', 'инфраструктура', 'figma', 'цель', 'стресс',
                'тепловая карта', 'поведение'
            ]

    # Categories and Tags loaded from external files
    CATEGORIES = load_categories()
    TAGS = load_tags()
