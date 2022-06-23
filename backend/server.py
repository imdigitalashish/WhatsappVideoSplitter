from distutils.command.upload import upload
import os
import random
import subprocess
from time import time
from fastapi import BackgroundTasks, FastAPI, File, Response, UploadFile

from datetime import timedelta

app = FastAPI()
def get_length(input_video):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_video], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)

def specific_string(length):  
    sample_string = 'pqrstuvwxakjlrasjfasdf32479vnvmnxc3i483y' 
    result = ''.join((random.choice(sample_string)) for x in range(length))  
    return result 

def convertToHourSeconds(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60


      
    return "%d:%02d:%02d" % (hour, minutes, seconds)


def splitMyVideo(TotalTime, duration):

    splits_happened = []

    splitsToBeDone = True

    currentDuration = 0
    obj = {}
    if(TotalTime<duration):
        obj["start"] = 0
        obj["end"] = TotalTime
        splits_happened.append(obj)
        splitsToBeDone = False


    while splitsToBeDone:
        obj = {}
      
        if((TotalTime - currentDuration ) < 30):
            obj["start"] = convertToHourSeconds(currentDuration)
            obj["end"] = convertToHourSeconds(TotalTime)
            splitsToBeDone = False
        else:
            obj["start"] = convertToHourSeconds(currentDuration)
            temp = currentDuration + 30
            print("The current duration is: ", currentDuration)
            obj["end"] =convertToHourSeconds(temp)

            currentDuration = currentDuration + 30
            print((TotalTime - currentDuration ) < 30)
        
        splits_happened.append(obj)


        
    return splits_happened


def runbackgroundcommand(command):
    os.system(command=command)

@app.post("/", status_code=200)
async def index(rs: Response,file: UploadFile = File(...)):

    success = False
    extension = ""

    uploaded_fileName = file.filename.replace(" ", "-").replace('""', '')

    try:
        contents = await file.read()
        
        with open(uploaded_fileName, 'wb') as f:
            f.write(contents)
            success = True
            extension = "."+file.content_type.split("/")[1]
    except Exception as e:
        return {"message": "There was an error uploading the file" + str(e)}
    finally:

        await file.close()




    if (success == True):
        video = get_length(uploaded_fileName)

        time_intervals = splitMyVideo(video, 30)


        print(time_intervals)


        

        filename = uploaded_fileName
        random_string = specific_string(10)
        print(random_string)


        # os.system("ffmpeg -i video.mp4 -ss 0 -t 30 firstvideo.mp4")
        print(time_intervals)


        filenames = []
        iteration = 0
        for i in time_intervals:
            print(i["start"], i["end"])
            # background.add_task(runbackgroundcommand, f"ffmpeg -i {filename} -ss {i['start']} -t 30 {random_string}{iteration}{iteration+1}firstvideo.mp4")
            os.system(f"ffmpeg -i {filename} -ss {i['start']} -t 30 {random_string}{iteration}{iteration+1}{filename}")
            iteration+= 1
            filenames.append(f"{random_string}{iteration}{iteration+1}{filename}")



        print
        return {"response": filenames}
    else:
        rs.status_code = 404
        return {'response', "failed"}
        

    