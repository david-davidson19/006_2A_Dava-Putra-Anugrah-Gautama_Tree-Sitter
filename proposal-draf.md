# Proposal Draf

## 1. Judul
Pendeteksi Potensi SQL Injection pada Kode Node.js/Express dengan Tree-sitter

## 2. Masalah
Di aplikasi web enterprise, query SQL sering dirangkai dari input pengguna lewat
template string atau penggabungan `+`. Pola ini rawan SQL injection dan sering lolos
saat code review. Yang mengalami: developer backend dan reviewer di tim.

## 3. Kenapa tidak cukup dengan AI saja
Review AI tidak konsisten antar-run, berbiaya per pemakaian, dan sulit dijalankan
otomatis di setiap pull request. Pemeriksa berbasis tree-sitter deterministik, cepat,
gratis, dan bisa berjalan di CI pada setiap commit.

## 4. Bahasa dan framework target
JavaScript (Node.js + Express, driver `mysql`/`pg`). Grammar: `tree-sitter-javascript`
(tersedia di PyPI).

## 5. Contoh kode
Harus terdeteksi:
    db.query(`SELECT * FROM users WHERE id = ${req.params.id}`)
    db.query("SELECT * FROM users WHERE name = '" + nama + "'")
Tidak boleh terdeteksi (parameterized):
    db.query("SELECT * FROM users WHERE id = ?", [id])
    // db.query(`... ${x}`) di dalam komentar atau string biasa
Regex gagal karena tidak mengenali struktur: komentar, string bersarang, dan argumen
yang tersebar di beberapa baris sulit dibedakan dari kode nyata.

## 6. Rancangan query (draf, akan diuji)
    (call_expression
      function: (member_expression
        property: (property_identifier) @metode)
      arguments: (arguments
        [(template_string (template_substitution))
         (binary_expression operator: "+")] @sql)
      (#match? @metode "^(query|execute)$"))

## 7. Bentuk output
Laporan terminal (`file:baris: potensi SQL injection`) dan file JSON agar bisa dipakai di CI.

## 8. Cara evaluasi
Jalankan pada 1-2 repo Express open source. Periksa manual 20 temuan, hitung berapa
yang benar (precision), dan catat kasus yang lolos (false negative).

## 9. Rencana kerja dan risiko
- Minggu 1: pasang `tree-sitter-javascript`, lihat pohon dengan `jelajah.py`, tulis query.
- Minggu 2: lengkapi aturan (template string, `+`, `concat`), output terminal.
- Minggu 3: output JSON, uji di repo nyata.
- Minggu 4: evaluasi 20 temuan, perbaiki false positive.
- Minggu 5: laporan dan demo.
Risiko: data mengalir lewat variabel perantara (`const q = ...; db.query(q)`) sulit
dilacak karena tree-sitter hanya sintaks; skop dibatasi pada pola langsung.