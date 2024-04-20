from typing import List

import anytree

from filelist_syntax import FilelistSyntax

class FilelistParser(FilelistSyntax):
    def __init__(self, paths: List[str]):
        super().__init__()
        self.paths = paths
        self.data = self.parse_files(paths)

    def get_optional_arguments(self, filters: List[str] | None) -> List[str]:
        identifiers = []
        for file_path, file_data in self.data.items():  # pylint: disable=W0612
            for filelist in file_data.tree.iter_find_all({'tag': 'kFilelistDeclaration'}):
                for obj in filelist.iter_find_all({'tag': ['kOptionalArgument']}):
                    argument = obj.find({'tag': ['argument']})
                    for filter_arg in filters:
                        if argument.text == filter_arg:
                            identifier = obj.find({'tag': ['identifier']})
                            identifiers.append(identifier.text)
        return identifiers

    def get_positional_arguments(self) -> List[str]:
        identifiers = []
        for file_path, file_data in self.data.items():  # pylint: disable=W0612
            for filelist in file_data.tree.iter_find_all({"tag": "kFilelistDeclaration"}):
                for obj in filelist.iter_find_all({"tag": ["kPositionalArgument"]}):
                    identifiers.append(obj.text)
        return identifiers

    @property
    def print_tree(self):
        for file_path, file_data in self.data.items():  # pylint: disable=W0612
            for prefix, _, node in anytree.RenderTree(file_data.tree):
                print(f"\033[90m{prefix}\033[0m{node.to_formatted_string()}")
            print()


def main():
    parser = FilelistParser(['filelist.f'])

    parser.print_tree
    srcs = parser.get_positional_arguments()
    print(srcs)
    incdirs = parser.get_optional_arguments(['+incdir'])
    print(incdirs)
    filelists = parser.get_optional_arguments(['-f'])
    print(filelists)
