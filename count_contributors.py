import json
from collections import OrderedDict
import pprint
import subprocess

import datetime

def getContributors(file, contributor_type, use_filter = False, count_ai = True):
    f = open(file, "r")
    loaded_json = json.load(f)
    edges = loaded_json

    contributors=[]

    print(len(edges))
    for x in edges:
        d = datetime.datetime.strptime(x["node"]["createdAt"], '%Y-%m-%dT%H:%M:%SZ')
        date_filter = datetime.datetime(2022, 1, 1)
        # date_filter = datetime.datetime(2022, 12, 1)
        if use_filter:
            if d > date_filter and count_ai:
                continue
            if d < date_filter and count_ai == False:
                continue
        if x["node"]["author"] is not None:
            contributors.append(x["node"]["author"]["login"])
        for y in x["node"]["comments"]["edges"]:
            if y["node"]["author"] is not None:
                contributors.append(y["node"]["author"]["login"])

    contributors = sorted(set(contributors))
    print(contributors)
    print(len(contributors))
    return contributors

def writeNamesToFile(names, file_name):
    with open("contributor_names/"+file_name, 'w') as fp:
        for name in names:
            fp.write("%s\n" % name)
    print('Done')



contributors = []

## autoware

autoware_discussions = []
contributor_type="discussions"
json_file="generated_json/autoware_discussions.json"
autoware_discussions += getContributors(json_file, contributor_type)
contributors += autoware_discussions
writeNamesToFile(autoware_discussions, "autoware_discussions.txt")

autoware_issues = []
contributor_type="issues"
json_file="generated_json/autoware_issues.json"
autoware_issues += getContributors(json_file, contributor_type)
contributors += autoware_issues
writeNamesToFile(autoware_issues, "autoware_issues.txt")

autoware_prs = []
contributor_type="pullRequests"
json_file="generated_json/autoware_prs.json"
autoware_prs += getContributors(json_file, contributor_type, True, False)
contributors += autoware_prs
writeNamesToFile(autoware_prs, "autoware_prs.txt")

autoware_ai_prs = []
contributor_type="pullRequests"
json_file="generated_json/autoware_prs.json"
autoware_ai_prs += getContributors(json_file, contributor_type, False, True)
writeNamesToFile(autoware_ai_prs, "autoware_ai_prs.txt")

## autoware_universe

universe_issues = []
contributor_type="issues"
json_file="generated_json/universe_issues.json"
universe_issues += getContributors(json_file, contributor_type)
contributors += universe_issues
writeNamesToFile(universe_issues, "universe_issues.txt")

universe_prs = []
contributor_type="pullRequests"
json_file="generated_json/universe_prs.json"
universe_prs += getContributors(json_file, contributor_type)
contributors += universe_prs
writeNamesToFile(universe_prs, "universe_prs.txt")

## autoware_core
autoware_core_issues = []
contributor_type="issues"
json_file="generated_json/autoware_core_issues.json"
autoware_core_issues += getContributors(json_file, contributor_type)
contributors += autoware_core_issues
writeNamesToFile(autoware_core_issues, "autoware_core_issues.txt")

autoware_core_prs = []
contributor_type="pullRequests"
json_file="generated_json/autoware_core_prs.json"
autoware_core_prs += getContributors(json_file, contributor_type)
contributors += autoware_core_prs
writeNamesToFile(autoware_core_prs, "autoware_core_prs.txt")

## autoware_msgs
autoware_msgs_issues = []
contributor_type="issues"
json_file="generated_json/autoware_msgs_issues.json"
autoware_msgs_issues += getContributors(json_file, contributor_type)
contributors += autoware_msgs_issues
writeNamesToFile(autoware_msgs_issues, "autoware_msgs_issues.txt")

autoware_msgs_prs = []
contributor_type="pullRequests"
json_file="generated_json/autoware_msgs_prs.json"
autoware_msgs_prs += getContributors(json_file, contributor_type)
contributors += autoware_msgs_prs
writeNamesToFile(autoware_msgs_prs, "autoware_msgs_prs.txt")

