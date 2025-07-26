import requests
import base64
from config import Config

class WordPressAPI:
    def __init__(self):
        self.base_url = Config.WORDPRESS_URL.rstrip('/')
        # Bedrock WordPress uses different API endpoints
        self.api_url = f"{self.base_url}/index.php?rest_route=/wp/v2"
        self.media_url = f"{self.base_url}/index.php?rest_route=/wp/v2/media"

        # Setup authentication
        if Config.WORDPRESS_APPLICATION_PASSWORD:
            # Use Application Passwords (recommended)
            auth_string = f"{Config.WORDPRESS_USERNAME}:{Config.WORDPRESS_APPLICATION_PASSWORD}"
            self.auth_header = f"Basic {base64.b64encode(auth_string.encode()).decode()}"
        else:
            # Fallback to username/password (less secure)
            self.auth_header = None
            self.session = requests.Session()
            self.session.auth = (Config.WORDPRESS_USERNAME, Config.WORDPRESS_PASSWORD)

    def _make_request(self, method, url, **kwargs):
        """Make authenticated request to WordPress API"""
        headers = kwargs.get('headers', {})
        headers['Content-Type'] = 'application/json'

        if self.auth_header:
            headers['Authorization'] = self.auth_header
            response = requests.request(method, url, headers=headers, **kwargs)
        else:
            response = self.session.request(method, url, headers=headers, **kwargs)

        response.raise_for_status()
        return response

    def create_post(self, title, content, date=None, categories=None, tags=None, featured_media_id=None):
        """Create a new WordPress post"""
        post_data = {
            'title': title,
            'content': content,
            'status': Config.DEFAULT_STATUS,
            'author': Config.DEFAULT_AUTHOR_ID
        }

        if date:
            post_data['date'] = date

        if categories:
            post_data['categories'] = categories

        if tags:
            post_data['tags'] = tags

        if featured_media_id:
            post_data['featured_media'] = featured_media_id

        response = self._make_request('POST', self.api_url + '/posts', json=post_data)
        return response.json()

    def upload_media(self, file_path, title=None):
        """Upload media file to WordPress"""
        with open(file_path, 'rb') as file:
            files = {'file': file}
            data = {}

            if title:
                data['title'] = title

            if self.auth_header:
                headers = {'Authorization': self.auth_header}
                response = requests.post(self.media_url, files=files, data=data, headers=headers)
            else:
                response = self.session.post(self.media_url, files=files, data=data)

        response.raise_for_status()
        return response.json()

    def get_categories(self):
        """Get all WordPress categories"""
        response = self._make_request('GET', f"{self.api_url}/categories&per_page=100")
        return response.json()

    def get_tags(self):
        """Get all WordPress tags"""
        response = self._make_request('GET', f"{self.api_url}/tags&per_page=100")
        return response.json()

    def create_category(self, name, slug=None):
        """Create a new category"""
        data = {'name': name}
        if slug:
            data['slug'] = slug

        response = self._make_request('POST', f"{self.api_url}/categories", json=data)
        return response.json()

    def create_tag(self, name, slug=None):
        """Create a new tag"""
        data = {'name': name}
        if slug:
            data['slug'] = slug

        response = self._make_request('POST', f"{self.api_url}/tags", json=data)
        return response.json()