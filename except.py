import sys  
try:  
    a=b  
    b=c  
except:  
    info=sys.exc_info()  
    print info[0],":",info[1]