from filelist_parser import FilelistParser

parser = FilelistParser(['filelist.f'])

tree = parser.print_tree
print(tree)

srcs = parser.get_positional_arguments()
print(srcs)
incdirs = parser.get_optional_arguments(['+incdir'])
print(incdirs)
filelists = parser.get_optional_arguments(['-f'])
print(filelists)
