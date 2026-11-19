# Laporan Tugas Tree-sitter

Nama: Dava Putra Anugrah Gautama
Repo: https://github.com/david-davidson19/006_2A_Dava-Putra-Anugrah-Gautama_Tree-Sitter

## Tugas 1: Membaca pohon
Saya menebak pohon tiga potongan kode (fungsi, if/else, kelas) di kertas sebelum
menjalankan parser, lalu membandingkan dengan hasil.

Pohon hasil parse (node anonim dalam tanda kutip). Tebakan tulisan tangan ada di
`tugas1-3/pohon_tulisan_tangan.jpeg`.

**Fungsi**
```
module
  function_definition
    "def"
    name: identifier
    parameters: parameters
      "("
      identifier
      ")"
    ":"
    body: block
      return_statement
        "return"
        identifier
```

**if/else**
```
module
  if_statement
    "if"
    condition: comparison_operator
      identifier
      ">"
      integer
    ":"
    consequence: block
      expression_statement
        assignment
          identifier
          "="
          integer
    alternative: else_clause
      "else"
      ":"
      body: block
        expression_statement
          assignment
            identifier
            "="
            integer
```

**Kelas**
```
module
  class_definition
    "class"
    name: identifier
    ":"
    body: block
      function_definition
        "def"
        name: identifier
        parameters: parameters
          "("
          identifier
          ")"
        ":"
        body: block
          return_statement
            "return"
            integer
```

Tebakan yang meleset: `x` saya kira keyword (ternyata `identifier`), `0` saya kira
`identifier` (ternyata `integer`), dan `(` `)` ternyata ada di dalam `parameters`,
bukan langsung di `function_definition`.

Node anonim (teks literal di grammar): `def`, `:`, `return`, `(`, `)`, `>`, `=`, `if`, `else`, `class`.

`children` memuat semua anak termasuk node anonim, `named_children` hanya yang bernama.
Pada `function_definition` hasilnya 5 dan 3 (selisih 2 = `def` dan `:`):
```
5 3
```
Kode dirusak dengan menghapus `:` setelah `def sapa(nama)`. Parser tetap menghasilkan
pohon (error recovery), tapi `function_definition` hilang diganti `ERROR`:
```
(module (ERROR (identifier) (parameters (identifier)) (identifier)))
```
Output lengkap: `tugas1-3/output_t1_*.txt`.

## Tugas 2: Penjelajah node (jelajah.py)
Fungsi rekursif yang menelusuri `node.children` dengan `enumerate`, melewati node anonim
(`is_named`), dan mengambil nama field lewat `node.field_name_for_child(i)`. Indeks `i`
harus dari `children`, bukan `named_children`, kalau tidak field tidak muncul.
```
module [1:0]
  import_from_statement [1:0]
    module_name: dotted_name [1:5]
      identifier [1:5]
      identifier [1:11]
    name: dotted_name [1:28]
      identifier [1:28]
    name: dotted_name [1:37]
```
Diuji pada `proyek.py` (122 baris, 817 baris output). Sebagian dicocokkan dengan Playground:
struktur, kedalaman, dan field sama. Nomor baris sengaja +1 (Playground mulai dari 0).

## Tugas 3: Query pertama (q.py)
Tiga query: nama fungsi + jumlah parameter (`matches()`, `named_child_count`), pemanggilan
`print`, dan nama modul import.
- `matches()` dipakai karena menjaga pasangan `@nama` dan `@params` dari fungsi yang sama.
- `named_child_count` dipakai karena `(`, `)`, `,` di dalam `parameters` adalah node anonim.

Hitungan manual vs hasil:
- `uji_print.py`: 4 `def` (4 ditemukan, jumlah parameter 0, 0, 1, 3), 3 `print` (3 ditemukan).
- `proyek.py`: 8 baris import. Pola awal hanya menemukan 7 karena `import matplotlib.pyplot as plt`
  berbentuk `aliased_import`. Setelah satu pola ditambahkan, 8 ditemukan:
```
@modul  baris 81: matplotlib.pyplot
```

## Tugas 4: Grammar DSL filter
Grammar mendukung perbandingan (`=`, `!=`, `>`, `<`, `>=`, `<=`), nilai string/angka/boolean,
`and`/`or`/`not`, kurung, `in`, dan `contains`, dengan `field(...)` di child penting.
`word: $ => $.identifier` agar `and` tidak terbaca sebagai identifier.
`and` (prec.left 2) lebih kuat dari `or` (prec.left 1), jadi
`a = 1 or b = 2 and c = 3` dikelompokkan `a = 1 or (b = 2 and c = 3)`. `not` memakai prec 3.
```
  dasar:
      1. ✓ perbandingan string
      2. ✓ perbandingan angka
      3. ✓ and sederhana
      4. ✓ prioritas and lebih kuat dari or
      5. ✓ kurung mengubah prioritas
      6. ✓ not dan boolean
      7. ✓ in dengan tiga nilai
      8. ✓ contains
      9. ✓ contains digabung in

Total parses: 9; successful parses: 9; failed parses: 0; success percentage: 100.00%
```

