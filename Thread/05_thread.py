from threading import Thread
from urllib.request import urlopen

urls = ('https://pbs.twimg.com/profile_images/965898239265325057/9FIW6ykj_400x400.jpg', 'http://www.backdrum.net/uploaded/board/2017/12/30/o_1c2j9ika3ed617371tdb1nn4f0q.jpg')

def download_contents(url, filename):
    res = urlopen(url)
    if res.code != 200:
        return
    with open(filename, 'wb') as f:
        f.write(res.read())

def main():
    threads = []
    for url in urls:
        filename = url.rsplit('/', 1)[1]
        print(filename)
        t = Thread(target=download_contents, args=(url, filename))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
