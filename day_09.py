from dataclasses import dataclass

from copy import copy

@dataclass
class FSNode:
    file_id: int|None
    file_length: int
    start_pos: int
    white_space: bool
    moved: bool = False

    def checksum(self):
        return sum(self.file_id * i for i in range(self.start_pos, self.start_pos + self.file_length))


DEBUG = True

class FileSystem:
    def __init__(self):
        self.data = []
        self.dirty = False
        self.next_id = 0
    def append(self, fsnode):
        self.data.append(fsnode)
        self.dirty = True
        if not fsnode.white_space:
            fsnode.file_id = self.next_id
            self.next_id += 1
    def append_compact(self, size, white_space=0):
        fsnode = FSNode(None, size, -1, white_space)
        self.append(fsnode)

    def load_compact(self, compact_string):
        for index, size_char in enumerate(compact_string):
            size = int(size_char)
            self.append_compact(size, index % 2)


    def reindex(self):
        index = 0
        for item in self.data:
            item.start_pos = index
            index += item.file_length
        self.dirty = False

    def __getitem__(self, pos):
        """Return filenode at given uncompacted position

        """
        if self.dirty:
            self.reindex()
        # linear search - we could move this to binary search later
        index = 0
        if pos == 0:
            return self.data[0]

        for item in self.data:
            index += item.file_length
            if index >= pos:
                return item
        raise IndexError()

    def __len__(self):
        if self.dirty:
            self.reindex()
        return self.data[-1].start_pos + self.data[-1].file_length



    def compress(self):
        fspointer = -1
        to_be_compacted_pointer = len(self.data) - 1
        index = 0

        fetch_whitespace = True
        fetch_compacting_node = True
        while True:
            if fspointer >= to_be_compacted_pointer - 1:
                break
            if fetch_compacting_node:
                while True:
                    compacting_node = self.data[to_be_compacted_pointer]
                    if compacting_node.white_space:
                        to_be_compacted_pointer -= 1
                    else:
                        break
                fetch_compacting_node = False

            if fetch_whitespace:
                # fetch next whitespace node:
                while True:
                    fspointer += 1
                    node = self.data[fspointer]
                    if node is None:
                        raise ValueError(" end of disk with no more whitespace")
                    if node.white_space:
                        break
                fetch_whitespace = False

            data_size = compacting_node.file_length
            empty_size = node.file_length

            new_data_size = data_size - empty_size

            node.file_id = compacting_node.file_id
            node.white_space = False

            if data_size < empty_size:
                # there is extra white space afeter moving all file in!
                # split white space node:
                node.file_length = data_size
                node = FSNode(None, empty_size - data_size, -1, white_space=True)
                fspointer += 1
                self.data.insert(fspointer, node)
                self.dirty = True
            elif data_size >= empty_size:
                fetch_whitespace = True

            if new_data_size > 0:
                # the file didn't fit into the empty space of this node
                compacting_node.file_length = new_data_size
                # insert a new whitespace node after the file
                # skipping that as solving the problem does not require it:
                # self.data.insert(to_be_compacted_pointer + len(self.data) + 1, NEW_EMPTY_NODE)
            else:
                # all data in file moved!
                # convert previous data file to empty file:
                compacting_node.white_space = True
                to_be_compacted_pointer -= 1
                fetch_compacting_node = True

            if DEBUG:
                print(self)


    def compress2(self):
        self.reindex()
        for file in reversed(self.data[:]):
            if file.white_space:
                continue
            if file.moved:
                continue
            file.moved = True
            for index, white_space in enumerate(self.data):
                if not white_space.white_space:
                    continue
                if white_space.start_pos >= file.start_pos:
                    break
                if white_space.file_length >= file.file_length:
                    self.data.insert(index, copy(file))
                    white_space.file_length -= file.file_length
                    file.white_space = True
                    self.dirty = True
                    break

            if DEBUG:
                print(self)


    def checksum(self):
        self.reindex()
        checksum = 0
        for item in self.data:
            if not item.white_space:
                checksum += item.checksum()
        return checksum

    def __repr__(self):
        return "".join(("." if item.white_space else str(item.file_id % 10)) * item.file_length for item in self.data)
# part1
m = FileSystem()
m.load_compact(aa)
m.compress()
print(m.checksum())

# part2:
m = FileSystem()
m.load_compact(aa)
m.compress2()
print(m.checksum())

