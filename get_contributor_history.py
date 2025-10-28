import json
from collections import OrderedDict
import pprint
import subprocess

import datetime

# name , date
code_contributors = {}
community_contributors = {}
autoware_contributors = {}

# day , countup
code_contributors_per_day = {}
community_contributors_per_day = {}
autoware_contributors_per_day = {}

start_date = datetime.datetime(2022, 1, 1)
end_date = datetime.datetime.today()

def date_range(start, stop, step = datetime.timedelta(1)):
    current = start
    while current < stop:
        yield current
        current += step

def getContributors(file, contributors):
    f = open(file, "r")
    loaded_json = json.load(f)
    edges = loaded_json

    for x in edges:
        d = datetime.datetime.strptime(x["node"]["createdAt"], '%Y-%m-%dT%H:%M:%SZ')
        date_filter = start_date

        if d < date_filter:
            continue
        if x["node"]["author"] is not None:
            author = x["node"]["author"]["login"]
            if author not in contributors:
                contributors[author] = d
            elif contributors[author] > d:
                contributors[author] = d

        for y in x["node"]["comments"]["edges"]:
            if y["node"]["author"] is not None:
                d = datetime.datetime.strptime(y["node"]["createdAt"], '%Y-%m-%dT%H:%M:%SZ')
                author = y["node"]["author"]["login"]
                if author not in contributors:
                    contributors[author] = d
                elif contributors[author] > d:
                    contributors[author] = d

    return contributors

def countContributorsPerDay(contributors, contributors_per_day):
    for contributor in contributors.keys():
        date = contributors[contributor]
        day = datetime.date(date.year, date.month, date.day)
        if day not in contributors_per_day:
            contributors_per_day[day]=1
        else:
            contributors_per_day[day]+=1
    contributors_per_day = sorted(contributors_per_day.items())

def writeToFile(contributors_per_day, file_name):
    with open("contributor_history/" + file_name, 'w') as fp:
        count = 0
        for item in sorted(contributors_per_day.items()):
            count += item[1]
            line = item[0].strftime('%Y/%m/%d') + "," + str(item[1])+"," + str(count)
            fp.write("%s\n" % line)
    print('Done')

def writeToCSV(autoware_contributors_per_day, code_contributors_per_day, community_contributors_per_day, file_name):
    with open("contributor_history/" + file_name, 'w') as fp:
        fp.write("date, autoware_contributors, code_contributors, community_contributors\n")
        autoware_contributor_count = 0
        code_contributor_count = 0
        community_contributor_count = 0
        for item in sorted(autoware_contributors_per_day.items()):
            date = item[0]
            count = item[1]

        for date in date_range(start_date,end_date):
            date_format = datetime.date(date.year,date.month,date.day)
            updated = False
            if date_format in autoware_contributors_per_day:
                autoware_contributor_count += autoware_contributors_per_day[date_format]
                updated = True
            if date_format in code_contributors_per_day:
                code_contributor_count+=code_contributors_per_day[date_format]
                updated = True
            if date_format in community_contributors_per_day:
                community_contributor_count+=community_contributors_per_day[date_format]
                updated = True

            if updated:
                line = date.strftime('%Y/%m/%d') + "," + str(autoware_contributor_count)+"," + str(code_contributor_count) + "," + str(community_contributor_count)
                print(line)
                fp.write("%s\n" % line)
    print('Done')

# name , date
code_contributors = {}
community_contributors = {}
autoware_contributors = {}

# day , countup
code_contributors_per_day = {}
community_contributors_per_day = {}
autoware_contributors_per_day = {}

getContributors("generated_json/autoware_discussions.json", community_contributors)
getContributors("generated_json/autoware_issues.json", community_contributors)
getContributors("generated_json/universe_issues.json", community_contributors)
getContributors("generated_json/autoware_core_issues.json", community_contributors)
getContributors("generated_json/autoware_msgs_issues.json", community_contributors)
getContributors("generated_json/autoware_launch_issues.json", community_contributors)
getContributors("generated_json/autoware_documentation_issues.json", community_contributors)

getContributors("generated_json/autoware_prs.json", code_contributors)
getContributors("generated_json/universe_prs.json", code_contributors)
getContributors("generated_json/autoware_core_prs.json", code_contributors)
getContributors("generated_json/autoware_msgs_prs.json", code_contributors)
getContributors("generated_json/autoware_launch_prs.json", code_contributors)
getContributors("generated_json/autoware_documentation_prs.json", code_contributors)

## merge two dict
autoware_contributors = community_contributors.copy()
for author in code_contributors.keys():
    if author not in autoware_contributors:
        autoware_contributors[author] = code_contributors[author]
    elif autoware_contributors[author] > code_contributors[author]:
        autoware_contributors[author] = code_contributors[author]


## count per day
countContributorsPerDay(code_contributors, code_contributors_per_day)
countContributorsPerDay(community_contributors, community_contributors_per_day)
countContributorsPerDay(autoware_contributors, autoware_contributors_per_day)

writeToFile(code_contributors_per_day, "code_contributors_per_day.txt")
writeToFile(community_contributors_per_day, "community_contributors_per_day.txt")
writeToFile(autoware_contributors_per_day, "autoware_contributors_per_day.txt")

writeToCSV(autoware_contributors_per_day, code_contributors_per_day, community_contributors_per_day, "contributors_count.csv")