## autoware_launch
autoware_launch_issues = []
contributor_type="issues"
json_file="generated_json/autoware_launch_issues.json"
autoware_launch_issues += getContributors(json_file, contributor_type)
contributors += autoware_launch_issues
writeNamesToFile(autoware_launch_issues, "autoware_launch_issues.txt")

autoware_launch_prs = []
contributor_type="pullRequests"
json_file="generated_json/autoware_launch_prs.json"
autoware_launch_prs += getContributors(json_file, contributor_type)
contributors += autoware_launch_prs
writeNamesToFile(autoware_launch_prs, "autoware_launch_prs.txt")

## autoware_documentation
autoware_documentation_issues = []
contributor_type="issues"
json_file="generated_json/autoware_documentation_issues.json"
autoware_documentation_issues += getContributors(json_file, contributor_type)
contributors += autoware_documentation_issues
writeNamesToFile(autoware_documentation_issues, "autoware_documentation_issues.txt")

autoware_documentation_prs = []
contributor_type="pullRequests"
json_file="generated_json/autoware_documentation_prs.json"
autoware_documentation_prs += getContributors(json_file, contributor_type)
contributors += autoware_documentation_prs
writeNamesToFile(autoware_documentation_prs, "autoware_documentation_prs.txt")

## autoware_ai

autoware_ai_issues = []
contributor_type="issues"
json_file="generated_json/autoware_ai_issues.json"
autoware_ai_issues += getContributors(json_file, contributor_type)
writeNamesToFile(autoware_ai_issues, "autoware_ai_issues.txt")

## autoware_ai_planning
autoware_ai_planning_issues = []
contributor_type="issues"
json_file="generated_json/autoware_ai_planning_issues.json"
autoware_ai_planning_issues += getContributors(json_file, contributor_type)
writeNamesToFile(autoware_ai_planning_issues, "autoware_ai_planning_issues.txt")

autoware_ai_planning_prs = []
contributor_type="pullRequests"
json_file="generated_json/autoware_ai_planning_prs.json"
autoware_ai_planning_prs += getContributors(json_file, contributor_type)
writeNamesToFile(autoware_ai_planning_prs, "autoware_ai_planning_prs.txt")

## autoware_ai_perception
autoware_ai_perception_issues = []
contributor_type="issues"
json_file="generated_json/autoware_ai_perception_issues.json"
autoware_ai_perception_issues += getContributors(json_file, contributor_type)
writeNamesToFile(autoware_ai_perception_issues, "autoware_ai_perception_issues.txt")

autoware_ai_perception_prs = []
contributor_type="pullRequests"
json_file="generated_json/autoware_ai_perception_prs.json"
autoware_ai_perception_prs += getContributors(json_file, contributor_type)
writeNamesToFile(autoware_ai_perception_prs, "autoware_ai_perception_prs.txt")

## autoware_ai_messages
autoware_ai_messages_issues = []
contributor_type="issues"
json_file="generated_json/autoware_ai_messages_issues.json"
autoware_ai_messages_issues += getContributors(json_file, contributor_type)
writeNamesToFile(autoware_ai_messages_issues, "autoware_ai_messages_issues.txt")

autoware_ai_messages_prs = []
contributor_type="pullRequests"
json_file="generated_json/autoware_ai_messages_prs.json"
autoware_ai_messages_prs += getContributors(json_file, contributor_type)
writeNamesToFile(autoware_ai_messages_prs, "autoware_ai_messages_prs.txt")

## autoware_ai_simulation
autoware_ai_simulation_issues = []
contributor_type="issues"
json_file="generated_json/autoware_ai_simulation_issues.json"
autoware_ai_simulation_issues += getContributors(json_file, contributor_type)
writeNamesToFile(autoware_ai_simulation_issues, "autoware_ai_simulation_issues.txt")

