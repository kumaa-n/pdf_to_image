import argparse
import os
from pathlib import Path
import re
import sys
from typing import List

import fitz
from tqdm import tqdm

def get_matching_files(input_dir: str | Path, regex: re.Pattern = re.compile(r'.+')) -> List[str]:
    """ 指定されたディレクトリ内のファイルを取得し、正規表現にマッチするファイル名のリストを返す。

    Args:
        dir (input_dir | Path): ディレクトリのパス
        regex (re.Pattern, optional): 正規表現パターン。デフォルトは全てのファイルを対象とする。

    Raises:
        OSError: 指定されたパスが存在するディレクトリでない場合に発生します。

    Returns:
        List[str]: 正規表現にマッチするファイル
    """

    input_dir = Path(input_dir)
    if not input_dir.is_dir():
        raise OSError('存在するディレクトリを指定してください。')

    return [str(f) for f in input_dir.glob('*') if f.is_file() and regex.fullmatch(str(f.name))]

def to_image_single(pdf_path: str | Path, image_type: str, dpi: int, *args, **kwargs) -> int:
    """ PDFファイルを画像に変換する。

    Args:
        pdf_path (str | Path): PDFファイルのパス
        image_type (str): 画像形式（jpg, jpeg, png, gif, tiffのいずれか）
        dpi (int): 画像の解像度（dpi）

    Raises:
        ValueError: キーワード引数以外の引数が指定された場合に発生します。

    Returns:
        int: 変換されたページ数
    """

    if args:
        raise ValueError('to_image_single：キーワード引数のみ指定可能です。')

    file_extension = image_type

    if image_type.lower() == 'jpg':
        image_type = 'jpeg'

    pdf_path = Path(pdf_path)
    output_dir = kwargs.get('output_dir', None)
    output_dir = Path(output_dir) if output_dir else pdf_path.parent
    output_dir.mkdir(exist_ok=True, parents=True)

    with fitz.open(pdf_path) as pdf_reader:
        # ページ数に応じて連番桁数を決定
        pdf_page_count = pdf_reader.page_count
        renban_len = len(str(pdf_page_count))
        is_add_renban = pdf_page_count > 1

        for page_count, page in enumerate(pdf_reader, start=1):
            renban = f'_{page_count:0{renban_len}d}' if is_add_renban else ''
            image_file = output_dir / f'{pdf_path.stem}{renban}.{file_extension}'
            pix = page.get_pixmap(dpi=dpi)
            pix.pil_save(image_file, format=image_type, optimize=True)

    return pdf_page_count

def main():
    IMAGE_TYPE_CHOICES = ('jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG', 'gif', 'GIF', 'tiff', 'TIFF')
    DEFAULT_DPI = 150

    parser = argparse.ArgumentParser(description='PDF->画像変換を行います。')
    parser.add_argument('input_dir', help='入力ディレクトリ')
    parser.add_argument('image_type', choices=IMAGE_TYPE_CHOICES, help='画像形式　jpg, jpeg, png, gif, tiffが指定可能。')
    parser.add_argument('--dpi', type=int, default=DEFAULT_DPI, help='画像の解像度（dpi）　整数値のみ指定可能。　未指定の場合は150が設定されます。')
    parser.add_argument('--output_dir', default=None, help='出力ディレクトリ　未指定の場合は入力ディレクトリと同じ場所に出力されます。')
    parser.add_argument('--input_delete', action='store_true', help='入力ファイルを削除します。　未指定の場合は入力ファイルを削除しません。')
    args = parser.parse_args()

    try:
        pdf_files = get_matching_files(args.input_dir, re.compile(r'.+\.pdf', re.IGNORECASE))
        input_file_count = len(pdf_files)
        output_file_count = 0

        for pdf in tqdm(pdf_files, desc='PDF→画像変換中'):
            convert_file_num = to_image_single(
                pdf,
                args.image_type,
                args.dpi,
                output_dir=args.output_dir,
            )

            output_file_count += convert_file_num

        if args.input_delete:
            for pdf in pdf_files:
                os.remove(pdf)

        print('**************************************************')
        print('*')
        print('* PDF→画像変換　正常終了')
        print('*')
        print(f'* 入力ファイル数　：{input_file_count}件')
        print(f'* 出力ファイル数　：{output_file_count}件')
        print(f'* 出力ディレクトリ：{args.output_dir or args.input_dir}')
        print('*')
        print('**************************************************')

    except Exception as e:
        print('**************************************************')
        print('*')
        print('* PDF→画像変換　異常終了')
        print('*')
        print(f'* {e}')
        print('*')
        print('**************************************************')
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
