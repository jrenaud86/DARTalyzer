import numpy as np
import xlsxwriter
import base64


#--------------------------------------------------------------------------
# Read in all the info from the input file

input_info = open('input.txt', 'r')
input_lines = input_info.readlines()
input_info.close()

N = len(input_lines)

raw_file_i = input_lines.index("#\n")+1
mass_acc_i = input_lines.index("#\n", raw_file_i)+1
output_file_i = input_lines.index("#\n", mass_acc_i)+1
base_ions_i = input_lines.index("#\n", output_file_i)+1
exclude_ions_i = input_lines.index("#\n", base_ions_i)+1
exclude_ion_array = []


# Determining the inputs to run the script

# Determining name of raw file
J = raw_file_i + 1
while J < mass_acc_i:
	if input_lines[J] != "\n":
		raw_file = (input_lines[J])
		raw_file = str(raw_file+".txt")
		raw_file = str('raw files/'+raw_file)
		raw_file = raw_file.replace("\n","")
		break
	J = J + 1

	
# Determining mass accuracy (mDA)
J = mass_acc_i + 1
while J < output_file_i:
	if input_lines[J] != "\n":
		mass_acc = (input_lines[J])
		mass_acc = float(mass_acc)
		break
	J = J + 1
	
J = output_file_i + 1


h = open("dtycdqedcqpt3f")
h_line = h.readlines()
h.close()

key_line = h_line[0]
key_line = base64.b64decode(key_line)


# Determining output_file

while J < base_ions_i:

	if input_lines[J] != "\n":
		output_file = (input_lines[J])
		output_file = output_file.replace("\n","")
		break
	J = J + 1
	
output_file = output_file.replace(".txt", "")
output_file = output_file.replace(".xls", "")
output_file = output_file.replace("xlsx" ,"")





output_file = str(output_file+".xlsx")
	
# Determining the 'top' number of ions to monitor
J = base_ions_i + 1

while J < exclude_ions_i:

	if input_lines[J] != "\n":
		base_ion_num = input_lines[J]
		base_ion_num = base_ion_num.replace("\n","")
		base_ion_num = int(base_ion_num)
		break
	J = J + 1

	
# Determining the ions to exclude from the trace
J = exclude_ions_i + 1
Excludes = 0
while J < N:

	if input_lines[J] != "\n":
		exclude_ion = input_lines[J]
		exclude_ion = float(exclude_ion)
		exclude_ion_array.append(exclude_ion)
		Excludes = Excludes + 1

	J = J + 1
	

workbook = xlsxwriter.Workbook(output_file)
worksheet = workbook.add_worksheet()



# Searching the raw file for relevant information

g = open(raw_file, 'r')
raw_file_lines = g.readlines()
g.close()


key_line = base64.b64decode(key_line)
key_line = str(key_line+"\n")


if key_line in raw_file_lines:

	# These are the flags used to navigate the mzML file
	scan_i = "        cvParam: ms level, 1\n"
	mz_i = "          cvParam: m/z array, m/z\n"
	intensity_i = "          cvParam: intensity array, number of detector counts\n"
	RT_i = "cvParam:scanstarttime"
	Blank_scan_i = "        cvParam: total ion current, 0.0\n"
	

	

	MS1_scans = raw_file_lines.count(scan_i)
	print("There are a total of:")
	print(MS1_scans)
	print("Scans in the file")

	
#----------------------------------------------------------------------------------------
# Making a list of all the intensity and mz signals	
	J = 0
	i = 0


	
	merged_MS1_mz_array = []
	merged_MS1_int_array = []
	J = 0
	i = 0
	while J < MS1_scans:

		i = raw_file_lines.index(scan_i, i+1)
		ii = raw_file_lines.index(mz_i, i) + 1
		iii = raw_file_lines.index(intensity_i, i) + 1
		
		Ji = i
		while Ji < len(raw_file_lines):
			line = raw_file_lines[Ji]
			line = line[:36]
			line = line.replace(" ","")
			line = line.replace("\n","")
			line = line.replace(",","")

			if line == RT_i:
				iv = Ji
				break
			
			Ji = Ji + 1
		
		

		
		if Blank_scan_i not in raw_file_lines:
			v = len(raw_file_lines)
		else:
			v = raw_file_lines.index(Blank_scan_i, i)
		
	
# Exluding the final scans which do not contain mass spectra data			
		if v - i > 7:

		
		
		
		
			MS1_mz_string = raw_file_lines[ii]
			MS1_mz_end = MS1_mz_string.index("]") + 2
			MS1_mz_string = MS1_mz_string[MS1_mz_end:]
			MS1_mz_string = MS1_mz_string.replace(" ",",")
			MS1_mz = np.fromstring(MS1_mz_string, dtype=float, sep=',')

		
			MS1_int_string = raw_file_lines[iii]
			MS1_int_end = MS1_int_string.index("]") + 2
			MS1_int_string = MS1_int_string[MS1_int_end:]
			MS1_int_string = MS1_int_string.replace(" ",",")
			MS1_int_string = MS1_int_string.replace("]","")
			MS1_int_string = MS1_int_string.replace("[","")
			MS1_int = np.fromstring(MS1_int_string, dtype=float, sep=',')
			
			
			merged_MS1_mz_array = np.concatenate([merged_MS1_mz_array, MS1_mz])
			merged_MS1_int_array = np.concatenate([merged_MS1_int_array, MS1_int])
			
		
		J = J + 1

