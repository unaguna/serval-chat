import pytest

from serval_chat_algorithm._algorithm import _is_question


class TestJudgeQuestion:

    @pytest.mark.parametrize('text, expected',
                             (('あなたは速く走れるの', True),
                              ('僕は速く走れるよ', False),
                              ('じゃあ泳げるの', True),
                              ('僕は泳げるよ', False),
                              ('空は飛べるの', True),
                              ('何もわからないんだね', False),
                              ('誰か助けて', False),
                              ('鞄の中には何も入っていないよ', False),
                              ('君は馬鹿か？', True),))
    def test_is_question(self, text, expected):
        assert _is_question(text) == expected
