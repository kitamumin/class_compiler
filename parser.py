import sys
import pytest

class Node():
    """ノード一つを型定義するクラス

    Attributes:
        token_type (str): トークンの種類
            123   = NUM
            PLUS  = OP
            MINUS = OP
            EOF   = EOF
        value (str): トークンの値
        lhs (Node): 左手のノード
        rhs (Node): 右手のノード
    """
    def __init__(self, value):
        self.value = value
        self.token_type = None
        if value.isdecimal():
            self.token_type = 'NUM'
        elif value == 'PLUS':
            self.token_type = 'OP'
        elif value == 'MINUS':
            self.token_type = 'OP'
        elif value == 'EOF':
            self.token_type = 'EOF'


def parse(file_str):
    """渡されたトークン文字列を木構造にしてステータスを返す
    
    トークン列を木構造にする。  
    成功したらTrueを返してglobal変数rootに木構造の根を格納する。
    失敗したらFalseを返す

    Args:
        file_str (str): トークン文字列

    Returns:
        Node: 成功したらTrue,失敗したらFalseする

    Raises:
        ValueError: トークン文字列が正しくない場合に発生

    Examples:
        >>> parse('[100 PLUS 200 MINUS 300 EOF]')
         True

                -  <-  このノードをrootに入れる
            +      300
        100   200

    """
    
    global root

    file_str = file_str[1:-1]   # []を削除
    token_list = file_str.split(' ')   # token文字列毎のlistが作成される

    try:
        # 最初のノードを生成
        root = Node(token_list[0])
        if root.token_type != 'NUM':
            raise ValueError(token_list[0])
        del token_list[0]
        
        # ノードを生成
        switch = True  # ノードの順番(記号 数値)を管理
        for token in token_list:
            node = Node(token)
            if node.token_type == 'OP' and switch:
                node.lhs = root
                root = node
                switch = False
            elif node.token_type == 'NUM' and not switch:
                root.rhs = node
                switch = True
            elif node.token_type == 'EOF' and switch:
                break
            else:
                raise ValueError(token)

    except ValueError as err:
        print('不正なトークンです : ', end='')
        print(err)
        return False

    return True


if __name__ == '__main__':
    global root
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
    elif len(sys.argv) == 1:
        file_path = 'samples/parser.txt'
    else:
        print('引数多すぎ!')
        exit(1)

    with open(file_path, 'rt') as f:

        file_str = list(f.read())
        del file_str[-1] # 末尾の改行を削除
        file_str = ''.join(file_str)
    
    parse(file_str)

    exit(0)


# tests

def test_1_parse():
    assert parse('') == False


def test_2_parse():
    assert parse('[100 PLUS 200 MINUS 300 EOF]') == True


def test_3_parse():
    assert parse('[10 20]') == False