## Tugas 5: Highlight
Isi `queries/highlights.scm`:
```
(string) @string
["and" "or" "not"] @keyword
["in" "contains"] @keyword
["=" "!=" ">" "<" ">=" "<="] @operator
(number) @number
(boolean) @constant.builtin
(comparison field: (identifier) @property)
(in_expression field: (identifier) @property)
(contains_expression field: (identifier) @property)
```
Di terminal, nama field berwarna merah, string hijau, keyword (and, or, not, in, contains) ungu, angka oker, boolean tosca, dan operator biru. Awalnya @operator tidak berwarna (tema bawaan hanya menebalkan) dan @constant.builtin mirip warna angka, jadi diganti @function dan @type. Nama capture dipilih supaya warnanya berbeda, bukan karena maknanya.
Bukti teks (`tree-sitter query`, lengkap di `tree-sitter-filter/output_highlight_query.txt`):
```
contoh.filter
  pattern: 6
    capture: 5 - property, start: (0, 0), end: (0, 6), text: `status`
  pattern: 3
    capture: 2 - operator, start: (0, 7), end: (0, 8), text: `=`
```

## Tugas 6: cek.py
Tiga fitur: komentar TODO/FIXME (query `#match?`), fungsi lebih dari 30 baris
(`end_point[0] - start_point[0] + 1`, +1 karena kedua ujung dihitung), dan file dengan syntax
error (`has_error` + penelusuran rekursif mencari node `ERROR`/`MISSING` pertama).
Diuji pada `cek/uji/` (3 file buatan sendiri) dan repo
https://github.com/dntdwp/A6-Mini_Project_ToDoListProgram (7 file Python):
```
G:\repo-uji\punya danang\ui.py:216: fungsi _create_task_row 42 baris
```
Pencocokan manual 2 file:
- `ui.py`: `def` di baris 216, isi sampai 257, 42 baris, 0 TODO/FIXME. Cocok. Pencarian teks `TODO` mentah di `ui.py` menghasilkan 11 temuan palsu (nama `todo` dan `TodoApp`), sedangkan `cek.py` yang hanya memeriksa node `comment` melaporkan 0, sesuai pengecekan manual.
- `main.py`: 0 TODO/FIXME, fungsi terpanjang paling banyak 12 baris (`get_progress_bar`, 9 fungsi total), cek.py tidak melaporkan apa pun. Cocok.

## Kendala dan solusi
- `python` tidak dikenali di PowerShell: PATH belum terbaca, terminal dibuka ulang.
- Isi file (baris filter, `config.json`) sempat diketik di terminal sebagai perintah. Solusi: isi file ditulis di editor atau lewat here-string.
- `grammar.js` bersarang saat ditempel, kurung kurang di `or_expression`, dan typo `$.expr` (seharusnya `$._expr`).
- Warning `highlights` belum terdaftar: ditambahkan manual di `tree-sitter.json`.
- Temuan dobel di `cek_error`: pengaman `if n is not None` ditambah tapi `print` lama tidak dihapus.
- @operator di tema bawaan tidak berwarna, diganti @function supaya operator terlihat berbeda.

## Catatan Penggunaan AI
Dalam pengerjaan tugas ini, AI digunakan sebagai rekan diskusi untuk menyusun kerangka awal dan memberikan petunjuk sintaks, seperti nama node `comparison_operator` dan `consequence`. Meskipun kerangka dasar terbantu oleh AI, seluruh logika inti, pengambilan keputusan, dan pengujian tetap dikerjakan secara mandiri. Bagian yang dirancang dan ditulis langsung meliputi tebakan nama node di Tugas 1, loop rekursi pada `jelajah.py`, pemilihan `_expr` di sisi kiri operator `and`, pengecekan kondisi `has_error`, serta eksekusi dan verifikasi seluruh hasil kode.

Rincian pembagian peran dan validasi per tugas:
- **Tugas 1-2:** Meminta arahan AI untuk penyusunan pohon dan kerangka awal `jelajah.py`, lalu mengisinya secara mandiri. Buktinya adalah catatan tebakan benar/salah di atas serta perbandingan hasil langsung dengan parse dan Tree-sitter Playground.
- **Tugas 3:** Menggunakan pola query dari AI sebagai titik awal, namun ditemukan bahwa pola tersebut melewatkan kasus `import ... as`. Melalui verifikasi mandiri dengan `Select-String`, ditemukan 8 baris kecocokan sementara query awal hanya menangkap 7 baris, sehingga pola diperbaiki sendiri hingga seluruh 8 kasus tertangkap.
- **Tugas 4:** Menguji prediksi AI yang memperkirakan semua 6 tes akan gagal setelah penambahan `field(...)`. Melalui eksekusi `tree-sitter test`, terbukti hanya 3 tes yang gagal, dan diff diperiksa secara manual terlebih dahulu sebelum menjalankan `--update`.
- **Tugas 5:** Mengikuti petunjuk AI terkait jalur `highlights` otomatis di CLI 0.27 yang ternyata memicu warning. Masalah ini diselesaikan secara mandiri dengan menuliskannya langsung di `tree-sitter.json` hingga warning hilang.
- **Tugas 6:** Menggunakan kerangka `cek.py` yang disarankan AI sebagai dasar, kemudian menyesuaikan dan mencocokkan hasilnya secara manual pada 2 file repositori nyata.