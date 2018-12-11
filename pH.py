#!/usr/bin/env python3
from os import walk, path, system, popen
from random import randint, choice
from subprocess import Popen
from time import sleep
import platform

class pH:
	# Initialize the settings
	def __init__(self):
	
		# User defined settings
		
		# Pathes start with a r: r'C:\Users\Anon', or r'/home/Anon'
		# Pathes can be absolute pathes or relative Pathes (from where the python file is located)
		self.rounds_path = r'rounds'
		self.intervals_path = r'intervals'
		self.finishes_path = r'finishes'
		
		# use_* are boolean
		# must be True or False
		self.use_fullscreen = True
		self.use_intervals = True
		self.use_custom_finish = True
		
		# The number of rounds will be randomized between those two values
		# Note: You'll need at least as many round videos (and intervals if you use them) as 'self.max_rounds'
		# If you want a given number of rounds, just set min and max to same value
		self.min_rounds = 6
		self.max_rounds = 16
		
		# The extensions of the file you're looking for
		# You probably won't ever have to change this, unless you use obscure file formats
		self.extensions = ['webm', 'mkv', 'mp4', 'avi', 'mov', 'wmv', 'mpg', 'mpeg']
		
		
		# End of user defined settings
		self.playlist = "pH_playlist_0.txt"
		nb = 0
		while path.isfile(self.playlist):
			nb += 1
			self.playlist = 'pH_playlist_' + str(nb) + '.txt'
		self.log = 'pH_log_' + str(nb) + '.txt'
		self.rounds = []
		self.intervals = []
		self.finishes = []
		self.messages = []
		self.mpv_installed = False


	# Print str to screen and put it in the message list for possible output to logfile
	def info(self, str):
		print(str)
		self.messages.append(str)

	# Search folder recursively for files with correct extensions in folder 'dir'
	# Append the results to list
	def files(self, dir, list):
		for root, directories, filenames in walk(dir):
			for filename in filenames:
				if filename.split('.')[-1] in self.extensions : list.append(path.join(root, filename))


	# Test the config
	# If it returns True, pH SHOULD run without problem
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
			
		if self.use_intervals:
			self.info('"self.intervals" is set to True')
			self.info('Testing "self.intervals_path"')
			if not(path.isdir(self.intervals_path)):
				result = False
				self.info('Error')
				self.info('    "self.intervals_path" is not a valid directory')
				self.info('    current: "' + self.intervals_path + '"')
			else:
				self.info('...done')
			self.info('')
		else:
			self.info('"self.use_intervals" is set to False')
			self.info('Skipping all intervals related tests')
			
		if self.use_custom_finish:
			self.info('"self.use_custom_finish" is set to True')
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
			self.info('"self.use_custom_finish" is set to False')
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
			
			if self.use_intervals:
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
			
			if self.use_custom_finish:
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
				self.mpv_installed = True
				self.info('...done')
			else:
				self.mpv_installed = False
				#result = False
				#self.info('Error')
				self.info('    mpv could not be used from terminal')
				#self.info('    Please either install it if not done already and/or add it to your PATH')
			self.info('')
		return result


	# Generate a random playlist
	def procedural_Hero(self):
		self.info('Generating a new pH')
		nb_rounds = randint(self.min_rounds, self.max_rounds)
		self.info('Number of rounds: ' + str(nb_rounds))
		i = 0
		pl = open(self.playlist, 'a')
		while i < (nb_rounds - 1):
			round = choice(self.rounds)
			self.rounds.remove(round)
			self.info('Round ' + str(i + 1) + '   : ' + round)
			pl.write(round + '\n')
			
			if self.use_intervals:
				interval = choice(self.intervals)
				self.intervals.remove(interval)
				self.info('Interval ' + str(i + 1) + ': ' + interval)
				pl.write(interval + '\n')
			self.info('')
			i += 1
		
		round = ""
		if self.use_custom_finish: 
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


	# Play the generated playlist
	# Try to use a static binary if mpv was not found on system
	# Win binary comes from https://mpv.srsfckn.biz/
	# OSX binary comes from https://laboratory.stolendata.net/~djinn/mpv_osx/
	# Haven't found a standalone binary for linux
	def play(self):
		mpv = 'mpv'
		if not self.mpv_installed:
			myOs = platform.system()
			if myOs == 'Windows':
				mpv = 'binaries/Windows/mpv.exe'
			elif myOs == 'Darwin':
				mpv = 'binaries/OSX/mpv'
			elif myOs == 'Linux':
			
				self.info('No static binary available for Linux')
				self.info('Please install mpv through your package manager')
				self.info('or through mpv-build') 
				self.info('')
				self.info('Error detected, outputting to logfile')
				log = open(self.log, 'a')
				for n in self.messages:
					log.write(n + '\n')
				log.close()
				return()
	
		print('Starting in 5 seconds, prepare yourself!')
		sleep(5)
		if self.use_fullscreen: mpv += ' -fs'
		Popen(mpv + ' --playlist="' + self.playlist + '"', shell=True)


	# main
	def start(self):
		self.info('Start')
		self.info('')
		if self.test_conf():
			self.procedural_Hero()
			self.play()
		else:
			self.info('Error detected, outputting to logfile')
			log = open(self.log, 'a')
			for n in self.messages:
				log.write(n + '\n')
			log.close()

acid = pH()
acid.start()