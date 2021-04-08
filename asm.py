import sys
import parser


assembly = """\
.intel_syntax noprefix
.global main

main:
"""


def asm(node):
    if node.lhs != None:
        asm(node.lhs)
    
    global assembly

    if node.token_type == 'OP':
        if node.value == '+':
            assembly += f"\tadd rax, {node.rhs.value}\n"
        else:
            assembly += f"\tsub rax, {node.rhs.value}\n"

    # 最初の左下の数字のノードのみこの処理に振られる
    elif node.token_type == 'NUM':
        assembly += f"\tmov rax, {node.value}\n"


if __name__ == '__main__':
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
    elif len(sys.argv) == 1:
        filepath = 'samples/asm.txt'
    else:
        print('引数多すぎ')
        exit(1)

    with open(filepath, 'rt') as f:
        filestr = f.read()
        filestr = filestr.strip('\n')
    
    if parser.parse(filestr):
        asm(parser.root)
    else:
        print('構文解析に失敗')
        exit(1)

    with open('out.s', 'wt') as out:
        out.write(assembly)

    exit(0)

