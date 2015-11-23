import config
from os import listdir, makedirs
from os.path import isfile, join, exists
from pydub import AudioSegment

def isMp3File(file):
    return isfile(join(config.inputDir, file)) & file.endswith('.mp3')

mp3FileNames = [file for file in listdir(config.inputDir) if isMp3File(file)]
mp3FileNames.sort()
print(mp3FileNames)

newFilesCountRange = range(0, ((len(mp3FileNames) - 1 ) / config.songsPerFile) + 1 )
songBlocks = dict()

for i in newFilesCountRange:
    if(i >= len(config.outputNames)):
        print 'Too many files in input dir. Skipping some'
        break

    songBlockRange = range(i * config.songsPerFile, (i + 1) * config.songsPerFile)
    songBlock = [mp3FileNames[j] for j in songBlockRange if j < len(mp3FileNames)]
    songBlocks[config.outputNames[i]] = songBlock

print songBlocks

if not exists(config.outputDir):
    makedirs(config.outputDir)

for outputName in songBlocks:
    songs = songBlocks[outputName]
    inputSounds = [AudioSegment.from_mp3(join(config.inputDir, song)) for song in songs]
    outputSound = reduce(AudioSegment.append, inputSounds)

    outputFile = join(config.outputDir, outputName)
    outputSound.export(outputFile + '.mp3', format='mp3', bitrate='320k')

    print 'Exported ' + outputName + ' from ' + str(songs);