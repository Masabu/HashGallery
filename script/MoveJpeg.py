## move jpeg
## cannon DSLR creates both jpeg and raw files (.CR) in the same folder
## this will search folders recursivly and move jpeg into separate folder

import os
import argparse
import glob
import shutil


def LookIntoFolder(folder,jpegfolder):        

    ## create individual html files

    images = glob.glob(folder + "/*.[jJ][pP][gG]")  + glob.glob(folder + "/*.[jJ][pP][eE][gG]")

    ## make folders and mv only if there are jpeg files

    print len(images)

    if len(images)>=2:

	    filepath  = folder.split("/")
	    foldername = filepath[-1]

	    try:
	    	os.mkdir(jpegfolder)
	    except OSError:
	    	print "folder" + jpegfolder + " exists already"
	    	pass

	    # make subfolder
	    try:
	    	os.mkdir(jpegfolder + '/' + foldername )
	    except OSError:
	    	print "subfolder" +  foldername  + " exists already"
	    	pass

	    for f in images:

	    	filename = f.split("/")[-1]
	    	copyto   = jpegfolder + '/' + foldername + '/' + filename
	    	print 'moving ', f, copyto
	    	shutil.move(f,copyto)




## give root directry and dictionary to store data
def WalkFolders(dir,jpegfolder):

    ## read files recursively
    for folder, subs, files in os.walk(dir):

    	print folder, subs
    	LookIntoFolder(folder,jpegfolder)


if __name__ == '__main__':

    parser=argparse.ArgumentParser(description='count number of tweets for each topic and send result to Redshift')
    parser.add_argument('folder'     , type=str , help='specify image folder name')
    parser.add_argument('jpegfolder' , type=str , help='specify locaiton to copy jpeg files')
    args=parser.parse_args()

    print ""
    print 'moving jpeg files from', args.folder
    print 'to folder ', args.jpegfolder

    WalkFolders(args.folder,args.jpegfolder)






