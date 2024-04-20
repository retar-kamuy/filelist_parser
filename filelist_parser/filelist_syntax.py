"""Wrapper for ``filelist-syntax --export_json``"""
import collections
import re
from typing import Callable, Dict, Iterable, List, Optional, Union

import dataclasses
import anytree

import ply.yacc as yacc

import yacc_filelist    # pylint: disable=W0611

_CSI_SEQUENCE = re.compile("\033\\[.*?m")


def _colorize(formats: List[str], strings: List[str]) -> str:
    result = ""
    fi = 0
    for s in strings:
        result += f"\033[{formats[fi]}m{s}\033[0m"
        fi = (fi+1) % len(formats)
    return result


# Type aliases

CallableFilter = Callable[["Node"], bool]
KeyValueFilter = Dict[str, Union[str, List[str]]]
TreeIterator = Union["_TreeIteratorBase", anytree.iterators.AbstractIter]


# Custom tree iterators with an option for reverse children iteration

class _TreeIteratorBase:
    def __init__(self, tree: "Node",
                    filter_: Optional[CallableFilter] = None,
                    reverse_children: bool = False):
        self.tree = tree
        self.reverse_children = reverse_children
        self.filter_ = filter_ if filter_ else lambda n: True

    def __iter__(self) -> Iterable["Node"]:
        yield from self._iter_tree(self.tree)

    def _iter_children(self, tree: Optional["Node"]) -> Iterable["Node"]:
        if not tree or not hasattr(tree, "children"):
            return []
        return tree.children if not self.reverse_children \
            else reversed(tree.children)

    def _iter_tree(self, tree: Optional["Node"]) -> Iterable["Node"]:
        raise NotImplementedError("Subclass must implement '_iter_tree' method")


class PreOrderTreeIterator(_TreeIteratorBase):
    def _iter_tree(self, tree: Optional["Node"]) -> Iterable["Node"]:
        if self.filter_(tree):
            yield tree
        for child in self._iter_children(tree):
            yield from self._iter_tree(child)


class PostOrderTreeIterator(_TreeIteratorBase):
    def _iter_tree(self, tree: Optional["Node"]) -> Iterable["Node"]:
        for child in self._iter_children(tree):
            yield from self._iter_tree(child)
        if self.filter_(tree):
            yield tree


class LevelOrderTreeIterator(_TreeIteratorBase):
    def _iter_tree(self, tree: Optional["Node"]) -> Iterable["Node"]:
        queue = collections.deque([tree])
        while len(queue) > 0:
            n = queue.popleft()
            if self.filter_(n):
                yield n
            queue.extend(self._iter_children(n))


class Node(anytree.NodeMixin):
    """Base VeribleVerilogSyntax syntax tree node.

    Attributes:
        parent (Optional[Node]): Parent node.
    """
    def __init__(self, parent: Optional["Node"] = None):
        self.parent = parent

    @property
    def text(self) -> Optional[str]:
        raise NotImplementedError("Subclass must implement 'text' property")

    @property
    def syntax_data(self) -> Optional["SyntaxData"]:
        return self.parent.syntax_data if self.parent else None

    def __repr__(self) -> str:
        return _CSI_SEQUENCE.sub("", self.to_formatted_string())

    def to_formatted_string(self) -> str:
        """Print node representation formatted for printing in terminal."""
        return super().__repr__()


