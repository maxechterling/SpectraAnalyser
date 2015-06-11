import matplotlib.pyplot as plt
import csv
import os

def makeLists(filename):
    '''Given a .csv file of emission spectra, returns tuple of lists: waves (list of wavelengths)
    and counts (counts per second at each wavelength)'''
    waves = []
    counts = []
    with open(filename) as opened:
        # Read .csv and put waves and counts data into lists
        for line in opened:
            splitted = line.split(',')
            waves.append(splitted[0])
            counts.append(splitted[1])
    # Get rid of column headers
    counts.remove(counts[0])
    counts.remove(counts[0])
    waves.remove(waves[0])
    waves.remove(waves[0])
    # Make values floats w/out line endings for counts, and make values integers for waves
    for i in range(len(counts)):
        waves[i] = int(waves[i])
        counts[i] = float(counts[i].strip('\n'))
    return waves, counts

def avgCPS(tupLists):
    '''Given a tuple of lists: waves and counts from makeLists(), returns the 
    average CPS from 340 to 360 nm'''
    # Define the index corresponding to 340 and 360 nm for use in counts list
    start = tupLists[0].index(340)
    end = tupLists[0].index(360)
    # Make counts list only containing values to be averaged
    counts2 = tupLists[1][start:end + 1]
    average = sum(counts2) / len(counts2)
    return average

def getInputFiles(filename):
    '''Given a .csv with input file information, returns tuple of lists: info which 
    describes information in file, and files which contains filenames. The first
    entry in both lists corresponds to the blank/buffer data'''
    info = []
    files = []
    # Read .csv and put info and files data into lists
    with open(filename) as opened:
        for line in opened:
            splitted = line.split(',')
            info.append(splitted[0])
            files.append(splitted[1])
    # Get rid of column headers
    info.remove(info[0])
    files.remove(files[0])
    # Make values floats w/out line endings for counts, and make values integers for waves
    for i in range(len(info)):
        if i != 0:
            info[i] = float(info[i])
        files[i] = files[i].strip('\n')
    return info, files

def getAllAverages(inputFiles):
    '''Given list of input files, returns list of CPS averages for each input'''
    Averages = []
    for line in inputFiles[1]:
        average = avgCPS(makeLists(line))
        Averages.append(average)
    return Averages

def dataForPlot(inputFiles):
    '''Given tuple of lists containing input file information (taken from getInputFiles)
    returns tuple of two lists: vols = list of titration volumes and avgs = volume
    corrected CPS averages'''
    # Get rid of blank from file info list
    vols = inputFiles[0][1:]
    # Correct average CPS for dilution and remove buffer baseline
    uncAvg = getAllAverages(inputFiles)
    corAvg = []
    for i in range(1, len(inputFiles[1])):
        val = uncAvg[i]
        buf = uncAvg[0]
        volume = inputFiles[0][i]
        bufCor = val - buf
        volCor = (bufCor * volume)/900.0
        corAvg.append(volCor)
    return vols, corAvg

def plotData(Data):
    '''Given the tuple of lists from dataForPlot, creates a plot of volume versus
    corrected CPS'''
    vol = Data[0]
    CPS = Data[1]
    plt.clf()
    plt.plot(vol,CPS, 'ro')
    plt.xlabel('Total Volume (microliters)')
    plt.ylabel('Corrected Counts/Second')
    # Puts y-axis in scientific notation
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.savefig('outputFigure1.png')
    plt.show()

def writeData(Data):
    '''Given a final to write to and the tuple of lists from dataForPlot, writes
    to a .csv document the results.'''
    #Need to convert data into .csv format
    csvLst = [['Volume(microliters)', 'Corrected CPS']]
    for i in range(len(Data[0])):
        pair = [Data[0][i], Data[1][i]]
        csvLst.append(pair)
    os.remove('outputDoc.csv')
    with open('outputDoc.csv', 'ab') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        writer.writerows(csvLst)
        
def main():
    '''When given an input CSV with a list of files and a description of their
    contents, writes to ouputDoc.csv and creates ouputFigure.png with a fluorescence
    titration assay analysis done on the input files.'''
    files = getInputFiles('Input Files.csv')
    analysedData = dataForPlot(files)
    plotData(analysedData)
    writeData(analysedData)

if __name__ == '__main__':
    main()
