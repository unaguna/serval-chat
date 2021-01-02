from typing import Sequence, Tuple, Any, Callable, Optional

import MeCab

import mecabpy.ipa


def _is_question(sentence: str) -> bool:
    """文が質問文かどうかを判定する。

    Args:
        sentence: 判定する文

    Returns:
        質問文なら True、そうでないなら False。
    """
    nodes = tuple(mecabpy.ipa.parse_to_node(sentence, MeCab.Tagger("-Ochasen")))

    # 最後の非記号単語より後に疑問符がついていたら質問文==================================================
    last_not_symbol_index, _ = _find_last(_is_not_symbol, nodes)
    surface_after_last_not_symbol = tuple(map(lambda n: n.surface, nodes[last_not_symbol_index+1:]))
    if '?' in surface_after_last_not_symbol or '？' in surface_after_last_not_symbol:
        return True

    # 最後の終助詞が疑問の意味を持つなら質問文===========================================================
    end_joshi_list = tuple(filter(_is_end_joshi, nodes))
    if len(end_joshi_list) > 0:
        # 最後の終助詞が「か」「の」なら質問文
        last_end_joshi = end_joshi_list[-1]
        if last_end_joshi.surface in ('か', 'の'):
            return True

    return False


def _is_end_joshi(node: mecabpy.ipa.Node) -> bool:
    return '終助詞' == node.feature.word_class1


def _is_symbol(node: mecabpy.ipa.Node) -> bool:
    return '記号' == node.feature.word_class0


def _is_not_symbol(node: mecabpy.ipa.Node) -> bool:
    return node.surface and not _is_symbol(node)


def _find_last(condition: Callable[[Any], bool], sequence: Sequence) -> Tuple[Optional[int], Any]:
    target_list = tuple(sequence)
    for i in reversed(range(len(target_list))):
        if condition(target_list[i]):
            return i, target_list[i]

    return None, None


def main():
    pass


if __name__ == '__main__':
    main()