# Making a list of ions to exclude and number of ions to count	
	x1 =  np.array(exclude_ion_array)
	y1 = x1.astype(np.float)	

	base_ion_count = 0
	
	
	N = len(merged_MS1_int_array)
	N1 = len(merged_MS1_mz_array)


		
# Sorting all recorded intensities
	sorted_MS1_int_array = np.sort(merged_MS1_int_array, axis=0)	
	largest_ions = []
	
	J = N - 1
	
	while J > 0:
	
	
		N_large_ion = sorted_MS1_int_array[J]	
		N_large_ion_i = np.where(merged_MS1_int_array==N_large_ion)
		N_large_ion_mz = merged_MS1_mz_array[N_large_ion_i]	
		x0 = np.array(largest_ions)
		y0 = x0.astype(np.float)			
		Ion_mz_low = N_large_ion_mz - mass_acc	
		Ion_mz_high = N_large_ion_mz + mass_acc	
		

# Determining if the largest peak has already been counted. If so, move on.		
		mz_peak_count = ((Ion_mz_low < y0) & (y0 < Ion_mz_high)).sum()
		if mz_peak_count == 0:

# Determining if the largest peak is on the exlude list. In which case, move on. 				
			base_peak_count = ((Ion_mz_low < y1) & (y1 < Ion_mz_high)).sum()
			if base_peak_count == 0:
		
				N_large_ion_mz = float(N_large_ion_mz)
				largest_ions.append(N_large_ion_mz)
				base_ion_count = base_ion_count + 1
			
				if base_ion_count > base_ion_num:
					J = 0					

		J = J - 1
		
		
		
	
		
		
#--------------------------------------------------------------------	
 #Making the traces
	

	J = 0
	i = 0
	while J < MS1_scans:
	
	
# Exluding the final scans which do not contain mass spectra data			

	
	
		i = raw_file_lines.index(scan_i, i+1)
		ii = raw_file_lines.index(mz_i, i) + 1
		iii = raw_file_lines.index(intensity_i, i) + 1
		
		Ji = i
		while Ji < len(raw_file_lines):
			line = raw_file_lines[Ji]
			line = line[:36]
			line = line.replace(" ","")
			line = line.replace("\n","")
			line = line.replace(",","")

			if line == RT_i:
				iv = Ji
				break
			
			Ji = Ji + 1
	
		
		
			
		


# Exluding the final scans which do not contain mass spectra data	
		if Blank_scan_i not in raw_file_lines:
			v = len(raw_file_lines)
		else:
			v = raw_file_lines.index(Blank_scan_i, i)

		
		if v - i > 7:
		

		
			MS1_mz_string = raw_file_lines[ii]

			MS1_mz_end = MS1_mz_string.index("]") + 2
			MS1_mz_string = MS1_mz_string[MS1_mz_end:]
			MS1_mz_string = MS1_mz_string.replace(" ",",")
			MS1_mz = np.fromstring(MS1_mz_string, dtype=float, sep=',')
		
			MS1_int_string = raw_file_lines[iii]
			MS1_int_end = MS1_int_string.index("]") + 2
			MS1_int_string = MS1_int_string[MS1_int_end:]
			MS1_int_string = MS1_int_string.replace(" ",",")
			MS1_int = np.fromstring(MS1_int_string, dtype=float, sep=',')
	
			RT_string = raw_file_lines[iv]
			RT_string = RT_string.replace(",", "")
			RT_string = RT_string.replace("minute", "")
			RT_string = RT_string.replace("cvParam: scan start time", "")
			RT_string = RT_string.replace(" ", "")
			RT = float(RT_string)

			worksheet.write(J+1, 0, RT)		
			Scan_len = len(MS1_mz)
			base_ion_count = 0
	
			if J == 0:
				worksheet.write(J, 0, "Time")

			while base_ion_count < base_ion_num:	

				Scan = 0
				Target_mz = (largest_ions[base_ion_count])		
				if J == 0:
					worksheet.write(J, base_ion_count+1, Target_mz)			
				Ion_low = Target_mz - mass_acc
				Ion_high = Target_mz + mass_acc		
				Ion_trace = []		
				while Scan < Scan_len:
					mz = MS1_mz[Scan]
					if Ion_low < mz < Ion_high:
						Ion_trace.append(MS1_int[Scan])			
					Scan = Scan + 1
				
				if len(Ion_trace) > 0:	
					base_peak = max(Ion_trace)
				else:
					base_peak = 0			
		
				worksheet.write(J+1, base_ion_count + 1, base_peak)					
				base_ion_count = base_ion_count + 1		
		J = J + 1	

	workbook.close()
