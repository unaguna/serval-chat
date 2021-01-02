from collections import namedtuple
from typing import Union, Tuple

import MeCab


class Feature(namedtuple('Feature',
                         'word_class0 word_class1 word_class2 word_class3 group form dict_form kana phonetic_kana')):
    word_class0: Union[str]
    word_class1: Union[str]
    word_class2: Union[str]
    word_class3: Union[str]
    group: Union[str]
    form: Union[str]
    dict_form: str
    kana: str
    phonetic_kana: Union[str]

    @property
    def word_class(self) -> Tuple[Union[str], Union[str], Union[str], Union[str]]:
        return self.word_class0, self.word_class1, self.word_class2, self.word_class3


def feature(param: Union[MeCab.Node, str]) -> Feature:
    """featureを分解する。

    Args:
        param:
            MeCabの形態素解析Node、もしくはその feature 文字列。

    Returns:
        feature の内容を保持するオブジェクト
    """
    if isinstance(param, MeCab.Node):
        param = param.feature

    feature_parts = param.split(',')

    if len(feature_parts) != 9:
        raise ValueError(f'feature 文字列が不正です: {param}')

    return Feature(*map(_ast_to_none, feature_parts))


def _ast_to_none(string: Union[str, None]) -> Union[str, None]:
    if string == '*':
        return None
    else:
        return string
