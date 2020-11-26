import requests
from bs4 import BeautifulSoup


class Translator(object):
    def __init__(self, allowed_languages):
        self.user_language = 0
        self.target_language = 0
        self.translate_word = ''

        self._request = ''
        self._literals = list()
        self._examples = list()
        self._full_target_lan = 'English'
        self._full_user_lan = 'English'
        self._trans_str = ''
        self._examples_str = ''
        self._allowed_languages = allowed_languages

    def create_request(self):
        self._full_target_lan = self._allowed_languages[self.target_language - 1]
        self._full_user_lan = self._allowed_languages[self.user_language]
        self._request = 'https://context.reverso.net/translation/{}-{}/{}'.format(
            self._full_user_lan.lower(), self._full_target_lan.lower(), self.translate_word)

    def request_server(self):
        try:
            result = requests.get(self._request, headers={'User-Agent': 'Mozilla/5.0'})
            if result.status_code == 200:
                return result.content
            elif result.status_code == 404:
                print(f'Sorry, unable to find {self.translate_word}')
                exit()
        except requests.exceptions.ConnectionError:
            print(f'Something wrong with your internet connection')
            exit()

    def parse_page(self, content):
        self._literals = list()
        self._examples = list()
        soup = BeautifulSoup(content, 'html.parser')
        founded_section = soup.find_all('section', id="examples-content")
        if not len(founded_section):
            print(f'Sorry, unable to find{self.translate_word}')
            exit()
        examples = founded_section[0].text.split('\n')
        for ex in examples:
            if ex:
                self._examples.append(ex.lstrip())
        for span in soup('span'):
            span.decompose()
        self._literals = soup.find_all('div', id="translations-content")[0].text.split()
        if not len(self._literals):
            print(f'Sorry, unable to find{self.translate_word}')
            exit()
        suggestions = [item.text.strip() for item in soup.find_all('div', {'class': 'suggestion'})]
        for suggestion in suggestions:
            if suggestion:
                self._examples.append(suggestion)

    def get_top_words(self):
        return '\n'.join(self._literals[0:1])

    def get_top_examples(self):
        result = ''
        pair = ''
        for idx, ex in enumerate(self._examples[0:2]):
            if idx % 2:
                pair += ex
                pair += '\n'
                result += pair
                result += '\n'
                pair = ''
            else:
                pair += ex
                pair += '\n'
        return result

    def work_chain(self):
        self.create_request()
        content = self.request_server()
        self.parse_page(content)
        self._trans_str = f'\n{self._full_target_lan} Translations:\n'
        self._trans_str += self.get_top_words()
        self._examples_str = f'\n{self._full_target_lan} Examples:\n'
        self._examples_str += self.get_top_examples()

    def translate_into_file(self, worker):
        with open(f'{self.translate_word}.txt', 'w', encoding='utf-8') as dict_file:
            worker(dict_file)
        with open(f'{self.translate_word}.txt', 'r') as check_file:
            print(check_file.read())

    def one_translate(self, dict_file):
        self.work_chain()
        dict_file.write(self._trans_str)
        dict_file.write(self._examples_str)

    def all_translate(self, dict_file):
        for index, lang in enumerate(self._allowed_languages):
            if lang == self._full_user_lan:
                continue
            self.target_language = index + 1
            self.one_translate(dict_file)

    def get_translate(self):
        if not self.target_language:
            return self.translate_into_file(self.all_translate)
        self.translate_into_file(self.one_translate)
