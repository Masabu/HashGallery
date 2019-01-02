#from PIL import Image
import rawpy
import imageio
#import ExifTags
import glob
import argparse
import re
import os
# import errno
# import markup
# from markup import oneliner as e
# import json
# import random

'''
# outline of the program

inputs
(1) input dir where raw files are saved
(2) output dir where jpg files will be saved
(3) hard code - raw file accepted

(4) recurively go after each file in subfolder
(5) convert raw (DNC, CR2 or whatever - but specify) files into jpeg
(6) create html file 
'''



def main(folder, output):

    dir_name = re.search('....-..-..', folder)

    print ''
    print 'process images inside', folder, 'directory name is', dir_name.group(0)

    print 'jpeg files will be saved within', output , 'sub directory of', dir_name.group(0)


    try:
        os.mkdir(output + '/' + dir_name.group(0))

    except OSError as exception:
            print OSError
            print 'folder exits - moving on'
        #if exception.errno != errno.EEXIST:
        #    raise

    # define container to store image names
    #htmls = []
    filetypes = ('*.ORF', '*.DNG', '*.CR2')
    filenames = []

    ## obtain file names
    for t in filetypes:
        for fullpath in insensitive_glob(folder + '/'  + t):
            #print 'match pattern', t, 'matched file is ', fullpath
            
            # remove path
            fname = fullpath.replace(folder + '/', "")
            names = re.split('/', fname)
            rname = re.split('\.', names[-1])

            outfile = output +  dir_name.group(0) + '/'  + rname[0] + '.jpeg'


            print 'ext = ',t[-3:], ', jpeg file=' , outfile , ', input = ', fname

            filenames.append(fname)

            # produce jpeg file
            to_jpg(fname,outfile)



    print '\n', len(filenames), 'images found in ', folder, '\n'


# from stackoverflow :)
def insensitive_glob(pattern):
    def either(c):
        return '[%s%s]'%(c.lower(),c.upper()) if c.isalpha() else c
    return glob.glob(''.join(map(either,pattern)))

# convert raw image into jpeg and save
def to_jpg(raw_file, outfile):

    raw = rawpy.imread(raw_file)
    img = raw.postprocess()

    imageio.imsave( outfile, img, quality=50)


# def MakeHTMLS(filenames, folder, EXIFs, segment, MaxSegment):

#     try:
#         import markup
#     except:
#         print __doc__
#         sys.exit( 1 )

#     ## initialization 
#     page = markup.page( )
#     page.init( title="Photo Gallery",
#     css=( '../one.css'), 
#     header="Produced by Pig Thumbnail Generator", 
#     footer="" )

#     ## define lightbox
#     page.link(href="../lightbox/css/lightbox.css",  rel="stylesheet")
#     page.script("" , src="../lightbox/js/jquery-1.11.0.min.js")
#     page.script( "", src="../lightbox/js/lightbox.js")

#     ## center everything
#     #page.div(class_ = "center")

#     ## test
#     page.H1("Photo Gallery " + folder)

#     page.h2(e.a( 'Go Back to the main index' , href = '../index.html'))

#     for s in range(MaxSegment):

#         if s == 0:
#             page.h2(e.a( 'Page' + str(s) , href = 'index.html'))
#         else:
#             page.h2(e.a( 'Page' + str(s) , href = 'index' + str(s) + '.html'))
   
#     for i in range(len(filenames)):
#         ## start of gallery area
#         page.div(class_ = "gallery")
#         page.div(class_ = "row")

#         page.a( e.img( src= 'thumbs/' + filenames[i] , height=280 ), data_title=filenames[i] + ';' +EXIFs[filenames[i]], href = 'thumbs/' + filenames[i], class_='image-link', data_lightbox="set" )
#         page.div(e.a(filenames[i],  href = filenames[i]),class_ = "desc")

#         page.div.close( ) # close image row
#         page.div.close( ) # close gallery

#     if segment == 0 :
#         outfile = 'index.html'
#     else :
#         outfile = 'index' + str(segment) + '.html'

#     print 's=',segment, 'saving', outfile

#     file = open( folder + '/' + outfile , 'w')
#     print >>file, page
#     file.flush()
#     file.close()  

# def main(folder, update):

