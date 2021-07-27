
class logger:

    from datetime import datetime
    start_at = None
    flow = ""
    __main_filename__ = ""

    def __init__(self, module, level = 0):

        from pathlib import Path

        # Set level of logs
        self.__info_lv__ = level >= 0
        self.__warning_lv__ = level >= 1

        # Create format and file management
        self.__format__ = "{0} - "
        if module.__type__ == "flow":
            self.__sub_module__ = False
            self.start_at = self.datetime.now().strftime("%Y-%m-%d_%H%M%S")
            self.flow = module.__name__
            self.__format__ += f"flow: {module.__name__} - " + "{1}: {2}"
            Path(f"logs/{self.flow}_{self.start_at}").mkdir(parents=True, exist_ok=True)
            self.__main_filename__ = f"logs/{self.flow}_{self.start_at}/{module.__type__}_{module.__name__}.log"
        else:
            self.__sub_module__ = True
            self.__format__ += f"{module.__type__}: {module.__name__}" + "{1}: {2}"
            print("main file: ", self.__main_filename__)
            self.__main_file__ = open(self.__main_filename__, "a")

        self.__filename__ = f"logs/{self.flow}_{self.start_at}/{module.__type__}_{module.__name__}.log"
        #self.__file__ = open(self.__filename__, "w")

        self.info(f"{module.__type__} {module.__name__} start at {self.datetime.now().strftime('%Y-%m-%d_%H%M%S')}")

    def info(self, message):
        if self.__info_lv__:
            self.__file__ = open(self.__filename__, "a")
            self.__file__.write(self.__format__.format(self.datetime.now().strftime("%Y-%m-%d_%H%M%S"), "INFO", message))
            if self.__sub_module__:
                self.__main_file__ = open(self.__main_filename__, "a")
                self.__main_file__.write(self.__format__.format(self.datetime.now().strftime("%Y-%m-%d_%H%M%S"), "INFO", message))

    def warning(self, message):
        if self.__warning_lv__:
            self.__file__ = open(self.__filename__, "a")
            self.__file__.write(self.__format__.format(self.datetime.now().strftime("%Y-%m-%d_%H%M%S"), "WARNING", message))
            if self.__sub_module__:
                self.__main_file__ = open(self.__main_filename__, "a")
                self.__main_file__.write(self.__format__.format(self.datetime.now().strftime("%Y-%m-%d_%H%M%S"), "WARNING", message))

    def error(self, message):
        print(self.__filename__)
        self.__file__ = open(self.__filename__, "a")
        self.__file__.write(self.__format__.format(self.datetime.now().strftime("%Y-%m-%d_%H%M%S"), "ERROR", message))
        if self.__sub_module__:
            self.__main_file__ = open(self.__main_filename__, "a")
            self.__main_file__.write(self.__format__.format(self.datetime.now().strftime("%Y-%m-%d_%H%M%S"), "ERROR", message))
