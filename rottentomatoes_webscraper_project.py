import urllib
from urllib.request import urlopen
import re
import copy


class rotten_tomatoes:
    def __init__(self, url):
        self.page = urlopen(url)
        self.html_bytes = self.page.read()
        self.html = self.html_bytes.decode('utf-8')

    def html_container(self):
        #finding the necessary div classes in the html
        start_indexes = []
        for string in re.finditer('article_movie_title', self.html):
            start_indexes.append(string.start())
        end_indexes = []
        for string in re.finditer('col-sm-4 col-full-xs', self.html):     
            end_indexes.append(string.start())

        #recording the div classes in one list
        movie_containers = []
        for n in range(len(start_indexes)):
            movie_containers.append(self.html[start_indexes[n]:end_indexes[n]])
        return movie_containers
        


    def html_refine(self):
        #refining the div classes, searching for titles, years, ratings
        containers = []
        for raw_container in self.html_container():
            start_indexes = []
            end_indexes = []
            #extracting the data from the <html> tag
            for n in range(len(raw_container)):
                if raw_container[n] == '>':
                    start_indexes.append(n)
                elif raw_container[n] == '<':
                    end_indexes.append(n)

            #recording the refined data
            condensed_container = []
            for i in range(len(start_indexes)):
                condensed_container.append(raw_container[start_indexes[i]:end_indexes[i]])
            containers.append(condensed_container)
        return containers



    def scrape(self):
        #further refining, extracting lines that have a number or letter
        movie_stats = []
        final_container = []
        for container in self.html_refine():
            for line in container:
                for char in line:
                    if char.isalnum() == True:
                        movie_stats.append(line)
                        break

        #removing special characters and leftover tags
        removed_char = '>()%'
        final_movie_stats = []
        for line in movie_stats:
            for char in removed_char:
                line=line.replace(char, '')

            #recording the clean data together
            final_movie_stats.append(line)
        return final_movie_stats



    def dataLists(self):
        final_movie_stats = self.scrape()
        titles = []
        years = []
        ratings = []

        #separating titles, years, and ratings
        for n in range(len(final_movie_stats)-1):
            #if not a year or rating number, it's a title
            if (len(final_movie_stats[n])>4) or final_movie_stats[n].isdecimal()!=True:
                if final_movie_stats[n+1].isdecimal() == True and final_movie_stats[n+2].isdecimal() == True:
                    titles.append(final_movie_stats[n])

                #if one of the two lines following the title are not a year or rating
                elif final_movie_stats[n+1].isdecimal == False or final_movie_stats[n+2].isdecimal() == False:

                    if len(final_movie_stats[n+1]) == 4 and final_movie_stats[n+1].isdecimal() == True:     #checking if a rating is missing
                        years.append(final_movie_stats[n+1])    #no rating, record the year
                        ratings.append(' ')     #representing missing rating with blank

                    if len(final_movie_stats[n+1]) <= 3 and final_movie_stats[n+1].isdecimal() == True:     #checking if a year is missing
                        ratings.append(final_movie_stats[n+1])  #no year, record the rating
                        years.append(' ')       #representing missing year with blank

            #checking if it's a year
            elif len(final_movie_stats[n]) == 4 and final_movie_stats[n].isdecimal() == True:
                years.append(final_movie_stats[n])
            #anything that's not a title or year, is a rating
            else:
                ratings.append(final_movie_stats[n])

        return titles, years, ratings



''' Example to use/call Object, insert Rotten Tomatoes url into rotten_tomatoes parameter:
RT = rotten_tomatoes('https://editorial.rottentomatoes.com/guide/best-christmas-movies/')
print(RT.dataLists())'''


#to import into Excel, separating columns with separater |
'''
    print('Title|' + '|'.join(titles))
    print('Year|' + '|'.join(years))
    print('Rating|' + '|'.join(ratings))
    return ''
'''

'''
    for line in titles:     #ratings from low to high
        print line
    for line in years:
        print line
    for line in ratings:
        print line

    for line in reversed(titles):     #ratings from high to low
        print line
    for line in reversed(years):
        print line
    for line in reversed(ratings):
        print line
'''


