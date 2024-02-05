#!venv/bin/python
import cv2
from pyautogui import prompt
import sys

def main():
    try:
        stream = cv2.VideoCapture(0)
        index = 0
    except:
        print("Unknown error")
    if stream.isOpened()==False:
        print("camera not found")
        sys.exit()
    filedir=prompt(text='Enter directory and file name for example mydir/img#.png # replaces order number.', title='Save to' , default='')
    while(True):
        ret, frame = stream.read()
        if ret:
            frame=cv2.flip(frame, 1)
            cv2.imshow('camera feed', frame)
            if cv2.waitKey(1) & 0xFF == 32:
                cv2.imwrite(filedir.replace("#",str(index)), frame)
                index=index+1
            if cv2.waitKey(1) & 0xFF == 27:
                break
        else:
            print("Lost connection with camera.")
            break
    stream.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()

