import os
import sys
import subprocess

def get_length_in_seconds(filename):
  result = subprocess.Popen(["ffprobe", filename], \
  	stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
  d = [x for x in result.stdout.readlines() if "Duration" in x]
  mins = int(d[0].split()[1].split(':')[1])
  secs = int(d[0].split()[1].split(':')[2].split('.')[0])
  milis = int(d[0].split()[1].split(':')[2].split('.')[1][:-1])
  total_secs = mins*60+secs
  if milis > 50:
  	total_secs += 1
  return total_secs

cwd = os.getcwd()
current_folder_name = cwd.split('/')[-1]
current_folder_name = current_folder_name.replace(' ', '_')

playlist_file = open(current_folder_name + '.m3u', 'w')

playlist_file.write('#EXTM3U'+'\n')

for root, dirs, files in os.walk(cwd):
  dirs.sort()
  files.sort()
  for name in files:
    if name.endswith((".mp4")):
      file_path = os.path.join(root, name)
      playlist_file.write('#EXTINF:'+str(get_length_in_seconds(file_path))+','+name+'\n')
      playlist_file.write(file_path.replace(' ','%20')+'\n')