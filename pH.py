#!/usr/bin/env python3
from os import walk, path, system, popen
from random import randint, choice
from subprocess import Popen
from time import sleep

class pH:
	# Initialize the settings
	def __init__(self):
		self.rounds_path = r''
		self.intervals_path = r''

		self.custom_finish = True
		self.finishes_path = r''
		
		self.min_rounds = 6
		self.max_rounds = 16
		
		self.extensions = ['webm', 'mkv', 'mp4', 'avi', 'mov', 'wmv', 'mpg', 'mpeg']
		
		self.log = "pH_log_0.txt"
		nb = 0
		while path.isfile(self.log):
			nb += 1
			self.log = 'pH_log_' + str(nb) + '.txt'
		self.playlist = 'pH_playlist_' + str(nb) + '.txt'
		system('rm ' + self.playlist)
		
		self.rounds = []
		self.intervals = []
		self.finishes = []


	# Print str both to screen and in the logfile
	def info(self, str):
		print(str)
		log = open(self.log, 'a')
		log.write(str + '\n')
		log.close()


	# Search folder recursively for files with correct extensions in folder dir
	# Append the results to list
	def files(self, dir, list):
		for root, directories, filenames in walk(dir):
			for filename in filenames:
				if filename.split('.')[-1] in self.extensions : 
					list.append(path.join(root, filename))


	# Test the config
	# If it returns True, pH CAN run
	# Else, error is described in logfile and terminal
	def test_conf(self):
		result = True
		self.info('Testing the configuration')
		self.info('Testing "self.rounds_path"')
		if not(path.isdir(self.rounds_path)):
			result = False
			self.info('Error')
			self.info('    "self.rounds_path" is not a valid directory')
			self.info('    current: "' + self.rounds_path + '"')
		else:
			self.info('...done')
		self.info('')
			
		self.info('Testing "self.intervals_path"')
		if not(path.isdir(self.intervals_path)):
			result = False
			self.info('Error')
			self.info('    "self.intervals_path" is not a valid directory')
			self.info('    current: "' + self.intervals_path + '"')
		else:
			self.info('...done')
		self.info('')
			
		if self.custom_finish:
			self.info('"self.custom_finish" is set to True')
			self.info('Testing "self.finishes_path"')
			if not(path.isdir(self.finishes_path)):
				result = False
				self.info('Error')
				self.info('    "self.finishes_path" is not a valid directory')
				self.info('    current: "' + self.finishes_path + '"')
			else:
				self.info('...done')
			self.info('')
		else:
			self.info('"self.custom_finish" is set to False')
			self.info('Skipping all finishes related tests')
			self.info('')
				
		if result:
			self.info('Trying to find round files in "' + self.rounds_path + '"')
			self.files(self.rounds_path, self.rounds)
			if len(self.rounds) < self.max_rounds:
				result = False
				self.info('Error')
				self.info('    ' + str(len(self.rounds)) + ' files found in "' + self.rounds_path + '"')
				self.info('    minimum number required, based on self.max_rounds is ' + str(self.max_rounds))
			else:
				self.info('...done')
			self.info('')
			
			
			self.info('Trying to find interval files in "' + self.intervals_path + '"')
			self.files(self.intervals_path, self.intervals)
			if len(self.intervals) < (self.max_rounds - 1):
				result = False
				self.info('Error')
				self.info('    ' + str(len(self.intervals)) + ' files found in "' + self.intervals_path + '"')
				self.info('    minimum number required, based on (self.max_rounds - 1) is ' + str(self.max_rounds - 1))
			else:
				self.info('...done')
			self.info('')
			
			if self.custom_finish:
				self.info('Trying to find finishes files in "' + self.finishes_path + '"')
				self.files(self.finishes_path, self.finishes)
				if len(self.finishes) == 0:
					result = False
					self.info('Error')
					self.info('    no file found in "' + self.finishes_path + '"')
					self.info('    minimum number required is one, more are suggested')
				else:
					self.info('...done')
				self.info('')
			
			self.info('Checking videoplayer')
			self.info('Checking if mpv can be used from terminal')
			test = popen('mpv --version').read()
			if test.startswith('mpv'):
				self.info('...done')
			else:
				result = False
				self.info('Error')
				self.info('    mpv could not be used from terminal')
			self.info('')
		return result


	# Generate a random playlist
	def procedural_Hero(self):
		self.info('Generating a new pH')
		nb_rounds = randint(self.min_rounds, self.max_rounds)
		i = 0
		pl = open(self.playlist, 'a')
		while i < (nb_rounds - 1):
			round = choice(self.rounds)
			self.rounds.remove(round)
			interval = choice(self.intervals)
			self.intervals.remove(interval)
			self.info('Round ' + str(i + 1) + '   : ' + round)
			self.info('Interval ' + str(i + 1) + ': ' + interval)
			pl.write(round + '\n')
			pl.write(interval + '\n')
			self.info('')
			i += 1
		round = ""
		if self.custom_finish:
			round = choice(self.finishes)
		else:
			round = choice(self.rounds)
		self.info('Last round: ' + round)
		pl.write(round)
		pl.close()
		self.info('')
		self.info('playlist content :')
		pl = open(self.playlist, 'r')
		for l in pl.readlines():
			self.info(l.split('\n')[0])
		pl.close()
		self.info('')
		self.info('Number of rounds : ' + str(nb_rounds))


	# play the generated playlist
	def play(self):
		print('Starting in 5 seconds, prepare yourself!')
		sleep(5)
		Popen('mpv -fs --playlist="' + self.playlist + '"')
		sleep(1)
		system('rm ' + self.playlist)


	# main
	def start(self):
		self.info('Start')
		self.info('')
		if self.test_conf():
			self.procedural_Hero()
			self.play()
		else:
			self.info('Stop')

hero = pH()
hero.start()