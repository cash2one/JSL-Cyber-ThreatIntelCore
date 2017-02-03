import glob
import os
import sys

def LoadScripts(scriptFolder):
    ''' Returns a list of module references '''
    # Find Script Files:
    # print scriptFolder
    scriptFiles = glob.glob(os.path.join(scriptFolder, "*.py"))
    #print "Found %d Script Files" % (len(scriptFiles))



    # Load scripts:
    loadedScripts = []
    for scriptFile in scriptFiles:

            scriptName = os.path.basename(scriptFile)
            folderName = scriptFolder
            # print scriptName
            #print folderName
            fullpathName = "%s/%s" % (folderName, scriptName)

            # fullpathName = os.path.abspath(scriptFolder+"/"+fullpathName)


            loadedScripts.append(fullpathName)

    return loadedScripts


def RunScripts(loadedScripts):


        #list of completed scripts
        namesOfCompletedScripts = []



        while (len(namesOfCompletedScripts) < len(loadedScripts)):
            nothingExecutedOnThisPass = True

            for script in loadedScripts:

                if (script not in namesOfCompletedScripts):
                    print "RUNNING : %s" % script
                    os.system("python " +script)
                    namesOfCompletedScripts.append(script)
                    nothingExecutedOnThisPass = False

            if (nothingExecutedOnThisPass):

                break

        # print "\nThe following scripts were successfully run:"
        #print namesOfCompletedScripts

        if (len(namesOfCompletedScripts) < len(loadedScripts)):
            print "Some scripts failed:"
            for script in loadedScripts:
                if (script not in namesOfCompletedScripts):
                    print "\t" + script


if __name__ == '__main__':
    print "main"

    # RunScripts(LoadScripts(str("/home/abdou/PycharmProjects/test/dir")))
