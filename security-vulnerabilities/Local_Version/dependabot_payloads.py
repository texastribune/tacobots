high_level_alert = """{
  "action": "created",
  "alert": {
    "number": 133,
    "state": "open",
    "dependency": {
      "package": {
        "ecosystem": "npm",
        "name": "pug"
      },
      "manifest_path": "package-lock.json",
      "scope": "runtime"
    },
    "security_advisory": {
      "ghsa_id": "GHSA-p493-635q-r6gr",
      "cve_id": "CVE-2021-21353",
      "summary": "Remote code execution via the `pretty` option.",
      "description": "### Impact\n\nIf a remote attacker was able to control the `pretty` option of the pug compiler, e.g. if you spread a user provided object such as the query parameters of a request into the pug template inputs, it was possible for them to achieve remote code execution on the node.js backend.\n\n### Patches\n\nUpgrade to `pug@3.0.1` or `pug-code-gen@3.0.2` or `pug-code-gen@2.0.3`, which correctly sanitise the parameter.\n\n### Workarounds\n\nIf there is no way for un-trusted input to be passed to pug as the `pretty` option, e.g. if you compile templates in advance before applying user input to them, you do not need to upgrade.\n\n### References\n\n\nOriginal report: https://github.com/pugjs/pug/issues/3312\n\n### For more information\n\nIf you believe you have found other vulnerabilities, please **DO NOT** open an issue. Instead, you can follow the instructions in our [Security Policy](https://github.com/pugjs/pug/blob/master/SECURITY.md)",
      "severity": "high",
      "identifiers": [
        {
          "value": "GHSA-p493-635q-r6gr",
          "type": "GHSA"
        },
        {
          "value": "CVE-2021-21353",
          "type": "CVE"
        }
      ],
      "references": [
        {
          "url": "https://github.com/pugjs/pug/security/advisories/GHSA-p493-635q-r6gr"
        },
        {
          "url": "https://github.com/pugjs/pug/issues/3312"
        },
        {
          "url": "https://github.com/pugjs/pug/pull/3314"
        },
        {
          "url": "https://github.com/pugjs/pug/commit/991e78f7c4220b2f8da042877c6f0ef5a4683be0"
        },
        {
          "url": "https://github.com/pugjs/pug/releases/tag/pug%403.0.1"
        },
        {
          "url": "https://www.npmjs.com/package/pug"
        },
        {
          "url": "https://www.npmjs.com/package/pug-code-gen"
        },
        {
          "url": "https://nvd.nist.gov/vuln/detail/CVE-2021-21353"
        },
        {
          "url": "https://github.com/advisories/GHSA-p493-635q-r6gr"
        }
      ],
      "published_at": "2021-03-03T02:03:52Z",
      "updated_at": "2022-08-13T03:06:18Z",
      "withdrawn_at": null,
      "vulnerabilities": [
        {
          "package": {
            "ecosystem": "npm",
            "name": "pug"
          },
          "severity": "high",
          "vulnerable_version_range": "< 3.0.1",
          "first_patched_version": {
            "identifier": "3.0.1"
          }
        },
        {
          "package": {
            "ecosystem": "npm",
            "name": "pug-code-gen"
          },
          "severity": "high",
          "vulnerable_version_range": "< 2.0.3",
          "first_patched_version": {
            "identifier": "2.0.3"
          }
        },
        {
          "package": {
            "ecosystem": "npm",
            "name": "pug-code-gen"
          },
          "severity": "high",
          "vulnerable_version_range": ">= 3.0.0, < 3.0.2",
          "first_patched_version": {
            "identifier": "3.0.2"
          }
        }
      ],
      "cvss": {
        "vector_string": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:N",
        "score": 6.8
      },
      "cwes": [
        {
          "cwe_id": "CWE-74",
          "name": "Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection')"
        }
      ]
    },
    "security_vulnerability": {
      "package": {
        "ecosystem": "npm",
        "name": "pug"
      },
      "severity": "high",
      "vulnerable_version_range": "< 3.0.1",
      "first_patched_version": {
        "identifier": "3.0.1"
      }
    },
    "url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/dependabot/alerts/133",
    "html_url": "https://github.com/shy540/Security-Vulnerability-Test/security/dependabot/133",
    "created_at": "2022-11-16T00:00:17Z",
    "updated_at": "2022-11-16T00:00:17Z",
    "dismissed_at": null,
    "dismissed_by": null,
    "dismissed_reason": null,
    "dismissed_comment": null,
    "fixed_at": null
  },
  "repository": {
    "id": 541801223,
    "node_id": "R_kgDOIEs7Bw",
    "name": "Security-Vulnerability-Test",
    "full_name": "shy540/Security-Vulnerability-Test",
    "private": true,
    "owner": {
      "login": "shy540",
      "id": 84746209,
      "node_id": "MDQ6VXNlcjg0NzQ2MjA5",
      "avatar_url": "https://avatars.githubusercontent.com/u/84746209?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/shy540",
      "html_url": "https://github.com/shy540",
      "followers_url": "https://api.github.com/users/shy540/followers",
      "following_url": "https://api.github.com/users/shy540/following{/other_user}",
      "gists_url": "https://api.github.com/users/shy540/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/shy540/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/shy540/subscriptions",
      "organizations_url": "https://api.github.com/users/shy540/orgs",
      "repos_url": "https://api.github.com/users/shy540/repos",
      "events_url": "https://api.github.com/users/shy540/events{/privacy}",
      "received_events_url": "https://api.github.com/users/shy540/received_events",
      "type": "User",
      "site_admin": false
    },
    "html_url": "https://github.com/shy540/Security-Vulnerability-Test",
    "description": null,
    "fork": false,
    "url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test",
    "forks_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/forks",
    "keys_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/keys{/key_id}",
    "collaborators_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/collaborators{/collaborator}",
    "teams_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/teams",
    "hooks_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/hooks",
    "issue_events_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/issues/events{/number}",
    "events_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/events",
    "assignees_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/assignees{/user}",
    "branches_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/branches{/branch}",
    "tags_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/tags",
    "blobs_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/git/blobs{/sha}",
    "git_tags_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/git/tags{/sha}",
    "git_refs_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/git/refs{/sha}",
    "trees_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/git/trees{/sha}",
    "statuses_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/statuses/{sha}",
    "languages_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/languages",
    "stargazers_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/stargazers",
    "contributors_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/contributors",
    "subscribers_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/subscribers",
    "subscription_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/subscription",
    "commits_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/commits{/sha}",
    "git_commits_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/git/commits{/sha}",
    "comments_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/comments{/number}",
    "issue_comment_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/issues/comments{/number}",
    "contents_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/contents/{+path}",
    "compare_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/compare/{base}...{head}",
    "merges_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/merges",
    "archive_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/{archive_format}{/ref}",
    "downloads_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/downloads",
    "issues_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/issues{/number}",
    "pulls_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/pulls{/number}",
    "milestones_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/milestones{/number}",
    "notifications_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/notifications{?since,all,participating}",
    "labels_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/labels{/name}",
    "releases_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/releases{/id}",
    "deployments_url": "https://api.github.com/repos/shy540/Security-Vulnerability-Test/deployments",
    "created_at": "2022-09-26T22:05:49Z",
    "updated_at": "2022-09-26T22:05:49Z",
    "pushed_at": "2022-11-16T00:00:15Z",
    "git_url": "git://github.com/shy540/Security-Vulnerability-Test.git",
    "ssh_url": "git@github.com:shy540/Security-Vulnerability-Test.git",
    "clone_url": "https://github.com/shy540/Security-Vulnerability-Test.git",
    "svn_url": "https://github.com/shy540/Security-Vulnerability-Test",
    "homepage": null,
    "size": 630,
    "stargazers_count": 0,
    "watchers_count": 0,
    "language": null,
    "has_issues": true,
    "has_projects": true,
    "has_downloads": true,
    "has_wiki": true,
    "has_pages": false,
    "has_discussions": false,
    "forks_count": 0,
    "mirror_url": null,
    "archived": false,
    "disabled": false,
    "open_issues_count": 2,
    "license": null,
    "allow_forking": true,
    "is_template": false,
    "web_commit_signoff_required": false,
    "topics": [

    ],
    "visibility": "private",
    "forks": 0,
    "open_issues": 2,
    "watchers": 0,
    "default_branch": "main"
  },
  "sender": {
    "login": "github",
    "id": 9919,
    "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
    "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
    "gravatar_id": "",
    "url": "https://api.github.com/users/github",
    "html_url": "https://github.com/github",
    "followers_url": "https://api.github.com/users/github/followers",
    "following_url": "https://api.github.com/users/github/following{/other_user}",
    "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/github/subscriptions",
    "organizations_url": "https://api.github.com/users/github/orgs",
    "repos_url": "https://api.github.com/users/github/repos",
    "events_url": "https://api.github.com/users/github/events{/privacy}",
    "received_events_url": "https://api.github.com/users/github/received_events",
    "type": "Organization",
    "site_admin": false
  }
}"""