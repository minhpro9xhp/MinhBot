from xml.dom import minidom

import nlp


class InfoBot:
    properties = dict()

    def __init__(self):
        infobot_data = minidom.parse("infobot_data.xml")
        properties_data = infobot_data.getElementsByTagName("properties")[0]

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
            print("[InfoBot is active]")

    def comply(self, cmd):
        return

    def help(self):
        return
