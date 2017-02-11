import sys, os, time,json
from stat import *


from PyQt4 import QtCore
from PyQt4 import QtGui


    
class mainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(mainWindow, self).__init__()
        self.defaultOpenDir = (r'c:\test')
        self.tabIndex = 0
        self.initalizeUI()


    def initalizeUI(self):
        
        #locations #######################################################################
        

        #defining widgets and attributes #################################################
        
        self.setWindowTitle("JSON Viewer")
        self.resize(350, 800)
        self.setMinimumSize(350,800)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setAcceptDrops(True)

        #main widgets 
        self.statusBar = QtGui.QStatusBar()
        self.main_Layout = QtGui.QVBoxLayout()
        

        #tabs
        self.tabHolder = QtGui.QTabWidget()
        self.tabHolder.setTabsClosable(True)
        self.tabHolder.tabCloseRequested.connect(self.closeFile)

        self.statusText = QtGui.QLabel()
        self.statusText.setText("Drag and Drop to open a file")
        self.statusIcon = QtGui.QToolButton()
        

        #menu bars ########################################################################
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('File')
        helpMenu = menuBar.addMenu('Help')

        #menu bar actions
        openFileItem = QtGui.QAction("Open File...", self, triggered = self.openFile)
        openFileItem.setShortcut('Ctrl+o')
        openFileItem.setStatusTip('Open JSON file')
        openFileItem.setIcon(self.style().standardIcon(QtGui.QStyle.SP_DirOpenIcon))
        
        exitAppItem = QtGui.QAction("Exit...", self, triggered =self.exitApp )
        exitAppItem.setIcon(self.style().standardIcon(QtGui.QStyle.SP_BrowserStop))

        #menu bar add actions
        fileMenu.addAction(openFileItem)
        fileMenu.addAction(exitAppItem)
    
        self.setCentralWidget(self.tabHolder)
        #statusBar 
        self.statusBar.addWidget(self.statusText,1)
        self.statusBar.addWidget(self.statusIcon,1)
        self.setStatusBar(self.statusBar)
        self.show()
 
    # main Json viewer window ##########################################################   
    def json_Viewer(self, data):
        
        jsonData = json.loads((data).read())
        #create Tree Widget to load file
        self.jsonViewer = QtGui.QTreeWidget()
        
        self.jsonViewer.setUniformRowHeights(True)
  
        parent = QtGui.QTreeWidgetItem(self.jsonViewer)   
        self.jsonViewer.invisibleRootItem()
        self.populateTree(parent, jsonData)
        

        #add tab with widget jsonViewer
        tabLabel = os.path.basename(str(data.name)).split(".")[0]
        self.tabHolder.addTab(self.jsonViewer, tabLabel)
    
    def populateTree(self, parent, value):

        self.jsonViewer.expandToDepth(3)

        if type(value) is dict:
            for key, val in sorted(value.iteritems()):
                child = QtGui.QTreeWidgetItem()    
                child.setText(0, str(key))
                if parent is None:
                    parent=self.jsonViewer.invisibleRootItem()
                parent.addChild(child)
                self.populateTree(child, val)

        elif type(value) is list:
            for v in value:
                child = QtGui.QTreeWidgetItem()
                parent.addChild(child)
                
                if type(v) is dict:
                    self.populateTree(child, v)
                elif type(v) is list:
                    child.setText(0, str(v[0]))
                    self.populateTree(child, v)
                else:
                    child.setText(0, str(v))              
                
                child.setExpanded(True)
    
    # application operations ###############################################################

    def openFile(self):

        self.jsonFile = QtGui.QFileDialog.getOpenFileName(self, 'Load JSON', self.defaultOpenDir)
        self.loadFile(self.jsonFile)
       
    
    def closeFile(self, currentIndex):
        #close selected tab
        currentWidget = self.tabHolder.widget(currentIndex)
        currentWidget.deleteLater()
        self.tabHolder.removeTab(currentIndex)
   
    def loadFile(self, file):
         if os.path.isfile(file):
            fileInstance = open(file, 'r+')
        
        
            with fileInstance:

                #display data
                self.json_Viewer(fileInstance)

                #set Status bar to show last modified time
                modifiedTime = str(time.ctime(os.path.getmtime(fileInstance.name)))
                tempText = ("Last modified: {0}").format(modifiedTime)
                self.statusText.setText(tempText)
                
                #set icon to show write status
                if os.access(self.jsonFile, os.W_OK):
                    self.statusIcon.setIcon(self.style().standardIcon(QtGui.QStyle.SP_DriveHDIcon))
                else:
                    self.statusIcon.setIcon(self.style().standardIcon(QtGui.QStyle.SP_BrowserStop))

    
    def exitApp(self):
        self.close()
    
        
    # drag and drop support #################################################################'
    
    def dragEnterEvent(self,event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self,event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                self.jsonFile = str(url.toLocalFile())
                self.loadFile(self.jsonFile)

      

def main():
    app = QtGui.QApplication(sys.argv)
    main_Window = mainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':

    main()