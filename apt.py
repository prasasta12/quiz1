from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

# Atur ukuran jendela agar tampak rapi di desktop (opsional)
Window.size = (600, 400)

# Tema laut: warna latar, aksen, dan teks
# Window.clearcolor uses RGBA with values 0-1 (teal/blue background)
Window.clearcolor = (0.05, 0.35, 0.45, 1)  # deep teal / sea color

# Warna tema untuk teks dan tombol
THEME_TEXT_COLOR = (1, 1, 1, 1)  # putih
THEME_BTN_COLOR = (0.12, 0.6, 0.7, 1)  # lighter teal for buttons
THEME_BTN_DOWN_COLOR = (0.02, 0.45, 0.55, 1)
THEME_ACCENT = (0.0, 0.7, 0.9, 1)

# Questions are stored in a separate module
from questions import QUESTIONS


class StartScreen(Screen):
    """Layar awal berisi judul dan tombol Mulai"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        title = Label(text='Quiz Sederhana', font_size=32, size_hint=(1, 0.4))
        subtitle = Label(text='Selamat datang! Tekan Mulai untuk memulai quiz.', size_hint=(1, 0.2))
        # Apply theme colors
        title.color = THEME_TEXT_COLOR
        subtitle.color = THEME_TEXT_COLOR

        start_btn = Button(text='Mulai', size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        start_btn.background_color = THEME_BTN_COLOR
        start_btn.color = THEME_TEXT_COLOR

        # Ketika tombol Mulai ditekan, pindah ke layar quiz dan mulai quiz dari awal
        start_btn.bind(on_release=self.start_quiz)

        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(start_btn)
        self.add_widget(layout)

    def start_quiz(self, *args):
        # Akses ScreenManager untuk menemukan widget QuizScreen dan memulai quiz
        sm = self.manager
        sm.current = 'quiz'
        quiz_screen = sm.get_screen('quiz')
        quiz_screen.start()


class QuizScreen(Screen):
    """Layar utama quiz yang menampilkan pertanyaan dan pilihan jawaban."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_index = 0
        self.score = 0

        # Layout utama vertikal
        self.page_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Label pertanyaan (ditempatkan di tengah, tanpa nomor soal)
        self.question_label = Label(text='', font_size=22, halign='center', valign='middle', size_hint=(1, 0.35))
        # center the text block and wrap
        self.question_label.bind(size=self._update_text_size)
        self.question_label.color = THEME_TEXT_COLOR

        # Layout untuk pilihan jawaban — tampilkan seperti Quizizz: 2 kolom
        self.answer_layout = GridLayout(cols=2, spacing=12, size_hint_y=None)
        # We will control the height so the grid doesn't collapse
        self.answer_layout.bind(minimum_height=self.answer_layout.setter('height'))

        # Buat 4 ToggleButton untuk pilihan A-D, tampil seperti kartu mendatar
        self.choice_buttons = []
        for i in range(4):
            tb = ToggleButton(text='', group='answers', allow_no_selection=True, size_hint=(0.95, None), height=70)
            # style toggle buttons to match theme and look like Quizizz cards
            tb.background_color = THEME_BTN_COLOR
            tb.color = THEME_TEXT_COLOR
            tb.font_size = 16
            tb.halign = 'left'
            tb.valign = 'middle'
            # bind text_size to the current width so text wraps correctly
            tb.bind(size=lambda inst, val: setattr(inst, 'text_size', (inst.width - 20, None)))
            # auto-adjust height when texture (rendered text) size changes
            tb.bind(texture_size=lambda inst, val: setattr(inst, 'height', max(60, inst.texture_size[1] + 20)))
            self.choice_buttons.append(tb)
            self.answer_layout.add_widget(tb)

        # Label informasi (mis. minta pilih jawaban jika belum)
        # Info label uses an accent color for emphasis
        self.info_label = Label(text='', size_hint=(1, 0.1), color=THEME_ACCENT)

        # Tombol Next
        self.next_btn = Button(text='Next', size_hint=(1, 0.15))
        self.next_btn.background_color = THEME_BTN_COLOR
        self.next_btn.color = THEME_TEXT_COLOR
        self.next_btn.bind(on_release=self.next_question)

        # Tambahkan widget ke layout
        # Place the question label on top and options below; question label has larger space for vertical centering
        self.page_layout.add_widget(self.question_label)
        self.page_layout.add_widget(self.answer_layout)
        self.page_layout.add_widget(self.info_label)
        self.page_layout.add_widget(self.next_btn)

        self.add_widget(self.page_layout)

    def _update_text_size(self, instance, value):
        # Membuat teks label membungkus sesuai ukuran
        instance.text_size = (instance.width - 20, None)

    def start(self):
        """Set ulang nilai dan tampilkan pertanyaan pertama."""
        self.current_index = 0
        self.score = 0
        self.info_label.text = ''
        self.show_question()

    def show_question(self):
        """Tampilkan pertanyaan dan isi pilihan jawaban."""
        q = QUESTIONS[self.current_index]
        # Tampilkan teks pertanyaan saja (tanpa nomor)
        self.question_label.text = q['question']

        # Tampilkan pilihan pada ToggleButton
        for i, choice in enumerate(q['choices']):
            btn = self.choice_buttons[i]
            btn.text = f"{chr(65 + i)}. {choice}"
            btn.state = 'normal'  # reset pilihan
            # update text wrapping and size
            btn.text_size = (btn.width - 20, None)
            btn.height = max(60, btn.texture_size[1] + 20)

        # Jika ada lebih sedikit pilihan dari 4, sembunyikan sisanya (tidak diperlukan di data ini)
        for j in range(len(q['choices']), 4):
            self.choice_buttons[j].text = ''
            self.choice_buttons[j].state = 'normal'
            self.choice_buttons[j].height = 0

    def next_question(self, *args):
        """Menangani logika saat tombol Next ditekan."""
        # Cari pilihan yang dipilih
        selected = None
        for i, btn in enumerate(self.choice_buttons):
            if btn.state == 'down':
                selected = i
                break

        if selected is None:
            # Jika belum memilih jawaban, tunjukkan pesan
            self.info_label.text = 'Pilih jawaban terlebih dahulu.'
            return

        # Reset pesan info
        self.info_label.text = ''

        # Cek jawaban benar
        correct = QUESTIONS[self.current_index]['answer']
        if selected == correct:
            self.score += 1

        # Lanjut ke soal berikutnya atau ke hasil
        self.current_index += 1
        if self.current_index < len(QUESTIONS):
            self.show_question()
        else:
            # Tampilkan layar hasil
            sm = self.manager
            result_screen = sm.get_screen('result')
            result_screen.show_result(self.score, len(QUESTIONS))
            sm.current = 'result'


