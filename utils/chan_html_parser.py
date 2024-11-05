import re
from html.parser import HTMLParser


class ChanHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        # Replace \n and \r characters with a whitespace
        data = re.sub(r"[\n\r]", " ", data)
        # Only add text that does not match the ">>12345" pattern
        if not re.match(r">>\d+", data.strip()):
            self.text.append(data)

    def clear(self):
        self.text = []  # Reset text to an empty list
