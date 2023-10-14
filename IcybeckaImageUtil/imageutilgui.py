
import os, sys, time, tempfile, threading, hashlib

try:
	from PIL import Image
except ImportError:
	print("Missing dependency PIL. Please install package pillow with pip.\nPress enter to exit.")
	input()

try:
	import PySimpleGUI as sg
except ImportError:
	print("Missing dependency PIL. Please install package pillow with pip.\nPress enter to exit.")
	input()

MAX_THREADS = 10
TEMP_DIR = os.path.join(tempfile.gettempdir(), "icybecka.imageutilgui")
IMAGE_FORMATS = tuple([("All Files", "* *.*")]+[(s.upper()+" Images", "*"+s) for s in [
				"apng","blp","bmp","cur","dcx","dds","emf","fits","fli","flc","fpx",
				"ftex","eps","gbr","gif","icns","ico","im","imt","iptc","jpeg",
				"jpg","j2k","j2p","jpx","mcidas","mic","mpo","msp","naa","pcd",
				"pcx","pixar","png","ppm","psd","qoi","sgi","spider","sun","tga",
				"tiff","wal","webp","wmf","xbm","xpm"]])

def InfoWindow(text, title="Info"):
	return sg.Window(title, [[sg.Text(text)],[sg.Ok()]], modal=True).read(close=True)

def ErrorWindow(text, title="Error"):
	return InfoWindow(text, title)

def FileNotFoundWindow(fname, title="File Not Found"):
	return InfoWindow(f"File \"{fname}\" not found", title)

def ConversionDialogWindow(md):
	finished = False
	taskqueue = []
	queuedtasks = 0
	layout = [
		[sg.Multiline(size=(60,40), autoscroll=True, auto_refresh=True, write_only=True, k="progresstext")],
		[sg.Button("Cancel", k="Cancel")],
	]
	window = sg.Window("Converting Images", layout)
	while True:
		event, values = window.read(50)
		if event in (sg.WIN_CLOSED, "Cancel", "Done"):
			break

		# remove finished threads from the queue
		i = 0
		while i < len(taskqueue):
			if not taskqueue[i].is_alive():
				taskqueue.pop(i)
			else:
				i += 1

		if queuedtasks < len(md["images"]):
			fname = md["images"][queuedtasks]
			dname = os.path.join(md["outputdir"], os.path.basename(fname).rsplit(".", maxsplit=1)[0]+"."+md["outformat"])
			if len(taskqueue) < MAX_THREADS:
				window["progresstext"].print(f"Converting {fname} -> {dname}")
				th = threading.Thread(target=ConversionTaskThread, args=(fname, dname, md))
				taskqueue.append(th)
				th.start()
				queuedtasks += 1
		elif not len(taskqueue):
			if not finished:
				finished = True
				window["progresstext"].print("Finished.")
				window["Cancel"].update("Done")
	try:
		window.close()
	except:
		pass


def ReduceImageChannelDepth(img, bits):
	if bits < 8:
		removebits = 8-bits
		px = img.load()
		for y in range(img.height):
			for x in range(img.width):
				px[x, y] = tuple([(c&(0xff*2**removebits)) for c in list(px[x, y])])
	return img

def ConversionTaskThread(fname, dname, md):
	try:
		img = Image.open(fname)
	except FileNotFoundError:
		# FileNotFoundWindow(fname)
		return False
	except Exception as e:
		# ErrorWindow(str(e))
		return False

	try:
		if len(md["width"]) and len(md["height"]):
			img = img.resize((int(md["width"]), int(md["height"])))
	except Exception as e:
		# ErrorWindow(str(e))
		return False

	try:
		if len(md["outdepth"]):
			img = ReduceImageChannelDepth(img, int(md["outdepth"]))
	except Exception as e:
		# ErrorWindow(str(e))
		return False

	try:
		if len(md["outchannels"]):
			if md["outchannels"] == "P":
				if len(md["outputcolors"]):
					img = img.convert("RGB").quantize(int(md["outputcolors"]), Image.Quantize.MEDIANCUT)
				else:
					img = img.quantize(256, Image.Quantize.MEDIANCUT)
			else:
				img = img.convert(md["outchannels"])
	except Exception as e:
		# ErrorWindow(str(e))
		return False

	try:
		try:
			img.save(dname)
		except:
			img.convert("RGB").save(dname)
	except Exception as e:
		# ErrorWindow(str(e))
		return False
	return True

