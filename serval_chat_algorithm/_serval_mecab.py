from typing import Sequence, Tuple, Any, Callable, Optional, Iterable

import MeCab
import discord

import discord_bot
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
    """ノードが終助詞のものかどうかを判定する。
    """
    return '終助詞' == node.feature.word_class1


def _is_symbol(node: mecabpy.ipa.Node) -> bool:
    """ノードが記号のものかどうかを判定する。
    """
    return '記号' == node.feature.word_class0


def _is_not_symbol(node: mecabpy.ipa.Node) -> bool:
    """ノードが記号でない単語のものであるかどうかを判定する。
    """
    return node.surface and not _is_symbol(node)


def _find_last(condition: Callable[[Any], bool], sequence: Sequence) -> Tuple[Optional[int], Any]:
    """条件に合う要素をシーケンスの末尾から順に探す。

    複数存在する場合、もっとも index が大きいものが返される。

    Args:
        condition: 条件
        sequence: 要素を探すシーケンス

    Returns:
        要素が見つかればその index と 要素。見つからなければ None と None。
    """
    target_list = tuple(sequence)
    for i in reversed(range(len(target_list))):
        if condition(target_list[i]):
            return i, target_list[i]

    return None, None


def _contains_any(target: str, candidate_list: Iterable[str]) -> bool:
    """指定した文字列に特定の文字列のいずれかが含まれるかどうかをチェックする。

    Args:
        target:
            候補文字列を含むかどうかを判定する文字列
        candidate_list:
            候補文字列からなるリスト

    Returns:
        target が candidate_list のいずれかの文字列を含むなら True、そうでないなら False。
    """
    for candidate in candidate_list:
        if candidate in target:
            return True
    return False


class ServalMecabChatAlgorithm(discord_bot.ChatAlgorithm):
    """チャットボット ServalChat の応答アルゴリズム
    """
    def input_message(self, message: discord.Message, self_client: discord.Client) -> Optional[str]:
        # 自身や他のBotからのメッセージには応答しない
        if message.author.bot or message.author == self_client:
            return None

        # チャンネル名に特定文字列が含まれない場合は応答しない
        channel_name = message.channel.name
        if not _contains_any(channel_name, ('サバンナ', 'さばんな')):
            return None

        print('メッセージが送られました')
        print('サーバ', message.guild.name)
        print('チャンネル', message.channel.name)
        print('送信者', message.author.display_name)
        print('内容', message.content)

        # 質問文かそうでないかで応答を変える
        if _is_question(message.content):
            return 'わかんないや'
        else:
            return 'すごーい'
