import os
from dotenv import load_dotenv

load_dotenv()

VK_API_VERSION = '5.199'
VK_API_BASE_URL = 'https://api.vk.com/method/'
VK_ACCESS_TOKEN = os.getenv('VK_ACCESS_TOKEN')

# Rate limit to prevent API bans
REQUEST_DELAY = 0.3