import json
from collections import OrderedDict
import pprint
import subprocess


def getFirstCursor(script, contributor_type, repository):
    res = subprocess.run(["bash", script, repository])
    f = open("tmp.txt", "r")
    loaded_json = json.load(f)
    if len(loaded_json["data"]["repository"][contributor_type]["edges"]) == 0:
        return None
    return loaded_json["data"]["repository"][contributor_type]["edges"][0]["cursor"]

def getContributors(script, cursor_script, contributor_type, respository):
    all_edges=[]

    first_cursor=getFirstCursor(cursor_script, contributor_type, repository)
    if first_cursor == None:
        return all_edges

    print(contributor_type, repository)
    cursor=first_cursor
    res = subprocess.run(["bash", script, cursor, repository])
    f = open("tmp.txt", "r")

    loaded_json = json.load(f)

    edges = loaded_json["data"]["repository"][contributor_type]["edges"]

    while len(edges) > 0:
        all_edges += edges
        print(len(edges))

        cursor=edges[-1]["cursor"]
        res = subprocess.run(["bash", script, cursor, repository])
        f = open("tmp.txt", "r")
        loaded_json = json.load(f)
        edges = loaded_json["data"]["repository"][contributor_type]["edges"]

    return all_edges

def dumpJson(json_dict, file_name):
    with open("generated_json/" +file_name, 'w') as fp:
        json.dump(json_dict, fp, indent=2)

contributors = []

## autoware

autoware_discussions = []
cursor_script="get_first_discussion.sh"
script="query_discussions.sh"
contributor_type="discussions"
repository="autoware"
autoware_discussions += getContributors(script, cursor_script, contributor_type, repository)
contributors += autoware_discussions
dumpJson(autoware_discussions, "autoware_discussions.json")

autoware_issues = []
cursor_script="get_first_issue.sh"
script="query_issues.sh"
contributor_type="issues"
repository="autoware"
autoware_issues += getContributors(script, cursor_script, contributor_type, repository)
contributors += autoware_issues
dumpJson(autoware_issues, "autoware_issues.json")

autoware_prs = []
cursor_script="get_first_pr.sh"
script="query_prs.sh"
contributor_type="pullRequests"
repository="autoware"
autoware_prs += getContributors(script, cursor_script, contributor_type, repository)
contributors += autoware_prs
dumpJson(autoware_prs, "autoware_prs.json")

## autoware_universe

universe_issues = []
cursor_script="get_first_issue.sh"
script="query_issues.sh"
contributor_type="issues"
repository="autoware_universe"
universe_issues += getContributors(script, cursor_script, contributor_type, repository)
contributors += universe_issues
dumpJson(universe_issues, "universe_issues.json")

universe_prs = []
cursor_script="get_first_pr.sh"
script="query_prs.sh"
contributor_type="pullRequests"
repository="autoware_universe"
universe_prs += getContributors(script, cursor_script, contributor_type, repository)
contributors += universe_prs
dumpJson(universe_prs, "universe_prs.json")

## autoware_core
autoware_core_issues = []
cursor_script="get_first_issue.sh"
script="query_issues.sh"
contributor_type="issues"
repository="autoware_core"
autoware_core_issues += getContributors(script, cursor_script, contributor_type, repository)
contributors += autoware_core_issues
dumpJson(autoware_core_issues, "autoware_core_issues.json")

autoware_core_prs = []
cursor_script="get_first_pr.sh"
script="query_prs.sh"
contributor_type="pullRequests"
repository="autoware_core"
autoware_core_prs += getContributors(script, cursor_script, contributor_type, repository)
contributors += autoware_core_prs
dumpJson(autoware_core_prs, "autoware_core_prs.json")

## autoware_msgs
autoware_msgs_issues = []
cursor_script="get_first_issue.sh"
script="query_issues.sh"
contributor_type="issues"
repository="autoware_msgs"
autoware_msgs_issues += getContributors(script, cursor_script, contributor_type, repository)
contributors += autoware_msgs_issues
dumpJson(autoware_msgs_issues, "autoware_msgs_issues.json")

