from pilet.pilet import Pilet
from pilet.agents import InteractiveAgent
from pilet.jobs import Translator, VideoStreaming, QA, SentimentAnalysis, Job

import os


trans = Translator(in_lang="auto", out_lang="eng")
vs = VideoStreaming()
qa = QA()
sa = SentimentAnalysis()

pilet = Pilet(jobs=[trans, vs, qa, sa], mode="interactive")