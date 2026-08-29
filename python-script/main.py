import requests
import Query
import json
import os
from collections import defaultdict
from dotenv import load_dotenv
from pathlib import Path
import config


# Path
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

response_file = DATA_DIR / "response.json"
gitresponse_file = DATA_DIR / "gitResponse.json"
svg_file = DATA_DIR / "github_heatmap.svg"

load_dotenv()
TOKENGITHUB = os.getenv("TOKENGITHUB")

json_data = {
    'query': Query.AIP,
    'variables': {
        'username': config.leetcodeusername,
    },
    'operationName': 'getUserProfile',
    
}

response = requests.post('https://leetcode.com/graphql/', json=json_data)

print("Done, LeetCode")

leetcodedata = json.loads(response.content)

with open (response_file, 'w') as f:
    json.dump(leetcodedata, f, indent=4)

# ==================
#      GITHUB
# ==================


json_data = {
    "query": Query.GITHUB,
    "variables": {
        "username": config.gtihubusername,
    },
    "operationName": "getUserProfile",
}

headers = {
    "Authorization": f"Bearer {TOKENGITHUB}",
    "Content-Type": "application/json",
}

response = requests.post(
    "https://api.github.com/graphql",
    json=json_data,
    headers=headers,
)

githubdata = response.json()

# Convenience variable
data = githubdata["data"]

# Calculate language breakdown
repos = data["user"]["topRepositories"]["nodes"]

languages = defaultdict(lambda: {"size": 0, "color": ""})

for repo in repos:
    for edge in repo["languages"]["edges"]:
        languages[edge["node"]["name"]]["size"] += edge["size"]
        languages[edge["node"]["name"]]["color"] = edge["node"]["color"]

total = sum(v["size"] for v in languages.values())

language_breakdown = [
    {
        "name": name,
        "percentage": round(info["size"] / total * 100, 2),
        "color": info["color"],
    }
    for name, info in languages.items()
]

language_breakdown.sort(key=lambda x: x["percentage"], reverse=True)

# Add it to your JSON
githubdata["data"]["user"]["languageBreakdown"] = language_breakdown

# Save everything
with open(gitresponse_file, "w") as f:
    json.dump(githubdata, f, indent=4)

print("Done, GitHub")

from xml.etree.ElementTree import Element, SubElement, ElementTree


weeks = githubdata["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]

CELL = 12
GAP = 4
RX = 2

WIDTH = len(weeks) * (CELL + GAP)
HEIGHT = 7 * (CELL + GAP)

colors = {
    "NONE": "#30363d",
    "FIRST_QUARTILE": "#126F5B",
    "SECOND_QUARTILE": "#17b58b",
    "THIRD_QUARTILE": "#20dba3",
    "FOURTH_QUARTILE": "#2CF5B9",
}

svg = Element(
    "svg",
    xmlns="http://www.w3.org/2000/svg",
    viewBox=f"0 0 {WIDTH} {HEIGHT}",
    width=str(WIDTH),
    height=str(HEIGHT),
)

for x, week in enumerate(weeks):
    for y, day in enumerate(week["contributionDays"]):

        SubElement(
            svg,
            "rect",
            x=str(x * (CELL + GAP)),
            y=str(y * (CELL + GAP)),
            width=str(CELL),
            height=str(CELL),
            rx=str(RX),
            fill=colors.get(day["contributionLevel"], "#222222"),
        )

ElementTree(svg).write(svg_file)

print("Generated github_heatmap.svg")