from pilet.pilet import Pilet
from pilet.jobs import Translator, VideoStreaming, QnA, SentimentAnalysis

import os

trans = Translator(in_lang="auto", out_lang="eng")
vs = VideoStreaming()
qa = QnA()
sa = SentimentAnalysis()

pilet = Pilet(jobs=[trans, vs, qa, sa], mode="interactive")
pilet.launch_interactive_mode(audio="temp_audio.wav")
