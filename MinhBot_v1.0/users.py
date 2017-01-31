from xml.dom import minidom

users_data = minidom.parse("users.xml")


class User:
    name = ""
    id = ""
    password = ""
    isLogOn = False
    lastTimeLogin = ""

    class Body:
        height = 0
        weight = 0
        bmi_rate = 0


def get_dict_users():
    _dict = dict()
    for user_data in users_data.getElementsByTagName("user"):
        user = User()

        user.name = user_data.getElementsByTagName("name")[0].firstChild.data
        user.id = user_data.getElementsByTagName("id")[0].firstChild.data
        user.password = user_data.getElementsByTagName("password")[0].firstChild.data

        _dict.update({user.id: user})
    return _dict


def login():
    _user = User()
    print("Please login ")
    _id = input("ID: ")

    if _id in dict_users.keys():
        while True:
            _password = input("Password: ")
            if _password == dict_users[_id].password:
                _user = dict_users[_id]

                break
            else:
                a = input("Password is not correct. Please enter again. <enter \"back\" to go back>:\n ")
                if a == "back":
                    break
    else:
        a = input("This account doesn't exist. Do you want to sign up ? <y/n>:\n")
        if a.lower() in ['y', 'yes']:
            sign_up()

    return _user, True


def sign_up():
    while True:
        while True:
            _id = input("What is your ID ?\n")
            if _id not in dict_users.keys():
                if _id.isalpha:
                    break
                else:
                    print("ID is not valid")
                    continue
            else:
                print("This ID is used")
                continue

        while True:
            _password = input("What is your password ?\n")
            _isValid = True
            for symbol in [' ', '/', '%', '$', '#', '@', '!', '^', '&', '*', '(', ')']:
                if symbol in _password:
                    print("Password is not valid")
                    _isValid = False
                    break

            if _isValid:
                break
        try:
            _name = input("What is your name ?\n")
        except ValueError:
            _name = "unknown"

        _user = User()
        _user.id = _id
        _user.password = _password
        _user.name = _name
        _user.lastTimeLogin = " "

        dict_users.update({_user.id: user})
        add_new_user()


def add_new_user():
    s = "<users>\n\t"
    for key in dict_users.keys():
        obj = dict_users[key]
        u = "<user>\n\t\t"
        u += "<name>" + obj.name + "</name>\n\t\t"
        u += "<id>" + obj.id + "</id>\n\t\t"
        u += "<password>" + obj.password + "</password>\n\t\t"
        u += "<lasttimelogin>" + obj.lastTimeLogin + "</lasttimelogin>\n\t"
        u += "</user>\n\t"

        s += u
    s += "</users>"

    f = open("users.xml", 'w', encoding="utf-8")
    f.write(s)
    f.close()


dict_users = get_dict_users()
