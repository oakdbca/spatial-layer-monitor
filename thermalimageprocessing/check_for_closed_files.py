#!/usr/bin/env python
import pyinotify
import subprocess
from datetime import datetime, timedelta

class MyEventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_NOWRITE(self, event):
        current_datetime = datetime.now().astimezone()
        seen_datetime = datetime.strftime(current_datetime, '%Y-%m-%d %H:%M:%S')

        # log watch
        print (seen_datetime+" File closed: "+ event.pathname)   

        two_char_extension = str(event.pathname)[-3:]
        three_char_extension = str(event.pathname)[-4:]
        if two_char_extension == '.7z' or three_char_extension == '.zip':
            try:
                result = subprocess.run(["/bin/bash", "./thermal_image_processing.sh", event.pathname], capture_output=True, text=True, check=True)
                print (result)
            except Exception as e:
                print (e)
                print (e.output)
                

    def process_IN_OPEN(self, event):
        current_datetime = datetime.now().astimezone()
        seen_datetime = datetime.strftime(current_datetime, '%Y-%m-%d %H:%M:%S')   
        print (seen_datetime+" File opened: "+ event.pathname)

def main():
    # Watch manager (stores watches, you can add multiple dirs)
    wm = pyinotify.WatchManager()
    # User's music is in /tmp/music, watch recursively    
    wm.add_watch('/data/data/projects/thermal-image-processing/thermalimageprocessing/thermal_data', pyinotify.ALL_EVENTS, rec=True)

    # Previously defined event handler class
    eh = MyEventHandler()

    # Register the event handler with the notifier and listen for events
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()

if __name__ == '__main__':
    main()
