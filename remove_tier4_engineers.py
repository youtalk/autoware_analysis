import json
from collections import OrderedDict
import pprint
import subprocess

tier4_engineers = []

with open("tier4_engineers/tier4_engineers.txt") as file:
    tier4_engineers = file.read().splitlines()

def CountNonTierIVUsers(file_name, tier4_engineers):
    names = []
    filtered_list = []
    
    with open(file_name) as file:
        names = file.read().splitlines()
    
    for name in names:
        if name in tier4_engineers:
            filtered_list.append(name)
    print( file_name, len(names), "(" + str(len(filtered_list)) + ")" )

# with open("contributor_names/autoware_code_contributors.txt") as file:
#     names = file.read().splitlines()
# names = sorted(set(names))

CountNonTierIVUsers("contributor_names/autoware_code_contributors.txt", tier4_engineers)
CountNonTierIVUsers("contributor_names/autoware_community_contributors.txt", tier4_engineers)
CountNonTierIVUsers("contributor_names/autoware_contributors.txt", tier4_engineers)

CountNonTierIVUsers("contributor_names/autoware_discussions.txt", tier4_engineers)
CountNonTierIVUsers("contributor_names/autoware_issues.txt", tier4_engineers)
CountNonTierIVUsers("contributor_names/autoware_prs.txt", tier4_engineers)

CountNonTierIVUsers("contributor_names/universe_issues.txt", tier4_engineers)
CountNonTierIVUsers("contributor_names/universe_prs.txt", tier4_engineers)

CountNonTierIVUsers("contributor_names/autoware_core_issues.txt", tier4_engineers)
CountNonTierIVUsers("contributor_names/autoware_core_prs.txt", tier4_engineers)

CountNonTierIVUsers("contributor_names/autoware_msgs_issues.txt", tier4_engineers)
CountNonTierIVUsers("contributor_names/autoware_msgs_prs.txt", tier4_engineers)

CountNonTierIVUsers("contributor_names/autoware_launch_issues.txt", tier4_engineers)
CountNonTierIVUsers("contributor_names/autoware_launch_prs.txt", tier4_engineers)

CountNonTierIVUsers("contributor_names/autoware_documentation_issues.txt", tier4_engineers)
CountNonTierIVUsers("contributor_names/autoware_documentation_prs.txt", tier4_engineers)

CountNonTierIVUsers("contributor_names/autoware_ai_issues.txt", tier4_engineers)
CountNonTierIVUsers("contributor_names/autoware_ai_prs.txt", tier4_engineers)

CountNonTierIVUsers("contributor_names/autoware_ai_planning_issues.txt", tier4_engineers)
CountNonTierIVUsers("contributor_names/autoware_ai_planning_prs.txt", tier4_engineers)

CountNonTierIVUsers("contributor_names/autoware_ai_perception_issues.txt", tier4_engineers)
CountNonTierIVUsers("contributor_names/autoware_ai_perception_prs.txt", tier4_engineers)

CountNonTierIVUsers("contributor_names/autoware_ai_messages_issues.txt", tier4_engineers)
CountNonTierIVUsers("contributor_names/autoware_ai_messages_prs.txt", tier4_engineers)

CountNonTierIVUsers("contributor_names/autoware_ai_simulation_issues.txt", tier4_engineers)
CountNonTierIVUsers("contributor_names/autoware_ai_simulation_prs.txt", tier4_engineers)

CountNonTierIVUsers("contributor_names/autoware_ai_visualization_issues.txt", tier4_engineers)
CountNonTierIVUsers("contributor_names/autoware_ai_visualization_prs.txt", tier4_engineers)

CountNonTierIVUsers("contributor_names/autoware_ai_drivers_issues.txt", tier4_engineers)
CountNonTierIVUsers("contributor_names/autoware_ai_drivers_prs.txt", tier4_engineers)

CountNonTierIVUsers("contributor_names/autoware_ai_utilities_issues.txt", tier4_engineers)
CountNonTierIVUsers("contributor_names/autoware_ai_utilities_prs.txt", tier4_engineers)

CountNonTierIVUsers("contributor_names/autoware_ai_common_issues.txt", tier4_engineers)
CountNonTierIVUsers("contributor_names/autoware_ai_common_prs.txt", tier4_engineers)


