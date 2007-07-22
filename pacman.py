# 
# namcap rules - pacman package interface
# Copyright (C) 2003-2007 Jason Chu <jason@archlinux.org>
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

import tarfile, os, os.path, re
pacmandb = '/var/lib/pacman/local/'

class PacPack:
	# All of the variables you can access
	def init(self):
		self.name = None
		self.version = None
		self.release = None
		self.desc = None
		self.url = None
		self.size = None 
		self.csize = None
		self.builddate = None
		self.installdate = None
		self.packager = None
		self.depends = None
		self.makedepends = None
		self.groups = None
		self.conflicts = None
		self.backup = None
		self.source = None
		self.md5sums = None
		self.install = None
		self.pkgbuild = None
		self.requiredby = None
		self.conflicts = None
		self.provides = None
		self.files = None
		self.backup = None

	def __str__(self):
		st = ""
		if self.name != None:
			st = st + "Name: " + str(self.name) + "\n"
		if self.version != None:
			st = st + "Version: " + str(self.version) + "\n"
		if self.release != None:
			st = st + "Release: " + str(self.release) + "\n"
		if self.desc != None:
			st = st + "Description: " + str(self.desc) + "\n"
		if self.url != None:
			st = st + "URL: " + str(self.url) + "\n"
		if self.size != None:
			st = st + "Size: " + str(self.size) + "\n"
		if self.csize != None:
			st = st + "Compressed Size: " + str(self.csize) + "\n"
		if self.builddate != None:
			st = st + "Build Date: " + str(self.builddate) + "\n"
		if self.installdate != None:
			st = st + "Install Date: " + str(self.installdate) + "\n"
		if self.packager != None:
			st = st + "Packager: " + str(self.packager) + "\n"
		if self.depends != None:
			st = st + "Depends: " + str(self.depends) + "\n"
		if self.groups != None:
			st = st + "Groups: " + str(self.groups) + "\n"
		if self.conflicts != None:
			st = st + "Conflicts: " + str(self.conflicts) + "\n"
		if self.backup != None:
			st = st + "Backup: " + str(self.backup) + "\n"
		if self.source != None:
			st = st + "Source: " + str(self.source) + "\n"
		if self.md5sums != None:
			st = st + "MD5sums: " + str(self.md5sums) + "\n"
		if self.install != None:
			st = st + "Install: " + str(self.install) + "\n"
		if self.pkgbuild != None:
			st = st + "Pkgbuild: " + str(self.pkgbuild) + "\n"
		if self.requiredby != None:
			st = st + "Required By: " + str(self.requiredby) + "\n"
		if self.conflicts != None:
			st = st + "Conflicts: " + str(self.conflicts) + "\n"
		if self.provides != None:
			st = st + "Provides: " + str(self.provides) + "\n"
		if self.files != None:
			st = st + "Files: " + str(self.files) + "\n"
		return st

