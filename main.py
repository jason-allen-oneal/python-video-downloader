from pytube import YouTube
from optparse import OptionParser

def completed(meta, filepath):
	print(f"Download of '{filepath}' completed.")

def download(url, dest):
	print(f"Trying download of '{url}'")
	try:
		yt = YouTube(url, on_complete_callback=completed)
		title = yt.title.replace(" ", "_")
		yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path=dest, filename=title+".mp4".replace("'", ''))
	except Exception as e:
		print(e)

def main():
	parser = OptionParser(usage='%prog [options]\r\nexample: python3 %prog -u 2lAe1cqCOXo -d ~/videos\r\nexample: python3 %prog -u http://youtube.com/watch?v=2lAe1cqCOXo -d ~/videos', version="%prog 0.1")
	parser.add_option('-u', '--url', action='store', dest='url', help="URL or ID of video which to download. Can be a single id or url or a comma-separated list.")
	parser.add_option('-d', '--destination', action='store', dest='destination', help="Local path to download to")
	options, args = parser.parse_args()
	print(options)
	if options.url is None:
		parser.print_help()
		exit(1)
	
	if options.destination is None:
		parser.print_help()
		exit(1)
	
	if "," in options.url:
		targets = options.url.split(",")
		for target in targets:
			if "youtube" in target:
				url = target
			else:
				url = "http://youtube.com/watch?v="+target
			download(url, options.destination)
	else:
		target = options.url.strip()
		if "youtube" in target:
			url = target
		else:
			url = "http://youtube.com/watch?v="+target
		download(url, options.destination)
	
	print("All done!")

if __name__ == "__main__":
	main()