import matplotlib.pyplot as plt
import sys

def plot_loss(logname):
    logf = open(logname,"r")
    pairs = {}
    l = []
    smooth = []
    for line in logf.xreadlines():
        line = line.strip()
        IterString = "Iteration"
        IterPos = line.find(IterString)
        lossString = " loss "
        lossPos = line.find(lossString)
        if lossPos >= 0 and IterPos >= 0 :
            #print line[lossPos + len(lossString) + 2:]
            l.append(float(line[lossPos + len(lossString) + 2:]))
    for i in xrange(100,len(l)):
        t = 0
        for j in xrange(0,100):
            t = t + l[i - j]
        t = t / 100.0
        smooth.append(t)

    plt.plot(smooth)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: ./plot_loss log"
        sys.exit()
    plot_loss(sys.argv[1])