class ResultScreen(Screen):
    """Layar hasil yang menampilkan skor total."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        self.result_label = Label(text='', font_size=24)
        self.detail_label = Label(text='')

        # Tombol untuk mengulang quiz
        restart_btn = Button(text='Ulangi', size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        restart_btn.background_color = THEME_BTN_COLOR
        restart_btn.color = THEME_TEXT_COLOR
        restart_btn.bind(on_release=self.restart)

        layout.add_widget(self.result_label)
        layout.add_widget(self.detail_label)
        layout.add_widget(restart_btn)
        self.add_widget(layout)

    def show_result(self, score, total):
        # Tampilkan skor akhir
        self.result_label.text = f"Skor Anda: {score} / {total}"
        # Berikan pesan sederhana berdasarkan skor
        if score == total:
            self.detail_label.text = 'Bagus! Semua jawaban benar.'
        elif score >= total // 2:
            self.detail_label.text = 'Cukup baik, coba lagi untuk mendapat nilai lebih baik.'
        else:
            self.detail_label.text = 'Ayo belajar lagi, jangan menyerah!'

    def restart(self, *args):
        # Kembali ke layar awal
        sm = self.manager
        sm.current = 'start'


class MyApp(App):
    def build(self):
        # Buat ScreenManager dan tambahkan tiga layar: start, quiz, result
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(QuizScreen(name='quiz'))
        sm.add_widget(ResultScreen(name='result'))
        return sm


if __name__ == '__main__':
    MyApp().run()