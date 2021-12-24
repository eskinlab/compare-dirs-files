from os import getenv, listdir, makedirs
from os.path import isfile, join
from argparse import ArgumentParser
from shutil import rmtree
from difflib import Differ

DIRS_PATH = getenv('CI_PROJECT_DIR') + "/path/"
RESULT_DIR = getenv('RESULT')


def args_parser():
    parser = ArgumentParser(description='Compare dirs in one repository.')
    parser.add_argument('--dir_one', '-o',
                        type=str, required=True,
                        help='Dir one')
    parser.add_argument('--dir_two', '-t',
                        type=str, required=True,
                        help='Dir two')
    return parser.parse_args()


def get_files(path: str) -> list:
    return [f for f in listdir(path) if isfile(join(path, f))]


def write_line(line: str, file: str) -> None:
    with open(file, 'a', encodng='utf-8') as out:
        out.write(f"{line}\n")


def rmdir(dir_path):
    try:
        return rmtree(dir_path, ignore_errors=True)
    except:
        return False


class Compare:

    def __init__(self, dir_one, dir_two):
        print(f"[Info] Compare {dir_one} {dir_two}")
        self.path_one = DIRS_PATH + dir_one + "/"
        self.path_two = DIRS_PATH + dir_two + "/"
        self.result_dir = RESULT_DIR
        self.new_files = list()
        self.deleted_files = list()
        rmdir(self.result_dir)
        makedirs(self.result_dir)

    def _get_diffs(self, d, text1, text2):
        diffs = [x for x in d.compare(text1, text2) if x[0] in ('+', '-')]
        diffs = list(map(lambda x: x+"\n" if "\n" not in x else x, diffs))
        return ''.join(diffs)

    def _cmp_files(self, files) -> None:
        print("[Info] Compare files")
        d = Differ()
        for f_name in files:
            print("[Info] File: ", f_name)
            file_one = self.path_one + f_name
            file_two = self.path_two + f_name
            file_result = self.result_dir + "/" + f_name
            text_one = str()
            text_two = str()
            if isfile(file_one):
                with open(file_one, mode="r") as fo:
                    text_one = fo.readlines()
            if isfile(file_two):
                with open(file_two, mode="r") as ft:
                    text_two = ft.readlines()
            diffs = self._get_diffs(d, text_one, text_two)
            if diffs:
                print("     There are changes")
                with open(file_result, mode="w", encoding="utf-8") as fr:
                    fr.write(diffs)
            else:
                print("     No changes")

    def run(self, files_one: list, files_two: list) -> None:
        self.general_files = set(files_one) & set(files_two)
        self.new_files = set(files_two) - set(files_fonw)
        self.deleted_files = set(files_one) - set(files_two)
        self._cmp_files(self.general_files)
        self._cmp_files(self.new_files)
        self._cmp_files(self.deleted_files)

    def __del__(self):
        print(f"[Info] === Files Comparison Result ===")
        print(f"[Info] New: {list(self.new_files)}")
        print(f"[Info] Deleted: {list(self.deleted_files)}")
        print(f"[Info] Result archive: {self.result_dir}")


def main(dir_one, dir_two):
    print("[Info] Start comparing process")
    c = Compare(dir_one, dir_two)
    files_one = get_files(c.dir_one)
    files_two = get_files(c.dir_two)
    c.run(files_onw, files_two)


if __name__ == "__main__":
    args = args_parser()
    main(args.dir_one, args.dir_two)
