import parsedatetime as pdt
from datetime import datetime
from time import mktime

import os
import re

error_file = open("error_checker.txt", 'w', encoding="utf8")
year_is_too_big = open("year_is_too_big.txt", 'w', encoding="utf8")
correct_dates_file = open("correct_dates.txt", 'a', encoding="utf8")
today = open("today.txt", 'w', encoding="utf8")

ARTICLES_DIR_NAME = 'articles'
ARTISTS_FILE_NAME = 'artists.txt'

counter_parsed = 0
counter_not_parsed_at_all = 0
counter_year_is_too_big = 0
counter_today = 0

amount_of_artists = {}
artists_names = list(map(lambda x : ' '.join(x.split()[1:]), open(ARTISTS_FILE_NAME, 'r').readlines()))


_, _, filenames = list(os.walk(ARTICLES_DIR_NAME))[0]
for filename in filenames:
	# print('Filename: ', filename, file=correct_dates_file)
	raw_article_date = filename.split('-')[0]
	article_year, article_month, article_day = int(raw_article_date[:4]), int(raw_article_date[4:6]), int(raw_article_date[6:8])

	with open(ARTICLES_DIR_NAME + '/' + filename) as article_file:
		c = pdt.Constants()
		c.BirthdayEpoch = 80
		p = pdt.Calendar(c)
		for line in article_file.readlines():
			for artist_name in artists_names:
				art_count = line.count(artist_name)
				if art_count > 0:
					print(artist_name, file=correct_dates_file)
			time_struct = p.parseDT(line, datetime(article_year, article_month, article_day))
			res, parse_status = datetime.fromtimestamp(mktime(time_struct[0].timetuple())), time_struct[1]
			if res.year > 2016:
				counter_year_is_too_big += 1
				print(res, file=year_is_too_big)
			elif (res.year == 2016) and (res.month == 5) and (res.day == 20):
				counter_today += 1
				print(res, file=today) 
			else:
				if parse_status != 0:
					counter_parsed += 1
					print(res, file=correct_dates_file)
				else:
					counter_not_parsed_at_all += 1
					print(res, file=error_file)
print(counter_parsed, '\n', counter_not_parsed_at_all, '\n', counter_year_is_too_big, '\n', counter_today)
