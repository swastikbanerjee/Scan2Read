import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.uix.camera import Camera
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import cv2
import pytesseract
from PIL import Image as PILImage
from gtts import gTTS
import os

kivy.require('1.11.1')


class Scan2Read(App):
    #GUI Setup
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Create camera instance
        self.camera = Camera(play=True)

        # Create a horizontal box layout for buttons
        button_layout = BoxLayout(size_hint_y=None, height=50)

        self.capture_button = Button(text='Capture Image', size_hint_x=0.5)
        self.capture_button.bind(on_press=self.capture_image)

        self.import_button = Button(text='Import Image', size_hint_x=0.5)
        self.import_button.bind(on_press=self.import_image)

        button_layout.add_widget(self.capture_button)
        button_layout.add_widget(self.import_button)

        # Create a scroll view for displaying the text
        self.scroll_view = ScrollView()
        self.text_layout = GridLayout(cols=1, size_hint_y=None)
        self.output_label = Label(text='Extracted Text will appear here...', size_hint_y=None)
        self.text_layout.add_widget(self.output_label)
        self.scroll_view.add_widget(self.text_layout)

        # Add widgets to the main layout
        self.layout.add_widget(self.camera)
        self.layout.add_widget(button_layout)
        self.layout.add_widget(self.scroll_view)

        return self.layout

    def capture_image(self, instance):
        # Capture the image
        self.camera.export_to_png("pic_ext.png")
        # Perform OCR
        extracted_text = self.perform_ocr("pic_ext.png")
        if extracted_text:
            # Update output label with extracted text
            self.output_label.text = extracted_text
            # Convert extracted text to speech
            self.text_to_speech(extracted_text)
        else:
            self.output_label.text = "No text detected in the image"

    def import_image(self, instance):
        # Open file chooser to select an image
        file_chooser = FileChooserListView()
        file_chooser.bind(on_submit=self.process_selected_image)
        self.layout.add_widget(file_chooser)

    def process_selected_image(self, instance, selection, *args):
        if selection:
            image_path = selection[0]
            # Perform OCR
            extracted_text = self.perform_ocr(image_path)
            self.process_and_display_text(extracted_text)

    def perform_ocr(self, image_path):
        # Use Tesseract for OCR
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        extracted_text = pytesseract.image_to_string(PILImage.open(image_path))
        return extracted_text

    def process_and_display_text(self, extracted_text):
        if extracted_text:
            # Update output label with extracted text
            self.output_label.text = extracted_text
            # Convert extracted text to speech
            self.text_to_speech(extracted_text)
        else:
            self.output_label.text = "No text detected in the image"

    def text_to_speech(self, text, language='en'):
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save("output1.mp3")
        # os.system("mpg321 output1.mp3")  # Play the audio file (Linux)
        os.system("start output1.mp3")  # Play the audio file (Windows)


if __name__ == '__main__':
    Scan2Read().run()