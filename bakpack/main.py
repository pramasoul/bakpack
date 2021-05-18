#
from absl import app
from absl import flags
from absl import logging

from collections import defaultdict
import json
from pathlib import Path
from sys import stdout

from .packer import binpack

FLAGS = flags.FLAGS

flags.DEFINE_integer("size", None, "How much a bin can hold", lower_bound=1)
flags.DEFINE_string("output", None, "Output filename (defaults to stdout)")
flags.DEFINE_bool("json", False, "Output only JSON of files with sizes")


def main(argv):
    logging.info(f"Bin size is {FLAGS.size}")
    logging.info(f"args are {argv}")
    pathnames_of_size = defaultdict(list)
    sizes = []
    for pathname in argv[1:]:
        path = Path(pathname)
        size = path.stat().st_size
        sizes.append(size)
        pathnames_of_size[size].append(pathname)
    logging.info(f"pathnames_of_size is {pathnames_of_size}")
    logging.info(f"sizes: {sizes}")
    packed = binpack(FLAGS.size, sizes)
    logging.info(f"packed {packed}")

    pathed = []
    for bin_contents in packed:
        paths = []
        for size in bin_contents:
            paths.append((pathnames_of_size[size].pop(), size))
        pathed.append(paths)

    with get_outfile() as f:
        if FLAGS.json:
            json.dump(pathed, f)
            return
        f.write("# Some overall preamble\n")
        for bin_contents in pathed:
            f.write(f"# Some preamble to a particular tape\n")
            for pathname, size in bin_contents:
                f.write(f"# process Path {pathname}\n")
            f.write(f"# Some post-process for a particular tape\n")
        f.write(f"# Any overall post-process\n")


def get_outfile():
    if FLAGS.output is None:
        return stdout
    return open(FLAGS.output, "w")


def entry():
    app.run(main)


if __name__ == "__main__":
    app.run(main)
