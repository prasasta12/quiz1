from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen


class Quiz(Screen):
    def __init__(self, name='first'):
        super().__init__(name=name)
        btn1 = Button(text="Button 1")
        btn2 = Button(text="Button 2")
        btn3 = Button(text="Button 3")
        btn4 = Button(text="Button 4")
        question_label = Label(text="Choose an answer:")
        answer_layout = BoxLayout(orientation="horizontal",padding=50,spacing=20)
        page_layout = BoxLayout(orientation="vertical")

        answer_layout.add_widget(btn1)
        answer_layout.add_widget(btn2)
        answer_layout.add_widget(btn3)
        answer_layout.add_widget(btn4)
        page_layout.add_widget(question_label)
        page_layout.add_widget(answer_layout)
        self.add_widget(page_layout)
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Quiz(name='first'))
        return sm
app = MyApp()
app.run()