import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

kode = open(sys.argv[1], "rb").read()
pola = open(sys.argv[2]).read()
tree = parser.parse(kode)

for idx, cap in QueryCursor(Query(PY, pola)).matches(tree.root_node):
    nama = cap["nama"][0]
    params = cap.get("params", [])
    jumlah = params[0].named_child_count if params else 0
    print(f"baris {nama.start_point[0] + 1}: {nama.text.decode()} -> {jumlah} parameter")