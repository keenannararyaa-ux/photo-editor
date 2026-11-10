import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog, QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from PIL import Image
from  PIL import ImageFilter
from PIL.ImageFilter import *

app = QApplication([])
window = QWidget()

window.setWindowTitle("Easy Editor")
window.resize(700,500)

btn_folder = QPushButton('Folder')
btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
btn_mirror = QPushButton('Mirror')
btn_sharp = QPushButton("Sharpness")
btn_bw = QPushButton("B/W")
btn_blurr = QPushButton("blurr")
btn_flip = QPushButton("Flip")

lw_files = QListWidget()
lb_image = QLabel("Image")

layout_left = QVBoxLayout()
layout_right = QVBoxLayout()
layout_btn = QHBoxLayout()
main_layout = QHBoxLayout()

layout_left.addWidget(btn_folder)
layout_left.addWidget(lw_files)

layout_btn.addWidget(btn_left)
layout_btn.addWidget(btn_right)
layout_btn.addWidget(btn_mirror)
layout_btn.addWidget(btn_sharp)
layout_btn.addWidget(btn_bw)
layout_btn.addWidget(btn_blurr)
layout_btn.addWidget(btn_flip)

layout_right.addWidget(lb_image,95)
layout_right.addLayout(layout_btn)

main_layout.addLayout(layout_left,stretch=1)
main_layout.addLayout(layout_right,stretch=5)

window.setLayout(main_layout)

workdir = ""

def chooseWorkdir():
   global workdir
   workdir = QFileDialog.getExistingDirectory()

def filter(files,extensions):
   result = []
   for filename in files:
      for ext in extensions:
         if filename.endswith(ext):
            result.append(filename)
   return result

def showFilenamesList():
   extensions = ['.jpg','.jpeg','.png','.gif','.bmp']
   chooseWorkdir()
   filenames = filter(os.listdir(workdir),extensions)
   lw_files.clear()
   for filename in filenames:
      lw_files.addItem(filename)

class ImageProcessor():
   def __init__(self):
      self.image = None
      self.filename = None
      self.dir = None
      self.save_dir = "Modified/"

   def loadImage(self,dir,filename):
      self.dir = dir
      self.filename = filename
      image_path = os.path.join(dir,filename)
      self.image = Image.open(image_path)

   def showImage(self,path):
      lb_image.hide()
      image = QPixmap(path)
      w,h = lb_image.width(),lb_image.height()
      image = image.scaled(w,h,Qt.KeepAspectRatio)
      lb_image.setPixmap(image)
      lb_image.show()

   def do_bw(self):
      self.image = self.image.convert('L')
      self.saveImage()
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)

   def do_left(self):
      self.image = self.image.transpose(Image.ROTATE_90)
      self.saveImage()
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)

   def do_right(self):
      self.image = self.image.transpose(Image.ROTATE_270)
      self.saveImage()
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)

   def do_mirror(self):
      self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
      self.saveImage()
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)

   def do_sharpness(self):
      self.image = self.image.filter(SHARPEN)
      self.saveImage()
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)

   def do_blurr(self):
      self.image = self.image.filter(BLUR)
      self.saveImage()
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)

   def do_flip(self):
      self.image = self.image.transpose(Image.ROTATE_180)
      self.saveImage()
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)

   def saveImage(self):
      path = os.path.join(self.dir,self.save_dir)
      if not(os.path.exists(path) or os.path.isdir(path)):
         os.mkdir(path)
      image_path =  os.path.join(path,self.filename)
      self.image.save(image_path)

    
work_image = ImageProcessor()
def showChosenImage():
   if lw_files.currentRow() >= 0:
      filename = lw_files.currentItem().text()
      work_image.loadImage(workdir,filename)
      image_path = os.path.join(workdir,filename)
      work_image.showImage(image_path)


lw_files.currentRowChanged.connect(showChosenImage)
btn_folder.clicked.connect(showFilenamesList)

btn_bw.clicked.connect(work_image.do_bw)
btn_left.clicked.connect(work_image.do_left)
btn_right.clicked.connect(work_image.do_right)
btn_mirror.clicked.connect(work_image.do_mirror)
btn_sharp.clicked.connect(work_image.do_sharpness)
btn_blurr.clicked.connect(work_image.do_blurr)
btn_flip.clicked.connect(work_image.do_flip)

window.show()
app.exec_()
