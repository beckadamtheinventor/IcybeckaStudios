
from PIL import Image
import os

def walk(d, types=None):
	for root,dirs,files in os.walk(d):
		for f in files:
			if types is None or f.rsplit('.', maxsplit=1)[-1].lower() in types:
				yield os.path.join(root, f)

if __name__=='__main__':
	import sys
	if len(sys.argv) < 5:
		print(f"Usage {sys.argv[0]} image_in image_out width height [output_format [input_formats]]\nIf image_in is a directory, resize all images in the directory.\noutput_format is the format (such as png) to output.\ninput_formats is a list of comma-delimited file formats to input from when image_in is a directory. example: png,jpg,bmp\n")

	if len(sys.argv) > 5:
		output_format = sys.argv[5]
		if not output_format.startswith("."):
			output_format = "." + output_format
	else:
		output_format = None

	if len(sys.argv) > 6:
		image_formats = sys.argv[6].split(",")
	else:
		image_formats = ["blp","bmp","dds","eps","gif","icns","ico","im","jpeg","jpg",
						"j2k","j2p","jpx","msp","pcx","png","apng","ppm","sgi","spider",
						"tga","tiff","webp","xbm","cur","dcx","fits","fli","flc","fpx",
						"ftex","gbr","imt","iptc","naa","mcidas","mic","mpo","pcd","pixar",
						"psd","qoi","sun","wal","wmf","emf","xpm"]

	width = int(sys.argv[3])
	height = int(sys.argv[4])
	fnames = [(sys.argv[1], sys.argv[2])]
	if os.path.isdir(sys.argv[1]):
		try:
			os.makedirs(sys.argv[2])
		except IOError:
			pass
		except Exception as e:
			print(f"Failed to create directory {sys.argv[2]}\nOriginal error: {e}")
			exit(1)
		if output_format is None:
			fnames = [(f, os.path.join(sys.argv[2], os.path.basename(f))) for f in walk(sys.argv[1], image_formats)]
		else:
			fnames = [(f, os.path.join(sys.argv[2], os.path.basename(f).rsplit(".", maxsplit=1)[0]+output_format)) for f in walk(sys.argv[1], image_formats)]

	for fname, dname in fnames:
		try:
			print(f"Resizing {fname} -> {dname}")
			img = Image.open(fname)
			img = img.resize((width, height))
			img.save(dname, optimize=True)
		except FileNotFoundError:
			print(f"File {fname} not found")
		except Exception as e:
			print(f"Failed to resize image file {fname}\nOriginal error: {e}")


