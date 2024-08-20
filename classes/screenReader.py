import cv2
import numpy as np
from mss import mss
from threading import Thread
import json
import os
import time

polygons = json.load(open('polygons.json', 'r'))

class ScreenReader(Thread):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.CAK_SIGNAL_POLYGON = polygons['polygons']['CAK_SIGNAL_POLYGON']
        self.CAK_SIGNALFOUND_POLYGON = polygons['polygons']['CAK_SIGNALFOUND_POLYGON']
        self.CAK_ENERGY_POLYGON = polygons['polygons']['CAK_ENERGY_POLYGON']

    def get_screenshot(self):
        with mss() as sct:
            return np.array(sct.grab(monitor={'top': 0, 'left': 0, 'width': self.width, 'height': self.height}))
    
    def get_pixels_by_polygon(self, polygon):
        points = polygon['points']
        
        # Находим минимальные и максимальные значения x и y
        min_x = min(point['x'] for point in points)
        max_x = max(point['x'] for point in points)
        min_y = min(point['y'] for point in points)
        max_y = max(point['y'] for point in points)
        
        # Определяем прямоугольную область
        monitor = {
            'top': min_y,
            'left': min_x,
            'width': max_x - min_x,
            'height': max_y - min_y
        }
        # Захватываем область экрана
        with mss() as sct:
            return sct.grab(monitor)
    
    def get_hex_array(self, polygon):
        return cv2.cvtColor(np.array(self.get_pixels_by_polygon(polygon)), cv2.COLOR_BGR2RGB)
        
    
    def write_to_file(self):
        os.remove('./trash/CAK_SIGNALFOUND_POLYGON.png')
        cv2.imwrite('./trash/CAK_SIGNAL_POLYGON.png', self.get_hex_array(self.CAK_SIGNAL_POLYGON))
        cv2.imwrite('./trash/CAK_SIGNALFOUND_POLYGON.png', self.get_hex_array(self.CAK_SIGNALFOUND_POLYGON))
        cv2.imwrite('./trash/CAK_ENERGY_POLYGON.png', self.get_hex_array(self.CAK_ENERGY_POLYGON))

    def compare_images_by_color(self, fc):
        img1 = cv2.imread("./trash/CAK_SIGNALFOUND_POLYGON_REF.png")
        img2 = cv2.imread("./trash/CAK_SIGNALFOUND_POLYGON.png")

        if img1 is None or img2 is None:
            raise ValueError("Одно или оба изображения не могут быть загружены.")

        hist1 = cv2.calcHist([img1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist2 = cv2.calcHist([img2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])

        # Нормализация гистограмм
        hist1 = cv2.normalize(hist1, hist1).flatten()
        hist2 = cv2.normalize(hist2, hist2).flatten()

        # Сравнение гистограмм
        comparison = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

        # Определение порогового значения для различий
        
        threshold = 0.90  # Можно настроить пороговое значение в зависимости от требуемой чувствительности
        print(f"fc: {fc}, threshold: {threshold}, comparison: {comparison}")
        # Возвращение результата
        return comparison < threshold
    
    def recognize(self):
        t1 = time.time()
        self.write_to_file()
        frames_count = 0
        while True:
            self.write_to_file()
            if self.compare_images_by_color(frames_count):
                return True
            frames_count += 1
            t2 = time.time()
            if t2 - t1 > 1:
                return False
        