import tempfile
import pygame
import azure.cognitiveservices.speech as speechsdk
from gtts import gTTS
from TTS.api import TTS
import cTTS


class CoquiTTS:
    def __init__(self, model_name: str = 'tts_models/de/thorsten/vits', play: bool = True):
        self.model_name: str = model_name
        self.model: TTS = TTS(model_name=model_name)
        self.play: bool = play
        if self.play:
            pygame.mixer.init()

    def tts(self, text: str) -> None or str:
        """
        method to convert text to speech
        :param text: str: text to convert to speech
        :return: None
        """
        tf = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        self.model.tts_to_file(text, file_path=tf)
        if self.play:
            pygame.mixer.music.load(tf)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.stop()
            return None
        else:
            return tf.name


class CoquiTTSServer:
    def __init__(self, server_address: str = 'http://localhost:5002', play: bool = True):
        self.server_address: str = server_address
        self.play: bool = play
        if self.play:
            pygame.mixer.init()

    def tts(self, text: str) -> None or str:
        """
        method to convert text to speech
        :param text: str: text to convert to speech
        :return: None
        """
        tf = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        cTTS.synthesizeToFile(tf.name, text, self.server_address)
        if self.play:
            pygame.mixer.music.load(tf)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.stop()
            return None
        else:
            return tf.name


class GoogleTTS:
    def __init__(self, language: str = 'de', play: bool = True):
        self.language: str = language
        self.play: bool = play
        if self.play:
            pygame.mixer.init()

    def tts(self, text: str) -> None or str:
        """
        method to convert text to speech
        :param text: str: text to convert to speech
        :return: None
        """
        tf = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
        speech = gTTS(text=text, lang=self.language, slow=False)
        speech.save(tf.name)
        if self.play:
            pygame.mixer.music.load(tf)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.stop()
            return None
        else:
            return tf.name


class AzureTTS:
    def __init__(self, api_key: str, region: str, model_name: str = 'de-DE-ConradNeural', play: bool = True):
        self.api_key: str = api_key
        self.region: str = region
        self.model_name: str = model_name
        self.play: bool = play
        self.speech_config = speechsdk.SpeechConfig(subscription=self.api_key, region=self.region)
        self.speech_config.speech_synthesis_voice_name = self.model_name
        if self.play:
            self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    def tts(self, text: str) -> None or str:
        """
        method to convert text to speech
        :param text: str: text to convert to speech
        :return: None
        """
        if not self.play:
            tf = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            self.audio_config = speechsdk.audio.AudioOutputConfig(filename=tf.name)
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config,
            audio_config=self.audio_config
        )
        speech_synthesis_result = self.speech_synthesizer.speak_text_async(text).get()
        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")
        if self.play:
            # get the duration of the audio file
            return None
        else:
            return tf.name
