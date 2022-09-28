Notes
=====

- Some set of paths get tar'ed up as the first file of each tape:
  
  - The code that made the backup script

  - The backup script

  - Various ls-LR's and b3sums etc over the entire contents

- Some data from the run gets accumulated and included in the first file of successive tapes:

  - The log of the run so far

Scheme
======

#. Create a file of the pathnames of the files to group and write to tape

#. Create a file of the pathnames of files/directories to be tar'ed up and recorded as the first file of a tape when it is started

#. Create a file of the tapes to use by label, in sequence

#. Run ``bakpack`` with the filenames above passed as arguments (details TBD), producing a shell script
   #. It will have to find out the tape robot slots of 

#. Review the script (this is alpha software at best). Script should do:
   #. ``mtx -f /dev/sg20 unload`` to get any tape that may be loaded back to its origin slot
   #. ``mtx -f /dev/sg20 load <first tape's slot number>`` to get the first tape in the drive
   #. ``tar czf preface.tgz <the preface files/directories>`` to create the first file for the tape, providing documentation and context for the tape
   #. ``mbuffer -i preface.tgz -o /dev/nst0 -s 512k -m 1G -P 90 --hash BLAKE2B_512`` to write the document & context tar file to the tape
   #. 



Hints
=====
- sudo mbuffer -i /lake/incoming/LaCie_FW/1t5.tgz -o /dev/st0 -s 512k -m 1G -P 90 --hash BLAKE2B_512

soul@ark:~/Projects/bakpack$ ls -l /dev/tape/by-path/
total 0
lrwxrwxrwx 1 root root  9 May 21 22:09 pci-0000:82:00.0-sas-phy0-lun-0 -> ../../st0
lrwxrwxrwx 1 root root 10 May 21 22:09 pci-0000:82:00.0-sas-phy0-lun-0-nst -> ../../nst0
lrwxrwxrwx 1 root root 10 May 21 22:09 pci-0000:82:00.0-sas-phy0-lun-1-changer -> ../../sg20

soul@ark:~/Projects/bakpack$ b2sum /lake/incoming/LaCie_FW/1t5.tgz
fcb1afe7206a0a0a1c15b1db47a15b264b450e0a997b03fd4abae8d8f0e4323d65eaf2f99d90e739f725689add97b18d4c7ff545a0df75044884cab53242e4af  /lake/incoming/LaCie_FW/1t5.tgz
soul@ark:~/Projects/bakpack$ b2sum -l 256  /lake/incoming/LaCie_FW/1t5.tgz
4dcab5a11463e982fd31f601357eb3f324919fda7adbc8ef8579d6b03851cc8a  /lake/incoming/LaCie_FW/1t5.tgz
soul@ark:~/Projects/bakpack$ mbuffer -i /lake/incoming/LaCie_FW/1t5.tgz -o /dev/null -s 512k -m 1G -P 90 --hash BLAKE2B_512
in @  0.0 kiB/s, out @  403 MiB/s, 38.2 GiB total, buffer  15% full, 100% done
BLAKE2B_512 hash: fcb1afe7206a0a0a1c15b1db47a15b264b450e0a997b03fd4abae8d8f0e4323d65eaf2f99d90e739f725689add97b18d4c7ff545a0df75044884cab53242e4af
summary: 38.4 GiByte in  2min 09.7sec - average of  303 MiB/s
soul@ark:~/Projects/bakpack$ mbuffer -i /lake/incoming/LaCie_FW/1t5.tgz -o /dev/null -s 512k -m 1G -P 90
in @  340 MiB/s, out @  0.0 kiB/s, 37.9 GiB total, buffer  45% full,  99% done
summary: 38.4 GiByte in  2min 03.0sec - average of  319 MiB/s, 42x empty
soul@ark:~/Projects/bakpack$ 


sudo mtx -f /dev/sg20 status
sudo mtx -f /dev/sg20 load 1

# Written with mbuffer -s 512k so each tape block is 1024 512byte historical-size blocks
sudo tar tvb 1024 -f /dev/st0
# But the zlib decompression makes it CPU-limited, and possibly makes the tape stop-start. Better to mbuffer move the file to disk, then process



soul@ark:~/Projects/bakpack$ sudo mt -f /dev/nst0 rewind
soul@ark:~/Projects/bakpack$ sudo mt -f /dev/nst0 status
drive type = 114
drive status = 1577058304
sense key error = 0
residue count = 0
file number = 0
block number = 0
soul@ark:~/Projects/bakpack$ time sudo mt -f /dev/nst0 fsf 1

real    1m9.693s
user    0m0.007s
sys     0m0.010s
soul@ark:~/Projects/bakpack$ sudo mt -f /dev/nst0 status
drive type = 114
drive status = 1577058304
sense key error = 0
residue count = 0
file number = 1
block number = 0
soul@ark:~/Projects/bakpack$ time sudo mt -f /dev/nst0 rewind

