#!/usr/bin/bash

gh api graphql -F repository=$1 -f query='
query($repository: String!) {
  repository(owner:"autowarefoundation", name:$repository) {
    stargazers(first:1) {
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