def load(package, root=None):
	if root == None:
		root = pacmandb
	# We know it's a local package
	if package[-7:] == '.tar.gz':
		pkgtar = tarfile.open(package, "r")
		if not pkgtar:
			return None
		if not '.PKGINFO' in pkgtar.getnames():
			return None
		pkginfo = pkgtar.extractfile('.PKGINFO')
		ret = PacPack()
		ret.init()
		for i in pkginfo.readlines():
			m = re.match('pkgname = (.*)\n', i)
			if m != None:
				ret.name = m.group(1)
			m = re.match('pkgver = (.*)-(.*)\n', i)
			if m != None:
				ret.version = m.group(1)
				ret.release = m.group(2)
			m = re.match('depend = ([^<=>]*)[<=>]*[^<=>]*\n', i)
			if m != None:
				if ret.depends == None:
					ret.depends = []
				ret.depends.append(m.group(1))
			m = re.match('backup = (.*)\n', i)
			if m != None:
				if ret.backup == None:
					ret.backup = []
				ret.backup.append(m.group(1))
			m = re.match('pkgdesc = (.*)\n', i)
			if m != None:
				ret.desc = m.group(1)
			m = re.match('url = (.*)\n', i)
			if m != None:
				ret.url = m.group(1)
			m = re.match('size = (.*)\n', i)
			if m != None:
				ret.size = int(m.group(1))
			m = re.match('builddate = (.*)\n', i)
			if m != None:
				ret.builddate = m.group(1)
			m = re.match('packager = (.*)\n', i)
			if m != None:
				ret.packager = m.group(1)

		filelist = pkgtar.extractfile('.FILELIST')
		for i in filelist.readlines():
			if ret.files == None:
				ret.files = []
			ret.files.append(i[:-1])
		pkgtar.close()
		return ret

	# Ooooo, it's a PKGBUILD
	elif package[-8:] == 'PKGBUILD':
		ret = PacPack()
		ret.init()
		pkgbuild = open(package)
		lines = []
		curline = ""
		for i in pkgbuild.readlines():
			curline = curline + i
			if curline[-2:] == '\\\n':
				curline = curline[:-2]
			else:
				lines.append(curline)
				curline = ""

		ret.pkgbuild = lines
			
		for i in lines:
			m = re.match('\s*pkgname\s*=\s*(.*)\n', i)
			if m != None:
				ret.name = m.group(1).strip()
			m = re.match('\s*pkgver\s*=\s*(.*)\n', i)
			if m != None:
				ret.version = m.group(1).strip()
			m = re.match('\s*pkgrel\s*=\s*(.*)\n', i)
			if m != None:
				ret.release = m.group(1).strip()
			m = re.match('\s*pkgdesc\s*=\s*(.*)\n', i)
			if m != None:
				ret.desc = m.group(1).strip()
			m = re.match('\s*url\s*=[ ]*(.*)\n', i)
			if m != None:
				ret.url = m.group(1).strip()
			m = re.match('\s*install\s*=\s*(.*)\n', i)
			if m != None:
				ret.install = m.group(1).strip()
			m = re.match('\s*depends\s*=\s*\((.*)\)', i)
			if m != None:
				for j in m.group(1).split():
					m = re.match("'?([^<=>']*)[<=>]*[^<=>]*'?", j)
					if m != None:
						if ret.depends == None:
							ret.depends = []
						ret.depends.append(m.group(1).strip())
			m = re.match('\s*makedepends\s*=\s*\((.*)\)', i)
			if m != None:
				for j in m.group(1).split():
					m = re.match("'?([^<=>']*)[<=>]*[^<=>]*'?", j)
					if m != None:
						if ret.makedepends == None:
							ret.makedepends = []
						ret.makedepends.append(m.group(1).strip())
			m = re.match('\s*conflicts\s*=\s*\((.*)\)', i)
			if m != None:
				for j in m.group(1).split():
					m = re.match("'?([^<=>']*)[<=>]*[^<=>]*'?", j)
					if m != None:
						if ret.conflicts == None:
							ret.conflicts = []
						ret.conflicts.append(m.group(1).strip())
			m = re.match('\s*backup\s*=\s*\((.*)\)', i)
			if m != None:
				for j in m.group(1).split():
					m = re.match("'?([^']*)'?", j)
					if m != None:
						if ret.backup == None:
							ret.backup = []
						ret.backup.append(m.group(1).strip())
			m = re.match('\s*source\s*=\s*\((.*)\)', i)
			if m != None:
				for j in m.group(1).split():
					if ret.source == None:
						ret.source = []
					ret.source.append(j)
			m = re.match('\s*md5sums\s*=\s*\((.*)\)', i)
			if m != None:
				for j in m.group(1).split():
					m = re.match("'?([^']*)'?", j)
					if m != None:
						if ret.md5sums == None:
							ret.md5sums = []
						ret.md5sums.append(m.group(1).strip())
			
		pkgbuild.close()
		return ret

	# Look at that, they're being all nice by giving us a package directory
	# No searching needed
	# I can't do it like this... if you want to load from a directory, you gotta use the other function
#	elif os.path.isdir(package):
#		return loadfromdir(package)
	# Most likely an already loaded package
	else:
		searchstr = re.compile('(.*)-([^-]*)-([^-]*)')
		for i in os.listdir(root):
			n = searchstr.match(i)
			if n == None:
				continue
			if n.group(1) == package:
				# We found the package!
				return loadfromdir(os.path.join(root, i))

		# Maybe it's a provides then...
		for i in os.listdir(root):
			prov = loadfromdir(os.path.join(root, i))

			if prov != None and prov.provides != None and package in prov.provides:
				return prov

		return None

