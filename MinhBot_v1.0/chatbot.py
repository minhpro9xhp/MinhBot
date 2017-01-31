from random import randint
from xml.dom import minidom

import learningbot
import nlp


class ChatBot:
    properties = dict()

    chatbot_keywords_data = minidom.parse("chatbot_keywords_data.xml")
    response_function_keywords = chatbot_keywords_data.getElementsByTagName("response_function")[0].firstChild.data.split(',')

    # Khoi tao csdl cua chatbot
    def __init__(self):
        chatbot_data = minidom.parse("chatbot_data.xml")
        properties_data = chatbot_data.getElementsByTagName("properties")[0]

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
            print("[ChatBot is active]")


    def choose_function(self, r_content):
        response_function_point = 0

        for _key in self.response_function_keywords:
            if _key.strip() in r_content:
                response_function_point += 1

        max_point = max(response_function_point, 0)

        # debug
        if self.properties['debugmode']:
            print('[response_function: ' + str(response_function_point) + "]")

        if [response_function_point, 0].count(max_point) > 1:
            a = input("Not very clear. Which function should i choose ?\n"
                 "1. Response\n"
                 "2. \n"
                 "3. \n"
                 "4. \n"
                 "Your choice: ")

            if a == '2':
                return 'response_function'

            elif a == '3':
                return 'response_function'
            elif a == '4':
                return 'response_function'
            else:
                self.response_function_keywords += nlp.word_tokenize(r_content)
                self.response_function_keywords = nlp.remove_duplicate_in_list(self.response_function_keywords)
                self.save_keywords_data_xml()
                return 'response_function'

        if max_point == 0 or max_point == response_function_point:
            return 'response_function'
        else:
            return 'response_function'

    def save_keywords_data_xml(self):
        s = "<root><keywords>"
        s += "<response_function>" + ', '.join(self.response_function_keywords) + "</response_function>\n"
        s += "</keywords></root>"
        f = open("chatbot_keywords_data.xml", "w", encoding='utf-8')
        f.write(s)
        f.close()
        print("Done !")

    def use_function(self, _cmd):
        if _cmd.content[1] == "response_function":
            self.response_function(_cmd.raw_content)

    def comply(self, cmd):
        cmd.content[1] = self.choose_function(cmd.raw_content)
        self.use_function(cmd)

    # FUNCTIONS OF CHATBOT:

    # talk with the user
    def response_function(self, inp):
        chatbot_response_function_data = minidom.parse("chatbot_data.xml").getElementsByTagName("response_function")[0].getElementsByTagName("case")
        _max_similarity_rate = 0.0
        _max_similarity_situation = chatbot_response_function_data[0]

        for _situation in chatbot_response_function_data:
            for _input in _situation.getElementsByTagName("input"):
                _similarity_rate = nlp.word_similarity(_input.firstChild.data, inp)
                if _similarity_rate > _max_similarity_rate:
                    _max_similarity_rate = _similarity_rate
                    _max_similarity_situation = _situation

        # debug
        if self.properties['debugmode']:
            print("[Similarity rate: " + str(_max_similarity_rate) + "]")

        if _max_similarity_rate > 0.1:
            print(_max_similarity_situation.getElementsByTagName("output")[randint(0,
                    len(_max_similarity_situation.getElementsByTagName("output")) - 1)].firstChild.data)
        else:
            a = input("Do you mean: " + _max_similarity_situation.getElementsByTagName('input')[0].firstChild.data + ' <y/n>:\n')
            if a in ['y', 'yes']:
                print(_max_similarity_situation.getElementsByTagName("output")[randint(0,
                    len(_max_similarity_situation.getElementsByTagName("output")) - 1)].firstChild.data)

            else:
                print("\n\nChatBot ko co phan hoi thich hop !")
                learningbot.LearningBot().train("chatbot")
