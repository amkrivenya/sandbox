#!/usr/bin/python
import os
#import array
#from typing import List

def folder_scan(name):

  vProcFile = open('07_in.txt', mode="r")
  vFldrSize=0
  vDone=0
  vOn=0

  for line in vProcFile:

    if line.find('$ cd '+name) >= 0: vOn=1

    if line.find('$ cd') >= 0 and line.find('$ cd '+name) < 0: vOn=0; vDone=1

    if line[0] >= "0" and line[0] <= "9" and vOn:
      vFldrSize = vFldrSize + int( line[ : line.find(" ") ] )
      print('vFldrSize in proc: ', line, vFldrSize)

    if line[0:3] == 'dir' and vOn: 
#      print('recurse call=',line[4: len(line) - 1 ],' recurse result=',folder_scan(line[4: len(line) - 1]))
      vFldrSize = vFldrSize + folder_scan(line[4: len(line) - 1])
      print('Recurse proc call: ', line, vFldrSize)
                              
    if vDone: break

  vProcFile.close()
  return vFldrSize


vcFile='07_in.txt'
vcFileOut='07_out.txt'
vfFile = open(vcFile, mode="r")
vfFileOut = open(vcFileOut, mode="w")
vLevel=0

i=0
vFileSize=0
vFldrSize=0
vAll=0
pwd=''
for line in vfFile:

#  i += 1; print(i)

  if line[0] >= "0" and line[0] <= "9":
    vFldrSize = vFldrSize + int( line[ : line.find(" ") ] )
    print('Main vFldrSize: ', line, vFldrSize)

  if line[0:3] == 'dir': 
    vFldrSize = vFldrSize + folder_scan(line[4: len(line) - 1])
    print('Main proc call: ', line, vFldrSize, 'dir_name='+line[4: len(line) - 1])

  if line[0:4] == '$ cd': 
    if line[5: len(line) - 1] == "/": pwd ="/"; vfFileOut.write(pwd+'\n')
    else:
      if line[5: len(line) - 1] == "..":
        pwd = pwd[: pwd.rfind("/")]
        if pwd == "": pwd ="/"
      else:
        if pwd == "/": pwd = pwd + line[5: len(line) - 1]  
        else: pwd = pwd + '/' + line[5: len(line) - 1]  
        if vFldrSize < 100000: vAll = vAll + vFldrSize; print('+++ ',vAll)
        vFldrSize = 0

        vfFileOut.write(pwd+'\n')

print (vAll);
vfFile.close()
vfFileOut.close()
