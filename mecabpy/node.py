from typing import Iterator

import MeCab


def iternode(first_node: MeCab.Node) -> Iterator[MeCab.Node]:
    """MeCab.Nodeをイテレータに変換する。

    MeCab.Node は双方向連結リストのノードになっているが、python ではこのような構造をイテレータとして扱いたいことがある。
    この関数でそれを実現する。

    Args:
        first_node:
            双方向連結リストの最初のノード。MeCab.Tagger.parseToNode の戻り値を指定することを想定する。

    Returns:
        引数の first_node を先頭ノードとするイテレータ。
    """
    current_node = first_node
    while current_node:
        yield current_node
        current_node = current_node.next
