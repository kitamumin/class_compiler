import sys
import pytest

def tokenizer(plain_text: str) -> 'token_list[str]':
    """引数の文字列からトークン文字列のリストを返す

    token_list = tokenizer(plain_text:str) -> list[str]
    
    「数値、+、-、空白」で構成される文字列をトークン文字列に変える

    Args:
        plain_text: 変換したい文字列

    Returns:
        the list of token

        [op, token]
        {数値:NUMBER,
        '+' : PLUS,
        '-' : MINUS,
        終端: EOF}


        example:
            plain_text : '1 + 2 - 3'
            return : ['NUMBER', 'PLUS', 'NUMBER', 'MINUS', 'NUMBER', 'EOF']

    Raises:
        ValueError: 予期しない文字が入っています

    Examples:
        token_list = tokenizer(plain_text)

    """
    token_list = list()

    source = list(plain_text)
    source.append(' ')

    try:
        
        while source:
            if source[0] == ' ':
                del source[0]

            elif source[0] == '+':
                del source[0]
                token_list.append('PLUS')

            elif source[0] == '-':
                del source[0]
                token_list.append('MINUS')

            elif ord('0') <= ord(source[0]) <= ord('9'):

                digit = 1

                while True: # 数字の桁数を求めている
                    if ord('0') <= ord(source[digit]) <= ord('9'):
                        digit += 1 
                    else:
                        break

                del source[0:digit]
                token_list.append('NUMBER')

            else:
                raise ValueError('予期しない文字が入っています')

    except ValueError as err:
        print(err)
        exit(1)

    token_list.append('EOF')
    return token_list


if __name__ == '__main__':

    if len(sys.argv) == 2:
        file_path = sys.argv[1]
    elif len(sys.argv) == 1:
        file_path = 'samples/lex.txt'
    else:
        print('引数多すぎ！')
        exit(1)

    with open(file_path, 'rt') as f:

        file_str = list(f.read())
        del file_str[-1] # 末尾の改行を削除
        ''.join(file_str)

    token_list = tokenizer(file_str)
    
    print(f"[{' '.join(token_list)}]", end='')

    exit(0)

# tests

def test_tokenizer():
    assert tokenizer('1 + 2 - 3') == ['NUMBER', 'PLUS', 'NUMBER', 'MINUS', 'NUMBER', 'EOF']

def test_1_tokenizer():
    assert tokenizer('+') == ['PLUS', 'EOF']

def test_2_tokenizer():
    assert tokenizer('-') == ['MINUS', 'EOF']

def test_3_tokenizer():
    assert tokenizer('1') == ['NUMBER', 'EOF']

def test_4_tokenizer():
    assert tokenizer('10') == ['NUMBER', 'EOF']

def test_5_tokenizer():
    assert tokenizer(' ') == ['EOF']

def test_Error_tokenizer():
    with pytest.raises(SystemExit):
        tokenizer('Errrrrrrrrrrrror')
