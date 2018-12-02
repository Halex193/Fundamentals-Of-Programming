class Settings:
    def __init__(self):
        self.__defaultSettings = {
            "repository": 'inmemory',
            "studentsFile": '',
            "gradesFile": '',
            "assignmentsFile": '',
            "ui": 'MenuUI'
        }
        self.__settings = {}
        self.__settings.update(self.__defaultSettings)
        self.readFile()

    def readFile(self):
        settingsFile = None
        try:
            settingsFile = open("settings.properties", "r")
            lines = settingsFile.readlines()
            for line in lines:
                components = line.split("=")
                if components[0] in self.__settings.keys():
                    self.__settings[components[0]] = components[1].replace('\"', '').replace("\n", '')
        except FileNotFoundError:
            pass
        finally:
            if settingsFile is not None:
                settingsFile.close()

    def __getitem__(self, item):
        return self.__settings[item]
