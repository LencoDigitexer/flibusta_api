from aiohttp import web, ClientSession
import requests
from bs4 import BeautifulSoup
from lxml import html


domain = "https://flibusta.is"


async def get_book_details(book_id):

    result = requests.get(domain + "/b/" + str(book_id))

    data = BeautifulSoup(result.text, "lxml")

    info = data.select("#main > p")

    for root in info:
        info = root.get_text()

    image = data.select("#main > img")

    for root in image:
        image = domain + root["src"]

    download = domain + "/b/" + str(book_id) + "/download"
    fb2 = domain + "/b/" + str(book_id) + "/fb2"
    epub = domain + "/b/" + str(book_id) + "/epub"
    mobi = domain + "/b/" + str(book_id) + "/mobi"
    pdf = domain + "/b/" + str(book_id) + "/pdf"

    details = {
        "info": info,
        "image": image,
        "download": download,
        "file" : {
            "fb2": fb2,
            "epub": epub,
            "mobi": mobi,
            "pdf": pdf,
        }
    }
    return details


async def booksearch(request):
    name = request.match_info.get("name", "Anonymous")

    result = requests.get(domain + "/booksearch?ask={}&chb=on".format(name))

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
        test = await get_book_details(book_a_href[3:])

        res[i]["book"] = {
            "name": book_a_text,
            "details": test,
        }

        for j in range(1, len(root)):

            author_a_text = root[j].get_text()
            authors_a_href = root[j].get("href")

            # print(author_a_text)
            # print(authors_a_href)

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
