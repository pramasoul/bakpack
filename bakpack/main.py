#
from absl import app
from absl import flags
from absl import logging

from collections import defaultdict
from pathlib import Path

from .packer import binpack

FLAGS = flags.FLAGS

flags.DEFINE_integer("size", None, "How much a bin can hold", lower_bound=1)

# (Path('d1') / Path('1.txt')).stat().st_size


def main(argv):
    logging.info(f"Bin size is {FLAGS.size}")
    logging.info(f"args are {argv}")
    paths_of_size = defaultdict(list)
    sizes = []
    for pathname in argv[1:]:
        path = Path(pathname)
        size = path.stat().st_size
        sizes.append(size)
        paths_of_size[size].append(path)
    logging.info(f"paths_of_size is {paths_of_size}")
    logging.info(f"sizes: {sizes}")
    packed = binpack(FLAGS.size, sizes)
    logging.info(f"packed {packed}")
    print("# Some overall preamble")
    for bin_contents in packed:
        print(f"# Some preamble to a particular tape")
        for size in bin_contents:
            path = paths_of_size[size].pop()
            print(f"# process Path {path}")
        print(f"# Some post-process for a particular tape")
    print(f"# Any overall post-process")

def entry():
    app.run(main)

if __name__ == '__main__':
    app.run(main)
