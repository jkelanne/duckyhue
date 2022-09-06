
from phue import Bridge
from pynput import keyboard
import sys, getopt, os, time
import zc.lockfile
from appdirs import *

class DuckyHue:
	def __init__(self):
		# Set lockfile so that we don't run multiple instances of the script
		appname = "DuckyHue"
		author = "null_ptr"
		lockpath = user_data_dir(appname, author)

		if not os.path.exists(lockpath):
			os.makedirs(lockpath)

		try:
			self.lock = zc.lockfile.LockFile(lockpath + '\\duckyhue.lock')
		except zc.lockfile.LockError:
			print("PROCESS IS ALREADY RUNNING!");
			sys.exit(2)

		# Initialize variables and settings
		b = Bridge('192.168.68.112')
		b.connect()
		# b.get_api()
		self.bridge = b
		self.lights = b.get_light_objects('id')
		self.brightness = b.get_light(2, 'bri')
		self.colortemp = self.lights[2].colortemp
		self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
		self.keyboard_modifiers = {'ctrl_l': False, 'shift': False, 'alt_l': False }


	def run(self):
		self.listener.start()
		self.listener.join()


	def on_release(self, key):
		try:
			k = key.char # Single-char keys
		except:
			k = key.name # Other keys

		if k in self.keyboard_modifiers.keys():
			self.keyboard_modifiers[k] = False

	def on_press(self,key):
		if key == keyboard.Key.esc:
			self.lock.close()
			return False # Stop the listener
		try:
			k = key.char # Single-char keys
		except:
			k = key.name # Other keys
		
		if k in self.keyboard_modifiers.keys():
			self.keyboard_modifiers[k] = True

		if k in ['f13']:
			self.bridge.set_light(2, 'on', not self.bridge.get_light(2, 'on'))
		if k in ['f14']:
			self.bridge.set_light(3, 'on', not self.bridge.get_light(3, 'on'))
			
		if k in ['f15']:
			self.brightness += 5
			if self.brightness >= 254:
				self.brightness = 254
			self.bridge.set_light([2,3], 'bri', self.brightness)
		
		if k in ['f16']:
			self.brightness -= 5
			if self.brightness <= 1:
				self.brightness = 1
			self.bridge.set_light([2,3], 'bri', self.brightness)

		if k in ['f22']:
			self.colortemp += 5
			self.bridge.set_light([2,3], 'ct', self.colortemp)
		if k in ['f23']:
			self.colortemp -= 5
			self.bridge.set_light([2,3], 'ct', self.colortemp)
		if k in ['f17'] and self.keyboard_modifiers['alt_l']:
			self.bridge.set_light(4, 'on', not self.bridge.get_light(4, 'on'))

		# Cosy warm
		if k in ['f20']:
			self.bridge.set_light([2,3], 'ct', 350)
			time.sleep(0.4)
			self.bridge.set_light([2,3], 'bri', 164)
			
		# Cold
		if k in ['f21']:
			self.bridge.set_light([2,3], 'ct', 250)
			time.sleep(0.4)
			self.bridge.set_light([2,3], 'bri', 254)

def main(argv):
	try:
		opts, args = getopt.getopt(argv, "D")
	except getopt.GetoptError:
		print('duckyhue -D')
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-D':
			d = DuckyHue()
			d.run()

if __name__ == "__main__":
	main(sys.argv[1:])
