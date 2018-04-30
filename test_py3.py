import ast


def test_source_code_compatible(code_data):
    try:
        return ast.parse(code_data)
    except SyntaxError as exc:
        return False


files = ['ishell/command.py', 'ishell/console.py', 'ishell/__init__.py', 'ishell/log.py', 'ishell/utils.py',
         'examples/cisco.py', 'examples/linux_shell.py']
for f in files:
    ast_tree = test_source_code_compatible(open(f).read())
    if not ast_tree:
        print("%s is not PY3 Compatiable" % f)
    else:
        print(ast_tree)
