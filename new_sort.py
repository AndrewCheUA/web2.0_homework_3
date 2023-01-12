from pathlib import Path
import re
from threading import Thread
import logging  # delete after testing
from timeit import default_timer  # delete after testing
import shutil
import os
import concurrent.futures
from multiprocessing import cpu_count


logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
f_catalog = ["images", "video", "documents", "music", "archives"]
file_dump = []


def normalize(file):
    trans_dict = {1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g',
                  1043: 'G', 1076: 'd', 1044: 'D', 1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E',
                  1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z', 1080: 'i', 1048: 'I', 1081: 'j',
                  1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 1051: 'L', 1084: 'm', 1052: 'M',
                  1085: 'n', 1053: 'N', 1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r',
                  1056: 'R', 1089: 's', 1057: 'S', 1090: 't', 1058: 'T', 1091: 'u', 1059: 'U',
                  1092: 'f', 1060: 'F', 1093: 'h', 1061: 'H', 1094: 'ts', 1062: 'TS',
                  1095: 'ch', 1063: 'CH', 1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH',
                  1098: '', 1066: '', 1099: 'y', 1067: 'Y', 1100: '', 1068: '', 1101: 'e',
                  1069: 'E', 1102: 'yu', 1070: 'YU', 1103: 'ya', 1071: 'YA', 1108: 'je',
                  1028: 'JE', 1110: 'i', 1030: 'I', 1111: 'ji', 1031: 'JI', 1169: 'g',
                  1168: 'G'}
    file_name = re.sub('\W', "'_'", file.name.rstrip(file.suffix).translate(trans_dict)) + file.suffix
    return file_name


def sort_funct(fdump_list):
    images = [".jpg", ".jpeg", ".png", ".svg"]
    video = [".avi", ".mp4", ".mov", "mkv"]
    documents = [".doc", "docx", ".txt", ".pdf", ".xlsx", ".pptx"]
    music = [".mp3", ".ogg", ".wav", ".amr"]
    archives = [".zip", ".gz", ".tar"]

    images_p = os.path.join(fdump_list[1], "images")
    video_p = os.path.join(fdump_list[1], "video")
    documents_p = os.path.join(fdump_list[1], "documents")
    music_p = os.path.join(fdump_list[1], "music")
    archives_p = os.path.join(fdump_list[1], "archives")
    if str(fdump_list[0].suffix) in images:
        Path(images_p).mkdir(exist_ok=True)
        file_name = normalize(fdump_list[0])
        fdump_list[0].rename(os.path.join(images_p, file_name))

    elif str(fdump_list[0].suffix) in video:
        Path(video_p).mkdir(exist_ok=True)
        file_name = normalize(fdump_list[0])
        fdump_list[0].rename(os.path.join(video_p, file_name))

    elif str(fdump_list[0].suffix) in documents:
        Path(documents_p).mkdir(exist_ok=True)
        file_name = normalize(fdump_list[0])
        fdump_list[0].rename(os.path.join(documents_p, file_name))

    elif str(fdump_list[0].suffix) in music:
        Path(music_p).mkdir(exist_ok=True)
        file_name = normalize(fdump_list[0])
        fdump_list[0].rename(os.path.join(music_p, file_name))

    elif str(fdump_list[0].suffix) in archives:
        Path(archives_p).mkdir(exist_ok=True)
        arc_name = re.sub(str(fdump_list[0].suffix), "", fdump_list[0].name)
        shutil.unpack_archive(fdump_list[0].name, archives_p + arc_name)
        fdump_list[0].unlink()
    else:
        file_name = normalize(fdump_list[0])
        fdump_list[0].rename(os.path.join(fdump_list[1], file_name))


def main_func(user_input: str):

    root_folder = Path(user_input)
    if root_folder.exists() and not root_folder.is_file():
        for item in root_folder.iterdir():
            if item.is_dir() and item.name not in f_catalog:
                print(f"FOLDER {item.name}")
                m1 = Thread(target=main_func, args=(item,))
                m1.start()
                m1.join()

            elif item.is_file():
                print(item.name)
                file_dump.append(item)

    elif not root_folder.exists():
        print("Incorrect folder path.")


if __name__ == '__main__':
    t1 = default_timer()    # delete after testing
    folder_input = input('Enter path to folder which should be cleaned: ')
    main_func(folder_input)
    final_file_dump = []
    for i in file_dump:
        final_file_dump.append([i, Path(folder_input)])
    with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_count()) as executor:
        results = list(executor.map(sort_funct, final_file_dump))
    print(final_file_dump)
    delta = default_timer() - t1    # delete after testing
    logging.info(f"Process run time {delta}")   # delete after testing
    