from pytube import YouTube
from optparse import OptionParser

class Download:
	def __init__(self, url, dest):
		self.url = url
		self.destination = dest
		try:
			self.yt = YouTube(url, on_progress_callback=self.progress, on_complete_callback=self.completed)
		except:
			print('Connection error')
			exit()
		
		self.process()
	
	def process(self):
		if self.yt.age_restricted:
			print("This video cannot be downloaded with this application as it is age-restricted.");
			exit()
		else:
			try:
				self.title = self.yt.title.replace(" ", "_").replace("'", '')
				self.vid = self.yt.streams.first()
				
				self.download()
			except Exception as e:
				print(e)
	
	def completed(self, meta, filepath):
		print(f"Download of '{filepath}' completed.")
	
	def progress(self, stream, chunk, bytes_remaining):
		progress = (abs(bytes_remaining-self.vid.filesize)/self.vid.filesize)*100
		print(progress,"% complete")
	
	def download(self):
		try:
			self.vid.download(output_path=self.destination)
		except Exception as e:
			print(e)

def parse(target):
	if "youtube" in target:
		url = target
	else:
		if "youtu.be" in target:
			url = target
		else:
			url = "http://youtube.com/watch?v="+target
	return url

def main():
	parser = OptionParser(usage='%prog [options]\r\nexample: python3 %prog -u 2lAe1cqCOXo -d ~/videos\r\nexample: python3 %prog -u http://youtube.com/watch?v=2lAe1cqCOXo -d ~/videos', version="%prog 0.1")
	parser.add_option('-u', '--url', action='store', dest='url', help="URL or ID of video which to download. Can be a single id or url or a comma-separated list.")
	parser.add_option('-d', '--destination', action='store', dest='destination', help="Local path to download to")
	options, args = parser.parse_args()
	
	if options.url is None:
		parser.print_help()
		exit(1)
	
	if options.destination is None:
		parser.print_help()
		exit(1)
	
	if "," in options.url:
		targets = options.url.split(",")
		for target in targets:
			target = target.strip()
			Download(parse(target), options.destination)
	else:
		target = options.url.strip()
		Download(parse(target), options.destination)
	
if __name__ == "__main__":
	main()