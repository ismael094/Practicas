def startScript(args):
    init = args.init
    end = args.end
    sentence = 'gLogviewer -l %s -L %s ' % (str(init), str(end))
    for item in range(1,37):
        segment = sentence+'M1CS/M1Segment%s/' % str(item)
        for positioner in range(1,4):
            positionerSentence = segment+'Positioner%s' % str(positioner)
            print positionerSentence
        else:
            sensor = segment+'EdgeSensor'
            print sensor
if __name__ == '__main__':
    import argparse
    import os
    import glob
    parser = argparse.ArgumentParser(description="Do you wish to scan?")
    parser.add_argument("-l", dest='init', action='store',help='Date init')
    parser.add_argument("-L", dest='end', action='store',\
    help='Date end', default=True)
    args = parser.parse_args()
    startScript(args)