class BranchNode(Node):
    """Syntax tree branch node

    Attributes:
        tag (str): Node tag.
        children (Optional[Node]): Child nodes.
    """
    def __init__(self, tag: str, parent: Optional[Node] = None,
                    children: Optional[List[Node]] = None):
        super().__init__(parent)
        self.tag = tag
        self.children = children if children is not None else []

    @property
    def text(self) -> Optional[str]:
        first_token = self.find(lambda n: isinstance(n, LeafNode),
                                iter_=PostOrderTreeIterator)
        return first_token.text if first_token else None

    def iter_find_all(self, filter_: Union[CallableFilter, KeyValueFilter, None],
                        max_count: int = 0,
                        iter_: TreeIterator = LevelOrderTreeIterator,
                        **kwargs) -> Iterable[Node]:
        def as_list(v):
            return v if isinstance(v, list) else [v]

        if filter_ and not callable(filter_):
            filters = filter_
            def f(node):
                for attr,value in filters.items():
                    if not hasattr(node, attr):
                        return False
                    if getattr(node, attr) not in as_list(value):
                        return False
                return True
            filter_ = f

        for node in iter_(self, filter_, **kwargs):
            yield node
            max_count -= 1
            if max_count == 0:
                break

    def find(self, filter_: Union[CallableFilter, KeyValueFilter, None],
                iter_: TreeIterator = LevelOrderTreeIterator, **kwargs) \
                -> Optional[Node]:

        return next(self.iter_find_all(filter_, max_count=1, iter_=iter_,
                    **kwargs), None)

    def find_all(self, filter_: Union[CallableFilter, KeyValueFilter, None],
                    max_count: int = 0, iter_: TreeIterator = LevelOrderTreeIterator,
                    **kwargs) -> List[Node]:

        return list(self.iter_find_all(filter_, max_count=max_count, iter_=iter_,
                    **kwargs))

    def to_formatted_string(self) -> str:
        tag = self.tag if self.tag == repr(self.tag)[1:-1] else repr(self.tag)
        return _colorize(["37", "1;97"], ["[", tag, "]"])


class RootNode(BranchNode):
    """Syntax tree root node."""
    def __init__(self, tag: str, syntax_data: Optional["SyntaxData"] = None,
                    children: Optional[List[Node]] = None):
        super().__init__(tag, None, children)
        self._syntax_data = syntax_data

    @property
    def syntax_data(self) -> Optional["SyntaxData"]:
        return self._syntax_data


class LeafNode(Node):
    """Syntax tree leaf node.

        This specific class is used for null nodes.
    """
    @property
    def text(self) -> None:
        """Byte offset of token's first character in source text"""
        return None

class TokenNode(LeafNode):
    """Syntax tree leaf node.

        This specific class is used for null nodes.
    """
    def __init__(self, tag: str, text: str,
                    parent: Optional[Node] = None):
        super().__init__(parent)
        self.tag = tag
        self._text = text

    @property
    def text(self) -> str:
        return self._text

    def to_formatted_string(self) -> str:
        tag = self.tag if self.tag == repr(self.tag)[1:-1] else repr(self.tag)
        parts = [
            _colorize(["37", "1;97"], ["[", tag, "]"])
        ]
        text = self.text
        if self.tag != text:
            parts.append(_colorize(["32", "92"], ["'", repr(text)[1:-1], "'"]))
        return " ".join(parts)


@dataclasses.dataclass
class SyntaxData:
    source_code: Optional[str] = None
    tree: Optional[RootNode] = None

class FilelistSyntax:
    """``verible-verilog-syntax`` wrapper.

    This class provides methods for running ``verible-verilog-syntax`` and
    transforming its output into Python data structures.

    Args:
        executable: path to ``verible-verilog-syntax`` binary.
    """
    @staticmethod
    def _transform_tree(tree, data: SyntaxData, skip_null: bool) -> RootNode:
        def transform(tree):
            # print(tree)
            if tree is None:
                return None
            if "children" in tree:
                children = [
                    transform(child) or LeafNode()
                        for child in tree["children"]
                        if not (skip_null and child is None)
                ]
                tag = tree["tag"]
                return BranchNode(tag, children=children)
            tag = tree["tag"]
            text = tree["text"]
            return TokenNode(tag, text)

        if "children" not in tree:
            return None

        children = [
            transform(child) or LeafNode()
                for child in tree["children"]
                if not (skip_null and child is None)
        ]
        tag = tree["tag"]
        return RootNode(tag, syntax_data=data, children=children)

    def _parse(self, paths: List[str]) -> Dict[str, SyntaxData]:
        """Common implementation of parse_* methods"""
        data = {}
        for pathname in paths:
            file_data = SyntaxData()
            try:
                f = open(pathname, encoding='UTF-8')
            except OSError as err:
                print(err)
            else:
                file_data.source_code = f.read()
                f.close()

            result = yacc.parse(file_data.source_code.replace('\n', ' '))
            file_data.tree = FilelistSyntax._transform_tree(result, file_data, True)
            data[pathname] = file_data

        return data

    def parse_files(self, paths: List[str]) -> Dict[str, SyntaxData]:
        return self._parse(paths)
