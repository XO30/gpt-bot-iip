import speech_recognition as sr
import azure.cognitiveservices.speech as speechsdk
import time



class GoogleSTT:
    def __init__(self, language: str = 'de-DE', timeout: int or None = None, conversation_timeout:int = 20, verbose: bool = False):
        self.language: str = language
        self.timeout: int or None = timeout
        self.conversation_timeout: int = conversation_timeout
        self.verbose: bool = verbose
        self.r: sr.Recognizer = sr.Recognizer()

    def stt(self) -> str or None or False:
        """
        method to convert speech to text using google speech to text
        :return: str orn None: user message or None or False
        """
        start_time = time.time()
        while True:
            try:
                with sr.Microphone() as source:
                    self.r.adjust_for_ambient_noise(source)
                    if self.verbose:
                        print('say something...')
                    audio = self.r.listen(source, timeout=self.timeout)
                try:
                    user_message = self.r.recognize_google(audio, language='de-DE')
                    if self.verbose:
                        print('you said: {}'.format(user_message))
                    return user_message
                except sr.UnknownValueError:
                    if self.verbose:
                        print('google speech recognition could not understand audio')
                    pass
                except sr.RequestError as e:
                    if self.verbose:
                        print('could not request results from google speech recognition service; {0}'.format(e))
                    pass
                if time.time() - start_time > self.conversation_timeout:
                    return False
            except sr.WaitTimeoutError:
                print('recognition still active, go on talking...')


class AzureSTT:
    def __init__(self, api_key, region, language: str = 'de-DE', conversation_timeout:int = 20, verbose: bool = False):
        self.api_key: str = api_key
        self.region: str = region
        self.language: str = language
        self.conversation_timeout: int = conversation_timeout
        self.verbose: bool = verbose
        self.speech_config = speechsdk.SpeechConfig(subscription=self.api_key, region=self.region)
        self.speech_config.speech_recognition_language = self.language
        self.audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config)

    def stt(self) -> str or None or False:
        """
        method to convert speech to text using azure speech to text
        :return: str orn None: user message or None or False
        """
        start_time = time.time()
        while True:
            try:
                if self.verbose:
                    print('say something...')
                speech_recognition_result = self.speech_recognizer.recognize_once_async().get()
                if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
                    user_message = speech_recognition_result.text
                    if self.verbose:
                        print('you said: {}'.format(user_message))
                    return user_message
                elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
                    if self.verbose:
                        print('ature stt could not understand audio')
                    pass
                elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
                    if self.verbose:
                        print('ature stt service could not be reached')
                    pass
                if time.time() - start_time > self.conversation_timeout:
                    return False
            except sr.WaitTimeoutError:
                print('recognition still active, go on talking...')
        
