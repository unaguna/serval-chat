from collections import Iterator

import MeCab

from mecabpy import iternode


class TestIterNode:

    INPUT_TEXT = '太郎はこの本を田中を見た女性に渡した。'
    OUTPUT_WORDS = ('', '太郎', 'は', 'この', '本', 'を', '田中', 'を', '見', 'た', '女性', 'に', '渡し', 'た', '。', '')

    def test_return_type(self):
        """iternode の戻り値の型チェック

        iternode がイテレーターを返し、そのイテレーターが Mecab.Node を順に与えることを確認する。
        """
        print()
        mecab = MeCab.Tagger("-Ochasen")
        first_node = mecab.parseToNode(self.INPUT_TEXT)

        iterator = iternode(first_node)

        assert isinstance(iterator, Iterator)
        for node in iterator:
            print(node)
            assert isinstance(node, MeCab.Node)

    def test_iterated_items(self):
        """iternode(first_node) が与える値の内容チェック

        イテレーターである iternode(first_node) が正しい順番で Node を返していることを確認する。
        """
        print()
        mecab = MeCab.Tagger("-Ochasen")
        first_node = mecab.parseToNode(self.INPUT_TEXT)

        iterator = iternode(first_node)
        surface_list = tuple(map(lambda n: n.surface, iterator))

        print(surface_list)
        assert surface_list == self.OUTPUT_WORDS
