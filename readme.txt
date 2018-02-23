Hi! With all scripts that need to run by themselves, I added #! as it is on my device
(which is '#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3')
So, to get it running on your devices, please go into the file and modify it to fit your own environment.
Also, maybe you need to change mode to make it executable.

For ls.py and stat.py, it should work the same as built in functions.
For registration, I did not include a thorough documentation in it,
But I think the prompts is clear enough to guide you through everything.
The basic functions could work properly if input was right (case sensitive)
Some of the errors may occur due to that... I think I have found most of them,
but some may still getaway.

The functions should have loosely followed the requirements. Please try following the prompts of my script.
Thanks!

I used pickle, inspired by my classmates, to store the data. I included a test .pkl file under data,
so you can directly load that if you input the file name of that. (pkl files are saved using the school name)