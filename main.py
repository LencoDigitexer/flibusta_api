from aiohttp import web, ClientSession
import requests
from bs4 import BeautifulSoup
from lxml import html


domain = "https://flibusta.is/"


async def booksearch(request):
    name = request.match_info.get("name", "Anonymous")

    result = requests.get(domain + "booksearch?ask={}&chb=on".format(name))

    data = BeautifulSoup(result.text, "lxml")

    res = []
    i = 0
    els = data.select("#main > ul > li")
    for div in els:
        root = div.find_all("a")

        res.append(
            {
                "book": {},
                "authors": [],
            }
        )

        book_a_text = root[0].get_text()
        book_a_href = root[0].get("href")

        res[i]["book"] = {"href": book_a_href, "name": book_a_text}

        for j in range(1, len(root)):

            author_a_text = root[j].get_text()
            authors_a_href = root[j].get("href")

            print(author_a_text)
            print(authors_a_href)

            res[i]["authors"].append({"href": authors_a_href, "name": author_a_text})
        i = i + 1

    return web.json_response(res)


app = web.Application()
app.add_routes(
    [
        web.get("/booksearch/{name}", booksearch),
    ]
)
web.run_app(app, port=4000)