def loadfromdir(directory):
	if not os.path.isdir(directory):
		return None
	ret = PacPack()
	ret.init()
	desc = open(directory+'/desc')
	section = ''
	for j in desc.readlines():
		if j == '\n':
			section = ''
			continue
		if j == '%NAME%\n':
			section = 'name'
			continue
		if j == '%VERSION%\n':
			section = 'version'
			continue
		if j == '%DESC%\n':
			section = 'desc'
			continue
		if j == '%GROUPS%\n':
			section = 'groups'
			continue
		if j == '%URL%\n':
			section = 'url'
			continue
		if j == '%BUILDDATE%\n':
			section = 'builddate'
			continue
		if j == '%INSTALLDATE%\n':
			section = 'installdate'
			continue
		if j == '%PACKAGER%\n':
			section = 'packager'
			continue
		if j == '%SIZE%\n':
			section = 'size'
			continue
		if j == '%CSIZE%\n':
			section = 'csize'
			continue

		if section == 'name':
			ret.name = j[:-1]
		if section == 'version':
			m = re.match('(.*)-(.*)',j[:-1])
			if m != None:
				ret.version = m.group(1)
				ret.release = m.group(2)
		if section == 'desc':
			ret.desc = j[:-1]
		if section == 'groups':
			if ret.groups == None:
				ret.groups = []
			ret.groups.append(j[:-1])
		if section == 'url':
			ret.url = j[:-1]
		if section == 'builddate':
			ret.builddate = j[:-1]
		if section == 'installdate':
			ret.installdate = j[:-1]
		if section == 'packager':
			ret.packager = j[:-1]
		if section == 'size':
			ret.size = int(j[:-1])
		if section == 'csize':
			ret.csize = int(j[:-1])
	desc.close()
	depends = open(directory+'/depends')
	dependssec = 0
	conflictssec = 0
	requiredbysec = 0
	providessec = 0
	ret.depends = []
	for j in depends.readlines():
		if dependssec and j != '\n':
			m = re.match('([^<=>]*)[<=>]*[^<=>]*\n', j)
			if m != None:
				if ret.depends == None:
					ret.depends = []
				ret.depends.append(m.group(1))
		if conflictssec and j != '\n':
			m = re.match('([^<=>]*)[<=>]*[^<=>]*\n', j)
			if m != None:
				if ret.conflicts == None:
					ret.conflicts = []
				ret.conflicts.append(m.group(1))
		if requiredbysec and j != '\n':
			m = re.match('([^<=>]*)[<=>]*[^<=>]*\n', j)
			if m != None:
				if ret.requiredby == None:
					ret.requiredby = []
				ret.requiredby.append(m.group(1))
		if providessec and j != '\n':
			m = re.match('([^<=>]*)[<=>]*[^<=>]*\n', j)
			if m != None:
				if ret.provides == None:
					ret.provides = []
				ret.provides.append(m.group(1))
		if j == '\n':
			dependssec = 0
			conflictssec = 0
			requiredbysec = 0
			providessec = 0
		if j == '%DEPENDS%\n':
			dependssec = 1
			conflictssec = 0
			requiredbysec = 0
			providessec = 0
		if j == '%REQUIREDBY%\n':
			conflictssec = 0
			dependssec = 0
			requiredbysec = 1
			providessec = 0
		if j == '%CONFLICTS%\n':
			conflictssec = 1
			dependssec = 0
			requiredbysec = 0
			providessec = 0
		if j == '%PROVIDES%\n':
			conflictssec = 0
			dependssec = 0
			requiredbysec = 0
			providessec = 1
	depends.close()
	if os.path.isfile(directory+'/files'):
		files = open(directory+'/files')
		filessec = 0
		backupsec = 0
		for j in files.readlines():
			if filessec and j != '\n':
				if ret.files == None:
					ret.files = []
				ret.files.append(j[:-1])
			if backupsec and j != '\n':
				if ret.backup == None:
					ret.backup = []
				m = re.match("(.*)\t(.*)\n", j)
				if m != None:
					ret.backup.append(m.group(1))
			if j == '\n':
				filessec = 0
				backupsec = 0
			if j == '%FILES%\n':
				filessec = 1
				backupsec = 0
			if j == '%BACKUP%\n':
				filessec = 0
				backupsec = 1
		files.close()
	return ret

def getprovides(provides):
	packagelist = []

	searchstr = re.compile('(.*)-([^-]*)-([^-]*)')
	for i in os.listdir(pacmandb):
		pac = loadfromdir(os.path.join(pacmandb, i))
		if pac.provides != None and provides in pac.provides:
			packagelist.append(pac.name)

	return packagelist
