import PySimpleGUI as sg
import Library.dictionairs as lib_dict
import Library.passwordGenerator as lib_pass
import json
import os

class main_windown():
    def __init__(self,theme='DarkAmber'):
        sg.theme(theme)   # Add a touch of color
        self.layout =   [[sg.Text('Password Generator')],
                        [sg.Text('Generated password: '), sg.Text(key="OutPass",size=(50,1))],
                        [sg.Button('Generate')],
                        [sg.Text("Configurations")],
                        [sg.Text("Add a new dictionair"),sg.Button("add folder"),sg.Button("add file")],
                        [sg.Text("Password size: "),sg.Slider(range=(1,50),orientation="h",key="SizeSlider",enable_events=True)],
                        [sg.Text("Numbers in password: "),sg.Slider((0,100),orientation="h",key="SliderNumber",enable_events=True),sg.Checkbox("Don't Care",enable_events=True,key="CheckNumber")],
                        [sg.Text("Upper case: "),sg.Slider((0,100),orientation="h",key="SliderUpper"),sg.Checkbox("Don't Care",key="CheckUpper")],
                        [sg.Text("Sybols: "),sg.Slider((0,100),orientation="h",key="SliderSybols"),sg.Checkbox("Don't Care",key="CheckSybols")]]
        
        self.window = sg.Window('Password Generator', self.layout)
        self.config_keys = {"defalt_configfile_path":"Library/win_config.txt",
                            "dictionair_filepath":[["/Dictionairs",True]]}
        self.Dictionair = []
        self.Generator = lib_pass.PasswordGenerator()
        self.load_config()
    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
                break
            if event == "add folder":
                path = sg.popup_get_folder("Please select a folder that contains the dictionairs")
                self.config_keys["dictionair_filepath"] += [path, True]
                self.save_config()
            if event == "Generate":
                password = self.Generator.generate_password(1)
                self.window["OutPass"].update(password[0])
            if event == "SliderNumber":
                if values["CheckNumber"] == False:
                    self.Generator.numbers = values["SliderNumber"]/100
            if event == "CheckNumber":
                if values["CheckNumber"] == True:
                    self.Generator.numbers = -1
                else:
                    self.Generator.numbers = values["SliderNumber"]/100
            if event == "SizeSlider":
                self.Generator.size = values["SizeSlider"]
        self.window.close()

    def save_config(self):
        with open(self.config_keys["defalt_configfile_path"],"w") as config_file:
            json.dump(self.config_keys,config_file)
    def load_config(self):
        if os.path.isfile(self.config_keys["defalt_configfile_path"]):
            with open(self.config_keys["defalt_configfile_path"]) as config_file:
                self.config_keys = json.load(config_file)
        else:
            sg.popup("Unable to load configuration files for this application")
        dict_to_check = self.config_keys["dictionair_filepath"]
        failed = []
        for item in dict_to_check:
            print(item)
            if not lib_dict.Dicionario.is_valid_path(item[0],bool(item[1])):
                failed.append(item[0])
        if len(failed) == len(dict_to_check) and len(failed) > 0:
            result = sg.popup_yes_no("Unable to load all dictionair files, do you want to remove then?")
            if result == "Yes":
                self.config_keys["dictionair_filepath"] = []
                self.save_config()
        elif len(failed) > 0:
            sg.popup("Unable to load: {}".format(failed))
        else:
            for dictionair in self.config_keys["dictionair_filepath"]:
                tempdict = lib_dict.Dicionario(dictionair[0],dictionair[1])
                tempdict.load_dictionair()
                self.Dictionair.append(tempdict)
            self.Generator.load_dictionairs(self.Dictionair)
            print(self.Generator.dicionario.data)