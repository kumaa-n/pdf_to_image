# PDF to Image

PDFファイルを画像に一括変換できるシンプルなコマンドラインツールです。<br>
対応形式：JPG / PNG / GIF / TIFF（出力は1ページごとに1枚の画像ファイル）

## 特長

- 任意のディレクトリ内のPDFを一括変換
- 画像形式（jpg, png, gif, tiff）を選択可能
- 解像度（dpi）を指定可能
- 出力先のディレクトリを指定可能
- 入力PDFの自動削除オプション付き
- プログレスバー付きで処理状況がわかりやすい

## 必要なライブラリ

以下のPythonライブラリを使用しています：

- [`PyMuPDF (fitz)`](https://pymupdf.readthedocs.io/)
- [`Pillow`](https://pillow.readthedocs.io/)
- [`tqdm`](https://tqdm.github.io/)

### インストール方法

```bash
pip install PyMuPDF Pillow tqdm
```

## 使い方

### 実行コマンド

```bash
python convert_pdf_to_images.py <input_dir> <image_type> [--dpi DPI] [--output_dir OUTPUT_DIR] [--input_delete]
```

#### 必須引数

| 引数 | 説明 |
| --- | --- |
| `<input_dir>`  | PDFファイルがあるディレクトリ |
| `<image_type>` | 出力する画像形式（例: jpg, png） |

#### オプション引数

| オプション | 説明 |
| --- | --- |
| `--dpi` | 出力画像の解像度。未指定時は150dpi。 |
| `--output_dir` | 出力ディレクトリ。未指定時は入力と同じ場所に出力。 |
| `--input_delete` | 変換後に元のPDFファイルを削除したい場合に指定。 |

## 実行例

```bash
python pdf_to_image.py ./pdf jpg --dpi 200 --output_dir ./image --input_delete
```

- `./pdf` にあるPDFをすべて `.jpg` に変換
- 解像度は200dpi
- 画像は `./image` に保存
- 元のPDFファイルは削除されます

## 出力ファイル名の形式

- 1ページのみのPDF → `sample.jpg`
- 複数ページのPDF → `sample_01.jpg`, `sample_02.jpg`, …