autoware_ai_simulation_prs = []
contributor_type="pullRequests"
json_file="generated_json/autoware_ai_simulation_prs.json"
autoware_ai_simulation_prs += getContributors(json_file, contributor_type)
writeNamesToFile(autoware_ai_simulation_prs, "autoware_ai_simulation_prs.txt")

## autoware_ai_visualization
autoware_ai_visualization_issues = []
contributor_type="issues"
json_file="generated_json/autoware_ai_visualization_issues.json"
autoware_ai_visualization_issues += getContributors(json_file, contributor_type)
writeNamesToFile(autoware_ai_visualization_issues, "autoware_ai_visualization_issues.txt")

autoware_ai_visualization_prs = []
contributor_type="pullRequests"
json_file="generated_json/autoware_ai_visualization_prs.json"
autoware_ai_visualization_prs += getContributors(json_file, contributor_type)
writeNamesToFile(autoware_ai_visualization_prs, "autoware_ai_visualization_prs.txt")

## autoware_ai_drivers
autoware_ai_drivers_issues = []
contributor_type="issues"
json_file="generated_json/autoware_ai_drivers_issues.json"
autoware_ai_drivers_issues += getContributors(json_file, contributor_type)
writeNamesToFile(autoware_ai_drivers_issues, "autoware_ai_drivers_issues.txt")

autoware_ai_drivers_prs = []
contributor_type="pullRequests"
json_file="generated_json/autoware_ai_drivers_prs.json"
autoware_ai_drivers_prs += getContributors(json_file, contributor_type)
writeNamesToFile(autoware_ai_drivers_prs, "autoware_ai_drivers_prs.txt")


## autoware_ai_utilities
autoware_ai_utilities_issues = []
contributor_type="issues"
json_file="generated_json/autoware_ai_utilities_issues.json"
autoware_ai_utilities_issues += getContributors(json_file, contributor_type)
writeNamesToFile(autoware_ai_utilities_issues, "autoware_ai_utilities_issues.txt")

autoware_ai_utilities_prs = []
contributor_type="pullRequests"
json_file="generated_json/autoware_ai_utilities_prs.json"
autoware_ai_utilities_prs += getContributors(json_file, contributor_type)
writeNamesToFile(autoware_ai_utilities_prs, "autoware_ai_utilities_prs.txt")

## autoware_ai_common
autoware_ai_common_issues = []
contributor_type="issues"
json_file="generated_json/autoware_ai_common_issues.json"
autoware_ai_common_issues += getContributors(json_file, contributor_type)
writeNamesToFile(autoware_ai_common_issues, "autoware_ai_common_issues.txt")

autoware_ai_common_prs = []
contributor_type="pullRequests"
json_file="generated_json/autoware_ai_common_prs.json"
autoware_ai_common_prs += getContributors(json_file, contributor_type)
writeNamesToFile(autoware_ai_common_prs, "autoware_ai_common_prs.txt")

### ALL

autoware_code_contributors = autoware_prs \
                           + autoware_core_prs \
                           + universe_prs \
                           + autoware_msgs_prs \
                           + autoware_launch_prs \
                           + autoware_documentation_prs
autoware_community_contributors = autoware_discussions \
                                + autoware_issues \
                                + universe_issues \
                                + autoware_msgs_issues \
                                + autoware_launch_issues \
                                + autoware_documentation_issues 
autoware_contributors = autoware_code_contributors + autoware_community_contributors

autoware_code_contributors = sorted(set(autoware_code_contributors))
autoware_community_contributors = sorted(set(autoware_community_contributors))
autoware_contributors = sorted(set(autoware_contributors))

contributors = sorted(set(contributors))
writeNamesToFile(contributors, "all.txt")
writeNamesToFile(autoware_code_contributors, "autoware_code_contributors.txt")
writeNamesToFile(autoware_community_contributors, "autoware_community_contributors.txt")
writeNamesToFile(autoware_contributors, "autoware_contributors.txt")

