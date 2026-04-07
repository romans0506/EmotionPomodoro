import cv2
from deepface import DeepFace
from collections import deque

class EmotionPipeline:

    def __init__(self):
        self.history = deque(maxlen=30)
        self.cap = None

    def start_background(self, callback):
        self.cap = cv2.VideoCapture(0)

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            avg = self.analyze(frame)

            if avg:
                callback(avg)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        self.stop()




    def analyze(self, frame):
        try:
            results = DeepFace.analyze(frame,actions=['emotion'], enforce_detection = False, silent = True)
            emotion = results[0]['emotion']
            self.history.append(emotion)

        
            avg = {}
            for emotion in self.history[0].keys():
                avg[emotion] = sum(h[emotion] for h in self.history) / len(self.history)

            return avg

        except Exception as e:
            print (f"Error: {e}")
            return None

    def stop(self):
        if self.cap:
            self.cap.release()
        print ("Pipeline has stopped.")


    

        
           
       


