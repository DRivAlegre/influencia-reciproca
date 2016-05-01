from glitchalgorithm import Glitch
import os, time, sys, json

# Entry point
def init():
    m = MainOperations(os.getcwd())
    limg, path, operations = operate(m)
    return limg,path,operations

def operate(m):
    os.chdir(m.DEFAULT_PATH + '/static/js/')
    jsondata = open('jsondata.json', 'r').read()
    os.chdir(os.getcwd() + '/..')
    os.chdir(os.getcwd() + '/..')
    m.move_img_folder()

    print('DEBUGGING')
    print('#############')
    print('Default path: ' + m.DEFAULT_PATH)
    print('getCwd(): ' + os.getcwd())
    print('#############')

    list_images = os.listdir(m.DEFAULT_PATH + '/static/imgs/original/')
    if len(os.listdir(m.DEFAULT_PATH + '/static/imgs/glitched/')) == 0:
        for img in list_images:
            m.create_glitch_element(img)

    setjsondata = set(json.loads(jsondata)['listofimages'])
    setloadlistdir = set(os.listdir(m.DEFAULT_PATH + '/static/imgs/glitched/'))

    print len(setloadlistdir.difference(setjsondata))

    if jsondata.find('listofimages') == -1 or not(len(json.loads(jsondata)['listofimages']) == len(os.listdir(m.DEFAULT_PATH + "/static/imgs/glitched/"))) or len(setloadlistdir.difference(setjsondata)) > 0:
        exportlistimgs(m.DEFAULT_PATH)
    return list_images, m.DEFAULT_PATH, m

def exportlistimgs(defaultpath):
    os.chdir(defaultpath)
    rootpath = os.getcwd()
    os.chdir(os.getcwd() + '/static/js/')
    listimagesinner = os.listdir(rootpath + '/static/imgs/glitched/')
    jsonfile = open('jsondata.json', 'w')
    jsondata = json.dumps({'listofimages': listimagesinner})
    jsonfile.write(jsondata)
    jsonfile.close()
    os.chdir(defaultpath + '/..')

class MainOperations:
    def __init__(self, defaultpath):
        self.DEFAULT_PATH = defaultpath
        self.executed = True
    def move_img_folder(self):
        os.chdir(os.getcwd() + '/static/imgs/original')
    def create_glitch_element(self, namefile):
        try:
            glitch = Glitch()
            glitch.trigger(namefile)
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print exc_type , fname , exc_tb.tb_lineno
            print sys.exc_info()
            os.chdir(self.DEFAULT_PATH)
            self.logs(str(sys.exc_info()))
            self.move_img_folder()

    def logs(self, error):
        logread = open('logs', 'r')
        logtext = logread.read()
        logread.close()
        logwrite = open('logs', 'w')
        logwrite.write(logtext + '\n\n' + error)
        logwrite.close()

class ObserverImgFolder:
    def __init__(self, list_imgs, path, objoperation):
        self.listimgs = list_imgs
        self.localpath = path
        self.start = True
        self.operation = objoperation
    def stop(self):
        self.start = False
    def start(self):
        self.start = True
    def observe_img(self):
        while self.start:
            try:
                os.chdir(self.localpath + '/static/imgs/original/')
                localimgs = set(os.listdir(os.getcwd()))
                setlistimgs = set(self.listimgs)
                if len(localimgs) > len(self.listimgs):
                    diffimgs = localimgs.difference(setlistimgs)
                    for dimg in diffimgs:
                        self.listimgs.append(dimg)
                        self.operation.create_glitch_element(dimg)
                    exportlistimgs(self.localpath)
                time.sleep(5)
            except KeyboardInterrupt:
                print 'Interrupted!'
                observerimg_instance.stop()
                break