real    0m0.021s
user    0m0.007s
sys     0m0.009s
soul@ark:~/Projects/bakpack$ sudo mt -f /dev/nst0 status
drive type = 114
drive status = 1577058304
sense key error = 0
residue count = 0
file number = 0
block number = 0
soul@ark:~/Projects/bakpack$ sudo mbuffer -i /dev/nst0 -o /lake/tmp/t.tar.1 -s 512k -m 1G -P 10
in @ 60.9 MiB/s, out @  138 MiB/s, 38.4 GiB total, buffer   0% full
summary: 38.4 GiByte in  3min 50.9sec - average of  170 MiB/s, 293x empty
# Note that the reading was delayed, apparently until the tape actually rewound, as if the mt rewind
# command merely queued the rewind rather than making it happen immediately
soul@ark:~/Projects/bakpack$ sudo mt -f /dev/nst0 status
drive type = 114
drive status = 1577058304
sense key error = 0
residue count = 0
file number = 1
block number = 0
soul@ark:~/Projects/bakpack$ sudo mbuffer -i /dev/nst0 -o /dev/null -s 512k -m 1G -P 90 --hash BLAKE2B_512
in @  0.0 kiB/s, out @  403 MiB/s, 38.3 GiB total, buffer   0% full
BLAKE2B_512 hash: fcb1afe7206a0a0a1c15b1db47a15b264b450e0a997b03fd4abae8d8f0e4323d65eaf2f99d90e739f725689add97b18d4c7ff545a0df75044884cab53242e4af
summary: 38.4 GiByte in  3min 34.2sec - average of  183 MiB/s, 10x empty
# Nice, the hash matches that of /lake/incoming/LaCie_FW/1t5.tgz, confirming that's the file written on the tape

# Does the tape get rewound before unloading? Experiment:
soul@ark:~/Projects/bakpack$ sudo mtx -f /dev/sg20 unload 1
Unloading drive 0 into Storage Element 1...done
soul@ark:~/Projects/bakpack$ sudo mbuffer -i /dev/nst0 -o /dev/null -s 512k -m 128M -P 10 --hash BLAKE2B_512
in @ 34.0 MiB/s, out @ 5114 kiB/s, 38.3 GiB total, buffer  11% full
BLAKE2B_512 hash: fcb1afe7206a0a0a1c15b1db47a15b264b450e0a997b03fd4abae8d8f0e4323d65eaf2f99d90e739f725689add97b18d4c7ff545a0df75044884cab53242e4af
summary: 38.4 GiByte in  2min 19.6sec - average of  282 MiB/s, 801x empty
# Answer: yes, it apparently got rewound before unloading into its slot

soul@ark:~/Projects/bakpack$ sudo tapeinfo -f /dev/nst0
Product Type: Tape Drive
Vendor ID: 'IBM     '
Product ID: 'ULTRIUM-HH8     '
Revision: 'MA21'
Attached Changer API: No
SerialNumber: '10WT087648'
MinBlock: 1
MaxBlock: 8388608
SCSI ID: 0
SCSI LUN: 0
Ready: yes
BufferedMode: yes
Medium Type: 0x88
Density Code: 0x5e
BlockSize: 0
DataCompEnabled: yes
DataCompCapable: yes
DataDeCompEnabled: yes
CompType: 0xff
DeCompType: 0xff
Block Position: 78585
Partition 0 Remaining Kbytes: -1
Partition 0 Size in Kbytes: -1
ActivePartition: 0
EarlyWarningSize: 0
NumPartitions: 0
MaxPartitions: 3
soul@ark:~/Projects/bakpack$ sudo mt -f /dev/nst0 rewind
soul@ark:~/Projects/bakpack$ sudo tapeinfo -f /dev/nst0
Product Type: Tape Drive
Vendor ID: 'IBM     '
Product ID: 'ULTRIUM-HH8     '
Revision: 'MA21'
Attached Changer API: No
SerialNumber: '10WT087648'
MinBlock: 1
MaxBlock: 8388608
SCSI ID: 0
SCSI LUN: 0
Ready: yes
BufferedMode: yes
Medium Type: 0x88
Density Code: 0x5e
BlockSize: 0
DataCompEnabled: yes
DataCompCapable: yes
DataDeCompEnabled: yes
CompType: 0xff
DeCompType: 0xff
BOP: yes
Block Position: 0
Partition 0 Remaining Kbytes: -1
Partition 0 Size in Kbytes: -1
ActivePartition: 0
EarlyWarningSize: 0
NumPartitions: 0
MaxPartitions: 3
soul@ark:~/Projects/bakpack$ sudo loaderinfo -f /dev/sg20
Product Type: Medium Changer
Vendor ID: 'BDT     '
Product ID: 'FlexStor II     '
Revision: '5.60'
Attached Changer: No
Bar Code Reader: Yes
EAAP: Yes
Number of Medium Transport Elements: 1
Number of Storage Elements: 23
Number of Import/Export Elements: 1
Number of Data Transfer Elements: 1
Transport Geometry Descriptor Page: Yes
Invertable: No
Device Configuration Page: Yes
Storage: Data Transfer, Import/Export, Storage
SCSI Media Changer (rev 2): Yes
Volume Tag Reader Present: Yes
Auto-Clean Enabled: No
Transfer Medium Transport: ->Data Transfer, ->Import/Export, ->Storage
Transfer Storage: ->Data Transfer, ->Import/Export, ->Storage
Transfer Import/Export: ->Data Transfer, ->Storage
Transfer Data Transfer: ->Import/Export, ->Storage
Exchange Medium Transport: None
Exchange Storage: <>Data Transfer, <>Import/Export, <>Storage
Exchange Import/Export: <>Data Transfer, <>Storage
Exchange Data Transfer: <>Import/Export, <>Storage