autoware_msgs_prs = []
cursor_script="get_first_pr.sh"
script="query_prs.sh"
contributor_type="pullRequests"
repository="autoware_msgs"
autoware_msgs_prs += getContributors(script, cursor_script, contributor_type, repository)
contributors += autoware_msgs_prs
dumpJson(autoware_msgs_prs, "autoware_msgs_prs.json")

## autoware_launch
autoware_launch_issues = []
cursor_script="get_first_issue.sh"
script="query_issues.sh"
contributor_type="issues"
repository="autoware_launch"
autoware_launch_issues += getContributors(script, cursor_script, contributor_type, repository)
contributors += autoware_launch_issues
dumpJson(autoware_launch_issues, "autoware_launch_issues.json")

autoware_launch_prs = []
cursor_script="get_first_pr.sh"
script="query_prs.sh"
contributor_type="pullRequests"
repository="autoware_launch"
autoware_launch_prs += getContributors(script, cursor_script, contributor_type, repository)
contributors += autoware_launch_prs
dumpJson(autoware_launch_prs, "autoware_launch_prs.json")

## autoware_documentation
autoware_documentation_issues = []
cursor_script="get_first_issue.sh"
script="query_issues.sh"
contributor_type="issues"
repository="autoware-documentation"
autoware_documentation_issues += getContributors(script, cursor_script, contributor_type, repository)
contributors += autoware_documentation_issues
dumpJson(autoware_documentation_issues, "autoware_documentation_issues.json")

autoware_documentation_prs = []
cursor_script="get_first_pr.sh"
script="query_prs.sh"
contributor_type="pullRequests"
repository="autoware-documentation"
autoware_documentation_prs += getContributors(script, cursor_script, contributor_type, repository)
contributors += autoware_documentation_prs
dumpJson(autoware_documentation_prs, "autoware_documentation_prs.json")

## autoware_ai

autoware_ai_issues = []
cursor_script="get_first_issue.sh"
script="query_issues.sh"
contributor_type="issues"
repository="autoware_ai"
autoware_ai_issues += getContributors(script, cursor_script, contributor_type, repository)
dumpJson(autoware_ai_issues, "autoware_ai_issues.json")

## autoware_ai_perception
autoware_ai_perception_issues = []
cursor_script="get_first_issue.sh"
script="query_issues.sh"
contributor_type="issues"
repository="autoware_ai_perception"
autoware_ai_perception_issues += getContributors(script, cursor_script, contributor_type, repository)
dumpJson(autoware_ai_perception_issues, "autoware_ai_perception_issues.json")

autoware_ai_perception_prs = []
cursor_script="get_first_pr.sh"
script="query_prs.sh"
contributor_type="pullRequests"
repository="autoware_ai_perception"
autoware_ai_perception_prs += getContributors(script, cursor_script, contributor_type, repository)
dumpJson(autoware_ai_perception_prs, "autoware_ai_perception_prs.json")

## autoware_ai_planning
autoware_ai_planning_issues = []
cursor_script="get_first_issue.sh"
script="query_issues.sh"
contributor_type="issues"
repository="autoware_ai_planning"
autoware_ai_planning_issues += getContributors(script, cursor_script, contributor_type, repository)
dumpJson(autoware_ai_planning_issues, "autoware_ai_planning_issues.json")

autoware_ai_planning_prs = []
cursor_script="get_first_pr.sh"
script="query_prs.sh"
contributor_type="pullRequests"
repository="autoware_ai_planning"
autoware_ai_planning_prs += getContributors(script, cursor_script, contributor_type, repository)
dumpJson(autoware_ai_planning_prs, "autoware_ai_planning_prs.json")

## autoware_ai_messages
autoware_ai_messages_issues = []
cursor_script="get_first_issue.sh"
script="query_issues.sh"
contributor_type="issues"
repository="autoware_ai_messages"
autoware_ai_messages_issues += getContributors(script, cursor_script, contributor_type, repository)
dumpJson(autoware_ai_messages_issues, "autoware_ai_messages_issues.json")

