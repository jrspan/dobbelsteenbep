functions.py contains all "def <function name>"
simulation.py contains dice simulation code. (Not created yet)

accelerometer data and gyroscope data have to be stored in same folder as .py files. (Might get changed in the future)

To do:
- Create simulation code for CSV files
- Create simulation code for real-time measurements
- Add a filter to remove bias for our codes (Most likely first in real-time)
- Add a storing method for valid results (writing to a .CSV file for example)
	- Or: Remove all unnecessary variables in old python code

More ideas if possible:
- Create UI
	- "Real-time measurement" option
		- Uses simulation code for real-time measurements with filter
		- If selected and dice is connected: will start measuring immediately
		- New file created that stores all valid throws. Name automatically generated.
	- "From datafiles" option
		- Uses simulation code for CSV files
		- If selected: asks user to upload both data files, then hit "start simulation" option
		- Will raise errors if files do not match in length (different measurements = not the same throw)
- Fully give a 3D-visualization of the dice
	- Possibly with a slider as well, with the slider adjusting the time