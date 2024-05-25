You know that time you wanted to move from one ext4 or ntfs filesystem to another ext4, and you wanted to retain the birth or creation date, but you just couldn't figure out how? Wondered if it was even possible? It is!

You can find the info by invoking stat command

`~$ stat filename`


This script as of today still remains untested, I will test it soon.

**WIP:**
[✔] Create the project and lay down groundworks.
[✘] Add command-line argv input
[✘] Verify script functionality
[✘] Add ext4 to ntfs (migrating birth info to ntfs creation date) - _(currently only works ext4 to ext4 or ntfs to ext4)
[✘] Potentially add other filesystems and expand program _(and accordingly change repo name)_

Original idea, thought and thanks [goes to Artem](https://unix.stackexchange.com/a/591388).

----

## How to run?

sudo python3 crtime.py
