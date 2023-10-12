
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <raylib.h>

#define min(a,b) ((a)<(b):(a):(b))
#define max(a,b) ((a)>(b):(a):(b))

uint32_t reduceColors(uint32_t color, uint8_t removebits, uint8_t cmin, uint8_t cmax) {
	uint8_t r = (color >>  0) & 0xff;
	uint8_t g = (color >>  8) & 0xff;
	uint8_t b = (color >> 16) & 0xff;
	uint8_t a = (color >> 24) & 0xff;
	if (r < cmin) r = 0;
	if (g < cmin) g = 0;
	if (b < cmin) b = 0;
	if (a < cmin) a = 0;
	if (r > cmax) r = 0xff;
	if (g > cmax) g = 0xff;
	if (b > cmax) b = 0xff;
	if (a > cmax) a = 0xff;
	if (r > 0 && r < 0xff) r &= 0xff << removebits;
	if (g > 0 && g < 0xff) g &= 0xff << removebits;
	if (b > 0 && b < 0xff) b &= 0xff << removebits;
	if (a > 0 && a < 0xff) a &= 0xff << removebits;
	return r | (g << 8) | (b << 16) | (a << 24);
}

Image reduceImageColorBits(Image img, uint8_t removebits, uint8_t cmin, uint8_t cmax) {
	size_t numcolors;
	size_t *counts;
	ImageFormat(&img, PIXELFORMAT_UNCOMPRESSED_R8G8B8A8);
	for (size_t y = 0; y < img.height; y++) {
		for (size_t x = 0; x < img.width; x++) {
			((uint32_t*)img.data)[x + y*img.width] = reduceColors(((uint32_t*)img.data)[x + y*img.width], removebits, cmin, cmax);
		}
	}
	return img;
}

int readint(const char *s) {
	char c;
	size_t i = 0;
	int num = 0;
	do {
		c = s[i++];
		if (c >= '0' && c <= '9') {
			num = num * 10 + c - '0';
		}
	} while (c);
	return num;
}

int main(int argc, char **argv) {
	int removebits, cmin, cmax;
	Image img;
	if (argc < 6) {
		printf("Usage: %s image_in image_out reduce_bits channel_min channel_max\nReduces colors from image_in to image_out. channel_min is the value per channel that is treated as minimum, channel_max is the value per channel that is treated as maximum. reduce_bits is the number of bits to chop off the value otherwise.\nreduce_bits: 0-7\nchannel_min: 0-255\nchannel_max: 0-255\n", argv[0]);
		return 0;
	}
	img = LoadImage(argv[1]);
	if (!IsImageReady(img)) {
		printf("Failed to open image file %s\n", argv[1]);
		return -1;
	}
	removebits = readint(argv[3]);
	cmin = readint(argv[4]);
	cmax = readint(argv[5]);
	if (removebits < 0 || removebits > 7) {
		printf("reduce_bits out of range. (0-7)\n");
		return 1;
	}
	if (cmin < 0 || cmin > 0xff) {
		printf("cmin out of range. (0-255)\n");
		return 1;
	}
	if (cmax < 0 || cmax > 0xff) {
		printf("cmax out of range. (0-255)\n");
		return 1;
	}
	img = reduceImageColorBits(img, removebits, cmin, cmax);
	if (!ExportImage(img, argv[2])) {
		printf("Failed to write output image file %s\n", argv[2]);
		return -2;
	}
	return 0;
}
