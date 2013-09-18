import os
import argparse
import glob
import errno
import Image
from PIL import Image
import string
import random
import shutil

#from PIL.ExifTags import TAG

def MakeIndex(folder, indexname):

    # create index hmtl
    htmls = []
    for name in glob.glob(folder +  '/hashed/*.jpeg'):

            name = name.replace(folder + '/hashed/', "")

            html = '<a href="./thumb/' + name.replace("jpeg", "html") + '">' + '<img src="./thumb/' + name + '" height="192" />' + '</a>'

            htmls.append(html)

    #print htmls
    '''
    title=os.getcwd()
    title=title.split("/")
    title=title.pop()
    '''
    title = 'Photo gallery of ' + folder

    # create index html inside the folder
    file = open( folder + '/' + indexname + '.html', 'w')
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

    for name in glob.glob(folder +  '/hashed/*.jpeg'):

        # remove path
        image = name.replace(folder + '/hashed/', "")
        html  = image.replace("jpeg", "html")

        file = open(folder + '/thumb/' + html, 'w')
        file.write('click to higher resolution image <br>')                
        file.write('<a href="../hashed/' + image + '">' + '<img src="../thumb/' + image + '"  />' + '</a>')        
        file.flush()
        file.close()

    return image, html, name


def processImage(imgdir, fname,newname):

    img = Image.open(imgdir + '/' + fname)

    try:
        os.mkdir(folder + '/hashed')
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    try:
        os.mkdir(folder + '/thumb')
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    img.save(imgdir + '/hashed/' + newname  + '.jpeg', 'jpeg')

    img.thumbnail((300, 300), Image.ANTIALIAS)
    img.save(imgdir + '/thumb/' + newname + '.jpeg', 'jpeg')

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

def MoveOriginals(folder):

    try:
        os.mkdir(folder + '/originals')
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise 

    for fname in glob.glob(folder + '/*.[jJ][pP][gG]'):
        toname = fname.replace(folder + '/', "")
        toname = folder + '/originals/' + toname
        shutil.move(fname, toname)



if __name__ == '__main__':

    parser=argparse.ArgumentParser(description='count number of tweets for each topic and send result to Redshift')
    parser.add_argument('folder' , type=str , help='specify image folder name')
    parser.add_argument('--remove','-r'  , default='FALSE',  help='specify keyword', type = str)  
    parser.add_argument('--update','-u'  , default='FALSE' ,  help='update images (else no update)', type = str)  
    args=parser.parse_args()
    folder    = args.folder 

    if args.update == "TRUE":
        ## search folder and create files with hashed names with original size
        ## and create thumbnail image with smaller size
        for fname in glob.glob(folder + '/*.[jJ][pP][gG]'):
            fname  = fname.replace(folder + '/', "")
            newname = randomword(5)
            print folder, '/',  fname, '/', newname
            processImage(folder, fname, newname)

    else:
        print "update htmls only"

    ## make index
    ## use randomly generated name
    MakeIndex(folder,randomword(8))

    ## index for thumbnails
    MakeSubHtmls(folder)

    if args.remove == "TRUE":

        print 'remove originals into original folder'

        MoveOriginals(folder)
        





