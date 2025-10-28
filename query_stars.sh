#!/usr/bin/bash

gh api graphql -F cursor=$1 -F repository=$2 -f query='
query($cursor: String!, $repository: String!) {
  repository(owner:"autowarefoundation", name:$repository) {
    stargazers(first:100, after: $cursor) {
      totalCount
      edges {
        cursor
        starredAt
        node {
          login
        }
      }
    }
  }
}
' > tmp.txt
