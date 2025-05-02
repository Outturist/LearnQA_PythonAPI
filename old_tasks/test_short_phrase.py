class TestShortPhrase:
    def test_short_phrase(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) <= 15, f'Phrase contains more than 15 characters. Actual length of phrase: {len(phrase)}'
