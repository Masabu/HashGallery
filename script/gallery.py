from PIL import Image
import ExifTags
import glob
import argparse
import os
import errno
import markup
from markup import oneliner as e

#from PIL.ExifTags import TAG




def MakeIndex(folder, files):

    # create index hmtl
    htmls = []
 
    for fname in files:

        print 'image dir', folder
        print 'file name', fname

        # replace longer string first
        # make name into upper case       
        html  = fname.upper()
        html_name = html.replace("JPEG", "html")
        html_name = html.replace("JPG" , "html")

        print 'name of liked file', fname 

        html = '<a href="./thumbs/' + html_name + '">' + '<img src="./thumbs/' + fname + '" height="250" />' + '</a>'

        htmls.append(html)

    title = 'Photo gallery of ' + folder

    # create index html inside the folder
    file = open( folder + '/' + 'index.html', 'w')
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
    file.write('<a href="../index.html"> Go back to Root </a><br><br>')  

    for entry in htmls:

        file.write(entry + '\n')

    file.write('</body>' + '\n')
    file.write('</html>')

    file.flush()
    file.close()    

def MakeSubHtmls(imagename, EXIF,previous,next):        

    # make name into upper case
   
    html  = imagename.upper()
    html  = html.replace("JPEG", "html")
    html  = html.replace("JPG" , "html")

    file = open(folder + '/thumbs/' + html, 'w')

    file.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"' + '\n')
    file.write('"http://www.w3.org/TR/html4/loose.dtd">' + '\n')
    file.write('<html>' + '\n')
    file.write('<title>' + imagename + '</title>' + '\n')
    file.write('<head>' + '\n')
    file.write('<style>' + '\n')
    file.write('body {padding:10px;background-color:black;margin-left:15%;margin-right:15%;font-family:"Lucida Grande",Verdana,Arial,Sans-Serif;color: white;}' + '\n')
    file.write('img {border-style:solid;border-width:5px;border-color:white;}' + '\n')
    file.write('</style>' + '\n')
    file.write('</head>' + '\n')
    file.write('<body>' + '\n')
    file.write('<h1>' + imagename + '</h1>' + '\n')


    ## image part
    file.write('<a href="../index.html">Go back </a>')    
    file.write('Click for higher resolution image <br><br>')


    ## previous image

    # make name into upper case
    html_pre  = previous.upper()
    html_pre  = html_pre.replace("JPEG", "html")
    html_pre  = html_pre.replace("JPG" , "html")

    ## next image
    file.write('<a href="../thumbs/' + html_pre + '">Previous Image </a>')        
    file.write('<a href="../' + imagename + '">' + '<img src="../' + imagename + '" height="800"  />' + '</a>')        

   # make name into upper case
    html_next  = next.upper()
    html_next  = html_next.replace("JPEG", "html")
    html_next  = html_next.replace("JPG" , "html")

    ## next image
    file.write('<a href="../thumbs/' + html_next + '"> Next Image </a>')        


    ##EXIF data

    file.write('<br><br>')
    file.write('<style type="text/css">')
    file.write('.tg  {border-collapse:collapse;border-spacing:0;}')
    file.write('.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}')
    file.write('.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}')
    file.write('.tg .tg-s6z2{text-align:center}')
    file.write('</style>\n')

    file.write('<style>\n')
    file.write('.center {\n')
    file.write('    margin-left: auto;\n')
    file.write('    margin-right: auto;\n')
    file.write('}\n')
    file.write('</style>\n')

    file.write('<div class="center">')
    file.write('<table class="tg">')
    file.write('  <tr>')
    file.write('    <th class="tg-s6z2">Tag</th>')
    file.write('    <th class="tg-s6z2">Value</th>')
    file.write('  </tr>')
    file.write('  <tr>')
    file.write('    <td class="tg-s6z2">Camera</td>')
    file.write('    <td class="tg-s6z2">' + EXIF['Model'] + '</td>')
    file.write('  </tr>')
    file.write('  <tr>')
    file.write('    <td class="tg-s6z2">Captured</td>')
    file.write('    <td class="tg-s6z2">' + EXIF['DateTime'] + '</td>')
    file.write('  </tr>')
    file.write('  <tr>')
    file.write('    <td class="tg-s6z2">Shuttler Speed</td>')
    file.write('    <td class="tg-s6z2">' + str(EXIF['ExposureTime']) + '</td>')
    file.write('  </tr>')
    file.write('  <tr>')
    file.write('    <td class="tg-s6z2">Apature </td>')
    file.write('    <td class="tg-s6z2">' + str(EXIF['FNumbe']) + '</td>')
    file.write('  </tr>')
    file.write('  <tr>')
    file.write('    <td class="tg-s6z2">ISO </td>')
    file.write('    <td class="tg-s6z2">' + str(EXIF['ISOSpeedRatings']) + '</td>')
    file.write('  </tr>')   
    file.write('</table>')
    file.write('<p>All right reserved</p>')
    file.write('<p>Generated by Pig Thumbnail Generator</p>')
    file.write('</div>')

    file.write('</body>' + '\n')
    file.write('</html>')

    file.flush()
    file.close()



