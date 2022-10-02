#
# make info from "mtx -f <changer> status" accessable to python

import subprocess
import sys

from pprint import pprint

class MTX:

    def __init__(self, changer):
        self.changer = changer
        self.slot_from_volume = {}
        self.volume_from_slot = {}

    def status(self):
        v = subprocess.run(["mtx", "-f", self.changer, "status"], capture_output=True)
        if v.returncode != 0:
            raise OSError(f"mtx failed with error {v.returncode}")
        output = v.stdout.decode('utf-8')
        split_lines = [line.strip().split(':') for line in output.split('\n')]
        ss_lines = [tuple(map(lambda s: s.strip(), sl)) for sl in split_lines]
        for sl in filter(lambda l: l[0].startswith('Storage Element '), ss_lines):
            slot = int(sl[0].split()[2])
            if sl[1] == "Full":
                try:
                    vtag = sl[2].split('=')[1]
                    self.slot_from_volume[vtag] = slot
                    self.volume_from_slot[slot] = vtag
                except IndexError:
                    self.volume_from_slot[slot] = 'UNLABELED'
            else:
                self.volume_from_slot[slot] = None
        return self

def main(args):
    print(f'hi from {args}')
    c = MTX(args[1])
    v = c.status()
    pprint(v.volume_from_slot)
    pprint(v.slot_from_volume)

if __name__ == '__main__':
    main(sys.argv)
