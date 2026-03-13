import feedparser
url = "https://feeds.folha.uol.com.br/emcimadahora/rss091.xml"
f = feedparser.parse(url)
# print(f)
print(f.entries[0].title)

 