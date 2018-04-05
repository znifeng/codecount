#!/usr/bin/python
# -*- coding: utf-8 -*
__author__ = 'zni.feng'
import sys
import os
reload (sys)
sys.setdefaultencoding('utf-8')

#DEFAULT_EXTENSIONS = ["java", "c", "cc", "cpp", "h", "hh", "hpp", "py", "glsl", "rb", "js", "sql"]
DEFAULT_EXTENSIONS = ["java"]
BASE_DIR_abs = os.getcwd()
BASE_DIR = os.path.split(BASE_DIR_abs)[1]

class Lines:
	total=0
	comment=0
	blank=0

class CodeCount:
	def __init__(self,base_dir):
		self.files={}
		self.base_dir = base_dir

	def is_valid_extension(self, extension):
		return extension in DEFAULT_EXTENSIONS
	
	def fetch_extension(self, filename):
		return os.path.splitext(filename)[1][1:]

	def is_dir(self, filename):
		return os.path.isdir(filename)

	def is_file(self, filename):
		return os.path.isfile(filename)

	def is_valid_file(self, filename):
		if not self.is_file(filename):
			return False
		extension = self.fetch_extension(filename)
		if self.is_valid_extension(extension):
			return True

		return False

	def fetch_files(self, base_dir):
		if base_dir ==self.base_dir:
			return os.listdir('.')
		else:
			return os.listdir(base_dir)

	def count_file_lines(self, filename):
		if not self.is_valid_file(filename):
			return None
		f = open(filename,'r')
		lines = Lines()
		iscomment = False
		##空白行：不统计； 注释行：统计
		for line in f.readlines():
			line = line.strip()
			lines.total += 1
			if not len(line) and not iscomment:
				lines.blank += 1
				continue
			
			if line.startswith('//') and not iscomment:
				lines.comment += 1
				continue
			if line.startswith('/*') and line.endswith('*/'):
				lines.comment += 1
				continue
			if line.startswith('/*') and not line.endswith('*/') and not iscomment:
				lines.comment += 1
				iscomment = True
				continue
			if line.endswith('*/') and iscomment:
				lines.comment += 1 
				iscomment = False
				continue

			if iscomment:
				lines.comment += 1

		return lines

	#给定当前根目录base_dir，统计该目录下所有有效文件的代码行数
	def modify_file_info(self, base_dir, files):
		file_list = self.fetch_files(base_dir)
		prefix = "." if base_dir == self.base_dir else base_dir
		for i in file_list:
			if self.is_valid_file(prefix+'/'+i):
				files[prefix+'/'+i] = self.count_file_lines(prefix+'/'+i)

			if self.is_dir(prefix+'/'+i):
				self.modify_file_info(prefix+'/'+i, self.files)

	def get_files_dict(self):
		if not self.files:
			self.modify_file_info(self.base_dir, self.files)

		return self.files

	def output2txt(self, output_file='CodeLinesbyFile.txt'):
		files = self.get_files_dict()
		title = 'FileName : TotalLines : CommentLines'
		total_lines = 0
		total_files = 0
		total_comments = 0
		lines_list=[]
		output=[]

		for key in files:
			total_lines += files[key].total
			total_files += 1
			total_comments += files[key].comment
			#去掉'.Java'后缀和前面的'./',key的形式为./path/file.java 
			classname = key[2:].split('.')[0]
			#用'.'连接
			classname ='.'.join(classname.split('/'))
			if classname.find('src.main.java.') < 0:
				continue
			classname = classname.split('src.main.java.')[1]

			lines_list.append(classname + " : " + str(files[key].total) + " : " + str(files[key].comment))
		lines_list.sort()
		
		ending = '\nTotal Files: ' + str(total_files) + '       Total Lines: ' + str(total_lines) + '       Total Comments: ' + str(total_comments)

		output.append(title)
		output.extend(lines_list)
		output.append(ending)

		open(output_file, 'w').write('%s' % '\n'.join(output))

def main():
	codecount = CodeCount(BASE_DIR)
	codecount.output2txt()

if __name__ == "__main__":
	main()
