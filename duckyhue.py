
from phue import Bridge
from pynput import keyboard
import sys, getopt, os
import zc.lockfile
from appdirs import *

class DuckyHue:
	def __init__(self):
		### SET LOCKFILE ###
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

		b = Bridge('192.168.68.112')
		b.connect()
		# b.get_api()
		self.bridge = b
		self.lights = b.get_light_objects('id')
		self.brightness = b.get_light(2, 'bri')
		self.colortemp = self.lights[2].colortemp
		self.listener = keyboard.Listener(on_press=self.on_press)
    		# on_release=on_release)
		self.listener.start()
		self.listener.join()

	def on_press(self,key):
		if key == keyboard.Key.esc:
			self.lock.close()
			return False # Stop the listener
		try:
			k = key.char # Single-char keys
		except:
			k = key.name # Other keys
		
		if k in ['f13']:
			self.bridge.set_light(2, 'on', True)
		if k in ['f14']:
			self.bridge.set_light(2, 'on', False)
		if k in ['f15']:
			self.brightness += 5
			if self.brightness >= 254:
				self.brightness = 254
			self.bridge.set_light(2, 'bri', self.brightness)
			print("Brghtness set to: {}".format(self.bridge.get_light(2, 'bri')))
		
		if k in ['f16']:
			self.brightness -= 5
			if self.brightness <= 1:
				self.brightness = 1
			self.bridge.set_light(2, 'bri', self.brightness)
			print("Brghtness set to: {}".format(self.bridge.get_light(2, 'bri')))

		if k in ['f22']:
			self.colortemp += 5
			self.lights[2].colortemp = self.colortemp
			print("colormode: {}\ncolortemp: {} ({}K)".format(self.lights[2].colormode, self.lights[2].colortemp, self.lights[2].colortemp_k))
		if k in ['f23']:
			self.colortemp -= 5
			self.lights[2].colortemp = self.colortemp
			print("colormode: {}\ncolortemp: {} ({}K)".format(self.lights[2].colormode, self.lights[2].colortemp, self.lights[2].colortemp_k))

		print('Key pressed: ' + k)

def main(argv):
	try:
		opts, args = getopt.getopt(argv, "tTDsv", ["test"])
	except getopt.GetoptError:
		print('duckyhue -t')
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-t':
			print('Setting lights ON')
			b = Bridge('192.168.68.112')
			b.connect()
			b.get_api()

			b.set_light(2, 'on', True)

		if opt == '-T':
			print('Setting lights OFF')
			b = Bridge('192.168.68.112')
			b.connect()
			b.get_api()

			b.set_light(2, 'on', False)
		if opt == '-D':
			d = DuckyHue()
		if opt == '-s':
			b = Bridge('192.168.68.112')
			b.connect()
			b.get_api()
			print("Something: \nbrightness: {}".format(b.get_light(2, 'bri')))
			lights = b.get_light_objects('id')
			print("Something else: {}".format(lights))
			print("colormode: {}\ncolortemp: {} ({}K)".format(lights[2].colormode, lights[2].colortemp, lights[2].colortemp_k))

if __name__ == "__main__":
	main(sys.argv[1:])
