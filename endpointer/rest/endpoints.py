
import json
import string
import random

from pprint import pprint

from faker import Faker


class Responser:

	def __init__(self):
		self.faker = Faker()

	def parse_template(self, json_string):
		self.response = json.loads(json_string)


	def fields(self):
		self.fields = [fname for _, fname, _, _ in string.Formatter().parse(template) if fname]

	def gen(self, d=None, depth=1):

		if depth > 10:
			return {}

		if not d:
			d = self.response

		res = {}
		for k,v in d.items():
			if isinstance(v, dict):
				t = self.gen(v, depth+1)
			elif isinstance(v, list):
				t = self.fake_list(v, depth+1)
			else:
				t = self.parse_value(v)
			res[k] = t
		return res

	def fake_list(self, value, depth):

		if depth > 10:
			return []

		results = []

		value = value[0]
		count = random.randrange(20)

		if value[0] != "&":
			return [self.faker.word() for x in range(random.randrange(10))]
		else:	
			value = value[1:]

		if ":" in value:
			value, count = value.split(":")
			if "~" in count:
				count = random.randrange(int(count[1:]))

		count = int(count)

		r = Responser.from_file(value)

		if count == 0:
			return dict(r.gen(None, depth))
		else:
			for x in range(int(count)):
				results.append(r.gen(None, depth))
			return results


	def parse_value(self, value):

		if value[0] == "!":

			att = getattr(self.faker, value[1:], None)

			if att:
				return att()
			else:
				return self.faker.text()
		else:
			return value

	@classmethod
	def from_file(cls, file, vars=[]):
		try:
			json_template = open(f"rest/templates/{file}", "r").read()

			json_template = __class__.replace_vars(json_template, vars)
			

			r = Responser()
			r.parse_template(json_template)
			
		except FileNotFoundError as e:
			raise ValueError(f"No template created for model: {file}")
		except json.decoder.JSONDecodeError as e:
			raise ValueError(f"Problem with template's {file} syntax: {str(e)}")
		except Exception as e:
			raise ValueError(str(e))
		
		return r

	@classmethod	
	def replace_vars(cls, json_template, vars):
		for var in vars:
			json_template = json_template.replace(f"%{var}%", vars.get(var))
		return json_template








