#!venv/bin/python
import cv2
import sys
import os
default_pattern="photo#.png"

#CHECKS AND TRIES TO LOAD CONFIGURATION
def load_config():
    if os.path.isfile("config.cfg"):
        config_file=open("config.cfg","r")
        config=config_file.read()
        config_args=config.split("\n")
        if len(config_args)>0:
            for arg in config_args:
                if len(arg.split(":"))>1:
                    photo_taker(arg.split(":")[1])
        else:
            return False

#STRIPS FILE NAME FROM PATH       
def filess_path(path):
    new_path=path.split("/")
    if len(path.split("/"))>1:
        new_path.pop()
        new_path="".join(new_path)
    else:
        new_path=""
    return new_path

#CHECKS PATH AND THROWS AN ERROR WHEN MORE THEN ONE ARG PASSED
def process_args(args):
    if len(args)>2:
        print("cli-photo-collecter takes in one argument cli-photo-collector 'savetamplate', but "+str(len(args))+" were passed.")
    else:
        path=args[1]
        if os.path.isdir(filess_path(path)) ==True or filess_path(path)=="":
            if path.count("#")>0:
                if path.count(".")>0:
                    photo_taker(path)
                else:
                    print("No file extension")
            else:
                print("No indexer added add # in your file_name exmaple: my_image#.png")

        else:
            print("Path doesn't exist. Directory has to be created beforehand")
            sys.exit()

#MAIN ACTION FUNCTION INPUT IS FILE PATH TEMPLATE PATH/FILE#.PNG #=IS REPLACED BY INDEX 
def photo_taker(path):
    try:
        stream = cv2.VideoCapture(0)
        index = 0
        if stream.isOpened()==False:
            print("camera not found")
            sys.exit()
        else:
            while(True):
                ret, frame = stream.read()
                if ret:
                    if cv2.waitKey(1) & 0xFF == 32:
                        print("Saving : "+path.replace("#",str(index)))
                        cv2.imwrite(path.replace("#",str(index)), frame)
                        index=index+1
                    if cv2.waitKey(1) & 0xFF == 27:
                        break

                    frame=cv2.flip(frame, 1)
                    cv2.imshow('camera feed', frame)
                else:
                    print("Lost connection with camera.")
                    break
            stream.release()
            cv2.destroyAllWindows()
    except Exception as e:
        print(e)
        

    
#FIRST CHECK FOR ARGUMENTS =>use pattern from agument
#NONE PASSED CHECKS FOR CONFIG =>use pattern from config file
#NO ARGS PASSED NO CONFIG IS FOUND=>fallback to default_pattern
def main():
    if len(sys.argv)>1:
        process_args(sys.argv)
    else:
        found=load_config()
        if found ==False:
            filess_path(default_pattern)

if __name__=="__main__":
    main()



