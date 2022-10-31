import argparse
import pathlib
from pathlib import *
import shutil
import sys
import re


import sys
from pathlib import Path

JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
MP3_AUDIO = []
DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
XLSX_DOCUMENTS = []
PPTX_DOCUMENTS = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
SMTH_OTHER = []
ARCHIVES = []

REGISTER_EXTENSIONS = {
    'JPEG': JPEG_IMAGES,
    'PNG': PNG_IMAGES,
    'JPG': JPG_IMAGES,
    'SVG': SVG_IMAGES,
    'DOC': DOC_DOCUMENTS,
    'DOCX': DOCX_DOCUMENTS,
    'TXT': TXT_DOCUMENTS,
    'PDF': PDF_DOCUMENTS,
    'XLSX': XLSX_DOCUMENTS,
    'PPTX': PPTX_DOCUMENTS,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MOV': MOV_VIDEO,
    'MKV': MKV_VIDEO,
    'ZIP': ARCHIVES,
    'GZ' : ARCHIVES,
    'TAR': ARCHIVES,

}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()


def get_extension(filename):
    return Path(filename).suffix[1:].upper()    # прибрали крапку для розширення


def scan(folder: Path) -> None:
    for item in folder.iterdir():
        if item.is_dir():  # Якщо це папка то додаємо її зі списку FOLDERS і переходимо до наступного елемента папки
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'SMTH_OTHER'):   # перевіряємо, щоб папка не була тією, в яку ми складаємо вже файли.
                FOLDERS.append(item)
                scan(item) # скануємо цю вкладену папку - рекурсія

            continue # перейти до наступного елемента в сканованій папці

        ext = get_extension(item.name)  # взяли розширення
        full_way = folder / item.name  # взяли ПОВНИЙ шлях до файлу
        if not ext:  # якщо файл не має розширення:
            SMTH_OTHER.append(full_way) #додати до невідомих

        else:
            try:
                # взяти список куди покласти повний шлях до файлу
                container = REGISTER_EXTENSIONS[ext]
                EXTENSIONS.add(ext)
                container.append(full_way)
            except KeyError:
                # Якщо ми не реєстрували розширення у REGISTER_EXTENSIONS, то додати до іншого
                UNKNOWN.add(ext)
                SMTH_OTHER.append(full_way)

def parser():

    folder_for_scan = sys.argv[1]
    print(f'Start in folder {folder_for_scan}')

    scan(Path(folder_for_scan))
    print(f'Images jpeg: {JPEG_IMAGES}')
    print(f'Images jpg: {JPG_IMAGES}')
    print(f'Images svg: {SVG_IMAGES}')
    print(f'Audio mp3: {MP3_AUDIO}')
    print(f'Archives: {ARCHIVES}')

    print(f'Types of files in folder: {EXTENSIONS}')
    print(f'Unknown files of types: {UNKNOWN}')

    print(FOLDERS[::-1])








transliteration_dict= {
    ord("а"): "a",
    ord("б"): "b" ,
    ord("в"): "v",
    ord("г"): "g",
    ord("д"): "d",
    ord("е"): "e",
    ord("є"): "ye",
    ord("ж"): "gj",
    ord("з"): "z",
    ord("и"): "u",
    ord("й"): "y",
    ord("к"): "k",
    ord("л"): "l",
    ord("м"): "m",
    ord("н"): "n",
    ord("п"): "p",
    ord("р"): "r",
    ord("с"): "s",
    ord("т"): "t",
    ord("у"): "u",
    ord("ф"): "f",
    ord("х"): "h",
    ord("ц"): "c",
    ord("ч"): "ch",
    ord("ш"): "sh",
    ord("щ"): "shch",
    ord("ь"): "`",
    ord("ю"): "yu",
    ord("я"): "ya",
}

def normalize(some_string):
    translated = ""
    suf = some_string.rfind(".")
    string = some_string[suf:]
    for i in some_string[0:suf]:
        if i.islower() == True:
            translated += i.translate(transliteration_dict)
        elif i.isupper() == True:
            i = i.lower()
            translated += i.translate(transliteration_dict).upper()
        else:
            translated += i


    result = re.sub(r"\W", "_", translated)
    result = result + string
    return result




def handle_media(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_other(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_archive(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / filename.name.replace(filename.suffix, '')
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()), str(folder_for_file.resolve()))
    except shutil.ReadError:
        print(f'Це не архів {filename}!')
        folder_for_file.rmdir()
        return None
    filename.unlink()

def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f'Помилка видалення папки {folder}')

def main(folder: Path):
    parser.scan(folder)
    for file in parser.JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in parser.JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in parser.PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in parser.SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')

    for file in parser.AVI_VIDEO:
        handle_media(file, folder / 'video' / 'AVI')
    for file in parser.MP4_VIDEO:
        handle_media(file, folder / 'video' / 'MP4')
    for file in parser.MOV_VIDEO:
        handle_media(file, folder / 'video' / 'MOV')
    for file in parser.MKV_VIDEO:
        handle_media(file, folder / 'video' / 'MKV')

    for file in parser.DOC_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'DOC')
    for file in parser.DOCX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'DOCX')
    for file in parser.TXT_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'TXT')
    for file in parser.PDF_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'PDF')
    for file in parser.XLSX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'XLSX')
    for file in parser.PPTX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'PPTX')


    for file in parser.MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3')

    for file in parser.SMTH_OTHER:
        handle_other(file, folder / 'SMTH_OTHER')

    for file in parser.ARCHIVES:
        handle_archive(file, folder / 'archives')


    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)

def start_function():
    try:
        folder = sys.argv[1]
    except IndexError:
        print("Enter valid path to the folder")
    else:
        folder_for_scan = Path(folder)
        print(f'Start in folder {folder_for_scan.resolve()}')
        main(folder_for_scan.resolve())

if __name__ == '__main__':
    start_function()