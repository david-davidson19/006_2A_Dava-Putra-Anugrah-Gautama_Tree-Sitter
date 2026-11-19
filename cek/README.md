# cek.py

CLI untuk memeriksa file Python dengan tree-sitter. Melaporkan:

1. Komentar yang mengandung `TODO` atau `FIXME`
2. Fungsi dengan panjang lebih dari 30 baris
3. File yang memiliki syntax error (beserta baris pertama yang bermasalah)

## Memasang dependensi

Butuh Python 3.10 atau lebih baru.

```
pip install tree-sitter tree-sitter-python
```

## Menjalankan

```
python cek.py <folder>
```

Semua file `*.py` di dalam folder (termasuk subfolder) diperiksa. Folder
`venv`, `.git`, dan `node_modules` dilewati.

## Contoh output

Folder uji buatan sendiri (`python cek.py uji`):

```
uji\panjang.py:1: fungsi panjang 36 baris
uji\rusak.py:1: syntax error
uji\todo.py:1: # TODO: tambahkan validasi
uji\todo.py:5: # FIXME: perbaiki ini
```

Repositori nyata
(https://github.com/dntdwp/A6-Mini_Project_ToDoListProgram, 7 file Python):

```
G:\repo-uji\punya danang\ui.py:216: fungsi _create_task_row 42 baris
```

Format tiap baris: `file:nomor_baris: temuan`.

## Catatan

- Semua fungsi dihitung, termasuk method di dalam kelas dan fungsi bersarang.
- Panjang fungsi = baris `def` sampai baris terakhir isinya, termasuk baris
  kosong dan komentar di dalamnya.
- Hanya komentar (`#`) yang dicari. `TODO` di dalam string tidak dilaporkan.
- Hanya satu syntax error pertama per file yang dilaporkan.

## Pengujian

Diuji pada folder `uji/` (3 file buatan sendiri) dan satu repositori GitHub
nyata. Hasil pada 2 file acak dicocokkan manual dengan hitungan sendiri
(lihat `laporan.md`).