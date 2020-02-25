# version 0.1.8

import subprocess, configparser, shutil, os, sys, ftplib

def getConfigSections():
    sections = config.sections()
    sections.remove('common')
    return sections

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

def localCopying(source, options):
    location = options['location']

    for src in source:
        if('source_location' in options):
            if(not src.startswith(options["source_location"].replace("/",os.sep))):
                continue

            dest = src.replace(options["source_location"].replace("/",os.sep)+os.sep, '', 1)
            dest = os.path.join(location, dest)
        else:
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
            d = os.path.dirname(src)
            if(os.sep!="/"):
                d = d.replace(os.sep,"/")
            
            # source location set
            if('source_location' in options):
                if(not d.startswith(options["source_location"])):
                    continue
                if(d==options["source_location"]):
                    d = ''
                else:
                    d = d.replace(options["source_location"]+'/', '', 1)

            # set destination
            dest = ''
            if(len(d)>0):
                dest = d+'/'
            dest += os.path.basename(src)

            # directories for make
            dirs = []
            if(len(d)>0):
                dirs = d.split('/')
                for i in range(1, len(dirs)):
                    if(len(dirs[i])==0):
                        continue
                    dirs[i] = dirs[i-1]+"/"+dirs[i]

            # make directories
            for d in dirs:
                try:
                    if(os.sep!="/"):
                        d = d.replace("\\","/")
                    ftp.mkd(d)
                    print("MKD "+d)
                except ftplib.error_perm:
                    continue

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
common = getConfigSectionMap('common')

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

# es6 translate
for i, src in enumerate(source):
    if(not src.endswith('.es6') and common['es6_translate'] != 'Y'):
        continue
    f = open(src, 'rt', encoding="utf-8")
    src_str = f.read()
    f.close()
    try:
        print("[Translate:ES6 to ES5]")
        import dukpy
        src_str = dukpy.babel_compile(src_str)['code']
    except ImportError:
        print("[Translate:ES6 to ES5 - Failed]")
    source[i] = src[:-3]+"js"
    print("CREATE "+source[i])
    f = open(source[i], 'wt', encoding="utf-8")
    f.write(src_str+" ")
    f.close()

# do copying
for section in getConfigSections():
    sectionMap = getConfigSectionMap(section)
    if(sectionMap["method"]=="local"):
        print("[Local:" + section + " Copying]")
        localCopying(source, sectionMap)
    elif(sectionMap["method"]=="ftp"):
        print("[FTP:" + section + " Copying]")
        ftpCopying(source, sectionMap)

print("[Delivery completed]")