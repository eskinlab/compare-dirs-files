from os import getenv, listdir, makedirs
from os.path import isfile, join
from argparse import ArgumentParser
from shutil import rmtree
from difflib import Differ

DIRS_PATH = getenv('CI_PROJECT_DIR') + "/path/"
RESULT_DIR = getenv('RESULT')


def args_parser():
    parser = ArgumentParser(description='Compare dirs in one repository.')
    parser.add_argument('--dir_from', '-f',
                        type=str, required=True,
                        help='Dir from')
    parser.add_argument('--dir_to', '-t',
                        type=str, required=True,
                        help='Dir to')
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

    def __init__(self, dir_from, dir_to):
        print(f"[Info] Compare {dir_from} {dir_to}")
        self.path_from = DIRS_PATH + dir_from + "/"
        self.path_to = DIRS_PATH + dir_to + "/"
        self.result_dir = RESULT_DIR
        self.new_files = list()
        self.deleted_files = list()
        rmdir(self.result_dir)
        makedirs(self.result_dir)

    def _get_diffs(self, d, text_f, text_t):
        diffs = [x for x in d.compare(text_f, text_t) if x[0] in ('+', '-')]
        diffs = list(map(lambda x: x+"\n" if "\n" not in x else x, diffs))
        return ''.join(diffs)

    def _cmp_files(self, files) -> None:
        print("[Info] Compare files")
        d = Differ()
        for f_name in files:
            print("[Info] File: ", f_name)
            file_from = self.path_from + f_name
            file_to = self.path_to + f_name
            file_result = self.result_dir + "/" + f_name
            text_from = str()
            text_to = str()
            if isfile(file_from):
                with open(file_from, mode="r") as ff:
                    text_from = ff.readlines()
            if isfile(file_to):
                with open(file_to, mode="r") as ft:
                    text_to = ft.readlines()
            diffs = self._get_diffs(d, text_from, text_to)
            if diffs:
                print("     There are changes")
                with open(file_result, mode="w", encoding="utf-8") as fr:
                    fr.write(diffs)
            else:
                print("     No changes")

    def run(self, files_from: list, files_to: list) -> None:
        self.general_files = set(files_from) & set(files_to)
        self.new_files = set(files_to) - set(files_from)
        self.deleted_files = set(files_from) - set(files_to)
        self._cmp_files(self.general_files)
        self._cmp_files(self.new_files)
        self._cmp_files(self.deleted_files)

    def __del__(self):
        print(f"[Info] === Files Comparison Result ===")
        print(f"[Info] New: {list(self.new_files)}")
        print(f"[Info] Deleted: {list(self.deleted_files)}")
        print(f"[Info] Result archive: {self.result_dir}")


def main(branch_from, branch_to):
    print("[Info] Start comparing process")
    c = Compare(dir_from, dir_to)
    files_from = get_files(c.dir_from)
    files_to = get_files(c.dir_to)
    c.run(files_from, files_to)


if __name__ == "__main__":
    args = args_parser()
    main(args.dir_from, args.dir_to)
