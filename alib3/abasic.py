# -*- coding: utf-8 -*-
# <-- AZLIBRARY PROJECT (Python2, 3) -->
# Started: 2018.02.02
# Latest: 2018.09.13
import os

def timeNow():
	import datetime
	now = datetime.datetime.now()
	return {'YY': now.strftime('%Y'),
			'MM': now.strftime('%m'),
			'DD': now.strftime('%d'),
			'hh': now.strftime('%H'),
			'mm': now.strftime('%M'),
			'ss': now.strftime('%S')}

class Log:

	DEBUG = 0
	INFO = 1
	WARNING = 2
	ERROR = 3

	def __init__(self, level, logfile=None):
		self.level = level
		self.logfile = logfile
	
	def debug(self, content):
		t = timeNow()
		ts = '%s/%s/%s-%s:%s:%s' % (t['YY'], t['MM'],t['DD'],t['hh'],t['mm'],t['ss'])
		ls = '%s <%s> %s' % (ts, 'DEBUG', content)
		if self.level == 0:
			print(ls)
		if self.logfile:
			os.system('echo \"%s\" >> \"%s\"' % (ls, self.logfile))

	def info(self, content):
		t = timeNow()
		ts = '%s/%s/%s-%s:%s:%s' % (t['YY'], t['MM'],t['DD'],t['hh'],t['mm'],t['ss'])
		ls = '%s <%s> %s' % (ts, 'INFO', content)
		if self.level <= 1:
			print(ls)
		if self.logfile:
			os.system('echo \"%s\" >> \"%s\"' % (ls, self.logfile))

	def warning(self, content):
		t = timeNow()
		ts = '%s/%s/%s-%s:%s:%s' % (t['YY'], t['MM'],t['DD'],t['hh'],t['mm'],t['ss'])
		ls = '%s <%s> %s' % (ts, 'WARNING', content)
		if self.level <= 2:
			print(ls)
		if self.logfile:
			os.system('echo \"%s\" >> \"%s\"' % (ls, self.logfile))

	def error(self, content):
		t = timeNow()
		ts = '%s/%s/%s-%s:%s:%s' % (t['YY'], t['MM'],t['DD'],t['hh'],t['mm'],t['ss'])
		ls = '%s <%s> %s' % (ts, 'ERROR', content)
		if self.level <= 3:
			print(ls)
		if self.logfile:
			os.system('echo \"%s\" >> \"%s\"' % (ls, self.logfile))
	
	def msg(self, content, attr):
		t = timeNow()
		ts = '%s/%s/%s-%s:%s:%s' % (t['YY'], t['MM'],t['DD'],t['hh'],t['mm'],t['ss'])
		ls = '%s <%s> %s' % (ts, attr, content)
		if self.level <= 3:
			print(ls)
		if self.logfile:
			os.system('echo \"%s\" >> \"%s\"' % (ls, self.logfile))
	
