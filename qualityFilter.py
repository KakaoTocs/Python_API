import os, sys, io
from PIL import Image

# 입출력 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

NOW_DIR = os.path.dirname(os.path.realpath(__file__))
CON_DIR = '\\'.join(NOW_DIR.split('\\')[:-1]) + "\\Crawling\\oldImage"
print("DIR Path: " + CON_DIR)

def searchAll(dirname):
    result = [[], []]
    for (path, dir, files) in os.walk(dirname):
        for filename in files:
            # print(filename)
            ext = os.path.splitext(filename)[-1]
            quality = os.path.splitext(filename)[0:1][0][0:3]
            # [0:1]: 이미지명 -> [0]: 0번쨰 인덱스(이미지명) -> [0:3]: FHD or UHD
            if ext == '.jpg':
                if quality == 'FHD':
                    result[0].append("%s\\%s" % (path, filename))
                if quality == 'UHD':
                    result[1].append("%s\\%s" % (path, filename))

    return result


def filteringImages(imageList):
    FHDList = imageList[0]
    UHDList = imageList[1]

    f1 = open(NOW_DIR + "//filteringFHDInfo.txt", 'w')
    f2 = open(NOW_DIR + "//filteringUHDInfo.txt", 'w')

    for FHDImage in FHDList:
        try:
            f = Image.open(FHDImage)
            if f.size != (1920, 1080):
                f1.write("NOT FHD: " + FHDImage)
                f.close()
                os.remove(FHDImage)
            else:
                f.close()
        except:
            f1.write("- Cant Open: " + FHDImage)
            os.remove(FHDImage)
    f1.close()

    for UHDImage in UHDList:
        try:
            f = Image.open(UHDImage)
            if f.size != (3840, 2160):
                f2.write("NOT UHD: " + UHDImage)
                f.close()
                os.remove(UHDImage)
            else:
                f.close()
        except:
            f2.write("- Cant Open: " + UHDImage)
            os.remove(UHDImage)
    f2.close()

if __name__ == "__main__":
    list = searchAll(CON_DIR)
    filteringImages(list)
    # print(list)
    # for image in list:
    #     print(">>{0}".format(image))
    #     os.remove(image)
