import os
from xml.dom import minidom

import learningbot
import nlp


class Program:
    name = ""
    directory = ""


class CmdBot:
    properties = dict()

    cmdbot_keywords_data = minidom.parse("cmdbot_keywords_data.xml")
    start_function_keywords = cmdbot_keywords_data.getElementsByTagName("start_function")[0].firstChild.data.split(',')
    shutdown_function_keywords = cmdbot_keywords_data.getElementsByTagName("shutdown_function")[0].firstChild.data.split(',')

    # Khoi tao csdl cua cmdbot
    def __init__(self):
        cmdbot_data = minidom.parse("cmdbot_data.xml")
        properties_data = cmdbot_data.getElementsByTagName("properties")[0]

        for _property_data in properties_data.childNodes:
            try:
                if _property_data.firstChild.data == "True":
                    self.properties.update({_property_data.tagName: True})
                elif _property_data.firstChild.data == "False":
                    self.properties.update({_property_data.tagName: False})
                elif nlp.isnumeric(_property_data.firstChild.data):
                    self.properties.update({_property_data.tagName: float(_property_data.firstChild.data)})
                else:
                    self.properties.update({_property_data.tagName: _property_data.firstChild.data})
            except AttributeError:
                continue

        if self.properties["debugmode"]:
            print("[CmdBot is active]")

    def comply(self, cmd):
        cmd.content[1] = self.choose_function(cmd.raw_content)
        self.use_function(cmd)

    def choose_function(self, r_content):
        start_function_point = 0
        shutdown_function_point = 0
        for _key in self.start_function_keywords:
            if _key.strip() in r_content:
                start_function_point += 1
        for _key in self.shutdown_function_keywords:
            if _key.strip() in r_content:
                shutdown_function_point += 1

        max_point = max(start_function_point, shutdown_function_point)

        # debug
        if self.properties['debugmode']:
            print('[start_function: ' + str(start_function_point) + "]")
            print('[shutdown_function: ' + str(shutdown_function_point) + ']')

        if [start_function_point, shutdown_function_point].count(max_point) > 1:
            a = input("Not very clear. Which function should i choose ?\n"
                      "1. start_function\n"
                      "2. shutdown_function\n"
                      "3. \n"
                      "4. \n"
                      "Your choice: ")

            if a == '2':
                self.shutdown_function_keywords += nlp.word_tokenize(r_content)
                self.shutdown_function_keywords = nlp.remove_duplicate_in_list(self.shutdown_function_keywords)
                return 'shutdown_function'

            elif a == '3':
                return 'start_function'
            elif a == '4':
                return 'start_function'
            else:
                self.start_function_keywords += nlp.word_tokenize(r_content)
                self.start_function_keywords = nlp.remove_duplicate_in_list(self.start_function_keywords)
                self.save_keywords_data_xml()
                return 'start_function'

        if max_point == 0 or max_point == start_function_point:
            return 'start_function'
        else:
            return 'shutdown_function'

    def use_function(self, _cmd):
        if _cmd.content[1] == "start_function":
            self.start_function(_cmd.raw_content)
        elif _cmd.content[1] == "shutdown_function":
            self.shutdown_function(_cmd.raw_content)

    def save_keywords_data_xml(self):
        s = "<root><keywords>"
        s += "<start_function>" + ', '.join(self.response_function_keywords) + "</response_function>\n"
        s += "</keywords></root>"
        f = open("chatbot_keywords_data.xml", "w", encoding='utf-8')
        f.write(s)
        f.close()
        print("Done !")

    # FUNCTIONS OF CMDBOT:

    # start a program.
    # HOW IT WORKS: use start in cmd.exe. So it only work on windows os currently
    def start_function(self, r_content):
        _cmd = ""
        start_function_case_data = minidom.parse("cmdbot_data.xml").getElementsByTagName("start_function")[0].getElementsByTagName("case")

        _max_similarity_rate = 0.0
        _max_similarity_case = start_function_case_data[0]

        for _case in start_function_case_data:
            for _input in _case.getElementsByTagName("input"):
                _similarity_rate = nlp.word_similarity(_input.firstChild.data, r_content)
                if _similarity_rate > _max_similarity_rate:
                    _max_similarity_rate = _similarity_rate
                    _max_similarity_case = _case

        # debug
        if self.properties['debugmode']:
            print("[Similarity rate: " + str(_max_similarity_rate) + "]")

        if _max_similarity_rate > 0.1:
            _cmd = _max_similarity_case.getElementsByTagName("output")[0].firstChild.data
        else:
            a = input("Do you mean: " + _max_similarity_case.getElementsByTagName('input')[0].firstChild.data + ' <y/n>:\n')
            if a in ['y', 'yes']:
                _cmd = _max_similarity_case.getElementsByTagName("output")[0].firstChild.data

            else:
                print("\n\nCmdBot ko co phan hoi thich hop !")
                learningbot.LearningBot().train("cmdbot")

        os.system(_cmd)

    # shutdown, restart, logout
    def shutdown_function(self, r_content):
        pass