def ReductionWindow():
	try:
		os.makedirs(TEMP_DIR)
	except:
		pass
	for i in range(6):
		try:
			os.remove(os.path.join(TEMP_DIR, f"preview{i+1}.png"))
		except:
			pass
	md = {"outdepth":"", "outformat":"", "outchannels":"", "width":"", "height":"", "outputdir":""}
	default_image_scale = (128, 128)
	layout = [
		[sg.Text("Source Images"), sg.InputText(), sg.FilesBrowse(k="images", file_types=IMAGE_FORMATS)],
		[sg.Image(k="preview1"),
			sg.Image(k="preview2"),
			sg.Image(k="preview3"),
			sg.Image(k="preview4"),
			sg.Image(k="preview5"),
			sg.Image(k="preview6"),],
		[sg.Text("Output Width"), sg.InputText(k="width"), sg.Text("Height"), sg.InputText(k="height")],
		[sg.Text("Output Format"), sg.InputText(k="outformat")],
		[sg.Text("Output Channels"), sg.Radio("RGBA", "outchannels", k="outchannelsRGBA", default=True),
			sg.Radio("RGB", "outchannels", k="outchannelsRGB"),
			sg.Radio("Palettized", "outchannels", k="outchannelsP"),
			sg.Radio("Grayscale", "outchannels", k="outchannelsL")],
		[sg.Text("Reduce Channel Bit Depth to"), sg.Radio("8", "outdepth", k="outdepth8", default=True), sg.Radio("7", "outdepth", k="outdepth7"),
			sg.Radio("6", "outdepth", k="outdepth6"), sg.Radio("5", "outdepth", k="outdepth5"), sg.Radio("4", "outdepth", k="outdepth4"),
			sg.Radio("3", "outdepth", k="outdepth3"), sg.Radio("2", "outdepth", k="outdepth2"), sg.Radio("1", "outdepth", k="outdepth1")],
		[sg.Text("Output Image Colors (palettized)"), sg.InputText(k="outputcolors")],
		[sg.Text("Output Folder"), sg.InputText(), sg.FolderBrowse(k="outputdir")],
		[sg.Button("Convert"), sg.Button("Quit")],
	]
	window = sg.Window("Icybecka ImageUtil GUI", layout)
	while True:
		event, values = window.read(50)
		if event in (sg.WIN_CLOSED, "Quit"):
			break

		for k in values.keys():
			if type(k) is str:
				if k.startswith("outdepth"):
					if values[k]:
						md["outdepth"] = k[8:]
				elif k.startswith("outchannels"):
					if values[k]:
						md["outchannels"] = k[11:]
				else:
					md[k] = values[k]
			else:
				md[k] = values[k]

		if not len(md["images"]):
			continue
		md["images"] = md["images"].split(";")

		if event == "Convert":
			ConversionDialogWindow(md)
		else:
			thl = []
			d = md.copy()
			d["width"], d["height"] = (str(a) for a in default_image_scale)
			for i in range(min(6, len(md["images"]))):
				th = threading.Thread(target=ConversionTaskThread, args=(md["images"][i], os.path.join(TEMP_DIR, f"preview{i+1}.png"), d))
				thl.append(th)
				th.start()

			for th in thl:
				th.join()

			for i in range(min(6, len(md["images"]))):
				window[f"preview{i+1}"].update(filename=os.path.join(TEMP_DIR, f"preview{i+1}.png"))

	try:
		window.close()
	except:
		pass

if __name__=='__main__':
	ReductionWindow()
