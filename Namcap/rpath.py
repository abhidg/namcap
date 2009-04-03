# 
# namcap rules - rpath
# Copyright (C) 2009 Abhishek Dasgupta <abhidg@gmail.com>
# 
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# 

import pacman, os, subprocess, re

process = lambda s: re.search("/tmp/namcap\.[0-9]*/(.*)", s).group(1)

def checkrpath(insecure_rpaths, dirname, names):
	"Checks if secure RPATH."

	allowed = ['/usr/lib']
	warn = ['/usr/local/lib']
	
	for i in names:
		if os.path.isfile(dirname+'/'+i):
			var = subprocess.Popen('readelf -d ' + dirname+'/'+i,
					shell=True,
					stdout=subprocess.PIPE,
					stderr=subprocess.PIPE).communicate()
			for j in var[0].split('\n'):
				n = re.search('Library rpath: \[(.*)\]', j)
				# Is this a Library rpath: line?
				if n != None:
					if ":" in n.group(1):
						rpaths=n.group(1).split(':')
					else:
						rpaths=[n.group(1)]
					for path in rpaths:
						if path not in allowed:
							insecure_rpaths[0].append(process(dirname+'/'+i))
							break
						if path in warn and process(dirname + "/" + i) not in insecure_rpaths:
							insecure_rpaths[1].append(process(dirname+'/'+i))
					
class package:
	def short_name(self):
		return "rpath"
	def long_name(self):
		return "Verifies correct and secure RPATH for files."
	def prereq(self):
		return "extract"
	def analyze(self, pkginfo, data):
		ret = [[],[],[]]
		insecure_rpaths = [[],[]]
		os.path.walk(data, checkrpath, insecure_rpaths)

		if len(insecure_rpaths) > 0:
			for j in (0,1):
				for f in insecure_rpaths[j]:
					ret[j].append(("insecure-rpath %s", f))
		return ret
	def type(self):
		return "tarball"
# vim: set ts=4 sw=4 noet:
