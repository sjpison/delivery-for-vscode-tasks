# version 0.1.4

import subprocess, configparser, shutil, os, sys, ftplib

def getConfigSections():
    return config.sections()

def getConfigSectionMap(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def localCopying(source, location):
    for src in source:
        dest = os.path.join(location, src)
        print(src + " -> " + dest)

        dstdir = os.path.dirname(dest)
        if not os.path.isdir(dstdir):
            os.makedirs(dstdir)

        shutil.copyfile(src, dest)
    return

def ftpGetLists(options):
    print("#FTP Connection Check - Get Lists")
    ftp = ftplib.FTP()
    ftp.connect(options["host"], int(options["port"]))
    ftp.login(user=options["userid"], passwd=options["password"])
    ftp.cwd(options['location'])
    ftp.retrlines('LIST')
    ftp.quit()
    return

def ftp_callback(line):
    print(line)
    return
    
def ftpCopying(source, options):
    ftp = ftplib.FTP()
    ftp.connect(options["host"], int(options["port"]))
    ftp.login(user=options["userid"], passwd=options["password"])
    ftp.cwd(options['location'])

    for src in source:
        if(os.path.isfile(src)):
            dirs = []
            d = os.path.dirname(src)
            if(os.sep!="/"):
                d = d.replace("\\","/")
            
            # source location set
            if(len(options["source_location"])>0 and len(d)>0):
                d = d.replace(options["source_location"], '', 1)
            
            # set destination
            dest = ''
            if(len(d)>0):
                dest += '/'
            dest += os.path.basename(src)
                
            while len(d) > 0:
                try:
                    #lines = []
                    #result = ftp.retrlines("LIST "+d, lines.append) # empty directory check, nlst() is error occurred.
                    ftp.mkd(d)
                    break
                except ftplib.error_temp:
                    dirs.insert(0,d)
                except ftplib.error_perm:
                    continue
                finally:
                    d=os.path.dirname(d)

            for d in dirs:
                if(os.sep!="/"):
                    d = d.replace("\\","/")
                print("MKD "+d)
                ftp.mkd(d)

            print('STOR '+dest)
            ftp.storbinary('STOR '+dest, open(src,'rb'))
    return

def getAllFiles(src):
    r = []
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)

        # vscode and git is pass
        file_name = os.path.relpath(full_file_name, os.getcwd())

        ignore_matched = False
        for ig in ignored:
            if(file_name.startswith(ig)):
                print("[Ignored] - " + file_name)
                ignore_matched = True
                break
        if(ignore_matched):
            continue

        if (os.path.isfile(full_file_name)):
            r.append(file_name)
        else:
            r = r + getAllFiles(full_file_name)
    return r
    
# load config
config = configparser.ConfigParser()
config.read("./.vscode/delivery-conf.ini")

# ignored config
ignored = [".vscode",".git"]

# argument check
if(sys.argv[1]=="all"):
    source = getAllFiles(os.getcwd())
elif(sys.argv[1]=="ftpCheck"):
    for section in getConfigSections():
        sectionMap = getConfigSectionMap(section)
        if(sectionMap["method"]=="ftp"):
            print("["+section+"]")
            ftpGetLists(sectionMap)
    sys.exit()
else:
    commonprefix = os.path.commonprefix([sys.argv[1], os.getcwd()])
    source = os.path.relpath(sys.argv[1], commonprefix)
    # single file ignore check
    for ig in ignored:
        if(source.startswith(ig)):
            print("[Ignored] - " + source)
            sys.exit()
    source = [source]

# do copying
for section in getConfigSections():
    sectionMap = getConfigSectionMap(section)
    if(sectionMap["method"]=="local"):
        print("[Local:" + section + " Copying]")
        localCopying(source, sectionMap["location"])
    elif(sectionMap["method"]=="ftp"):
        print("[FTP:" + section + " Copying]")
        ftpCopying(source, sectionMap)

print("[Delivery completed]")