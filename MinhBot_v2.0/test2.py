import os
import csv

def process_file(current_directory, file_name, output_directory):

    file = open(current_directory + file_name, 'r', encoding="utf-8")

    header = file.readline().split(',')

    title_index = header.index('title')
    selftext_index = header.index('selftext')
    url_index = header.index('url')


    raw_text = file.read()

    file.close()

    while ",,," in raw_text:
        raw_text = raw_text.replace(",,,", ",0,0,")
    while ",," in raw_text:
        raw_text = raw_text.replace(",,", ",0,")
    while ",\n" in raw_text:
        raw_text = raw_text.replace(",\n", ",0\n")

    a = 0
    b = 0

    database = []
    ls = []

    while True:
        if b == len(raw_text):
            ls.append(raw_text[a: b])

            if len(ls) == len(header):
                database.append(ls)

            break
        elif (raw_text[b] == ',' and raw_text[b-1] == '\"' and raw_text[b-2] != '\"') or (raw_text[b] == ',' and raw_text[a] != '\"'):
            ls.append(raw_text[a: b])
            raw_text = raw_text[(b - a + 1):]
            a = 0
            b = 0
            if len(ls) == len(header) - 1:
                ls.append('0')
                database.append(ls)

                raw_text = raw_text[1:]
                # print(ls)
                ls = []
        elif raw_text[b] == '\"' and raw_text[b - 1] == ',':
            a = b

        b += 1

    new_file = open(output_directory + file_name, 'w', encoding="utf-8")
    new_file.writelines("title,selftext,url\n")
    for line in database:
        s = line[title_index] + ',' + line[selftext_index] + ',' + line[url_index] + '\n'
        new_file.writelines(s)

    new_file.close()

    print(file_name)
    return database

"""
for file_name in os.listdir("reddit-top-2.5-million/data"):
    if file_name not in os.listdir("data"):
        process_file("reddit-top-2.5-million/data/", file_name, "data/")


file_name = "3amjokes.csv"
process_file("reddit-top-2.5-million/data/", file_name, "data/")
"""


def process_file_2(current_directory, file_name, output_directory, columns):
    import csv
    if current_directory[:-1] != '/':
        current_directory += '/'

    csvfile = open(current_directory + file_name, 'r', encoding="utf-8")
csvfile = open("reddit-top-2.5-million/data/3amjokes.csv", 'r', encoding="utf-8")
spamreader = csv.reader(csvfile)
