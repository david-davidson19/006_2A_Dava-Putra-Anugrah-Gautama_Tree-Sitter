import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

with open(sys.argv[1], "rb") as f:
    kode = f.read()

tree = parser.parse(kode)

def jelajah(node, kedalaman=0, field=None):
    baris, kolom = node.start_point
    label = f"{field}: " if field else ""
    print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")
    for i, c in enumerate(node.children):
        if not c.is_named:
            continue
        nama_field = node.field_name_for_child(i)
        jelajah(c, kedalaman + 1, nama_field)

jelajah(tree.root_node)