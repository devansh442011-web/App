import cv2
import requests
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

# 🔴 CHANGE THIS TO YOUR SERVER
SERVER_URL = "http://YOUR_SERVER_IP:5000/frame"

class CameraStreamApp(App):
    def build(self):
        self.img = Image()
        self.cap = cv2.VideoCapture(0)  # Android camera
        Clock.schedule_interval(self.update, 1/15)  # 15 FPS
        return self.img

    def update(self, dt):
        ret, frame = self.cap.read()
        if not ret:
            return

        # ---- SEND FRAME TO SERVER (RECORDING) ----
        _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        try:
            requests.post(
                SERVER_URL,
                files={"frame": buffer.tobytes()},
                timeout=0.1
            )
        except:
            pass  # ignore network delay

        # ---- SHOW PREVIEW ----
        frame = cv2.flip(frame, 0)
        texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]),
            colorfmt="bgr"
        )
        texture.blit_buffer(
            frame.tobytes(),
            colorfmt="bgr",
            bufferfmt="ubyte"
        )
        self.img.texture = texture

    def on_stop(self):
        self.cap.release()

if __name__ == "__main__":
    CameraStreamApp().run()