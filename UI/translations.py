
import json
from PyQt5.QtWidgets import QWidget


class Translator(QWidget):
    """docstring for Translator"""

    lang = {}
    languages = {}

    def __init__(self, parent=None):
        super(Translator, self).__init__(parent)
        self._intents = []
        self._load_languages()
        self._load_last_used()

    def _load_languages(self):
        try:
            with open('tr/languages.json', 'rt') as f:
                jsobj = json.loads(f.read())
            Translator.languages = jsobj['languages']
            print('Translator load languages list: ', Translator.languages)
        except Exception as e:
            print('Error load /languages/ file - ', e)

    def _load_translation(self, code):
        with open('./tr/%s.json' % code, 'rt') as f:
            Translator.lang = json.loads( f.read() )

    def _load_last_used(self):
        try:
            with open('./tr/last.json', 'rt') as f:
                name, code = json.loads(f.read())
            self._load_translation(code)
            print('Translator load last used: ', code)
        except Exception as e:
            print(e)

    def _save_last_used(self, name, code):
        with open('./tr/last.json', 'wt') as f:
            f.write( json.dumps( (name, code) ) )

    def _intents_update(self):
        for intmethod, text in self._intents:
            try:
                intmethod( Translator.lang.get(text, text) )
            except Exception:
                pass

    def load(self, lang):
        for name, code in Translator.languages:
            if name == lang:
                self._load_translation(code)
                self._save_last_used(name, code)
                return True

    def translate(self, string):
        return Translator.lang.get(string, string)

    def change_translation(self):
        sendername = self.sender().objectName()
        try:
            self.load(sendername)
            self.update()
        except Exception:
            pass

    def add_intent(self, setmethod, text):
        self._intents.append( (setmethod, text) )

    def update(self):
        self._intents_update()