def createSmallerImage(folder, filename, size, update):

    ## make thumbnail folder
    try:
        os.mkdir(folder + '/thumbs')
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

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

    # do not save jpeg file if update switch is TRUE
    if update == 'FALSE':

        ## export thumnail file, clean up buffer otherwise it can corrupt!!
        out_file = open( folder + '/thumbs/' + filename, 'wb' )
        img.thumbnail(size, Image.ANTIALIAS)
        img.save( out_file, 'JPEG' )  # Must specify desired format here
        out_file.flush()
        out_file.close()
    else:
        print 'do not update jpeg files, update htmls only'

    return ExifDict


def main2(folder, update):

    print 'process images inside', folder

    # create index hmtl
    htmls = []
    filetypes = ('*.jpg', '*.jpeg')

    filenames = []

    for t in filetypes:
        for fullpath in insensitive_glob(folder + '/'  + t):

            #print 'match pattern', t, 'file is matched is ', fullpath
            # remove path
            fname = fullpath.replace(folder + '/', "")
            filenames.append(fname)

    print '\n', len(filenames), 'images found in ', folder, '\n'
    print filenames


    i = 0
    for f in filenames:

        print 'processing file:', f
        ## create smaller image into thumbmail folder
        ExifDict = createSmallerImage(folder, f,(500, 500), update)
        #print ExifDict

        if i == 0:
            previous = filenames[i-1]
            next     = filenames[-1]
        elif i == len(filenames)-1:
            previous = filenames[i-1]
            next     = filenames[0]
        else:
            previous = filenames[i-1]
            next     = filenames[i+1]

        ## create htmls
        MakeSubHtmls(f, ExifDict,previous,next)

        i+=1


    ## create main index
    ## pass folder name and list of files
    MakeIndex(folder, filenames)


# from stackoverflow :)
def insensitive_glob(pattern):
    def either(c):
        return '[%s%s]'%(c.lower(),c.upper()) if c.isalpha() else c
    return glob.glob(''.join(map(either,pattern)))


def SuperIndex(folder):

    # glob folder names
    # assumes ISO-date  20xx-xx-xx 

    print '\n'
    print '*********************************************************************'
    print "This program assumes ISO-date format directories such as 2015-01-05"
    print '*********************************************************************\n'

    for directory in insensitive_glob('????-??-??'):

        print directory

    ## create index.html using above list

def MakeHTMLS(filenames, folder):

    try:
        import markup
    except:
        print __doc__
        sys.exit( 1 )

    items  = ( "Item one", "Item two", "Item three", "Item four" )
    paras  = ( "This was a fantastic list.", "And now for something completely different." )
    images = ( "./thumbs/_MG_4925.jpg","./thumbs/_MG_4944.jpg","./thumbs/_MG_4956.jpg","./thumbs/_MG_4981.jpg" )
    links  = ("./thumbs/_MG_4925.jpg","./thumbs/_MG_4944.jpg","./thumbs/_MG_4956.jpg","./thumbs/_MG_4981.jpg")

    page = markup.page( )
    page.init( title="My title",
    css=( '../one.css', 'two.css' ), 
    header="Something at the top", 
    footer="The bitter end." )

    ## define lightbox
    page.link(href="../lightbox/css/lightbox.css",  rel="stylesheet")
    page.script("" , src="../lightbox/js/jquery-1.11.0.min.js")
    page.script( "", src="../lightbox/js/lightbox.js")

    ## any info

    page.ul( class_='mylist' )
    page.li( items, class_='myitem' )
    page.ul.close( )  
    page.p( paras )

    ## start of gallery area
    page.div(class_ = "gallery")

    ## i is an index that starts with 0
    for i in range(len(filenames)):

        mod = i % 3

        ## close div if it is 3rd of 3
        if mod == 2:

            page.a( e.img( src=filenames[i] , height=300 ), href = filenames[i], class_='example-image-link', data_lightbox="example-set" )
            page.div.close( ) 

        ## start div row if it is first of 3
        elif mod == 0:
            page.div(class_ = "row")
            page.a( e.img( src=filenames[i] , height=300 ), href = filenames[i], class_='example-image-link', data_lightbox="example-set" )

        else:
            page.a( e.img( src=filenames[i] , height=300 ), href = filenames[i], class_='example-image-link', data_lightbox="example-set" )

 
    page.div.close( ) 

    file = open( folder + '/' + 'index.html', 'w')

    print >>file, page

    file.flush()
    file.close()  


def main(folder):

    print 'process images inside', folder

    # create index.html inside specific image folder
    htmls = []
    filetypes = ('*.jpg', '*.jpeg')

    ## container to store image names
    filenames = []

    for t in filetypes:
        for fullpath in insensitive_glob(folder + '/'  + t):

            #print 'match pattern', t, 'file is matched is ', fullpath
            # remove path
            fname = fullpath.replace(folder + '/', "")
            filenames.append(fname)

    print '\n', len(filenames), 'images found in ', folder, '\n'
    print filenames

    return filenames

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
    parser.add_argument('folder' , type=str , help='specify image folder name')
    parser.add_argument('--fullupdate','-f'  , default='FALSE' ,  help='TRUE = full update, default is html only', type = str) 

    args=parser.parse_args()
    folder= args.folder 

    #SuperIndex(folder)
    #MakeHTMLS()
    filenames = main(folder)
    MakeHTMLS(filenames, folder)


    #main(folder, args.update)
