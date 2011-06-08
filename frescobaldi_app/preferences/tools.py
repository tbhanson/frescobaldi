# This file is part of the Frescobaldi project, http://www.frescobaldi.org/
#
# Copyright (c) 2008 - 2011 by Wilbert Berendsen
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# See http://www.gnu.org/licenses/ for more information.

"""
Per-tool preferences.
"""

from __future__ import unicode_literals

from PyQt4.QtCore import QSettings, Qt
from PyQt4.QtGui import (
    QCheckBox, QDoubleSpinBox, QFont, QFontComboBox, QGridLayout, QHBoxLayout,
    QLabel, QSlider, QSpinBox, QVBoxLayout)

import app
import util
import preferences


class Tools(preferences.GroupsPage):
    def __init__(self, dialog):
        super(Tools, self).__init__(dialog)

        layout = QVBoxLayout()
        self.setLayout(layout)
        
        layout.addWidget(LogTool(self))
        layout.addWidget(MusicView(self))
        layout.addStretch(1)
            

class LogTool(preferences.Group):
    def __init__(self, page):
        super(LogTool, self).__init__(page)
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.fontLabel = QLabel()
        self.fontChooser = QFontComboBox(currentFontChanged=self.changed)
        self.fontSize = QDoubleSpinBox(valueChanged=self.changed)
        self.fontSize.setRange(6.0, 32.0)
        self.fontSize.setSingleStep(0.5)
        self.fontSize.setDecimals(1)

        box = QHBoxLayout()
        box.addWidget(self.fontLabel)
        box.addWidget(self.fontChooser, 1)
        box.addWidget(self.fontSize)
        layout.addLayout(box)
        
        self.showlog = QCheckBox(toggled=self.changed)
        layout.addWidget(self.showlog)
        
        self.rawview = QCheckBox(toggled=self.changed)
        layout.addWidget(self.rawview)
        
        app.translateUI(self)
        
    def translateUI(self):
        self.setTitle(_("LilyPond Log"))
        self.fontLabel.setText(_("Font:"))
        self.showlog.setText(_("Show log when a job is started"))
        self.rawview.setText(_("Display plain log output"))
        self.rawview.setToolTip(_(
            "If checked, Frescobaldi will not shorten filenames in the log output."""))
    
    def loadSettings(self):
        s = QSettings()
        s.beginGroup("log")
        font = QFont(s.value("fontfamily", "monospace"))
        font.setPointSizeF(float(s.value("fontsize", 9.0)))
        with util.signalsBlocked(self.fontChooser, self.fontSize):
            self.fontChooser.setCurrentFont(font)
            self.fontSize.setValue(font.pointSizeF())
        self.showlog.setChecked(s.value("show_on_start", True) not in (False, "false"))
        self.rawview.setChecked(s.value("rawview", True) not in (False, "false"))

    def saveSettings(self):
        s = QSettings()
        s.beginGroup("log")
        s.setValue("fontfamily", self.fontChooser.currentFont().family())
        s.setValue("fontsize", self.fontSize.value())
        s.setValue("show_on_start", self.showlog.isChecked())
        s.setValue("rawview", self.rawview.isChecked())


class MusicView(preferences.Group):
    def __init__(self, page):
        super(MusicView, self).__init__(page)
        
        layout = QGridLayout()
        self.setLayout(layout)

        self.magnifierSizeLabel = QLabel()
        self.magnifierSizeSlider = QSlider(Qt.Horizontal, valueChanged=self.changed)
        self.magnifierSizeSlider.setSingleStep(50)
        self.magnifierSizeSlider.setRange(200, 800)
        self.magnifierSizeSpinBox = QSpinBox()
        self.magnifierSizeSpinBox.setRange(200, 800)
        self.magnifierSizeSpinBox.valueChanged.connect(self.magnifierSizeSlider.setValue)
        self.magnifierSizeSlider.valueChanged.connect(self.magnifierSizeSpinBox.setValue)
        layout.addWidget(self.magnifierSizeLabel, 0, 0)
        layout.addWidget(self.magnifierSizeSlider, 0, 1)
        layout.addWidget(self.magnifierSizeSpinBox, 0, 2)
        
        self.magnifierScaleLabel = QLabel()
        self.magnifierScaleSlider = QSlider(Qt.Horizontal, valueChanged=self.changed)
        self.magnifierScaleSlider.setSingleStep(50)
        self.magnifierScaleSlider.setRange(200, 500)
        self.magnifierScaleSpinBox = QSpinBox()
        self.magnifierScaleSpinBox.setRange(200, 500)
        self.magnifierScaleSpinBox.valueChanged.connect(self.magnifierScaleSlider.setValue)
        self.magnifierScaleSlider.valueChanged.connect(self.magnifierScaleSpinBox.setValue)
        layout.addWidget(self.magnifierScaleLabel, 1, 0)
        layout.addWidget(self.magnifierScaleSlider, 1, 1)
        layout.addWidget(self.magnifierScaleSpinBox, 1, 2)
        
        app.translateUI(self)
        
    def translateUI(self):
        self.setTitle(_("Music View"))
        self.magnifierSizeLabel.setText(_("Magnifier Size:"))
        self.magnifierSizeLabel.setToolTip(_(
            "Size of the magnifier glass (Ctrl+Click in the Music View)\n"
            "(ranging from {min} to {max} pixels).").format(min=200, max=800))
        # L10N: as in "400 pixels", appended after number in spinbox, note the leading space
        self.magnifierSizeSpinBox.setSuffix(_(" pixels"))
        self.magnifierScaleLabel.setText(_("Magnifier Scale:"))
        self.magnifierScaleLabel.setToolTip(_(
            "Magnification of the magnifier\n"
            "(ranging from {min} to {max} percent).").format(min=200, max=500))
        self.magnifierScaleSpinBox.setSuffix(_("percent unit sign", "%"))
            
    def loadSettings(self):
        s = QSettings()
        s.beginGroup("musicview/magnifier")
        try:
            size = int(s.value("size", 300))
        except ValueError:
            size = 300
        self.magnifierSizeSlider.setValue(size)
        try:
            scale = int(s.value("scale", 300))
        except ValueError:
            scale = 300
        self.magnifierScaleSlider.setValue(scale)
    
    def saveSettings(self):
        s = QSettings()
        s.beginGroup("musicview/magnifier")
        s.setValue("size", self.magnifierSizeSlider.value())
        s.setValue("scale", self.magnifierScaleSlider.value())


