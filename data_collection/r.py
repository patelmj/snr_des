from time import time,sleep

starttime = time()
while time() - starttime<1:
    print((time()-starttime)*1000)
    sleep((10-((time()-starttime)*1000)%10)/1000)
