import email
import sys
from importlib_metadata import entry_points
import pymsgbox
import sqlite3
from unicodedata import name
from PyQt5 import QtWidgets,uic
import icons_rc
import RTSP
 

app = QtWidgets.QApplication([ ])
main_win = uic.loadUi('App.ui')


def showpage_1():
    main_win.stackedWidget.setCurrentWidget(main_win.page_2)
    
def showpage_2():
    main_win.stackedWidget.setCurrentWidget(main_win.page_3)

def alert():
    pymsgbox.alert('Please Login First!!','Alert')
    

def execute():
    m = main_win.lineEdit.text()
    RTSP.gogo(m)
    import DDDSystem

def login():
    email1 = main_win.lineEdit_5.text()
    password1 = main_win.lineEdit_4.text() 
    data = sqlite3.connect('Database.db')
    cursor = data.cursor()
    cursor.execute("SELECT * FROM SignUpData where Email=? AND Password=?",(email1, password1))
    checkinfo = cursor.fetchone()
    if checkinfo:
        pymsgbox.alert('Log In Successful!\n\nWELCOME!!!', 'Alert')
        showpage_2()
    else:
        pymsgbox.alert('Log In Failed!\n\nTry again with valid User and Password!!!', 'Alert')
        main_win.lineEdit_5.clear() 
        main_win.lineEdit_4.clear() 
    data.commit()
    data.close()
    
    main_win.lineEdit_5.clear() 
    main_win.lineEdit_4.clear() 
    

def reset2():
    main_win.lineEdit_5.clear() 
    main_win.lineEdit_4.clear() 


main_win.pushButton_2.clicked.connect(showpage_1)
main_win.pushButton.clicked.connect(showpage_1)
main_win.pushButton_3.clicked.connect(alert)

main_win.pushButton_5.clicked.connect(execute)
main_win.pushButton_11.clicked.connect(login)
main_win.pushButton_10.clicked.connect(reset2)



main_win.show()

sys.exit(app.exec())

    
