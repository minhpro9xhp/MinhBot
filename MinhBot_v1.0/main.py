from cmd import Cmd
from xml.dom import minidom

import nlp
import users
from chatbot import ChatBot
from cmdbot import CmdBot
from infobot import InfoBot
from learningbot import LearningBot


class MainBot:
    properties = dict()

    bot_keywords_data = minidom.parse("bot_keywords_data.xml")
    chatbot_keywords = bot_keywords_data.getElementsByTagName("chatbot")[0].firstChild.data.strip().split(',')
    infobot_keywords = bot_keywords_data.getElementsByTagName("infobot")[0].firstChild.data.strip().split(',')
    cmdbot_keywords = bot_keywords_data.getElementsByTagName("cmdbot")[0].firstChild.data.strip().split(',')
    learningbot_keywords = bot_keywords_data.getElementsByTagName("learningbot")[0].firstChild.data.strip().split(',')

    # Khoi tao properties
    def __init__(self):
        mainbot_data = minidom.parse("mainbot_data.xml")
        properties_data = mainbot_data.getElementsByTagName("properties")[0]

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
            print("[MainBot is active]")

    def choose_bot(self, r_content):
        chatbot_point = 0
        infobot_point = 0
        cmdbot_point = 0
        learningbot_point = 0
        r_content_list = nlp.word_tokenize(r_content)
        for _key in self.chatbot_keywords:
            if _key.strip() in r_content_list:
                chatbot_point += 1
        for _key in self.infobot_keywords:
            if _key.strip() in r_content_list:
                infobot_point += 1
        for _key in self.cmdbot_keywords:
            if _key.strip() in r_content_list:
                cmdbot_point += 1
        for _key in self.learningbot_keywords:
            if _key.strip() in r_content_list:
                learningbot_point += 1

        max_point = max(chatbot_point, infobot_point, cmdbot_point, learningbot_point)

        # debug
        if self.properties['debugmode']:
            print('[chatBot: ' + str(chatbot_point) + "]")
            print('[infoBot: ' + str(infobot_point) + "]")
            print('[cmdBot:  ' + str(cmdbot_point) + "]")
            print('[learningBot: ' + str(learningbot_point) + "]")
            print('[max_point: ' + str(max_point) + "]")

        # Hoi y kien nguoi dung neu co 2 hoac nhieu bot co cung so diem
        if [chatbot_point, infobot_point, cmdbot_point, learningbot_point].count(max_point) > 1:
            a = input("Not very clear. Which bot should i choose ?\n"
                 "1. ChatBot\n"
                 "2. InfoBot\n"
                 "3. CmdBot\n"
                 "4. LearningBot\n"
                 "Your choice: ")

            if a == '2':
                self.infobot_keywords += nlp.word_tokenize(cmd.raw_content)
                self.infobot_keywords = nlp.remove_duplicate_in_list(self.infobot_keywords)
                self.save_keywords_data_xml()
                return 'infobot'

            elif a == '3':
                self.cmdbot_keywords += nlp.word_tokenize(cmd.raw_content)
                self.cmdbot_keywords = nlp.remove_duplicate_in_list(self.cmdbot_keywords)
                self.save_keywords_data_xml()
                return 'cmdbot'
            elif a == '4':
                self.learningbot_keywords += nlp.word_tokenize(cmd.raw_content)
                self.learningbot_keywords = nlp.remove_duplicate_in_list(self.learningbot_keywords)
                self.save_keywords_data_xml()
                return 'learningbot'
            else:
                self.chatbot_keywords += nlp.word_tokenize(cmd.raw_content)
                self.chatbot_keywords = nlp.remove_duplicate_in_list(self.chatbot_keywords)
                self.save_keywords_data_xml()
                return 'chatbot'

        if max_point == 0 or max_point == chatbot_point:
            return 'chatbot'
        else:
            if max_point == infobot_point:
                return 'infobot'
            elif max_point == cmdbot_point:
                return 'cmdbot'
            else:
                return 'learningbot'

    def comply(self):
        cmd.raw_content = nlp.remove_punctuation(input())
        cmd.raw_content = nlp.check_spelling(cmd.raw_content)
        cmd.content[0] = self.choose_bot(cmd.raw_content)

        self.send_cmd_to_bot()

    @staticmethod
    def send_cmd_to_bot():
        if cmd.content[0] == "chatbot":
            chatBot.comply(cmd)
        elif cmd.content[0] == "cmdbot":
            cmdBot.comply(cmd)
        elif cmd.content[0] == "infobot":
            infoBot.comply(cmd)
        elif cmd.content[0] == "learningbot":
            learningBot.comply(cmd)


    def save_keywords_data_xml(self):
        # write to .xml file
        s = "<root><keywords>"
        s += "<chatbot>" + ', '.join(self.chatbot_keywords) + "</chatbot>\n"
        s += "<infobot>" + ', '.join(self.infobot_keywords) + "</infobot>\n"
        s += "<cmdbot>" + ', '.join(self.cmdbot_keywords) + "</cmdbot>\n"
        s += "<learningbot>" + ', '.join(self.learningbot_keywords) + "</learningbot>\n"
        s += "</keywords></root>"
        f = open("bot_keywords_data.xml", "w", encoding='utf-8')
        f.write(s)
        f.close()
        print("Done !")

mainBot = MainBot()
chatBot = ChatBot()
cmdBot = CmdBot()
infoBot = InfoBot()
learningBot = LearningBot()


while not mainBot.properties['isactive']:
    user, mainBot.properties['isactive'] = users.login()

# main program
print("Minh's bot are ready to serve !\nYour command:")
while True:
    cmd = Cmd()
    mainBot.comply()