autoware_ai_messages_prs = []
cursor_script="get_first_pr.sh"
script="query_prs.sh"
contributor_type="pullRequests"
repository="autoware_ai_messages"
autoware_ai_messages_prs += getContributors(script, cursor_script, contributor_type, repository)
dumpJson(autoware_ai_messages_prs, "autoware_ai_messages_prs.json")

## autoware_ai_simulation
autoware_ai_simulation_issues = []
cursor_script="get_first_issue.sh"
script="query_issues.sh"
contributor_type="issues"
repository="autoware_ai_simulation"
autoware_ai_simulation_issues += getContributors(script, cursor_script, contributor_type, repository)
dumpJson(autoware_ai_simulation_issues, "autoware_ai_simulation_issues.json")

autoware_ai_simulation_prs = []
cursor_script="get_first_pr.sh"
script="query_prs.sh"
contributor_type="pullRequests"
repository="autoware_ai_simulation"
autoware_ai_simulation_prs += getContributors(script, cursor_script, contributor_type, repository)
dumpJson(autoware_ai_simulation_prs, "autoware_ai_simulation_prs.json")

## autoware_ai_visualization
autoware_ai_visualization_issues = []
cursor_script="get_first_issue.sh"
script="query_issues.sh"
contributor_type="issues"
repository="autoware_ai_visualization"
autoware_ai_visualization_issues += getContributors(script, cursor_script, contributor_type, repository)
dumpJson(autoware_ai_visualization_issues, "autoware_ai_visualization_issues.json")

autoware_ai_visualization_prs = []
cursor_script="get_first_pr.sh"
script="query_prs.sh"
contributor_type="pullRequests"
repository="autoware_ai_visualization"
autoware_ai_visualization_prs += getContributors(script, cursor_script, contributor_type, repository)
dumpJson(autoware_ai_visualization_prs, "autoware_ai_visualization_prs.json")

## autoware_ai_drivers
autoware_ai_drivers_issues = []
cursor_script="get_first_issue.sh"
script="query_issues.sh"
contributor_type="issues"
repository="autoware_ai_drivers"
autoware_ai_drivers_issues += getContributors(script, cursor_script, contributor_type, repository)
dumpJson(autoware_ai_drivers_issues, "autoware_ai_drivers_issues.json")

autoware_ai_drivers_prs = []
cursor_script="get_first_pr.sh"
script="query_prs.sh"
contributor_type="pullRequests"
repository="autoware_ai_drivers"
autoware_ai_drivers_prs += getContributors(script, cursor_script, contributor_type, repository)
dumpJson(autoware_ai_drivers_prs, "autoware_ai_drivers_prs.json")

## autoware_ai_utilities
autoware_ai_utilities_issues = []
cursor_script="get_first_issue.sh"
script="query_issues.sh"
contributor_type="issues"
repository="autoware_ai_utilities"
autoware_ai_utilities_issues += getContributors(script, cursor_script, contributor_type, repository)
dumpJson(autoware_ai_utilities_issues, "autoware_ai_utilities_issues.json")

autoware_ai_utilities_prs = []
cursor_script="get_first_pr.sh"
script="query_prs.sh"
contributor_type="pullRequests"
repository="autoware_ai_utilities"
autoware_ai_utilities_prs += getContributors(script, cursor_script, contributor_type, repository)
dumpJson(autoware_ai_utilities_prs, "autoware_ai_utilities_prs.json")

## autoware_ai_common
autoware_ai_common_issues = []
cursor_script="get_first_issue.sh"
script="query_issues.sh"
contributor_type="issues"
repository="autoware_ai_common"
autoware_ai_common_issues += getContributors(script, cursor_script, contributor_type, repository)
dumpJson(autoware_ai_common_issues, "autoware_ai_common_issues.json")

autoware_ai_common_prs = []
cursor_script="get_first_pr.sh"
script="query_prs.sh"
contributor_type="pullRequests"
repository="autoware_ai_common"
autoware_ai_common_prs += getContributors(script, cursor_script, contributor_type, repository)
dumpJson(autoware_ai_common_prs, "autoware_ai_common_prs.json")

