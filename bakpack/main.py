#
# e.g. soul@ark:~/Projects/bakpack$ poetry run bakpack -v -1 --output t1.json --json --size 13194139533312 `cat tarnames`
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
flags.DEFINE_bool("json", False, "Output only JSON of grouped files with sizes")


def main(argv):
    logging.info(f"Bin size is {FLAGS.size}")
    logging.info(f"args are {argv}")

    pathnames_of_size = defaultdict(list)
    sizes = []
    too_big = []
    for pathname in argv[1:]:
        path = Path(pathname)
        size = path.stat().st_size
        if size > FLAGS.size:
            too_big.append((pathname, size))
        else:
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

    with get_outfile() as outf:
        if FLAGS.json:
            json.dump(pathed, outf, indent=2)
            return
        overall_preamble(outf)
        for pathname, size in too_big:
            outf.write(f"# {pathname} is {size} bytes which is too big, skipping\n")
        for bin_contents in pathed:
            tape_preamble(outf)
            for pathname, size in bin_contents:
                process_path(outf, pathname)
            tape_postamble(outf)
        overall_postamble(outf)


def get_outfile():
    if FLAGS.output is None:
        return stdout
    return open(FLAGS.output, "w")


def overall_preamble(f):
    f.write("# Some overall preamble\n")

def tape_preamble(f):
    f.write(f"# Some preamble to a particular tape\n")

def tape_postamble(f):
    f.write(f"# Some post-process for a particular tape\n")

def overall_postamble(f):
    f.write(f"# Any overall post-process\n")

def process_path(f, pathname):
    f.write(f"# process Path {pathname}\n")


def entry():
    app.run(main)


if __name__ == "__main__":
    app.run(main)
