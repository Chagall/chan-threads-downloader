import re
from html.parser import HTMLParser


class ChanHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = ""

    def handle_data(self, data):
        # Remove newlines, carriage returns, and quotation marks
        data = data.replace("\n", "").replace("\r", " ").replace('"', " ").replace("==", " ").strip()
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
#     '>18014 E eu também demorei demais https://old.27chan.org/ pra agir, poderia ter poupado mais o https://www.youtube.com/watch?v=BFzL4q95kAY passarinho se eu não fosse bicha e não tivesse medinho de esmagar ele com algum objeto pesado. Por mim, a pá pode ter sido uma morte menos dolorosa, mas acho que só o tempo que eu demorei pra pegar a porra da pá e pensar em como matar pode ter feito ele sofrer mais. "apenas membros" fixe\'d. ==Limpeza realizada!==Dessa vez foram as boards que não foram abandonadas a serem limpas, acompanhe na thread de tábuas no >>>/mod/. >início de 2017 >faço a Fuvest em Ribeirão Preto >conheço um sujeito redpillado enquanto espero o portão abrir >falamos sobre o Trump >falamos sobre assuntos que eram discutidos nos chans da época >não falamos abertamente que somos anões >nem mencionamos o recinto uma única vez Eu tenho minhas dúvidas se o cara também era channer, mas é muita coincidência encontrar alguém que sabia com detalhes sobre a forçação do mês. Se estiver lendo isso, saiba que você é baseado.'
# )
# print("\nparsed_message:", parser.text)

# parsed_message = parser.get_parsed_text()
