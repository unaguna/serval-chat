import MeCab

import mecabpy
import mecabpy.ipa


class TestNode:
    """mecabpy.ipa.Node のテスト
    """

    INPUT_TEXT = '太郎はこの本を田中を見た女性に渡した。'

    def test_attr_surface(self):
        """NodeWrapper.surface のテスト
        """
        surface = '見'
        node = mecabpy.ipa.Node(surface=surface,
                                feature_obj=mecabpy.ipa.Feature(word_class0='動詞',
                                                                word_class1='自立',
                                                                word_class2=None,
                                                                word_class3=None,
                                                                group='一段',
                                                                form='連用形',
                                                                dict_form='見る',
                                                                kana='ミ',
                                                                phonetic_kana=None))
        assert node.surface == surface

    def test_attr_feature(self):
        """NodeWrapper.feature のテスト
        """
        feature = mecabpy.ipa.Feature(word_class0='動詞',
                                      word_class1='自立',
                                      word_class2=None,
                                      word_class3=None,
                                      group='一段',
                                      form='連用形',
                                      dict_form='見る',
                                      kana='ミ',
                                      phonetic_kana=None)
        node = mecabpy.ipa.Node(surface='見', feature_obj=feature)
        assert node.feature == feature


class TestParseToNode:
    """mecabpy.ipa.parse_to_node のテスト
    """

    INPUT_TEXT = '太郎はこの本を田中を見た女性に渡した。'
    OUTPUT_WORDS = ('太郎', 'は', 'この', '本', 'を', '田中', 'を', '見', 'た', '女性', 'に', '渡し', 'た', '。', '')

    def test_normal(self):
        node_list = *mecabpy.ipa.parse_to_node(self.INPUT_TEXT, MeCab.Tagger("-Ochasen")),
        surface_list = tuple(map(lambda n: n.surface, node_list))

        for node in node_list:
            print(node.feature)
            assert isinstance(node, mecabpy.ipa.Node)

        assert surface_list == self.OUTPUT_WORDS
