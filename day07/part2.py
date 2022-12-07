import sys


class FileNode:
    def __init__(self, parent, name, size: int = 0):
        self.parent = parent
        self.name = name
        self.size = size
        self.children: list[FileNode] = []

    def __str__(self):
        desc = "dir" if self.is_dir() else "file"
        if not self.is_dir():
            desc += ", size=" + str(self.size)
        return self.name + " (" + desc + ")"

    def __repr__(self):
        return str(self)

    def get_size(self) -> int:
        if len(self.children) == 0:
            return self.size
        children_size: int = 0
        for child in self.children:
            children_size = children_size + child.get_size()
        return self.size + children_size

    def is_dir(self):
        return self.size == 0

    def path(self):
        if self.name == None:
            return ""
        if self.parent != None:
            return self.parent.path() + " " + self.name
        return self.name


def print_filesystem(node, level=0):
    print("  " * level + "- " + str(node))
    for child in node.children:
        print_filesystem(child, level + 1)


def create_or_get_dir(working_dir: FileNode, name):
    if working_dir != None:
        for file in working_dir.children:
            if file.is_dir() and file.name == name:
                return file
    dir = FileNode(working_dir, name)
    if working_dir != None:
        working_dir.children.append(dir)
    return dir


def create_filesystem(lines: list[str]):
    root_dir = None
    working_dir = None
    for line in lines:
        if line.startswith("$ cd"):
            command_parts = line.split()
            command = command_parts[1]
            path = command_parts[2]
            if path == "..":
                working_dir = working_dir.parent
            else:
                working_dir = create_or_get_dir(working_dir, path)
        elif not line.startswith("$"):
            file_parts = line.split()
            file_desc = file_parts[0]
            file_name = file_parts[1]
            if file_desc != "dir":
                file = FileNode(working_dir, file_name, int(file_desc))
                working_dir.children.append(file)
            else:
                create_or_get_dir(working_dir, file_name)
        if root_dir == None:
            root_dir = working_dir
    return root_dir


def find_all_dirs(root: FileNode, dirs: list[FileNode] = []) -> list[FileNode]:
    dirs.append(root)
    for file in root.children:
        if file.is_dir():
            find_all_dirs(file)
    return dirs


f = open(sys.argv[1], "r")
lines = f.read().splitlines()
root = create_filesystem(lines)

DISK_SIZE = 70000000
UPDATE_SIZE = 30000000
used_space = root.get_size()
delete_size = UPDATE_SIZE - (DISK_SIZE - used_space)

directories_big_enough = filter(lambda dir: dir.get_size() >= delete_size, find_all_dirs(root))
smallest_matching_dir = min(directories_big_enough, key = lambda dir: dir.get_size())
print(smallest_matching_dir.get_size())
