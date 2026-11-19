import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')

Q_FUNGSI = Query(PY, '(function_definition name: (identifier) @nama) @fungsi')

def cek_panjang(path, tree):
    for _, cap in QueryCursor(Q_FUNGSI).matches(tree.root_node):
        fungsi = cap["fungsi"][0]
        nama = cap["nama"][0].text.decode(errors="replace")
        jumlah = fungsi.end_point[0] - fungsi.start_point[0] + 1
        if jumlah > 30:
            print(f"{path}:{fungsi.start_point[0] + 1}: fungsi {nama} {jumlah} baris")

def cek_todo(path, tree):
    for nama, nodes in QueryCursor(Q_TODO).captures(tree.root_node).items():
        for n in nodes:
            print(f"{path}:{n.start_point[0] + 1}: {n.text.decode(errors='replace')}")

def cari_error(node):
    if node.is_error or node.is_missing:
        return node
    for c in node.children:
        hasil = cari_error(c)
        if hasil is not None:
            return hasil
    return None

def cek_error(path, tree):
    if tree.root_node.has_error:
        n = cari_error(tree.root_node)
        if n is not None:
            print(f"{path}:{n.start_point[0] + 1}: syntax error")

def cek_file(path):
    kode = path.read_bytes()
    tree = parser.parse(kode)
    cek_todo(path, tree)
    cek_panjang(path, tree)
    cek_error(path, tree)
if len(sys.argv) < 2:
    print("Pemakaian: python cek.py <folder>")
    sys.exit(1)

folder = Path(sys.argv[1])
for p in folder.rglob("*.py"):
    if any(x in p.parts for x in ("venv", ".git", "node_modules")):
        continue
    cek_file(p)