#this script extracts the best phrases and writes them to a new text file

with open("10460.txt",'r') as f:
     phrases = f.readlines()
f.close()

#strip tabs and new lines
phrases = [s for s in phrases if (s[2] == '9') or (s[2] == '8')]

tab_removed_phrases = [s.replace("\t", " ").replace("\n", "") for s in phrases]

tags_only_phrases = [s.split(' ', 1)[1] for s in tab_removed_phrases]

if tags_only_phrases == []:
	with open('','w') as out: #need to create textfile with same name
		for tag in common_tags:
			out.write('Insufficient Data')
else:
	with open('','w') as out:
		for tag in common_tags:
			out.write(tag + '\n')