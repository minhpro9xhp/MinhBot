from botlib import Botlib
from collections import deque
from xml.dom import minidom


class Bot:
    history_cmd = deque()

    function_dict = {}


    def __init__(self):
        self.initialize_keywords()
        self.history_cmd = deque(['' for i in range(5)], maxlen=5)


    def initialize_keywords(self):

        keywords_function_file = minidom.parse("keywords_function.xml")
        functions_data = keywords_function_file.getElementsByTagName("function")

        for function in functions_data:
            self.function_dict[function.getElementsByTagName("id")[0].firstChild.data] = \
                function.getElementsByTagName("keywords")[0].firstChild.data.split(',')


    def comply(self, cmd):
        # tao dict de kiem tra so diem cua moi function. Function nao co diem cao nhat thi chon function ay
        point_dict = {key: 0 for key in self.function_dict.keys()}
        for key in point_dict.keys():
            for keyword in self.function_dict[key]:
                if keyword in cmd:
                    point_dict[key] += 1

        max_point = max(point_dict.values())
        selected_function = ''

        for key in point_dict.keys():
            if point_dict[key] == max_point:
                selected_function = key
        #

        botlib.use_function(selected_function, cmd)


    def response(self, *args):
        if args:
            print(args[0])
            return
        if type(botlib.response) is list:
            for res in botlib.response:
                print(res)
        elif type(botlib.response) is str:
            print(botlib.response)
        else:
            print("Error: TypeError ! bot.response()")


botlib = Botlib()
bot = Bot()


bot.response('I\'m ready to serve you, sir !')
bot.response('What is your command ?:\n')

while True:
    command = input().strip()
    if command == '':
        continue
    bot.history_cmd.append(command)
    bot.comply(command)
    bot.response()
