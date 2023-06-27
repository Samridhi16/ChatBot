import socket
import threading
import pyttsx3
import sys
import winsound
from TTS.api import TTS
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QHBoxLayout, \
    QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal, QObject


class ChatClient(QObject):
    message_received = pyqtSignal(str)

    def __init__(self, host, port, username):
        super().__init__()
        self.host = host
        self.port = port
        self.username = username
        self.socket = None
        self.text_to_speech_enabled = False
        self.last_response = ""
        self.entity_labels = ['ORGANIZATION', 'PERSON', 'LOCATION', 'DATE', 'TIME', 'MONEY', 'PERCENT', 'FACILITY', 'GPE', 'NORP', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'QUANTITY', 'ORDINAL', 'CARDINAL']


    def connect_to_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.send(self.username.encode())

    def send_message(self, message):
        self.socket.send(message.encode())

    def receive_message(self):
        while True:
            message = self.socket.recv(1024).decode()
            if message:
                entity_detected = False

                for label in self.entity_labels:
                    if message.startswith(label + ':'):
                        entity_detected = True
                        # Extract entity label and message content
                        label_end_index = message.index(':')
                        entity_label = message[:label_end_index]
                        message = message[label_end_index + 1:]

                        self.message_received.emit(f'<b class="entity">Entity=>{entity_label}:</b> {message}')
                        break

                if not entity_detected:
                    self.last_response = message
                    message_with_prefix = f'<b class="bot">{message}</b>'
                    self.message_received.emit(message_with_prefix)
                    if self.text_to_speech_enabled:
                        self.speak_message()

    def speak_message(self):
        engine = pyttsx3.init()
        engine.say(self.last_response)
        engine.runAndWait()

    def neural_speak_message(self):
        tts.tts_to_file(text=self.last_response, speaker=tts.speakers[0],
                        language=tts.languages[0], file_path="output.wav")
        file_path = "output.wav"
        winsound.PlaySound(file_path, winsound.SND_FILENAME)

    def check_entities(self):
        if self.last_response:
            self.send_message("Check Entities")
        else:
            QMessageBox.warning("Error", "Need a message to identify entities!!")

    def send_exit_signal(self):
        self.socket.send("exit".encode())


class ChatbotUI(QWidget):
    def __init__(self, name, port):
        super().__init__()
        self.check_entities_button = None
        self.chat_output = None
        self.user_input = None
        self.submit_button = None
        self.toggle_button = None
        self.nn_speak_button = None
        self.client = None
        self.port = port
        self.name = name
        self.init_ui()

    def init_ui(self):
        self.chat_output = QTextEdit()
        self.chat_output.setReadOnly(True)
        self.chat_output.setStyleSheet("background-color: black; color: white;")
        self.chat_output.setTextInteractionFlags(Qt.TextBrowserInteraction)
        # setting the colors for the names
        self.chat_output.document().setDefaultStyleSheet(
            "b.bot { color: yellow; } b.user { color: green; } b.entity { color: cyan; }")

        self.user_input = QLineEdit()
        self.user_input.returnPressed.connect(self.submit_message)

        # call submit_message when send button is pushed
        self.submit_button = QPushButton("Send")
        self.submit_button.clicked.connect(self.submit_message)

        # call speak_message when Speak button is pushed
        self.toggle_button = QPushButton("Speak")
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(False)
        self.toggle_button.clicked.connect(self.speak_message)

        # call neural_speak_message when Neural Speak button is pushed
        self.nn_speak_button = QPushButton("Neural Speak")
        self.nn_speak_button.clicked.connect(self.neural_speak_message)

        self.check_entities_button = QPushButton("Check Entities")
        self.check_entities_button.clicked.connect(self.check_entities)

        layout = QVBoxLayout()
        layout.addWidget(self.chat_output)
        layout.addWidget(self.user_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.toggle_button)
        button_layout.addWidget(self.nn_speak_button)
        button_layout.addWidget(self.check_entities_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setWindowTitle(self.name)

        # connecting to the chat server
        self.client = ChatClient('localhost', self.port, 'Client')
        self.client.message_received.connect(self.display_message)
        self.client.connect_to_server()

        receive_thread = threading.Thread(target=self.client.receive_message)
        receive_thread.start()

    def submit_message(self):
        user_message = self.user_input.text().strip()
        if user_message:
            self.client.send_message(user_message)
            self.display_message(f'<b class="user">You:</b> {user_message} \n\n')
        self.user_input.clear()

    def display_message(self, message):
        self.chat_output.append(message)

    def closeEvent(self, event):
        self.client.send_exit_signal()
        event.accept()

    def speak_message(self):
        self.client.speak_message()

    def neural_speak_message(self):
        self.client.neural_speak_message()

    def check_entities(self):
        self.client.check_entities()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        client_port = int(sys.argv[1])
        client_name = f'Client {int(sys.argv[2])}'

        model_name = TTS.list_models()[0]
        tts = TTS(model_name)

        app = QApplication([])
        chatbot_ui = ChatbotUI(client_name, client_port)
        chatbot_ui.show()
        sys.exit(app.exec_())
