#!/usr/bin/env python
# coding: utf-8

# In[3]:


from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import os

# 定義一個叫做PhotoEditor的class
class PhotoEditor:
    def __init__(self, window):
        # 初始化PhotoEditor class，將傳入的window物件賦值給實例變數window
        self.window = window
        # 設定應用程式標題為"修圖神器"
        self.window.title("修圖神器")
        # 建立應用程式的所有widget
        self.setup_widgets()

    def setup_widgets(self):
        # 在頂部建立一個Frame widget
        top_frame = Frame(self.window)
        top_frame.pack(side=TOP, fill=X, padx=10, pady=10)
        
        # 在頂部frame中建立一個Label widget，用於顯示"修圖神器"
        retouch_label = Label(top_frame, text="修圖神器", font=("Microsoft JhengHei UI", 30, "bold"))
        retouch_label.pack(side=LEFT, anchor=N, padx=(30, 0), pady=(33, 0))

        # 在頂部frame中建立一個Button widget，用於選擇圖片
        self.load_button = Button(top_frame, text="選擇圖片", command=self.load_image, width=13, height=2, font=("Microsoft JhengHei UI", 18))
        self.load_button.pack(side=RIGHT, anchor=N, padx=10, pady=10)

        # 在主視窗中建立一個Frame widget
        self.main_frame = Frame(self.window)
        self.main_frame.pack(side=TOP, padx=10, pady=10)
        
        # 在主視窗中建立一個Canvas widget，用於顯示圖片
        self.canvas = Canvas(self.main_frame, width=500, height=500)
        self.canvas.pack(side=LEFT)
        
        # 建立一個控制frame，用於放置調整圖片效果的滑動條
        self.controls_frame = Frame(self.main_frame)
        self.controls_frame.pack(side=LEFT, padx=20)
        
        # 在底部建立一個Frame widget
        bottom_frame = Frame(self.window)
        bottom_frame.pack(side=BOTTOM, fill=X, padx=10, pady=10)
        
        # 在底部frame中建立一個Label widget，用於顯示"人工智慧與多尺度模擬實驗室"
        LAiMM_label = Label(bottom_frame, text="人工智慧與多尺度模擬實驗室", font=("Microsoft JhengHei UI", 24, "bold"))
        LAiMM_label.pack(side=LEFT, anchor=N, padx=10, pady=21)

        # 在底部frame中建立一個Button widget，用於儲存圖片
        self.save_button = Button(bottom_frame, text="儲存圖片", command=self.save_image, width=13, height=2, font=("Microsoft JhengHei UI", 18))
        self.save_button.pack(side=RIGHT, anchor=N, padx=10, pady=10) 

        # 建立多個滑動條，用於調整圖片的效果
        self.rotate_slider = self.create_slider("旋轉", from_=0, to=360, command=self.rotate_image)
        self.sharpness_slider = self.create_slider("銳利度", from_=0, to=200, command=self.adjust_sharpness)
        self.shadow_slider = self.create_slider("陰影度", from_=0, to=10, command=self.adjust_shadow)
        self.contrast_slider = self.create_slider("對比度", from_=0, to=10, command=self.adjust_contrast)
        self.brightness_slider = self.create_slider("亮度", from_=0, to=10, command=self.adjust_brightness)
        self.saturation_slider = self.create_slider("飽和度", from_=0, to=10, command=self.adjust_saturation)
        self.blur_slider = self.create_slider("模糊度", from_=0, to=100, command=self.adjust_blur)
        # 保存原始圖片的副本
        self.original_image = None

    def create_slider(self, name, from_, to, command):
        # 建立一個滑動條widget，用於調整圖片效果
        frame = Frame(self.controls_frame)
        frame.pack(pady=10, padx=1)

        label = Label(frame, text=name, width=11, font=("Microsoft JhengHei UI", 16))
        label.pack(side=LEFT)

        slider = Scale(frame, from_=from_, to=to, orient=HORIZONTAL, command=command, showvalue=0)
        slider.set(0)
        slider.pack(side=LEFT)

        return slider

    def load_image(self):
        # 打開一個檔案選擇對話框，選擇要編輯的圖片
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if self.image_path:
            # 如果成功選擇了圖片，則讀取該圖片並顯示在canvas中
            self.image = Image.open(self.image_path)
            self.original_image = self.image.copy()
            self.image.thumbnail((500, 500))
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(250, 250, image=self.photo)
            self.canvas.image = self.photo

    def rotate_image(self, value):
        # 旋轉圖片
        if self.image:
            self.image = self.original_image.copy()
            self.image.thumbnail((500, 500))
            self.image = self.image.rotate(int(value), resample=Image.BICUBIC, expand=True)
            self.update_canvas()

    def adjust_sharpness(self, value):
        # 調整圖片的銳利度
        self.image = self.original_image.copy()
        enhancer = ImageEnhance.Sharpness(self.image)
        self.image = enhancer.enhance(float(value) / 10)
        self.image.thumbnail((500, 500))
        self.update_canvas()

    def adjust_shadow(self, value):
        # 調整圖片的陰影效果
        self.image = self.original_image.copy()
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(1 - float(value) / 10)
        self.image.thumbnail((500, 500))
        self.update_canvas()

    def adjust_contrast(self, value):
        # 調整圖片的對比度
        self.image = self.original_image.copy()
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(1 + float(value) / 10)
        self.image.thumbnail((500, 500))
        self.update_canvas()

    def adjust_brightness(self, value):
        # 調整圖片的亮度
        self.image = self.original_image.copy()
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(1 + float(value) / 10)
        self.image.thumbnail((500, 500))
        self.update_canvas()

    def adjust_saturation(self, value):
        # 調整圖片的飽和度
        self.image = self.original_image.copy()
        enhancer = ImageEnhance.Color(self.image)
        self.image = enhancer.enhance(1 + float(value) / 10)
        self.image.thumbnail((500, 500))
        self.update_canvas()

    def adjust_blur(self, value):
        # 調整圖片的模糊度
        self.image = self.original_image.copy()
        self.image = self.image.filter(ImageFilter.GaussianBlur(radius=float(value) / 10))
        self.image.thumbnail((500, 500))
        self.update_canvas()

    def update_canvas(self):
        # 更新canvas中的圖片
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(250, 250, image=self.photo)
        self.canvas.image = self.photo

    def save_image(self):
        # 儲存圖片到檔案
        if self.image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                self.image.save(file_path)

if __name__ == "__main__":
    # 創建一個Tkinter的root widget      
    root = Tk()
    # 創建一個PhotoEditor的實例
    app = PhotoEditor(root)
    # 開始Tkinter的主循環
    root.mainloop()

