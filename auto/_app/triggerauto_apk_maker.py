import sys
import subprocess
import auto
import math

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooser
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

def text_rearrange(text:str, width:int, height:int)->str:
    font_sum = math.floor(width / 10)
    line_sum = math.floor(height / 30)
    text_list = text.split("\n")
    text_matrix = [[text_one[i * font_sum:min((i + 1) * font_sum, len(text_one))] for i in range(math.ceil(len(text_one) / font_sum))] for text_one in text_list if text_one != ""]
    text_ans = ""
    for enter_now in range(len(text_matrix) - 1, -1, -1):
        if len(text_matrix[enter_now]) < line_sum:
            text_temp = ""
            for line_now in range(len(text_matrix[enter_now])):
                text_temp = text_temp + text_matrix[enter_now][line_now]
            text_ans = text_temp + "\n" + text_ans
            line_sum = line_sum - len(text_matrix[enter_now])
        else:
            text_temp = ""
            for line_now in range(len(text_matrix[enter_now]) - line_sum, len(text_matrix[enter_now])):
                text_temp = text_temp + text_matrix[enter_now][line_now]
            text_ans = text_temp + "\n" + text_ans
            break
    return text_ans

class AutoFileChooser(BoxLayout):
    pass 

class TriggerAutoMission(BoxLayout):

    def run_command(self, command):
        result = subprocess.run(command, shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text=True)
        self.ids.stdout.text = text_rearrange(self.ids.stdout.text + result.stdout, self.ids.stdout.width, self.ids.stdout.height)
        self.ids.stderr.text = text_rearrange(self.ids.stderr.text + result.stderr, self.ids.stderr.width, self.ids.stderr.height)

    def startTriggerAuto(self):
        inputfilepath = self.ids.inputfilepath.text
        outputfilepath = self.ids.outputfilepath.text
        options = self.ids.options.text
        outputfileoption = " -o " + outputfilepath if outputfilepath != "" else ""
        command = 'triggerauto ' + inputfilepath + outputfileoption + " " + options  # 这里是一个示例命令，实际使用时替换为需要执行的命令
        self.run_command(command)

class TriggerAutoApp(App):
    def build(self):
        triggerautomission = TriggerAutoMission()
        return triggerautomission


if __name__ == '__main__':
    TriggerAutoApp().run()