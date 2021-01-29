import cv2

class CobitOpenCVCamRC:

    def __init__(self):
        print("test")
        self.frame = None
        self.ret = False
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 320)
        self.cap.set(4, 240)

    def get_frame(self):
        return self.frame

    def run(self):
        print("test")
        while True:
            print("test")
            self.ret, self.frame = self.cap.read()
            if self.ret:
                cv2.imshow("lane", self.frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        
    def finish(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    cam = CobitOpenCVCamRC()
    cam.run()
