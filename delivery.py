import subprocess, configparser, shutil, os, sys

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
    if isinstance(source, str):
        source = [source]
    for src in source:
        dest = os.path.join(location, src)
        print(src + " -> " + dest)

        dstdir = os.path.dirname(dest)
        if not os.path.isdir(dstdir):
            os.makedirs(dstdir)

        shutil.copyfile(src, dest)
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

# source file
if(sys.argv[1]!="all"):
    commonprefix = os.path.commonprefix([sys.argv[1], os.getcwd()])
    source = os.path.relpath(sys.argv[1], commonprefix)
    # single file ignore check
    for ig in ignored:
        if(source.startswith(ig)):
            print("[Ignored] - " + source)
            sys.exit()
else:
    source = getAllFiles(os.getcwd())

# do copying
for section in getConfigSections():
    sectionMap = getConfigSectionMap(section)
    if(sectionMap["method"]=="local"):
        print("[" + section + " Copying]")
        localCopying(source, sectionMap["location"])