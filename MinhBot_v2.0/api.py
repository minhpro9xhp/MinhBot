import wikipedia
from PIL import Image
import requests
from io import BytesIO

def search_information(target):
    import wikipedia
    from PIL import Image
    import requests
    from io import BytesIO
    import os

    response = []

    try:
        pg = wikipedia.page(target)
    except:
        # Truong hop bi timeouterror do wikipedia chan ko cho su dung api
        response.append("Wikipedia API is currently unable to access via MinhBot.")
        return response

    # find suitable image
    keywords = ['logo', 'flag']
    keywords.extend(target.strip().split(' '))

    point_list = []
    for image in pg.images:
        i = 0
        for keyword in keywords:
            if keyword in image.lower():
                i += 1
        point_list.append(i)

    img_url = pg.images[point_list.index(max(point_list))]

    response = [pg.title, pg.summary, img_url, pg.url]

    return response



print(search_information("pikachu"))

