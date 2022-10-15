with open("dune.txt", encoding="UTF-8") as f:
    lines = [line for line in f]

chapter_ind = 1
chapters = {i:[] for i in range(1, 57)}
for line in lines:
	if "= = =" in line:
		chapter_ind += 1
	else:
		chapters[chapter_ind].append(line)

for chapter_ind, lines in chapters.items():
	with open(f"dune_{chapter_ind}.txt", 'w') as f:
		f.writelines(lines)