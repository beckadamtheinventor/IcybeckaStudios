
from PIL import Image
import os

def walk(d, types=None):
	for root,dirs,files in os.walk(d):
		for f in files:
			if types is None or f.rsplit('.', maxsplit=1)[-1].lower() in types:
				yield os.path.join(root, f)

def reduceImageColors(img, removebits=0, cmin=0, cmax=0xff):
	px = img.load()
	for y in range(img.height):
		for x in range(img.width):
			o = []
			for c in list(px[x, y]):
				if c > 0 and c < cmin: c = cmin
				if c < 255 and c > cmax: c = cmax
				if c > 0 and c < 255: c &= 0xff * 2 ** removebits
				o.append(c)
			px[x, y] = tuple(o)
	return img

if __name__=='__main__':
	import sys
	if len(sys.argv) < 6:
		print(f"Usage: {sys.argv[0]} image_in image_out reduce_bits channel_min channel_max [output_format [input_formats]]\nReduces colors from image_in to image_out.\nIf image_in is a directory, all images within will be reduced into directory specified by image_out.\nchannel_min is the value per channel that is treated as minimum, channel_max is the value per channel that is treated as maximum.\nreduce_bits is the number of bits to chop off the value otherwise.\nreduce_bits: 0-7\nchannel_min: 0-255\nchannel_max: 0-255\noutput_format is the format (such as png) to output.\ninput_formats is a list of comma-delimited file formats to input from when image_in is a directory. example: png,jpg,bmp\n")
		exit(0)

	if len(sys.argv) > 6:
		output_format = sys.argv[6]
		if not output_format.startswith("."):
			output_format = "." + output_format
	else:
		output_format = None

	if len(sys.argv) > 7:
		image_formats = sys.argv[7].split(",")
	else:
		image_formats = ["blp","bmp","dds","eps","gif","icns","ico","im","jpeg","jpg",
						"j2k","j2p","jpx","msp","pcx","png","apng","ppm","sgi","spider",
						"tga","tiff","webp","xbm","cur","dcx","fits","fli","flc","fpx",
						"ftex","gbr","imt","iptc","naa","mcidas","mic","mpo","pcd","pixar",
						"psd","qoi","sun","wal","wmf","emf","xpm"]

	removebits = int(sys.argv[3])
	cmin = int(sys.argv[4])
	cmax = int(sys.argv[5])
	if removebits < 0 or removebits > 7:
		print("remove_bits out of range. (0-7)")
		exit(1)
	if cmin < 0 or cmin > 255:
		print("cmin out of range. (0-255)")
		exit(1)
	if cmax < 0 or cmax > 255:
		print("cmax out of range. (0-255)")
		exit(1)
	
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
			print(f"Reducing {fname} -> {dname}")
			img = Image.open(fname)
			img = reduceImageColors(img, removebits, cmin, cmax)
			if removebits >= 4 and "A" in img.channels:
				img = img.convert("")
			img.save(dname, optimize=True)
		except FileNotFoundError:
			print(f"File {fname} not found")
		except Exception as e:
			print(f"Failed to reduce image file {fname}\nOriginal error: {e}")

