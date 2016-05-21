import re

lines = open("correct_dates.txt", 'r', encoding="utf8").readlines()

ARTISTS_FILE_NAME = 'artists.txt'
artists_names = list(map(lambda x : ' '.join(x.split()[1:]), open(ARTISTS_FILE_NAME, 'r').readlines()))

art_dict = {}
START_YEAR = 2013

for i, line in enumerate(lines):
	if re.match(r"^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d", line) is None:
		artist_name = line
		art_dict[artist_name] = art_dict.get(artist_name, {})
		found_date = False
		for line in lines[i+1:]:
			m = re.match(r"^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d", line)
			if found_date and not bool(m):
				break
			found_date = bool(m) or found_date
			if bool(m):
				year = int(line.split()[0].split('-')[0])
				if year < START_YEAR:
					year = START_YEAR - 1
				art_dict[artist_name][year] = art_dict[artist_name].get(year, 0) + 1

with open("sorted_dates.txt", 'w', encoding="utf8") as result_file:
	print(art_dict, file=result_file)
