import random

class ThermohigrometerSim:
	def __init__(self, temperature=25.0, humidity=50.0):
		self.temperature = temperature
		self.humidity = humidity

	def read_temperature(self):
		return self.temperature

	def read_humidity(self):
		return self.humidity

	def simulate_changes(self):
		self.temperature = self.random_walk(self.temperature, 0.5, -30.0, 50.0)
		self.humidity = self.random_walk(self.humidity, 1.0, 0.0, 100.0)

	@staticmethod
	def random_walk(value, step, min_v = 0.0, max_v = 100.0):
		value += random.uniform(-step, step)
		value = max(min_v, min(max_v, value))
		return value
