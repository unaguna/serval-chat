import pytest


import mecabpy.ipa


class TestFeature:
    """mecabpy.ipa.feature および mecabpy.ipa.feature のテスト
    """

    def test_equally(self):
        """Featureの等価性のテスト
        """
        feature0 = mecabpy.ipa.feature('名詞,固有名詞,人名,名,*,*,太郎,タロウ,タロー')
        feature1 = mecabpy.ipa.feature('名詞,固有名詞,人名,名,*,*,太郎,タロウ,タロー')
        assert feature0 == feature1

    def test_non_equally(self):
        """Featureの等価性のテスト
        """
        feature0 = mecabpy.ipa.feature('名詞,固有名詞,人名,名,*,*,太郎,タロウ,タロー')
        feature1 = mecabpy.ipa.feature('名詞,固有名詞,人名,名,*,*,次郎,ジロウ,ジロー')
        assert feature0 != feature1

    @pytest.mark.parametrize('feature_str, word_class',
                             (('名詞,固有名詞,人名,名,*,*,太郎,タロウ,タロー', ('名詞', '固有名詞', '人名', '名')),
                              ('動詞,自立,*,*,一段,連用形,見る,ミ,ミ', ('動詞', '自立', None, None)),
                              ('形容詞,自立,*,*,形容詞・アウオ段,基本形,薄い,ウスイ,ウスイ', ('形容詞', '自立', None, None)),
                              ('連体詞,*,*,*,*,*,この,コノ,コノ', ('連体詞', None, None, None)),
                              ('副詞,一般,*,*,*,*,そっと,ソット,ソット', ('副詞', '一般', None, None)),
                              ('接続詞,*,*,*,*,*,しかし,シカシ,シカシ', ('接続詞', None, None, None)),
                              ('感動詞,*,*,*,*,*,わあ,ワア,ワア', ('感動詞', None, None, None)),
                              ('助動詞,*,*,*,特殊・タ,基本形,た,タ,タ', ('助動詞', None, None, None)),
                              ('助詞,係助詞,*,*,*,*,は,ハ,ワ', ('助詞', '係助詞', None, None)),
                              ('記号,句点,*,*,*,*,。,。,。', ('記号', '句点', None, None)),
                              ('BOS/EOS,*,*,*,*,*,*,*,*', ('BOS/EOS', None, None, None)),))
    def test_attr_word_class(self, feature_str, word_class):
        """Feature.word_class のテスト
        """
        feature = mecabpy.ipa.feature(feature_str)
        assert feature.word_class == word_class

    @pytest.mark.parametrize('feature_str, word_class0',
                             (('名詞,固有名詞,人名,名,*,*,太郎,タロウ,タロー', '名詞'),
                              ('動詞,自立,*,*,一段,連用形,見る,ミ,ミ', '動詞'),
                              ('形容詞,自立,*,*,形容詞・アウオ段,基本形,薄い,ウスイ,ウスイ', '形容詞'),
                              ('連体詞,*,*,*,*,*,この,コノ,コノ', '連体詞'),
                              ('副詞,一般,*,*,*,*,そっと,ソット,ソット', '副詞'),
                              ('接続詞,*,*,*,*,*,しかし,シカシ,シカシ', '接続詞'),
                              ('感動詞,*,*,*,*,*,わあ,ワア,ワア', '感動詞'),
                              ('助動詞,*,*,*,特殊・タ,基本形,た,タ,タ', '助動詞'),
                              ('助詞,係助詞,*,*,*,*,は,ハ,ワ', '助詞'),
                              ('記号,句点,*,*,*,*,。,。,。', '記号'),
                              ('BOS/EOS,*,*,*,*,*,*,*,*', 'BOS/EOS'),))
    def test_attr_word_class0(self, feature_str, word_class0):
        """Feature.word_class0 のテスト
        """
        feature = mecabpy.ipa.feature(feature_str)
        assert feature.word_class0 == word_class0

    @pytest.mark.parametrize('feature_str, word_class1',
                             (('名詞,固有名詞,人名,名,*,*,太郎,タロウ,タロー', '固有名詞'),
                              ('動詞,自立,*,*,一段,連用形,見る,ミ,ミ', '自立'),
                              ('形容詞,自立,*,*,形容詞・アウオ段,基本形,薄い,ウスイ,ウスイ', '自立'),
                              ('連体詞,*,*,*,*,*,この,コノ,コノ', None),
                              ('副詞,一般,*,*,*,*,そっと,ソット,ソット', '一般'),
                              ('接続詞,*,*,*,*,*,しかし,シカシ,シカシ', None),
                              ('感動詞,*,*,*,*,*,わあ,ワア,ワア', None),
                              ('助動詞,*,*,*,特殊・タ,基本形,た,タ,タ', None),
                              ('助詞,係助詞,*,*,*,*,は,ハ,ワ', '係助詞'),
                              ('記号,句点,*,*,*,*,。,。,。', '句点'),
                              ('BOS/EOS,*,*,*,*,*,*,*,*', None),))
    def test_attr_word_class1(self, feature_str, word_class1):
        """Feature.word_class1 のテスト
        """
        feature = mecabpy.ipa.feature(feature_str)
        assert feature.word_class1 == word_class1

    @pytest.mark.parametrize('feature_str, word_class2',
                             (('名詞,固有名詞,人名,名,*,*,太郎,タロウ,タロー', '人名'),
                              ('動詞,自立,*,*,一段,連用形,見る,ミ,ミ', None),
                              ('形容詞,自立,*,*,形容詞・アウオ段,基本形,薄い,ウスイ,ウスイ', None),
                              ('連体詞,*,*,*,*,*,この,コノ,コノ', None),
                              ('副詞,一般,*,*,*,*,そっと,ソット,ソット', None),
                              ('接続詞,*,*,*,*,*,しかし,シカシ,シカシ', None),
                              ('感動詞,*,*,*,*,*,わあ,ワア,ワア', None),
                              ('助動詞,*,*,*,特殊・タ,基本形,た,タ,タ', None),
                              ('助詞,係助詞,*,*,*,*,は,ハ,ワ', None),
                              ('記号,句点,*,*,*,*,。,。,。', None),
                              ('BOS/EOS,*,*,*,*,*,*,*,*', None),))
    def test_attr_word_class2(self, feature_str, word_class2):
        """Feature.word_class2 のテスト
        """
        feature = mecabpy.ipa.feature(feature_str)
        assert feature.word_class2 == word_class2

    @pytest.mark.parametrize('feature_str, word_class3',
                             (('名詞,固有名詞,人名,名,*,*,太郎,タロウ,タロー', '名'),
                              ('動詞,自立,*,*,一段,連用形,見る,ミ,ミ', None),
                              ('形容詞,自立,*,*,形容詞・アウオ段,基本形,薄い,ウスイ,ウスイ', None),
                              ('連体詞,*,*,*,*,*,この,コノ,コノ', None),
                              ('副詞,一般,*,*,*,*,そっと,ソット,ソット', None),
                              ('接続詞,*,*,*,*,*,しかし,シカシ,シカシ', None),
                              ('感動詞,*,*,*,*,*,わあ,ワア,ワア', None),
                              ('助動詞,*,*,*,特殊・タ,基本形,た,タ,タ', None),
                              ('助詞,係助詞,*,*,*,*,は,ハ,ワ', None),
                              ('記号,句点,*,*,*,*,。,。,。', None),
                              ('BOS/EOS,*,*,*,*,*,*,*,*', None),))
    def test_attr_word_class3(self, feature_str, word_class3):
        """Feature.word_class3 のテスト
        """
        feature = mecabpy.ipa.feature(feature_str)
        assert feature.word_class3 == word_class3

    @pytest.mark.parametrize('feature_str, group',
                             (('名詞,固有名詞,人名,名,*,*,太郎,タロウ,タロー', None),
                              ('動詞,自立,*,*,一段,連用形,見る,ミ,ミ', '一段'),
                              ('形容詞,自立,*,*,形容詞・アウオ段,基本形,薄い,ウスイ,ウスイ', '形容詞・アウオ段'),
                              ('連体詞,*,*,*,*,*,この,コノ,コノ', None),
                              ('副詞,一般,*,*,*,*,そっと,ソット,ソット', None),
                              ('接続詞,*,*,*,*,*,しかし,シカシ,シカシ', None),
                              ('感動詞,*,*,*,*,*,わあ,ワア,ワア', None),
                              ('助動詞,*,*,*,特殊・タ,基本形,た,タ,タ', '特殊・タ'),
                              ('助詞,係助詞,*,*,*,*,は,ハ,ワ', None),
                              ('記号,句点,*,*,*,*,。,。,。', None),
                              ('BOS/EOS,*,*,*,*,*,*,*,*', None),))
    def test_attr_group(self, feature_str, group):
        """Feature.group のテスト
        """
        feature = mecabpy.ipa.feature(feature_str)
        assert feature.group == group

    @pytest.mark.parametrize('feature_str, form',
                             (('名詞,固有名詞,人名,名,*,*,太郎,タロウ,タロー', None),
                              ('動詞,自立,*,*,一段,連用形,見る,ミ,ミ', '連用形'),
                              ('形容詞,自立,*,*,形容詞・アウオ段,基本形,薄い,ウスイ,ウスイ', '基本形'),
                              ('連体詞,*,*,*,*,*,この,コノ,コノ', None),
                              ('副詞,一般,*,*,*,*,そっと,ソット,ソット', None),
                              ('接続詞,*,*,*,*,*,しかし,シカシ,シカシ', None),
                              ('感動詞,*,*,*,*,*,わあ,ワア,ワア', None),
                              ('助動詞,*,*,*,特殊・タ,基本形,た,タ,タ', '基本形'),
                              ('助詞,係助詞,*,*,*,*,は,ハ,ワ', None),
                              ('記号,句点,*,*,*,*,。,。,。', None),
                              ('BOS/EOS,*,*,*,*,*,*,*,*', None),))
    def test_attr_form(self, feature_str, form):
        """Feature.form のテスト
        """
        feature = mecabpy.ipa.feature(feature_str)
        assert feature.form == form

    @pytest.mark.parametrize('feature_str, dict_form',
                             (('名詞,固有名詞,人名,名,*,*,太郎,タロウ,タロー', '太郎'),
                              ('動詞,自立,*,*,一段,連用形,見る,ミ,ミ', '見る'),
                              ('形容詞,自立,*,*,形容詞・アウオ段,基本形,薄い,ウスイ,ウスイ', '薄い'),
                              ('連体詞,*,*,*,*,*,この,コノ,コノ', 'この'),
                              ('副詞,一般,*,*,*,*,そっと,ソット,ソット', 'そっと'),
                              ('接続詞,*,*,*,*,*,しかし,シカシ,シカシ', 'しかし'),
                              ('感動詞,*,*,*,*,*,わあ,ワア,ワア', 'わあ'),
                              ('助動詞,*,*,*,特殊・タ,基本形,た,タ,タ', 'た'),
                              ('助詞,係助詞,*,*,*,*,は,ハ,ワ', 'は'),
                              ('記号,句点,*,*,*,*,。,。,。', '。'),
                              ('BOS/EOS,*,*,*,*,*,*,*,*', None),))
    def test_attr_dict_form(self, feature_str, dict_form):
        """Feature.dict_form のテスト
        """
        feature = mecabpy.ipa.feature(feature_str)
        assert feature.dict_form == dict_form

    @pytest.mark.parametrize('feature_str, kana',
                             (('名詞,固有名詞,人名,名,*,*,太郎,タロウ,タロー', 'タロウ'),
                              ('動詞,自立,*,*,一段,連用形,見る,ミ,ミ', 'ミ'),
                              ('形容詞,自立,*,*,形容詞・アウオ段,基本形,薄い,ウスイ,ウスイ', 'ウスイ'),
                              ('連体詞,*,*,*,*,*,この,コノ,コノ', 'コノ'),
                              ('副詞,一般,*,*,*,*,そっと,ソット,ソット', 'ソット'),
                              ('接続詞,*,*,*,*,*,しかし,シカシ,シカシ', 'シカシ'),
                              ('感動詞,*,*,*,*,*,わあ,ワア,ワア', 'ワア'),
                              ('助動詞,*,*,*,特殊・タ,基本形,た,タ,タ', 'タ'),
                              ('助詞,係助詞,*,*,*,*,は,ハ,ワ', 'ハ'),
                              ('記号,句点,*,*,*,*,。,。,。', '。'),
                              ('BOS/EOS,*,*,*,*,*,*,*,*', None),))
    def test_attr_kana(self, feature_str, kana):
        """Feature.kana のテスト
        """
        feature = mecabpy.ipa.feature(feature_str)
        assert feature.kana == kana

    @pytest.mark.parametrize('feature_str, phonetic_kana',
                             (('名詞,固有名詞,人名,名,*,*,太郎,タロウ,タロー', 'タロー'),
                              ('動詞,自立,*,*,一段,連用形,見る,ミ,ミ', 'ミ'),
                              ('形容詞,自立,*,*,形容詞・アウオ段,基本形,薄い,ウスイ,ウスイ', 'ウスイ'),
                              ('連体詞,*,*,*,*,*,この,コノ,コノ', 'コノ'),
                              ('副詞,一般,*,*,*,*,そっと,ソット,ソット', 'ソット'),
                              ('接続詞,*,*,*,*,*,しかし,シカシ,シカシ', 'シカシ'),
                              ('感動詞,*,*,*,*,*,わあ,ワア,ワア', 'ワア'),
                              ('助動詞,*,*,*,特殊・タ,基本形,た,タ,タ', 'タ'),
                              ('助詞,係助詞,*,*,*,*,は,ハ,ワ', 'ワ'),
                              ('記号,句点,*,*,*,*,。,。,。', '。'),
                              ('BOS/EOS,*,*,*,*,*,*,*,*', None),))
    def test_attr_phonetic_kana(self, feature_str, phonetic_kana):
        """Feature.phonetic_kana のテスト
        """
        feature = mecabpy.ipa.feature(feature_str)
        assert feature.phonetic_kana == phonetic_kana
