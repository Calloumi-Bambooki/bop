import unittest

from bop.run import *
from bop import __version__

from tests import game_recorder, mock_random

import json
import time


class MyTestCase(unittest.TestCase):
	def setUp(self):
		self.game = Game([width, height], drag, size, speed, not hosting, randomAPI=mock_random)
		self.host = Host(self.game)
		self.director = Director(ip, self.game)

	def test_1(self):
		assert __version__ == '0.1.2'

		with open('test1.json') as json_file:
			recorded = json.load(json_file)

		self.user_playback = game_recorder.UserPlayback(recorded["input"])
		self.director.newUser(self.user_playback)

		time.sleep(1)

		print("Beginning test 1")
		print("Using record:")
		print(recorded)

		encoder = game_recorder.Recorder.Encoder()

		for output in recorded["output"]:
			self.user_playback.next()
			self.game.loop()
			self.host.sync()
			self.director.loop()

			self.assertEqual(output, encoder.encode(self.game.data))


if __name__ == '__main__':
	unittest.main()