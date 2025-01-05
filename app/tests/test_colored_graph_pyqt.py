import sys
import numpy as np
import pandas as pd
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow
from io import StringIO

# CSV Data
data = '''
Time (s),Frequency (Hz),Intensity (dB)
0.01,100,-10
0.01,200,-15
0.01,300,-10
0.02,100,-25
0.02,200,-18
0.02,300,-12
'''

# Load the CSV data into DataFrame
df = pd.read_csv(StringIO(data))

# Pivot the DataFrame to create a 2D array for plotting
spectrogram = df.pivot(index='Frequency (Hz)', columns='Time (s)', values='Intensity (dB)').T
intensities = spectrogram.values

app = QApplication(sys.argv)
mainWin = QMainWindow()
mainWin.setWindowTitle('Spectrogram Display')
mainWin.resize(800, 600)
mainWin.setStyleSheet("background-color:white;")
# Use GraphicsLayoutWidget for easy layout management
widget = pg.GraphicsLayoutWidget()
mainWin.setCentralWidget(widget)

maxX = 2.1
maxY = 3
plotItem = widget.addPlot()  # Add a plot area to the widget
plotItem.hideButtons()
plotItem.getViewBox().setMouseEnabled(x=False, y=False)
plotItem.getViewBox().setRange(xRange=[0, maxX], yRange=[0, maxY], padding=0)
plotItem.getViewBox().setXRange(0, maxX, padding=0)
plotItem.getViewBox().setYRange(0, maxY, padding=0)

imageItem = pg.ImageItem()
plotItem.addItem(imageItem)
imageItem.setImage(intensities)

# Setup colormap
colormap = pg.colormap.get('inferno', source='matplotlib')
imageItem.setLookupTable(colormap.getLookupTable())
plotItem.getAxis('left').setLabel('Frequency (Hz)')
plotItem.getAxis('bottom').setLabel('Time (s)')

# Add a color bar
colorBar = pg.ColorBarItem(interactive=False, colorMap=colormap)
colorBar.setImageItem(imageItem)
widget.addItem(colorBar)  # Properly add color bar to GraphicsLayoutWidget

mainWin.show()
sys.exit(app.exec_())
