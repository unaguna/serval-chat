from typing import Iterator, Optional, List

import MeCab

from .feature import Feature


class Node:
    """MeCab.Node の代替 (IPA辞書スタイル)

    このパッケージが提供する機能をスムーズに使用するためのNode。
    """
    _node: Optional[MeCab.Node]
    _surface: str
    _feature: Feature

    def __init__(self, surface: str, feature_obj: Feature, node: Optional[MeCab.Node] = None):
        self._node = node
        self._surface = surface
        self._feature = feature_obj

    @property
    def surface(self) -> str:
        return self._surface

    @property
    def feature(self) -> Feature:
        return self._feature


def parse_to_node(text: str, tagger: MeCab.Tagger) -> Iterator[Node]:
    """文字列の解析

    このパッケージが提供する機能をスムーズに使用できる形のオブジェクトを返す。

    Returns:
        解析結果として最有力候補となるNodeを文字列の先頭から順に与えるイテレータ
    """
    parsed_text: str = tagger.parse(text)
    return map(_word_line_to_node, parsed_text.rstrip('\n').split('\n'))


def _word_line_to_node(line: str) -> Node:

    # parseToNode の結果に近づけるため、BOS, EOS の行は別処理
    if line in ('BOS', 'EOS'):
        parts = ['', None, None, 'BOS/EOS', None, None, None, None, None]
    else:
        parts = list(map(_empty_to_none, line.split('\t')))

    # word_class の取り出し
    if parts[3] is not None:
        word_classes: List[Optional[str]] = parts[3].split('-')
    else:
        word_classes = []
    word_class_list = word_classes + [None, None, None, None]

    return Node(surface=parts[0],
                feature_obj=Feature(kana=parts[1],
                                    dict_form=parts[2],
                                    word_class0=word_class_list[0],
                                    word_class1=word_class_list[1],
                                    word_class2=word_class_list[2],
                                    word_class3=word_class_list[3],
                                    group=parts[4],
                                    form=parts[5],
                                    phonetic_kana=None))


def _empty_to_none(string: Optional[str]) -> Optional[str]:
    if string == '':
        return None
    else:
        return string
