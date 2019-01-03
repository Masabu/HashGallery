import rawpy
import imageio
import glob
import argparse
import re
import os
import errno


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

    filetypes = ('*.ORF', '*.DNG', '*.CR2', '*.PEF','*.X3F')
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

# glob case insensitive
def insensitive_glob(pattern):
    def either(c):
        return '[%s%s]'%(c.lower(),c.upper()) if c.isalpha() else c
    return glob.glob(''.join(map(either,pattern)))

# convert raw image into jpeg and save
def to_jpg(raw_file, outfile):

    raw = rawpy.imread(raw_file)  
    img = raw.postprocess()

    imageio.imwrite( outfile, img, format ='JPEG-PIL' , quality=60)


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




