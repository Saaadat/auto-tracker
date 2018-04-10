import sys
from PyQt4.QtCore import *
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import *
from PyQt4 import QtGui
import time
import gps_data_script as gps
import serial
from math import log10, floor
import maps as maps

global x,y
x = 10
y = 10

def round_sig(x, sig=2):
    if x == 0:
        return 0
    else:
        return round(x,sig-int(floor(log10(abs(x))))-1)

class gui(QtGui.QWidget,QObject):
    trigger = pyqtSignal()
    def __init__(self):
        super(gui, self).__init__()

        self.initUI()

    def initUI(self):

        #GPS DATA
        self.lbl1 = QLabel('GPS DATA', self)
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.lbl1)

        self.lbl2 = QLabel('TIME', self)
        self.lbl3 = QLabel('LAT', self)
        self.lbl4 = QLabel('LONG', self)
        self.lbl5 = QLabel('SPEED (kt/h)', self)
        self.lbl6 = QLabel('HEADING', self)
        self.lbl7 = QLabel('ALTITUDE (Ft)', self)
        self.lbl8 = QLabel('DISTANCE (Km)', self)
        self.lbl9 = QLabel('BEARING', self)
        self.lbl10 = QLabel('ELEVATION', self)
        
        hbox2 = QtGui.QHBoxLayout()
        #hbox.addStretch(1)
        hbox2.addWidget(self.lbl2)
        hbox2.addWidget(self.lbl3)
        hbox2.addWidget(self.lbl4)
        hbox2.addWidget(self.lbl5)
        hbox2.addWidget(self.lbl6)
        hbox2.addWidget(self.lbl7)
        hbox2.addWidget(self.lbl8)
        hbox2.addWidget(self.lbl9)
        hbox2.addWidget(self.lbl10)

        self.time = QLineEdit()
        self.time.setReadOnly(True)
        self.lat = QLineEdit()
        self.lat.setReadOnly(True)
        self.lon = QLineEdit()
        self.lon.setReadOnly(True)
        self.speed = QLineEdit()
        self.speed.setReadOnly(True)
        self.heading = QLineEdit()
        self.heading.setReadOnly(True)
        self.alt = QLineEdit()
        self.alt.setReadOnly(True)
        self.dist = QLineEdit()
        self.dist.setReadOnly(True)
        self.bearing = QLineEdit()
        self.bearing.setReadOnly(True)
        self.elevation = QLineEdit()
        self.elevation.setReadOnly(True)
        
        hbox3 = QtGui.QHBoxLayout()
        hbox3.addWidget(self.time)
        hbox3.addWidget(self.lat)
        hbox3.addWidget(self.lon)
        hbox3.addWidget(self.speed)
        hbox3.addWidget(self.heading)
        hbox3.addWidget(self.alt)
        hbox3.addWidget(self.dist)
        hbox3.addWidget(self.bearing)
        hbox3.addWidget(self.elevation)

        #OFFSETS
        self.lbl11 = QLabel('OFFSETS', self)
        hbox4 = QtGui.QHBoxLayout()
        hbox4.addWidget(self.lbl11)

        self.lbl12 = QLabel('AZIMUTH', self)
        self.azimuth1 = QLineEdit()
        self.azimuth1.setReadOnly(True)
        self.lbl13 = QLabel('AZIMUTH OFFSET', self)
        self.azimuth2 = QLineEdit()
        self.azimuth2.setText('0')
        self.b1 = QPushButton()
        self.b1.setText("<")
        self.b2 = QPushButton()
        self.b2.setText(">")
        self.b3 = QPushButton()
        self.b3.setText("R")
        self.lbl14 = QLabel('ELEVATION', self)
        self.elevation1 = QLineEdit()
        self.elevation1.setReadOnly(True)
        self.lbl15 = QLabel('ELEVATION OFFSET', self)
        self.elevation2 = QLineEdit()
        self.b4 = QPushButton()
        self.b4.setText("^")
        self.b5 = QPushButton()
        self.b5.setText("v")
        self.b6 = QPushButton()
        self.b6.setText("R")
        
        hbox5 = QtGui.QHBoxLayout()
        hbox5.addWidget(self.lbl12)
        hbox5.addWidget(self.azimuth1)
        hbox5.addWidget(self.lbl13)
        hbox5.addWidget(self.azimuth2)
        hbox5.addWidget(self.b1)
        hbox5.addWidget(self.b2)
        hbox5.addWidget(self.b3)
        hbox5.addWidget(self.lbl14)
        hbox5.addWidget(self.elevation1)
        hbox5.addWidget(self.lbl15)
        hbox5.addWidget(self.elevation2)
        hbox5.addWidget(self.b4)
        hbox5.addWidget(self.b5)
        hbox5.addWidget(self.b6)

        #DISTANCE THRESHOLD
        self.lbl16 = QLabel('DISTANCE THRESHOLD', self)
        self.lbl17 = QLabel('Auto Track Distance Limit', self)
        self.autoTrackLimit = QLineEdit()
        self.autoTrackLimit.setReadOnly(True)
        self.lbl18 = QLabel('Auto Zenithal', self)
        self.cb1 = QCheckBox()
        self.cb1.setChecked(True)
        

        
        h1box = QtGui.QHBoxLayout()
        h1box.addWidget(self.lbl16)
        h2box = QtGui.QHBoxLayout()
        h2box.addWidget(self.lbl17)
        h2box.addWidget(self.autoTrackLimit)
        h3box = QtGui.QHBoxLayout()
        h3box.addWidget(self.lbl18)
        h3box.addWidget(self.cb1)
        #h3box.addWidget(pic)

        vbox2 = QtGui.QVBoxLayout()
        vbox2.addLayout(h1box)
        vbox2.addStretch(1)
        vbox2.addLayout(h2box)
        vbox2.addLayout(h3box)
        vbox2.addStretch(3)

        #TRACKET POSITION
        self.lbl19 = QLabel('TRACKER POSITION', self)
        self.lbl20 = QLabel('POSITION COMMAND', self)
        self.lbl21 = QLabel('POSITION PRESENT', self)
        self.lbl22 = QLabel('AZIMUTH', self)
        self.azimuth3 = QLineEdit()
        self.lbl23 = QLabel('AZIMUTH', self)
        self.azimuth4 = QLineEdit()
        self.lbl24 = QLabel('ELEVATION', self)
        self.elevation3 = QLineEdit()
        self.lbl25 = QLabel('ELEVATION', self)
        self.elevation4 = QLineEdit()
        self.b7 = QPushButton()
        self.b7.setText('AUTO')
        self.b8 = QPushButton()
        self.b8.setText('ENABLE')
        self.b9 = QPushButton()
        self.b9.setText('DISABLE')
        #self.b9.setEnabled(False)
        self.b10 = QPushButton()
        self.b10.setText('EXIT')

        h4box = QtGui.QHBoxLayout()
        h4box.addWidget(self.lbl19)
        h5box = QtGui.QHBoxLayout()
        h5box.addWidget(self.lbl20)
        h5box.addWidget(self.lbl21)
        h6box = QtGui.QHBoxLayout()
        h6box.addWidget(self.lbl22)
        h6box.addWidget(self.azimuth3)
        h6box.addWidget(self.lbl23)
        h6box.addWidget(self.azimuth4)
        h7box = QtGui.QHBoxLayout()
        h7box.addWidget(self.lbl24)
        h7box.addWidget(self.elevation3)
        h7box.addWidget(self.lbl25)
        h7box.addWidget(self.elevation4)
        h8box = QtGui.QHBoxLayout()
        h8box.addWidget(self.b7)
        h8box.addWidget(self.b8)
        h8box.addWidget(self.b9)
        h8box.addWidget(self.b10)

        #MAP SETTINGS
        #self.pic2 = QImage("tempt.png")
        maps.currentmap(2.9,101.8)
        self.pic = QLabel(self)
        self.pic.setPixmap(QPixmap(QImage("tempt.png")))
        #pic.show()
        global h99box
        h99box = QtGui.QHBoxLayout()
        h99box.addWidget(self.pic)

        global vbox3
        vbox3 = QtGui.QVBoxLayout()
        vbox3.addLayout(h4box)
        vbox3.addStretch(1)
        vbox3.addLayout(h5box)
        vbox3.addLayout(h6box)
        vbox3.addLayout(h7box)
        vbox3.addStretch(1)
        vbox3.addLayout(h99box)
        vbox3.addLayout(h8box)

        #STATUS_MESSAGE
        self.lbl26 = QLabel('STATUS MESSAGES', self)
        self.msgBox = QTextEdit()
        self.msgBox.setReadOnly(True)

        global h9box,h10box,vbox4,hbox6
        h9box = QtGui.QHBoxLayout()
        h9box.addWidget(self.lbl26)
        h10box = QtGui.QHBoxLayout()
        h10box.addWidget(self.msgBox)

                
        vbox4 = QtGui.QVBoxLayout()
        vbox4.addLayout(h9box)
        vbox4.addLayout(h10box)
        vbox4.addStretch(1)

        hbox6 = QtGui.QHBoxLayout()
        hbox6.addLayout(vbox2)
        hbox6.addLayout(vbox3)
        hbox6.addLayout(vbox4)

        #PORT CONFIGURATION
        self.lbl27 = QLabel('PORT CONFIGURATION', self)
        self.lbl28 = QLabel('INTERFACE PORT', self)
        self.com1 = QComboBox()
        self.com1.addItem('COM1')
        self.com1.addItem('COM3')
        self.com1.addItem('COM10')
        self.lbl29 = QLabel('BAUD', self)
        self.baud1 = QComboBox()
        self.baud1.addItem('4800')
        self.baud1.addItem('9600')
        self.baud1.addItem('19200')
        self.lbl30 = QLabel('GPS PORT', self)
        self.com2 = QComboBox()
        self.com2.addItem('COM1')
        self.com2.addItem('COM3')
        self.com2.addItem('COM10')
        self.lbl31 = QLabel('BAUD', self)
        self.baud2 = QComboBox()
        self.baud2.addItem('4800')
        self.baud2.addItem('9600')
        self.baud2.addItem('19200')

        global h11box,h12box
        h11box = QtGui.QHBoxLayout()
        h11box.addWidget(self.lbl27)
        h12box = QtGui.QHBoxLayout()
        h12box.addWidget(self.lbl28)
        h12box.addWidget(self.com1)
        h12box.addWidget(self.lbl29)
        h12box.addWidget(self.baud1)
        h12box.addWidget(self.lbl30)
        h12box.addWidget(self.com2)
        h12box.addWidget(self.lbl31)
        h12box.addWidget(self.baud2)

        #GROUND CONTROL STATION
        self.lbl32 = QLabel('GROUND CONTROL STATION', self)
        self.lbl33 = QLabel('LATITUDE', self)
        self.lat2 = QLineEdit()
        self.lat2.setText('2.883161')
        self.lbl34 = QLabel('LONGITUDE', self)
        self.lon2 = QLineEdit()
        self.lon2.setText('101.679512')
        self.lbl35 = QLabel('ALTITUDE (Ft)', self)
        self.alt2 = QLineEdit()

        h13box = QtGui.QHBoxLayout()
        h13box.addWidget(self.lbl32)
        h14box = QtGui.QHBoxLayout()
        h14box.addWidget(self.lbl33)
        h14box.addWidget(self.lat2)
        h14box.addWidget(self.lbl34)
        h14box.addWidget(self.lon2)
        h14box.addWidget(self.lbl35)
        h14box.addWidget(self.alt2)

        vbox5 = QtGui.QVBoxLayout()
        vbox5.addLayout(h11box)
        vbox5.addLayout(h12box)
        vbox5.addLayout(h13box)
        vbox5.addLayout(h14box)

        #CONFIG BUTTON
        self.config = QPushButton()
        self.config.setText('Configure')

        h15box = QtGui.QHBoxLayout()
        h15box.addWidget(self.config)

        h16box = QtGui.QHBoxLayout()
        h16box.addLayout(vbox5)
        h16box.addLayout(h15box)
        
        
        #FINAL VBOX
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addStretch(1)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addStretch(1)
        vbox.addLayout(hbox6)
        vbox.addStretch(1)
        vbox.addLayout(h16box)
        vbox.addStretch(1)
        
        self.setLayout(vbox)
        self.setGeometry(50,50,1200,650)
        self.setFixedSize(1200, 650)

        self.connect(self.config, SIGNAL("clicked()"), self.config_clicked)
        self.connect(self.b1, SIGNAL("clicked()"), self.b1_clicked)
        self.connect(self.b2, SIGNAL("clicked()"), self.b2_clicked)
        self.connect(self.b3, SIGNAL("clicked()"), self.b3_clicked)
        self.connect(self.b7, SIGNAL("clicked()"), self.auto_clicked)
        self.connect(self.b8, SIGNAL("clicked()"), self.enabled_clicked)
        self.connect(self.b9, SIGNAL("clicked()"), self.disabled_clicked)
        self.connect(self.b10, SIGNAL("clicked()"), self.exit_clicked)
        self.trigger.connect(self.change_map)        
        
        self.setWindowTitle('AUTO TRACKING SYSTEM')
        self.Config_Thread = Config_Thread()
        self.AutoTrack_Thread = AutoTrack_Thread()
        self.AutoTrackEnable_Thread = AutoTrackEnable_Thread()
        self.Map_Thread = Map_Thread()
        self.show()

        #print self.lat2.text()

    def change_map(self):
        maps.currentmap((self.lat.text()),(self.lon.text()))
        self.pic.setPixmap(QPixmap("tempt.png"))
        
    def b1_clicked(self):
        self.azimuth2.setText(str(int(self.azimuth2.text()) - 1))

    def b2_clicked(self):
        self.azimuth2.setText(str(int(self.azimuth2.text()) + 1))

    def b3_clicked(self):
        self.azimuth2.setText(str(0))

        
    def config_clicked(self):

        global lat_current, lon_current
        lat_current = ex.lat2.text()
        lon_current = ex.lon2.text()

        if len(lat_current) != 0 and len(lon_current) != 0:
            self.Config_Thread.start()

        else:
            ex.msgBox.append('Please enter lattitude and longitude')

    def auto_clicked(self):
        self.AutoTrack_Thread.start()

    def enabled_clicked(self):
        self.AutoTrackEnable_Thread.start()

    def disabled_clicked(self):
        lat = self.lat.text()
        lon = self.lon.text()
        self.change_map(lat,lon)
        print 'working'

    def exit_clicked(self):
        self.AutoTrackEnable_Thread.quit()
        self.AutoTrack_Thread.quit()
        self.Config_Thread.quit()
        self.Map_Thread.quit()
        sys.exit()

