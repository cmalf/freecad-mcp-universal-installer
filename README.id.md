# FreeCAD-MCP Universal Installer

Alat bantu CLI Node.js interaktif lintas platform yang dirancang untuk mengotomatisasi instalasi addon FreeCAD-MCP dan mempermudah konfigurasi lingkungan Model Context Protocol (MCP) pada berbagai klien AI terkemuka seperti Google Gemini, Anthropic Claude, Goose, dan Aider.

<img width="428" height="440" alt="FreeCAD-MCP Universal Installer" src="https://github.com/user-attachments/assets/ff33be3c-7afd-45de-ba10-aee2bb1296d3" />

Bahasa Lain: [English](README.md)

## Fitur Utama

- **Dukungan Multi-Client**: Pembuatan otomatis berkas konfigurasi siap pakai untuk Gemini CLI, Claude Desktop/Code, Goose CLI, dan Aider CLI.
- **Lintas Platform**: Resolusi jalur direktori sistem dan berkas otomatis yang disesuaikan untuk macOS, Linux, dan Windows.
- **Lokalisasi Interaktif**: Antarmuka konsol dinamis dengan dukungan bahasa penuh untuk bahasa Inggris, Indonesia, Mandarin, dan Thai.
- **Automasi Prasyarat**: Memvalidasi kesiapan lingkungan sistem (Node.js 16+ dan Git) secara langsung sebelum eksekusi berjalan.
- **Mode Hemat Token**: Menyediakan opsi khusus untuk menginisialisasi parameter konfigurasi dalam mode efisiensi (`--only-text-feedback`).

## Prasyarat Sistem

Sebelum menjalankan alat instalasi ini, pastikan perangkat Anda telah memenuhi ketentuan berikut:
- **Node.js** versi 16 atau lebih tinggi.
- **Git** telah terpasang dan terdaftar di dalam environment variable sistem.
- Salah satu Klien AI yang didukung telah terpasang di sistem Anda.

## Cara Menjalankan

1. Salin atau unduh repositori installer ini ke dalam direktori kerja Anda.
	```bash
	git clone https://github.com/cmalf/freecad-mcp-universal-installer.git
	```
2. Inisialisasi proyek atau pastikan skrip berada di lokasi target.
	```bash
	cd freecad-mcp-universal-installer
	```
3. Jalankan CLI interaktif melalui terminal menggunakan Node:

	```bash
	node fui.js
	```
4. Jalankan CLI interaktif melalui terminal menggunakan Python:

	```bash
	python fui.py
	```

	or

	```bash
	python3 fui.py
	```

*Atau, jika Anda telah mendaftarkannya pada manifes berkas lokal proyek(NodeJS):*


```bash
npm start
```

Jejak Jalur Konfigurasi (Footprints)
------------------------------------

Alat ini mengelola penulisan berkas dan struktur data secara otomatis pada arsitektur jalur berikut:

### 1\. Google Gemini CLI

-   **Jalur Berkas**: `~/.gemini/settings.json` (Unix) | `%USERPROFILE%\.gemini\settings.json` (Windows)

-   **Format**: Struktur JSON terenkapsulasi dengan izin `mcpServers` dan modul shell interaktif.

### 2\. Claude Desktop & Claude Code CLI

-   **Jalur Berkas**: Berada pada direktori AppData (Windows), Application Support (macOS), atau `.config` (Linux).

-   **Format**: Blok konfigurasi JSON terstandarisasi untuk eksekusi server via `uvx`.

### 3\. Goose CLI

-   **Jalur Berkas**: Menargetkan folder spesifik sistem menuju berkas `config.yaml`.

-   **Format**: Struktur penulisan ekosistem berbasis YAML untuk blok ekstensi.

### 4\. Aider CLI

-   **Jalur Berkas**: Mengarah global pada direktori utama pengguna (User Home) menuju berkas `.aider.conf.yml`.

-   **Format**: Parameter deklaratif YAML untuk kontrol luaran `mcp-output` dan argumen baris perintah.

Atribusi Teknis & Sumber Daya (Footprints)
------------------------------------------

Skrip otomatisasi ini merupakan utilitas independen pihak ketiga yang dibangun untuk mempermudah alur kerja instalasi pengguna. Seluruh fungsionalitas perkakas spasial, pemodelan, dan perintah *runtime* yang dieksekusi di dalam lingkungan sistem sepenuhnya bergantung pada repositori hulu berikut:

-   **Repositori Utama Addon**: [freecad-mcp oleh neka-nat](https://github.com/neka-nat/freecad-mcp)

-   **Spesifikasi Protokol**: [Model Context Protocol (MCP) Specification](https://modelcontextprotocol.io/)


Kontribusi Terbuka
------------------------------------------

Kontribusi sangat terbuka bagi siapa saja! Jika Anda menemukan bug, memiliki ide fitur baru, atau ingin menambahkan dukungan untuk konfigurasi AI client/MCP lainnya, silakan ikuti langkah-langkah berikut:

1. Lakukan **Fork** pada repositori ini.
2. **Buat branch baru** untuk fitur atau perbaikan bug Anda:
   ```bash
   git checkout -b feature/nama-fitur-anda
   ```

1.  **Commit perubahan Anda** dengan deskripsi pesan yang jelas dan ringkas.

2.  **Push branch Anda** ke repositori hasil fork Anda.

3.  Ajukan sebuah **Pull Request (PR)** dengan menjelaskan perubahan yang Anda buat secara detail.

Untuk perubahan arsitektur script skala besar, silakan ajukan diskusi terlebih dahulu melalui menu **Issue** sebelum membuat Pull Request.

Lisensi
-------

Skrip utilitas installer ini didistribusikan di bawah [Lisensi MIT](https://github.com/cmalf/freecad-mcp-universal-installer?tab=MIT-1-ov-file). FreeCAD beserta platform AI terkait merupakan hak cipta dari masing-masing pengembang dan pemegang lisensi hulu terkait.
