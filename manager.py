import nbamodel
import nflmodel
import sys
def fullB(str1,str2,type):
    if type == "Score Differential":
        return nbamodel.start(str1,str2,"score")
    else:
        return nbamodel.start(str1,str2,"attend")

def fullF(str1,str2):
    return nflmodel.start(str1,str2)

if __name__ == '__main__':
    if sys.argv[3] == "fb":
        print(fullF(sys.argv[1],sys.argv[2]))
    else:
        print(fullB(sys.argv[1],sys.argv[2],sys.argv[3]))
