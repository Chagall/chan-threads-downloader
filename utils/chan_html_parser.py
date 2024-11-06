import re
from html.parser import HTMLParser


class ChanHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = ""

    def handle_data(self, data):
        # Remove newlines, carriage returns, and quotation marks
        data = data.replace("\n", "").replace("\r", " ").replace('"', " ").replace("==", " ").replace("||", " ").strip()
        # Remove references to other posts (e.g., >>12345 or >12345)
        data = re.sub(r">>\d+", "", data).strip()
        data = re.sub(r">\d+", "", data).strip()
        # Remove website links (e.g., https://fmhy.net/)
        data = re.sub(r"http[s]?://\S+", "", data).strip()
        # Remove standalone '>' symbols at the beginning of words
        data = re.sub(r">\s*", " ", data).strip()
        # Replace multiple whitespaces with a single whitespace
        data = re.sub(r"\s+", " ", data).strip()
        self.text = data

    def clear(self):
        self.text = ""  # Reset text to an empty list

    def get_parsed_text(self):
        return self.text


# parser = ChanHTMLParser()
# parser.feed(
#     "O quanto de ciência tem isso aqui? Digo, o quanto frequências podem afetar materiais orgânicos? Usar frequências para curar o corpo é algo real, mas os esquizos que postam esse tipo de foto sabem nada sobre o assunto. Você precisa de um aparelho de ressonância que nem é mais fabricado, pois o próprio criador morreu pobre depois dos dubaienses ferrarem a vida dele. Desculpa por não ter o nome na língua, você também não vai achar facilmente na internet, estão espero que um anão elabore mais."
# )
# parsed_message = parser.get_parsed_text()
# print("\nparsed_message:", parsed_message)
