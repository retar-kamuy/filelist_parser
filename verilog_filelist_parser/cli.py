from typing import List

import anytree

from filelist_syntax import FilelistSyntax

class FilelistParser(FilelistSyntax):
    def __init__(self, paths: List[str]):
        super().__init__()
        self.paths = paths
        self.data = self.parse_files(paths)

    def get_optional_arguments(self, tags: List[str]) -> List[str]:
        identifiers = []
        for file_path, file_data in self.data.items():
            for filelist in file_data.tree.iter_find_all({'tag': 'kFilelistDeclaration'}):
                for identifier_obj in filelist.iter_find_all({'tag': tags}):
                    identifier_id = identifier_obj.find({'tag': ['identifier']})
                    identifiers.append(identifier_id.text)
        return identifiers

    def get_positional_arguments(self) -> List[str]:
        identifiers = []
        for file_path, file_data in self.data.items():
            for filelist in file_data.tree.iter_find_all({"tag": "kFilelistDeclaration"}):
                for identifier_obj in filelist.iter_find_all({"tag": ["kPositionalArgument"]}):
                    identifiers.append(identifier_obj.text)
        return identifiers

    @property
    def print_tree(self):
        for file_path, file_data in self.data.items():
            for prefix, _, node in anytree.RenderTree(file_data.tree):
                print(f"\033[90m{prefix}\033[0m{node.to_formatted_string()}")
            print()


def main():
    parser = FilelistParser(['filelist.f'])

    parser.print_tree
    srcs = parser.get_positional_arguments()
    print(srcs)
    incdirs = parser.get_optional_arguments(['kIncludeArgument'])
    print(incdirs)
    filelists = parser.get_optional_arguments(['kFileArgument'])
    print(filelists)
