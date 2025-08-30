import re

ALLOWED_CHARS = re.compile(r'^[A-Za-z0-9]{1,16}$')
RESERVED = {"files"}

ORIGINAL_MAX_LENGTH = 2048
CUSTOM_ID_MAX_LENGTH = 16
