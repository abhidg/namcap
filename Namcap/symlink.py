# 
# namcap rules - symlink
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
import tarfile, re

class package:
	def short_name(self):
		return "symlink"
	def long_name(self):
		return "Checks that symlinks point to the right place"
	def prereq(self):
		return "tar"
	def analyze(self, pkginfo, tar):
		ret = [[],[],[]]
		for i in tar:
			if i.issym() or i.islnk():
				ret[2].append("Symlink (" + i.name + ") found that points to " + i.linkname)
				if re.search("pkg/", i.linkname):
					ret[0].append("Symlink (" + i.name + ") points to " + i.linkname)
		return ret	
	def type(self):
		return "tarball"
