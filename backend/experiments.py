

TotalTime = 134
duration = 30


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

print(splitMyVideo(57.43, 30))
         