class Map_Thread(QThread):
    def __init__(self):
        super(Map_Thread, self).__init__()

    def run(self):
        #ex.msgBox.append('Configure Button Pressed')
        #while True:
        lat = ex.lat.text()
        lon = ex.lon.text()
        print lat, lon

        #ex.lat2.setText('asfaf')
        time.sleep(1)
            
    

class Config_Thread(QThread):
    def __init__(self):
        super(Config_Thread, self).__init__()

    def run(self):
        ex.msgBox.append('Configure Button Pressed')
        
        
        while True:
            
            ex.time.setText(time.strftime("%H:%M:%S"))
            time.sleep(1)
            #ex.msgBox.append('ERROR CONNECTION TO PIXHAWK2')

            #try:
            alt, lat, lon, speed, heading = gps.raw_data()
            #except urllib2.HTTPError:
                #print 'error'
                #alt, lat, lon, speed, heading = 0,0,0,0,0

            if lat == 0 or lon == 0:
                pass
            else:
                try:
                    lat = float(lat)/10000000
                    lon = float(lon)/10000000
                except ValueError, e:
                    lat = 0
                    lon = 0
            
            try:
                azimuth = gps.azimuth(float(lat_current), float(lon_current),
                                      float(lat),float(lon))
            except ValueError, e:
                azimuth = float(0)

            
            bearing = gps.bearing(azimuth)

            distance = gps.distance(float(lat_current), float(lon_current),
                                  float(lat),float(lon))
            try:
                ex.alt.setText(str(round_sig(float(alt))))
            except ValueError, e:
                ex.alt.setText('0')
            ex.lat.setText(str(lat))
            ex.lon.setText(str(lon))
            try:
                ex.speed.setText(str(speed))
            except ValueError, e:
                ex.speed.setText('0')
            try:
                ex.heading.setText(str(heading))
            except ValueError, e:
                ex.heading.setText('0')
            ex.azimuth1.setText(str(azimuth))
            ex.bearing.setText(str(bearing))
            ex.dist.setText(str(distance))
            if ex.lat != '' and ex.lon !='':
                ex.trigger.emit()
            

