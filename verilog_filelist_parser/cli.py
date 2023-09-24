import os
from typing import List

import anytree

from filelist_syntax import FilelistSyntax

class FilelistParser(FilelistSyntax):
    def __init__(self, paths: List[str]):
        super().__init__()
        self.paths = paths
        self.data = self.parse_files(paths)

    def get_source_files(self) -> List[str]:
        srcs = []
        for file_path, file_data in self.data.items():
            for filelist in file_data.tree.iter_find_all({"tag": "kFilelistDeclaration"}):
                for src_obj in filelist.iter_find_all({"tag": ["kPositionalArgument"]}):
                    srcs.append(src_obj.text)
        return srcs

    @property
    def print_tree(self):
        for file_path, file_data in self.data.items():
            for prefix, _, node in anytree.RenderTree(file_data.tree):
                print(f"\033[90m{prefix}\033[0m{node.to_formatted_string()}")
            print()


def main():
    parser = FilelistParser(['filelist.f'])

    parser.print_tree
    srcs = parser.get_source_files()
    print(srcs)

    # for file_path, file_data in data.items():
    #     for filelist in file_data.tree.iter_find_all({"tag": "kFilelistDeclaration"}):
    #         for positional in filelist.iter_find_all({"tag": ["kPositionalArgument"]}):
    #             print(positional.text)
    #             positional_id = positional.find({"tag": ["identifier"]})
    #             print(positional_id.text)
# 
    #     for filelist in file_data.tree.iter_find_all({"tag": "kFilelistDeclaration"}):
    #         for file in filelist.iter_find_all({"tag": ["kFileArgument"]}):
    #             print(file.text)
    #             file_id = file.find({"tag": ["identifier"]})
    #             print(file_id.text)
