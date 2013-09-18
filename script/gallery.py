import os
import argparse
import glob
import errno
import Image
from PIL import Image
#from PIL.ExifTags import TAG

def MakeIndex(folder):

    # create index hmtl
    htmls = []
    for name in glob.glob(folder + '/*.jpg'):

            name = name.replace(folder + '/', "")

            html = '<a href="./thumb/' + name.replace("jpg", "html") + '">' + '<img src="./thumb/' + name + '" height="192" />' + '</a>'

            htmls.append(html)

    #print htmls
    title=os.getcwd()
    title=title.split("/")
    title=title.pop()

    # create index html inside the folder
    file = open( folder + '/index.html', 'w')
    file.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"' + '\n')
    file.write('    "http://www.w3.org/TR/html4/loose.dtd">' + '\n')
    file.write('<html>' + '\n')
    file.write('<title>' + title + '</title>' + '\n')
    file.write('<head>' + '\n')
    file.write('<style>' + '\n')
    file.write('body {padding:10px;background-color:black;margin-left:15%;margin-right:15%;font-family:"Lucida Grande",Verdana,Arial,Sans-Serif;color: white;}' + '\n')
    file.write('img {border-style:solid;border-width:5px;border-color:white;}' + '\n')
    file.write('</style>' + '\n')
    file.write('</head>' + '\n')
    file.write('<body>' + '\n')
    file.write('<h1>' + title + '</h1>' + '\n')

    for entry in htmls:

        file.write(entry + '\n')

    file.write('</body>' + '\n')
    file.write('</html>')

    file.flush()
    file.close()

def MakeSubHtmls(folder):        

    ## create individual html files

    try:
        os.mkdir(folder + '/thumb')
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    for name in glob.glob(folder + '/*.jpg'):

        # remove path
        image = name.replace(folder + '/', "")
        html  = image.replace("jpg", "html")

        file = open(folder + '/thumb/' + html, 'w')
        file.write('<a href="../' + image + '">' + '<img height="50%" src="../'  + image + '" />' + '</a>')
        file.flush()
        file.close()


def processImage(imgdir, fname):
    img = Image.open(imgdir + '/' + fname)

    '''
    exif = img._getexif()
    if exif != None:
        for tag, value in exif.items():
            decoded = TAGS.get(tag, tag)
            if decoded == 'Orientation':
                if value == 3: img = img.rotate(180)
                if value == 6: img = img.rotate(270)
                if value == 8: img = img.rotate(90)
                break
    '''

    img.thumbnail((192, 192), Image.ANTIALIAS)
    img.save(imgdir + '/thumb/' + fname, 'jpeg')

if __name__ == '__main__':



    parser=argparse.ArgumentParser(description='count number of tweets for each topic and send result to Redshift')
    parser.add_argument('folder' , type=str , help='specify image folder name')
    args=parser.parse_args()
    folder    = args.folder 

    MakeIndex(folder)
    MakeSubHtmls(folder)

    for fname in glob.glob(folder + '/*.jpg'):
        fname  = fname.replace(folder + '/', "")
        print folder, '/',  fname
        processImage(folder, fname)




