import gradio as gr
import numpy as np
import sys
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentdir)

from modules.pipelines import InferencePipeLine

notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def greet(name):
    return "Hello " + name + "!"

def generate_tone(note, octave, duration):
    sr = 48000
    a4_freq, tones_from_a4 = 440, 12 * (octave - 4) + (note - 9)
    frequency = a4_freq * 2 ** (tones_from_a4 / 12)
    duration = int(duration)
    audio = np.linspace(0, duration, duration * sr)
    audio = (20000 * np.sin(audio * (2 * np.pi * frequency))).astype(np.int16)
    return (sr, audio)

class GradioBase:
    def __init__(self, inputs_type, outputs_type):
        self.inputs_type = inputs_type
        self.outputs_type = outputs_type

        if self.inputs_type == "text":
            self.inputs = gr.Textbox(lines=2, label="Input Text")
        elif self.inputs_type == "audio":
            self.inputs = gr.Audio(label="Input Audio")
        elif isinstance(self.inputs_type, list):
            self.inputs = self.inputs_type

        if self.outputs_type == "text":
            self.outputs = gr.Textbox(label="Output Text")
        elif self.outputs_type == "audio":
            self.outputs = gr.Audio(label="Output Audio")
        elif isinstance(self.outputs_type, list):
            self.outputs = self.outputs_type

        self.title = None
        self.examples = None
        self.descriptions = None

    def prepare_main_function(self, main_func):
        self.main_func = main_func

    def prepare_pipeline(self, pipeline):
        self.main_func = pipeline.run
        print(self.main_func)

    def prepare_examples(self, examples):
        self.examples = examples

    def prepare_title_n_descriptions(self, title, descriptions):
        self.title = title
        self.descriptions = descriptions

    def prepare_demo(self):
        self.demo = gr.Interface(
            fn=self.main_func, examples=self.examples,
            title=self.title, description=self.descriptions,
            inputs=self.inputs, outputs=self.outputs
        )
    
    def launch(self):
        self.demo.launch()


# test = GradioBase([
#     gr.Dropdown(notes, type="index"),
#     gr.Slider(minimum=2, maximum=8, step=1, label="Octave"),
#     gr.Textbox(type="text", value="1", label="Duration in seconds")
# ], "audio")
# test.prepare_main_function(
#     generate_tone
# )
# test.prepare_examples([
#     ["C", 4, 1],
#     ["D", 5, 2]
# ])
# test.prepare_demo()
# test.launch()

# test2 = GradioBase(
#     "text", "text"
# )
# test2.prepare_pipeline(
#     InferencePipeLine("text_generation", "google/flan-t5-small")
# )
# test2.prepare_demo()
# test2.launch()

pl = InferencePipeLine("text_generation", "mistralai/Mistral-7B-v0.1")
a = pl.run("Make poem that starts with: I am handsome")
print(a)