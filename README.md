# proceduralHero

## Introduction

This script will generate a random playlist of files to be played with mpv, before starting that playlist in mpv.
The name is a pun: procedural from procedurally generated games, Hero from Guitar Heroes and the like, the initials giving us the chemistry scale for acids.

Note: We got ourselves a great name, still recruiting for the logo.

## Prerequisites

- Python: Duh.
- mpv : Windows and OSX binaries are packaged in the release, but linux users HAVE to install it.
I still recommend to install mpv even on Windows and OSX. Because it's good.

## Installing

1.download pH.py or extract the release archive.
2. edit pH.py to set it up properly:
```
	self.rounds_path = r'rounds'
	self.intervals_path = r'intervals'
	self.finishes_path = r'finishes'
	self.use_intervals = True
	self.use_custom_finish = True
	self.min_rounds = 6
	self.max_rounds = 16
```
   - self.rounds_path: path to the files to be played (folder is searched recursively, so all subfolders will be looked in too).
   - self.intervals_path: path to files to be played in between rounds (still recursive).
   - self.finishes_path: path to files to be played as last round.
   - self.use_intervals: If you set this to False, all interval related things will be skipped (tl;dr: you won't play intervals).
   - self.use_custom_finish: If this is true, pH.py will use one file from the finishes_path to play last round. Else, it'll be from the rounds_path.
   - self.min_rounds: The minimum number of rounds you want (6 means 6 rounds + 5 intervals, if you want them).
   - self.max_rounds: The maximum number of rounds. In case you didn't understand. Because the number will be random in between those two.
3. You may edit if you want/need the self.extensions. But I doubt you'll need to do it, unless you want to use pH to play music.
4. You are now a procedural Hero. Act like one.

## How to use

Well. Just run it. With Python, you know.

## License

This code is licensed under [the Unlicense](https://github.com/gary-stu/FL/blob/master/LICENSE).