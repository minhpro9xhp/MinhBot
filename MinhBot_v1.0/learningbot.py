from xml.dom import minidom

import nlp


class LearningBot:
    properties = dict()

    def __init__(self):
        learningbot_data = minidom.parse("learningbot_data.xml")
        properties_data = learningbot_data.getElementsByTagName("properties")[0]

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
            print("[LearningBot is active]")

    def comply(self, cmd):
        if cmd.content[2] == "chatbot":
            self.train_chatbot()
        elif cmd.content[2] == "cmdbot":
            self.train_cmdbot()
        elif cmd.content[2] == "infobot":
            self.train_infobot()
        elif cmd.content[2] == "learningbot":
            self.train()
        return

    @staticmethod
    def train_chatbot():
        print("1. Quick training: ")
        print("2. Manual traning: ")
        try:
            a = int(input("Your choice : "))
        except ValueError:
            a = 1
        if a != 2:
            _code = input("Enter the code: (Write it care fully)\n")
            # Example: @bot chatbot @function response @parameter Bonjour @response I don't speak croissant !

            def proceed_code(_para):
                if _para.count("@function") != 1:
                    print("Missing @function !")
                    return
                if _para.count("@input") != 1:
                    print("Missing @input !")
                    return
                if _para.count("@output") != 1:
                    print("Missing @output !")

                _list = _para.strip().replace(' @', ' @@').split(' @')
                _list.sort()
                if _list.count("@output") == 0:
                    _list.append("@output null")
                _list[0] = _list[0].replace("@function ", "")
                _list[1] = _list[1].replace("@input ", "")
                _list[2] = _list[2].replace("@output ", "")
                return _list

            _list = proceed_code(_code)
            print(_list)
            if len(_list) < 4:
                return
            else:
                _function = _list[1]
                _parameter = _list[2]
                _response = _list[3]

            chatbot_data = minidom.parse("chatbot_data.xml")

            if _function == "response":
                chatbot_response_data = chatbot_data.getElementsByTagName("response_function")[0]

                _new_element = chatbot_data.createElement("case")
                _new_input = chatbot_data.createElement("input")
                _new_output = chatbot_data.createElement("output")
                _new_input.appendChild(chatbot_data.createTextNode(_parameter))
                _new_output.appendChild(chatbot_data.createTextNode(_response))
                _new_element.appendChild(_new_input)
                _new_element.appendChild(_new_output)
                chatbot_response_data.appendChild(_new_element)

                f = open("chatbot_data.xml", 'w', encoding='utf-8')
                chatbot_data.writexml(f)
                f.close()

                print("Finished training process !")


        return

    @staticmethod
    def train_cmdbot():
        print("1. Quick training: ")
        print("2. Manual traning: ")
        a = input('Your choice:\n')
        if a != '2':
            _code = input("Enter the code: (Write it care fully)\n")

            # Example: @function response @parameter Bonjour @response I don't speak croissant !

            def proceed_code(_para):
                if _para.count("@function") != 1:
                    print("Missing @function !")
                    return
                if _para.count("@input") != 1:
                    print("Missing @input !")
                    return
                if _para.count("@output") != 1:
                    print("Missing @output !")
                    return

                _list = _para.strip().replace(' @', ' @@').split(' @')
                _list.sort()
                if _list.count("@output") == 0:
                    _list.append("@response null")
                _list[0] = _list[0].replace("@function ", "")
                _list[1] = _list[1].replace("@input ", "")
                _list[2] = _list[2].replace("@output ", "")
                return _list

            _list = proceed_code(_code)
            print(_list)
            if len(_list) < 3:
                return
            else:
                _function = _list[0]
                _parameter = _list[1]
                _response = _list[2]

            cmdbot_data = minidom.parse("cmdbot_data.xml")

            cmdbot_function_data = []
            if _function == "start":
                cmdbot_function_data = cmdbot_data.getElementsByTagName("start_function")[0]

            elif _function == "shutdown":
                cmdbot_function_data = cmdbot_data.getElementsByTagName("shutdown_function")[0]

            _new_element = cmdbot_data.createElement("case")
            _new_input = cmdbot_data.createElement("input")
            _new_output = cmdbot_data.createElement("output")
            _new_input.appendChild(cmdbot_data.createTextNode(_parameter))
            _new_output.appendChild(cmdbot_data.createTextNode(_response))
            _new_element.appendChild(_new_input)
            _new_element.appendChild(_new_output)
            cmdbot_function_data.appendChild(_new_element)

            f = open("cmdbot_data.xml", 'w', encoding='utf-8')
            cmdbot_data.toprettyxml()
            cmdbot_data.writexml(f)
            f.close()

            print("Finished training process !")

        return

    def train_infobot(self):
        return

    def train(self, *para):
        if len(para) == 0:
            a = input("Do you want to teach me ? <y/n>")
            if a.lower() == "y" or a.lower() == "yes":
                print("Choose bot to train:\n")
                print("1. Chatbot")
                print("2. Cmdbot")
                print("3. Infobot")

                if a == '1':
                    self.train_chatbot()
                elif a == '2':
                    self.train_cmdbot()
                elif a == '3':
                    self.train_infobot()
                else:
                    self.train_chatbot()
        else:
            a = input("Do you want to teach me ? <y/n>")
            if a.lower() in ['y', 'yes']:
                if para[0] == "chatbot":
                    self.train_chatbot()
                elif para[0] == "infobot":
                    self.train_infobot()
                elif para[0] == "cmdbot":
                    self.train_cmdbot()
