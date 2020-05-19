class ChromeRequest(object):
	""" Parses the text of "Request Headers" section from Chrome network inspector,
		Will contain a dictionary of headers and a dictionary of cookies if found.
	"""

	ignore_headers = [
	'accept',
	'accept-encoding',
	'accept-language',
	]

	@classmethod
	def from_file(cls, ifile, **kwargs):
		"""
		Helper Constructor: takes a file name or file object,
		Reads each line and instantiates class with default constructor, 
		passing lines list as argument.
		"""
		instance = None
		hlines = None
		try:
			if isinstance(ifile, str):
				with open(ifile, 'r') as fh:
					hlines = fh.readlines()
			else:
				hlines = ifile.readlines()
		except Exception as e:
			print(e)
		if hlines != None:
			instance = cls(hlines, **kwargs)
		return instance


	def __init__(self, lines, **kwargs):
		if not hasattr(lines, '__iter__'):
			raise ValueError("Argument 'lines' must be iterable containing strings")

		ignore_headers = self.ignore_headers
		if "ignore_headers" in kwargs:
			ignore_headers = kwargs["ignore_headers"]

		(headers, sheaders, iheaders) = self.get_headers(lines, ignore_headers)

		if 'cookie' in headers:
			self.cookies = self.get_cookies(headers['cookie'])
			del headers['cookie']

		self.headers = headers
		self.special_headers = sheaders
		self.ignored_headers = iheaders
		
		url = self.gen_url()
		if url != None:
			self.url = url

		if "user-agent" in headers:
			self.user_agent = headers["user-agent"]

	def gen_url(self):
		required_keys = ['authority', 'path', 'scheme']
		if not all(key in self.special_headers for key in required_keys):
			return None
		hs = {key: self.special_headers[key] for key in required_keys}
		url = '{scheme}://{authority}{path}'.format(**hs) 
		return url


	@staticmethod
	def get_cookies(cstr):
		cookies = {}
		for cpair in cstr.split(';'):
			kv = cpair.split('=',1)
			if len(kv) == 2:
				(k,v) = kv
				cookies[k.strip()]=v
		return cookies


	@staticmethod
	def get_headers(lines, ignore_headers={}):
		headers = {}
		ignored_h ={}
		special_h = {}
		for line in lines:
			isspecial = False
			if line[0] == ':':
				isspecial = True
				spi = line[1:].find(':')+1
			else:
				spi = line.find(':')
			if spi != -1:
				k = line[0:spi]
				v = strip_newline(line[spi+1:])
				if isspecial:
					k = line[1:spi]
					special_h[k] = v
				elif k in ignore_headers:
					ignored_h[k] = v
				else:	
					headers[k] = v
		return (headers, special_h, ignored_h)



def strip_newline(string):
	sL = len(string)
	s1i = string.rfind('\n')
	s2i = string.rfind('\r\n')

	if s1i != -1 and s1i == sL-1:
		return string[:-1]
	elif s2i != -1 and s2i == sL-2:
		return string[:-2]
	else:
		return string