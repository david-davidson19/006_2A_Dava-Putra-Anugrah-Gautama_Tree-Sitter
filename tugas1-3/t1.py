import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

kode = b"def sapa(nama):\n    return nama\n"
tree = parser.parse(kode)
print(tree.root_node)
print()

def cetak(node, d=0):
    jenis = "bernama" if node.is_named else "anonim"
    print("  " * d + node.type + "  (" + jenis + ")")
    for c in node.children:
        cetak(c, d + 1)

cetak(tree.root_node)

print()
akar = tree.root_node.children[0]
print(len(akar.children), len(akar.named_children))