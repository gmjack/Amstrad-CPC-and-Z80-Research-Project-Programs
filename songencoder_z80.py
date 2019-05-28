import sys


# Parses a note-unit
# Returns encoded list that contains [octave, key, length] in that order. 
def parseNote(notestr,octave=-1):
	cust_oct = False

	# Checks to see if there is a custom octave for the note-unit. 
	if octave == -1:
		octave = int(notestr[0]) - 1
	else:
		cust_oct = True

	# Checks to see if the note is a sharp or flat and makes adjustments to the reading index. 
	if not notestr[2 - cust_oct].isnumeric():
		note = notestr[1 - cust_oct:3 - cust_oct]
		index = 3 - cust_oct
	else:
		note = notestr[1 - cust_oct]
		index = 2 - cust_oct

	# Dictionary of keys w/ their encoded values. 
	keys = {
	 	'C' : '0',
	 	'C#': '1',
	 	'Db': '1',
	 	'D' : '2',
	 	'D#': '3',
	 	'Eb': '3',
	 	'E' : '4',
	 	'E#': '5',
	 	'Fb': '4',
	 	'F' : '5',
	 	'F#': '6',
	 	'Gb': '6',
	 	'G' : '7',
	 	'G#': '8',
	 	'Ab': '8',
	 	'A' : '9',
	 	'A#': 'A',
	 	'Bb': 'A',
	 	'B' : 'B',
	 	'R':  'C'
	}
	note = keys[note]

	length = notestr[index::] # The length is designated as the rest of the note-unit's string past the octave/key.  

	# dictionary of lengths, really just hexadecimal conversion. 
	lengths = {

	 	'1'	    : '01',
	 	'2'		: '02',
	 	'4'		: '04',
	 	'6'		: '06',
	 	'8'		: '08',
	 	'12'	: '0C',
	 	'16'	: '10',
	 	'24'	: '18'
	}
	
	length = lengths[length]
	return [octave, note, length]	


# Parses an entire staff
# staffstr - staff to be parsed
# linelim  - number of note-units per line. The assembler doesn't like really long lines and it makes it less readable. 
def parseStaff(staffstr,linelim=16):
	notelist = staffstr.replace(" ", "").replace("\t","").split(",") # Removes spaces/tabs and splits it into note-unit stings based on comma's
	newstr = "defw "
	lc = 1			# variable used to keep track of if we have reached the linelim
	curr_octave = -1
	for note in notelist:
		if note[0] == ":":
			if note[1].isnumeric():	# Checks for octave
				curr_octave = int(note[1])
			else:
				if  note[1] == ">":				#All that is neccesary is one '>' or '<' technically, but convention is '>>' or '<<' for greater clarity. 
					curr_octave += 1
				elif  note[1] == "<":
					curr_octave -= 1
		else:
			comps = parseNote(note, octave=curr_octave)			# grabs a list of [octave, key, length]
			newstr += "#" + str(comps[0]) + str(comps[1]) +str(comps[2]) # Designates a part of the memory to it. 
			if lc == linelim:
				newstr +="\ndefw "		# defw is used to declare two-bit datastrings, but only needs to be declared once per line. 
				lc = 0
			else:
				newstr += ","
			lc += 1
	if lc < 16:
		newstr = newstr[0:len(newstr)-1]	
	print("Length = " + str(len(newstr.split("#"))))	# Tells us how long the staff is so that we can know if its in the 256-note limit. 
	return newstr

# A better way to do this is to read from file, but this works fine. 
inp = ":4,E8,:<<,B4,:>>,B4,A4,G4,F#4,E4,G8,E24,E8,:<<,B4,:>>,B4,:>>,D4,C4,:<<,B4,A4,B24,G4,A4,B8,D4,G4,F#4,E4,F#4,G4,E8,:<<,B8,:>>,D12,:<<,B4,:>>,C4,E4,B4,A4,F8,G4,A4,G16,F#16,E8,:<<,B4,:>>,B4,A4,G4,F#4,E4,G8,E24,E8,:<<,B4,:>>,B4,:>>,D4,C4,:<<,B4,A4,B24,G4,A4,B8,D4,G4,F#4,E4,F#4,G4,E8,:<<,B8,:>>,D12,:<<,B4,:>>,C4,E4,B4,A4,F8,G4,A4,G16,F#16,E16"
print(parseStaff(inp))		# Prints out result
