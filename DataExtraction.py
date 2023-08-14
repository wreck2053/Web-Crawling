import csv
import requests
from bs4 import BeautifulSoup
from lxml import etree

f = open("Input.csv")
data = csv.reader(f)

# Iterate through links
for row in data:
    try:
        if row[1] == 'URL':  # skip the row with column names
            continue
        
        filename, url = row[0], row[1]
        g = open(filename + '.txt', 'w')

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
        }
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        tree = etree.HTML(str(soup))

        # If invalid link, raise Exception
        if 'Page not found' in tree.xpath('/html/head/title/text()')[0]:
            raise Exception

        # Extract the article heading
        g.write(tree.xpath('body//h1/text()')[0])
        g.write('\n')

        # Extract paragraphs from the article
        for i in range(1, len(tree.xpath('body//p'))+1):
            paragraph = tree.xpath('body//p[{}]/text()'.format(i))

            if not paragraph:  # then it is a subheading
                paragraph = tree.xpath('body//p[{}]/strong/text()'.format(i))

            for t in paragraph:
                g.write(t)

            g.write('\n')

        g.close()

    except Exception:
        pass

f.close()
