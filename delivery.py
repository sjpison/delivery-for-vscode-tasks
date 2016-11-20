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
    dest = os.path.join(location, source)
    print(source + " -> " + dest)

    dstdir = os.path.dirname(dest)
    if not os.path.isdir(dstdir):
        os.makedirs(dstdir)

    shutil.copyfile(source, dest)
    return

def getAllFiles(src):
    r = []
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)

        # vscode and git is pass
        file_name = os.path.relpath(full_file_name, os.getcwd())
        if(file_name.startswith(".vscode") or file_name.startswith(".git")):
            continue

        if (os.path.isfile(full_file_name)):
            r.append(file_name)
        else:
            r = r + getAllFiles(full_file_name)
    return r
    
# load config
config = configparser.ConfigParser()
config.read("./.vscode/delivery-conf.ini")

# source file
if(sys.argv[1]!="all"):
    commonprefix = os.path.commonprefix([sys.argv[1], os.getcwd()])
    source = os.path.relpath(sys.argv[1], commonprefix)
else:
    source = sys.argv[1]

# ignore under vscode directory
if(source.startswith(".vscode")):
    print("[Ignored] - " + source)
    sys.exit()

# do copying
for section in getConfigSections():
    sectionMap = getConfigSectionMap(section)
    if(sectionMap["method"]=="local"):
        print("[" + section + " Copying]")
        if(source=="all"):
            for src in getAllFiles(os.getcwd()):
                localCopying(src, sectionMap["location"])
        else:
            localCopying(source, sectionMap["location"])