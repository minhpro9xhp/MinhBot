import random
from xml.dom import minidom
import collections


class Botlib:
    class Directory:
        jokes = 'reddit-top-2.5-million/data/3amjokes.csv'
        quotes = 'reddit-top-2.5-million/data/quotes.csv'
        notes = 'data/notes.xml'
        catpictures = 'reddit-top-2.5-million/data/catpictures.csv'

    directory = Directory()

    response = []


    def __init__(self):

        return


    def use_function(self, s, *args):
        if s == "search_information":
            self.response = self.search_information(args[0])
        elif s == "tell_a_random_quote":
            self.response = self.response_random_data(self.directory.quotes)
        elif s == "tell_a_random_joke":
            self.response = self.response_random_data(self.directory.jokes)
        elif s == "show_a_random_cat_picture":
            self.response = self.show_a_random_cat_picture()
        elif s == "take_a_note":
            self.response = self.take_a_note(args[0])
        elif s == "list_notes":
            self.response = self.list_notes()
        else:
            self.response = ["Error: No function to choose (botlib.use_function())"]

    def search_information(self, target):
        import wikipedia
        from PIL import Image
        import requests
        from io import BytesIO
        import os

        keywords_function_file = minidom.parse("keywords_function.xml")
        functions_data = keywords_function_file.getElementsByTagName("function")
        keywords = []
        for function in functions_data:
            if function.getElementsByTagName("id")[0].firstChild.data == "search_information":
                keywords.extend(function.getElementsByTagName("keywords")[0].firstChild.data.split(','))

        for keyword in keywords:
            if keyword in target:
                target = target.replace(keyword, '')


        response = []

        try:
            pg = wikipedia.page(target)
        except:
            # Truong hop bi timeouterror do wikipedia chan ko cho su dung api
            response.append("Wikipedia API is currently unable to access via MinhBot.")
            return response

        # find suitable image
        img_url = ''
        if pg.images:
            keywords = ['logo', 'flag', 'art', 'corp', 'corporation']

            keywords.extend(pg.title.split(' ') * 2)

            point_list = []
            for image_url in pg.images:
                i = 0
                for keyword in keywords:
                    if keyword.lower() in image_url.lower():
                        i += 1
                point_list.append(i)

            if point_list.count(max(point_list)) >= 2:
                """
                Neu co nhieu img_url co cung diem max thi se chon ra img_url co DO DAI NGAN NHAT
                """
                max_point_img_url_list = []
                i = 0
                for point in point_list:
                    if point == max(point_list):
                        max_point_img_url_list.append(pg.images[i])
                    i += 1

                img_url = min(max_point_img_url_list)
            else:
                img_url = pg.images[point_list.index(max(point_list))]

        response = [pg.title, pg.summary, img_url, pg.url]

        return response


    def response_random_data(self, directory):
        import csv
        import random
        with open(directory, 'r', encoding="utf-8") as csvfile:
            data = list(csv.reader(csvfile))

            csvrow = data[random.randint(1, len(data) - 1)]
            title = csvrow[4]
            selftext = csvrow[9]

            return [title, selftext]


    def tell_a_random_quote(self):
        import csv
        import random
        with open(self.directory.quotes, 'r', encoding="utf-8") as csvfile:
            data = list(csv.reader(csvfile))

            csvrow = data[random.randint(1, len(data) - 1)]
            title = csvrow[4]
            selftext = csvrow[9]

            return [title, selftext]


    def tell_a_random_joke(self):
        import csv
        import random
        with open(self.directory.jokes, 'r', encoding="utf-8") as csvfile:
            data = list(csv.reader(csvfile))

            csvrow = data[random.randint(1, len(data) - 1)]
            title = csvrow[4]
            selftext = csvrow[9]

            return [title, selftext]


    def show_a_random_cat_picture(self):
        import csv
        import random
        with open(self.directory.catpictures, 'r', encoding="utf-8") as csvfile:
            data = list(csv.reader(csvfile))
            pic_url = data[random.randint(1, len(data) - 1)][19]

            copy_to_clipboard(pic_url)
            return ['*copied to clipboard !', pic_url]

    def take_a_note(self, note):
        notes = load_data_from_xml_file(self.directory.notes, "note")

        keywords = load_keywords("keywords_function.xml", "take_a_note")
        for keyword in keywords:
            if keyword in note:
                note = note.replace(keyword, '')

        notes.append(note.strip())

        save_data_to_xml_file(notes, self.directory.notes, "note")

        return ["*MinhBot have taken this note !"]


    def list_notes(self):
        notes = load_data_from_xml_file(self.directory.notes, "note")

        for i in range(len(notes)):
            notes[i] = str(i + 1) + '. ' + notes[i]

        return notes


    def delete_note(self, note):

        return ["*This note have been deleted !"]


def load_data_from_xml_file(file_name, node):

    """

    :param file_name: string
    :param node: string
    :return: list
    """
    from xml.dom import minidom
    xml_file = minidom.parse(file_name)
    ls = []
    ls_xml = xml_file.getElementsByTagName(node)
    for _node in ls_xml:
        ls.append(_node.firstChild.data)
    return ls


def save_data_to_xml_file(_list, file_name, node, *args):
    """
    export data from list to a xml file

    :param _list: list
    :param file_name: string
    :param node: string
    :param root: string
    """
    root = 'root'
    if args:
        root = args[0]

    s = '<' + root + '>\n'

    for i in _list:
        s += "\t<" + node + ">" + i + "</" + node + ">\n"

    s += '</' + root + '>'

    xml_file = open(file_name, 'w', encoding="utf-8")
    xml_file.write(s)
    xml_file.close()


def load_keywords(file_name, function_name):
    keywords = []
    keywords_function_file = minidom.parse(file_name)
    functions_data = keywords_function_file.getElementsByTagName("function")
    for function in functions_data:
        if function.getElementsByTagName("id")[0].firstChild.data == function_name:
            keywords.extend(function.getElementsByTagName("keywords")[0].firstChild.data.split(','))

    return keywords


def copy_to_clipboard(text):
    try:
        import pyperclip
    except ImportError:
        print("ImportError: No module named \'pyperclip\'")
        return
    pyperclip.copy(text)