class AutoTrack_Thread(QThread):
    def __init__(self):
        super(AutoTrack_Thread, self).__init__()

    def run(self):
        ex.msgBox.append('Auto-Tracking Started')
        if len(ex.azimuth1.text()) != 0:
            while True:
                azimuth_val = str(ex.azimuth1.text())
                ex.azimuth3.setText(str(int(ex.azimuth1.text())+int(ex.azimuth2.text())))

class AutoTrackEnable_Thread(QThread):
    def __init__(self):
        super(AutoTrackEnable_Thread, self).__init__()

    def run(self):
        ex.msgBox.append('Serial Port Connected')
        ser = serial.Serial('COM10', 9600, timeout=0,parity=serial.PARITY_NONE, rtscts=0)

        #ser.write('verbose 0\r\n')
        ser.write('PC 0\r\n')
        ser.write('VS 0\r\n')
        time.sleep(.1)
        #ser.flush()
        ser.readline()
        ser.readline()
        current_azimuth = 0.0
        #ser.readline()
        #ser.readline()
        while True:
            #data = float(ex.azimuth1.text())
            
            alt, lat, lon, speed, heading = gps.raw_data()
            #except urllib2.HTTPError:
                #print 'error'
                #alt, lat, lon, speed, heading = 0,0,0,0,0

            if lat == 0 or lon == 0:
                pass
            else:
                try:
                    lat = float(lat)/10000000
                    lon = float(lon)/10000000
                except ValueError, e:
                    lat = 0
                    lon = 0
            
            try:
                azimuth1 = gps.azimuth(float(lat_current), float(lon_current),
                                      float(lat),float(lon))
            except ValueError, e:
                azimuth1 = float(0)

            data = float(azimuth1)    
            if data == 0:
                move = 'ma ' + '0\r\n' #str(float(data/360)) + '\r\n'
            else:
                move = 'ma ' + str(float(round_sig(data/360))) + '\r\n'

            diff = abs(current_azimuth-(float(round_sig(data/360))))
            #print 'diff = {}    move = {}   curr = {}'.format(diff,move,current_azimuth)

            ex.azimuth4.setText(str(int(current_azimuth*360)))
            
            if diff >= 0.01 and diff <= 0.2:
                #print abs(current_azimuth-(float(round_sig(data/360))))
                ser.write('VR 0.1 \r\n')
                time.sleep(.1)
                ser.write(move)
                time.sleep(.1)
                current_azimuth = float(round_sig(data/360))

            elif diff > 0.2:
                ser.write('VR 0.5 \r\n')
                time.sleep(.1)
                ser.write(move)
                time.sleep(.1)
                current_azimuth = float(round_sig(data/360))


            ser.readline()
            ser.readline()
            pc = 'pc\r\n'
            ser.write(pc)
            time.sleep(.1)
            dummy1 = ser.readline()
            dummy = ser.readline()
            
            #print dummy
            if len(dummy) > 3:
                pass
                #ex.azimuth4.setText(str(int(360*float(dummy[5:len(dummy)-6]))))
            ser.flush()
            time.sleep(3)
            

    

        

def main():

    app = QtGui.QApplication(sys.argv)
    global ex
    ex = gui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
