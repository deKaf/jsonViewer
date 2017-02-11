import sys, os, pprint, time, re
from stat import *
import webbrowser

from PyQt4 import QtCore
from PyQt4 import QtGui


    
class mainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(mainWindow, self).__init__()
        self.initalizeUI()


    def initalizeUI(self):
        
        #locations #######################################################################
        self.defaultOpenDir = (r'c:\logging')

        #defining widgets and attributes #################################################
        
        self.setWindowTitle("JSON Viewer")
        self.resize(350, 800)
        self.setMinimumSize(350,800)
        
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.statusBar = QtGui.QStatusBar()
        self.main_Layout = QtGui.QVBoxLayout()
        self.jsonViewer = QtGui.QTextEdit()

        self.tabHolder = QtGui.QTabWidget()
        

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
    
    def jsonViewer(self):
        #self.jsonViewer = QtGui.QTreeView()
        pass
        
    def exitApp(self):
        self.close()
        
        

    def openFile(self):

        jsonFile = QtGui.QFileDialog.getOpenFileName(self, 'Load JSON', self.defaultOpenDir)

        fileInstance = open(jsonFile, 'r')
        
        with fileInstance:
            data = fileInstance.read()
            #display data
            self.jsonViewer.setText(data)
            self.tabHolder.addTab(self.jsonViewer, fileInstance.name)
            #set Status bar to show last modified time
            modifiedTime = str(time.ctime(os.path.getmtime(fileInstance.name)))
            tempText = ("Last modified: {0}").format(modifiedTime)
            self.statusText.setText(tempText)
            #set icon to show write status

            if os.access(jsonFile, os.W_OK):
                self.statusIcon.setIcon(self.style().standardIcon(QtGui.QStyle.SP_DriveHDIcon))
            else:
                self.statusIcon.setIcon(self.style().standardIcon(QtGui.QStyle.SP_BrowserStop))

            

      

def main():
    app = QtGui.QApplication(sys.argv)
    main_Window = mainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':

    main()