#     print 'process images inside', folder

#     # create index.html inside specific image folder
#     # container to store image names
 
#     htmls = []
#     filetypes = ('*.jpg', '*.jpeg')
#     filenames = []

#     ## obtain file names
#     for t in filetypes:
#         for fullpath in insensitive_glob(folder + '/'  + t):

#             #print 'match pattern', t, 'file is matched is ', fullpath
#             # remove path
#             fname = fullpath.replace(folder + '/', "")
#             filenames.append(fname)

#     print '\n', len(filenames), 'images found in ', folder, '\n'

#     EXIFs = {}

#     ## make thumbnails
#     j = 0.0
#     for i in filenames:

#         ratio = j / len(filenames) * 100
#         print folder, ratio, "% completed"

#         Exif  = CreateSmallerImages(folder, i, (1200,1200), update)
#         EXIFs[i] = json.dumps(Exif)

#         j +=1

#     ## if number of images are large, split into multiple htmls    
#     segment = len(filenames) / 50

#     if segment == 0:

#         MakeHTMLS(filenames, folder, EXIFs, 0,0)

#     for s in range(segment):

#         beg = s * 50
#         end = (s+1)*50-1

#         if s  < segment -1 :
#             print s, segment -1 , beg, end
#             MakeHTMLS(filenames[beg:end], folder, EXIFs, s,segment)
#         else:
#             print s, segment - 1, beg, "end"
#             MakeHTMLS(filenames[beg:], folder, EXIFs, s, segment)

#     return filenames
        

# def SuperIndex(folder, update, NSample):

#     # glob folder names
#     # assumes ISO-date  20xx-xx-xx 

#     print '\n'
#     print '*********************************************************************'
#     print "This program assumes ISO-date format directories such as 2015-01-05"
#     print '*********************************************************************\n'

#     Directories = []
#     CoverPhotos = []

#     for directory in insensitive_glob('????-??-??'):

#         filenames = main(directory , update)
#         Directories.append(directory + '/index.html')

#         cover = []
#         # select 5 images
#         for i in range(NSample):

#             rand = random.randint(0, len(filenames)-1)
#             #print i, len(filenames), rand
#             cover.append(filenames[rand])
        
#         CoverPhotos.append(cover)

#     ## create super index file
#     ## initialization 

#     page = markup.page( )
#     page.init( title="Photo Gallery",
#     css=( '../one.css'), 
#     header="", 
#     footer="Produced by Pig Thumbnail Generator" )

#     page.H1("Photo Gallery")

#     ## take random sample of photos
#     ## to create cover

#     for i in range(len(Directories)):

#         page.p(Directories[i].replace("/index.html",""))

#         for j in range(NSample):
#             page.a(e.img(height=160, src= Directories[i].replace("index.html","") + 'thumbs/' + CoverPhotos[i][j]  ) ,href = Directories[i])
#         page.hr()

#     file = open( "index.html" , 'w')
#     print >>file, page
#     file.flush()
#     file.close()  


# ##########################################################################
# ##########################################################################
# ##########################################################################

if __name__ == '__main__':

    '''
    The program can scan directory and update all the images recursively
    two options:

    (1) full update -- update jpeg thumbnails and everything
    (2) update htmls only
    '''

    parser=argparse.ArgumentParser(description='Create jpeg thumbnail from raw image files')
    parser.add_argument('-f' , default='empty_folder', type=str , help='specify input folder name')
    parser.add_argument('-o' , default='empty_folder', type=str , help='specify output folder name')

    #parser.add_argument('--update', default='FALSE' ,  help='TRUE = full update, default is html only', type = str)
    #parser.add_argument('--Nsample', default=10 ,  help='Number of sample images', type = int)
 
    args=parser.parse_args()

    if args.f == 'empty_folder':
        print "Please specify input folder"
    if args.o == 'empty_folder':
        print "Please specify output folder"
    elif args.f != 'empty_folder':
        if args.o != 'empty_folder':
            print "looks good"
            print "input folder is" ,args.f
            print "output folder is", args.o
            main(args.f,args.o)
        else:
            print "Please specify output folder"



#elif args.folder == 'empty_folder':
#    print "update everything"
#         SuperIndex(args.folder, args.update, args.Nsample)




