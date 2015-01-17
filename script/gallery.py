from PIL import Image
import ExifTags
import glob
import argparse
import os
import errno
import markup
from markup import oneliner as e
import json

## process single image
def CreateSmallerImages(folder, filename, size, update):

    ## make thumbnail folder
    try:
        os.mkdir(folder + '/thumbs')
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    # store EXIF info as list of dictionary
    ExifDict = {}

    img = Image.open(folder + '/' + filename)
    exif_data = img._getexif()

    if exif_data is not None:

        #print exif_data
        for key, value in sorted(exif_data.items()):

            keyname = ExifTags.TAGS.get(key)
            
            if keyname == 'Orientation':

                if value == 3: img = img.rotate(180)
                if value == 6: img = img.rotate(270)
                if value == 8: img = img.rotate(90)

        # store meta data for index
        
        ExifDict['DateTime']        = exif_data[306]
        
        try:
            ExifDict['ExposureTime']    = exif_data[33434]
        except:
            ExifDict['ExposureTime'] = 0
        try:
            ExifDict['FNumbe']          = exif_data[33437]
        except:
            ExifDict['FNumbe'] = (0,0)
        try:
            ExifDict['ISOSpeedRatings'] = exif_data[34855]
        except:
            ExifDict['ISOSpeedRatings'] = 0
        try:
            ExifDict['Model']           = exif_data[272]
        except:
            ExifDict['Model'] = 'Missing'
        try:
            ExifDict['Orientation']     = exif_data[274]
        except:
            pass
        try:
            ExifDict['ApertureValue']   = exif_data[37378]
        except:
            pass

    else:
        print 'No Exit data, will not be rotated'


    ## export thumnail file, clean up buffer otherwise it can corrupt!!

    if update == 'FALSE':

        out_file = open( folder + '/thumbs/' + filename, 'wb' )
        img.thumbnail(size, Image.ANTIALIAS)
        quality_val = 90
        img.save( out_file, 'JPEG' , quality=quality_val)  # Must specify desired format here
        out_file.flush()
        out_file.close()

    return ExifDict


# from stackoverflow :)
def insensitive_glob(pattern):
    def either(c):
        return '[%s%s]'%(c.lower(),c.upper()) if c.isalpha() else c
    return glob.glob(''.join(map(either,pattern)))


def MakeHTMLS(filenames, folder, EXIFs, segment, MaxSegment):

    try:
        import markup
    except:
        print __doc__
        sys.exit( 1 )

    ## initialization 
    page = markup.page( )
    page.init( title="Photo Gallery",
    css=( '../one.css'), 
    header="Produced by Pig Thumbnail Generator", 
    footer="" )

    ## define lightbox
    page.link(href="../lightbox/css/lightbox.css",  rel="stylesheet")
    page.script("" , src="../lightbox/js/jquery-1.11.0.min.js")
    page.script( "", src="../lightbox/js/lightbox.js")

    ## center everything
    #page.div(class_ = "center")

    ## test
    page.H1("Photo Gallery " + folder)

    for s in range(MaxSegment):

        if s == 0:
            page.h2(e.a( 'Page' + str(s) , href = 'index.html'))
        else:
            page.h2(e.a( 'Page' + str(s) , href = 'index' + str(s) + '.html'))
   
    for i in range(len(filenames)):
        ## start of gallery area
        page.div(class_ = "gallery")
        page.div(class_ = "row")

        page.a( e.img( src= 'thumbs/' + filenames[i] , height=280 ), data_title=filenames[i] + ';' +EXIFs[filenames[i]], href = 'thumbs/' + filenames[i], class_='image-link', data_lightbox="set" )
        page.div(e.a(filenames[i],  href = filenames[i]),class_ = "desc")

        page.div.close( ) # close image row
        page.div.close( ) # close gallery

    if segment == 0 :
        outfile = 'index.html'
    else :
        outfile = 'index' + str(segment) + '.html'

    print 's=',segment, 'saving', outfile

    file = open( folder + '/' + outfile , 'w')
    print >>file, page
    file.flush()
    file.close()  

def main(folder, update):

    print 'process images inside', folder

    # create index.html inside specific image folder
    # container to store image names
 
    htmls = []
    filetypes = ('*.jpg', '*.jpeg')
    filenames = []

    ## obtain file names
    for t in filetypes:
        for fullpath in insensitive_glob(folder + '/'  + t):

            #print 'match pattern', t, 'file is matched is ', fullpath
            # remove path
            fname = fullpath.replace(folder + '/', "")
            filenames.append(fname)

    print '\n', len(filenames), 'images found in ', folder, '\n'
    print filenames

    EXIFs = {}

    ## make thumbnails
    j = 0.0
    for i in filenames:

        ratio = j / len(filenames) * 100
        print folder, ratio, "% completed"

        Exif  = CreateSmallerImages(folder, i, (1200,1200), update)
        EXIFs[i] = json.dumps(Exif)

        j +=1

    ## if number of images are large, split into multiple htmls    
    segment = len(filenames) / 50

    for s in range(segment):

        beg = s * 50
        end = (s+1)*50-1

        if s  < segment -1 :
            print s, segment -1 , beg, end
            MakeHTMLS(filenames[beg:end], folder, EXIFs, s,segment)
        else:
            print s, segment - 1, beg, "end"
            MakeHTMLS(filenames[beg:], folder, EXIFs, s, segment)

def SuperIndex(update):

    # glob folder names
    # assumes ISO-date  20xx-xx-xx 

    print '\n'
    print '*********************************************************************'
    print "This program assumes ISO-date format directories such as 2015-01-05"
    print '*********************************************************************\n'

    for directory in insensitive_glob('????-??-??'):

        print "processing", directory

        main(directory , update)
 

##########################################################################
##########################################################################
##########################################################################

if __name__ == '__main__':

    '''
    the program can scan directory and update all the images recursively

    two options:

    (1) full update -- update jpeg thumbnails and everything
    (2) update htmls only

    '''

    parser=argparse.ArgumentParser(description='Create thumbnail keeping original file names')
    #parser.add_argument('folder' , type=str , help='specify image folder name')
    parser.add_argument('--update','-f'  , default='FALSE' ,  help='TRUE = full update, default is html only', type = str)
 
    args=parser.parse_args()

    SuperIndex(args.update)

    #main(args.folder , args.update)



