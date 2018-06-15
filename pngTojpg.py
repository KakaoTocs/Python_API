import os, sys, io
from PIL import Image

# 입출력 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

NOW_DIR = os.path.dirname(os.path.realpath(__file__))
CON_DIR = '\\'.join(NOW_DIR.split('\\')[:-1]) + "\\Crawling\\oldImage"
print(CON_DIR)

def search(dirname):
    result = []
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        ext = os.path.splitext(full_filename)[-1]
        if ext == '.c':
            result.append(full_filename)
    return result


def searchAll(dirname):
    result = []
    for (path, dir, files) in os.walk(dirname):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if ext == '.png':
                result.append("%s\\%s" % (path, filename))
    return result


def infoWrite(warringInfo):
    extensionWarring = warringInfo["extension"]
    downloadError = warringInfo["error"]
    pc = 0
    # extension Error
    f = open(NOW_DIR + "WarringInfo.txt", 'w')
    f.write("1_Extension\n")
    for warring in extensionWarring:
        f.write("%d: %s\n" % (pc, warring))
        pc += 1

    pc = 0
    f.write("\n")
    f.write("2_Error\n")
    for error in downloadError:
        f.write("%d: %s\n" % (pc, error))
        pc += 1
    f.close()


# infoWrite(Info)

if __name__ == "__main__":
    list = searchAll(CON_DIR)
    print(CON_DIR)
    for image in list:
        print(">>{0}".format(image))
        os.remove(image)
        # im = Image.open(image)
        # im = im.convert("RGB")
        # im.save(image[:-3]+"jpg")

# print(search(CON_DIR))
# print(searchAll(CON_DIR))
