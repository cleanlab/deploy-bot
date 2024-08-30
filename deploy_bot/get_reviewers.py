import os
from typing import Dict, List, Set

import requests
from six import b


GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN")


def find_contributors_to_branch(repository: str, head_branch: str, base_branch: str) -> Set[str]:
    """Finds authors of commits to head branch that are NOT in base branch.

    :param head_branch: head branch of diff
    :param base_branch: base branch of diff
    :return: set of authors of commits in head branch but not in base
    """
    gh_api_response: requests.Response = requests.get(
        f"https://api.github.com/repos/{repository}/compare/{base_branch}...{head_branch}",
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
        }
)

    assert gh_api_response.status_code == 200, f"Bad response from GitHub compare API {gh_api_response.url, gh_api_response.text}."

    response_dict: Dict = gh_api_response.json()
    commits: List[Dict] = response_dict.get("commits")

    return {commit.get("author").get("login") for commit in commits}


def cast_bool_arg(val: str) -> bool:
    """Casts value from argparse to bool."""
    return val.lower() == "true"


if __name__ == "__main__":

    import argparse

    parser: argparse.ArgumentParser = argparse.ArgumentParser(prog="Get reviewers for PR")
    parser.add_argument(
        "--repository",
        help="repository to get diff from",
    )
    parser.add_argument(
        "--head-branch",
        dest="head_branch",
        help="head branch for comparison",
    )
    parser.add_argument(
        "--base-branch",
        dest="base_branch",
        help="base branch for comparison",
    )
    parser.add_argument(
        "--should-add-reviewers",
        dest="should_add_reviewers",
        help="if should add reviewers to PR",
        type=cast_bool_arg,
    )
    parser.add_argument(
        "--required-reviewers",
        dest="required_reviewers",
        help="list of required reviewers, as comma separated list"
    )

    args = parser.parse_args()

    if args.should_add_reviewers:
        # find contributors to branch
        contributors: Set[str] = find_contributors_to_branch(args.repository, args.head_branch, args.base_branch)

        # output reviewers as comma delimited list
        reviewers = contributors | set(args.required_reviewers.split(","))
        print(",".join(reviewers))

    exit(0)
