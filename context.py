from langchain_community.document_loaders import WebBaseLoader
from bs4 import BeautifulSoup
import html2text


url = "https://suits.fandom.com/wiki/Louis_Litt"

loader = WebBaseLoader(url)
data = loader.load()

raw_html = data[0].page_content
soup = BeautifulSoup(raw_html, "html.parser")

for tag in soup(["script", "style", "header", "footer", "nav", "aside", "noscript"]):
    tag.decompose()

for div in soup.find_all("div", class_="mw-editsection"):
    div.decompose()

clean_html = str(soup)
text_maker = html2text.HTML2Text()
text_maker.ignore_links = True
markdown_text = text_maker.handle(clean_html)

with open("louis_litt.txt","w", encoding="utf-8") as f:
    f.write(markdown_text)

