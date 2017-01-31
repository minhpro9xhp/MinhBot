from xml.dom import minidom

import nlp

cmd_data_list = minidom.parse("cmd.xml").getElementsByTagName("cmd")


class Cmd:
    raw_content = ""
    content = ["", "", ""]
    # content[0] la bot
    # content[1] la function
    # content[2] la parameter

    def nlp(self):
        _max_similarity_rate = 0.0
        _max_similarity_cmd = cmd_data_list[0]

        for _cmd in cmd_data_list:
            for _user in _cmd.getElementsByTagName("user"):
                _similarity_rate = nlp.word_similarity(_user.firstChild.data, self.raw_content)

                if _similarity_rate > 0.9:
                    _max_similarity_cmd = _cmd
                    _max_similarity_rate = _similarity_rate
                    break

                if _similarity_rate > _max_similarity_rate:
                    _max_similarity_cmd = _cmd
                    _max_similarity_rate = _similarity_rate

        def proceed_code(_code):
            if _code.count("@bot") != 1:
                print("Missing @bot !")
                return
            if _code.count("@function") != 1:
                print("Missing @function !")
                return
            if _code.count("@parameter") != 1:
                print("Missing @parameter !")
                return
            if _code.count("@response") != 1:
                print("Missing @response !")

            _list = _code.strip().replace(' @', ' @@').split(' @')
            _list.sort()
            if _list.count("@response") == 0:
                _list.append("@response null")
            _list[0] = _list[0].replace("@bot ", "")
            _list[1] = _list[1].replace("@function ", "")
            _list[2] = _list[2].replace("@parameter ", "")
            _list[3] = _list[3].replace("@response ", "")
            return _list

        if _max_similarity_rate > 0.1:
            self.content = proceed_code(_max_similarity_cmd.getElementsByTagName("bot")[0].firstChild.data)
            return
        else:
            self.content = ["chatbot", 'response', self.raw_content]
            return



