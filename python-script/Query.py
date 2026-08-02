LANGUAGE = """
query languageStats($username: String!) {
    matchedUser(username: $username) {    
        languageProblemCount {      
            languageName      
            problemsSolved    
        }  
    }
}  
  
"""


PROGRESS = """    
query userProfileUserQuestionProgressV2($username: String!) {  
    userProfileUserQuestionProgressV2(userSlug: $username) {    
        numAcceptedQuestions {      
            count      
            difficulty    
        }    
        numFailedQuestions {      
            count      
            difficulty    
        }    
        numUntouchedQuestions {      
            count      
            difficulty    
        }    
        userSessionBeatsPercentage {      
            difficulty      
            percentage    
        }    
        totalQuestionBeatsPercentage  
        
    }
}    
"""


PROGRESSv2 = """
query userSessionProgress($username: String!) {  
    allQuestionsCount {    
        difficulty    
        count  
    }  
    matchedUser(username: $username) {    
        submitStats {      
            acSubmissionNum {        
                difficulty        
                count        
                submissions      
            }      
            totalSubmissionNum {        
                difficulty        
                count        
                submissions      
            }    
        }  
    }
}

"""

CALENDER = """
query userProfileCalendar($username: String!, $year: Int) {  
    matchedUser(username: $username) {    
        userCalendar(year: $year) {      
            activeYears      
            streak      
            totalActiveDays      
            dccBadges {        
                timestamp        
                badge {          
                    name          
                    icon        
                }      
            }      
            submissionCalendar    
        }  
    }
}

"""

AIP = """
query getUserProfile($username: String!, $year: Int) {
    allQuestionsCount {
        difficulty
        count
    }
    matchedUser(username: $username) {
        username
        contributions {
            points
            questionCount
            testcaseCount
        }
        profile {
            realName
            userAvatar
            ranking
        }
        badges {
            id
            displayName
            icon
            creationDate
        }
        activeBadge {
            id
            displayName
            icon
            creationDate
        }
        submitStats {
            totalSubmissionNum {
                difficulty
                count
                submissions
            }
            acSubmissionNum {
                difficulty
                count
                submissions
            }
        }
        userCalendar(year: $year) {      
            activeYears      
            streak      
            totalActiveDays         
        }  
        submissionCalendar
    }
}
"""



COMBINED = """
query userData($username: String!, $year: Int) {

  allQuestionsCount {
    difficulty
    count
  }

  matchedUser(username: $username) {
    languageProblemCount {
      languageName
      problemsSolved
    }

    submitStats {
      acSubmissionNum {
        difficulty
        count
        submissions
      }
      totalSubmissionNum {
        difficulty
        count
        submissions
      }
    }
    userCalendar(year: $year) {      
        activeYears      
        streak      
        totalActiveDays      
        dccBadges {        
            timestamp        
            badge {          
                name          
                icon        
            }      
        }      
        submissionCalendar    
    }  
    
  }

  userProfileUserQuestionProgressV2(userSlug: $username) {
    numAcceptedQuestions {
      count
      difficulty
    }
    numFailedQuestions {
      count
      difficulty
    }
    numUntouchedQuestions {
      count
      difficulty
    }
    userSessionBeatsPercentage {
      difficulty
      percentage
    }
    totalQuestionBeatsPercentage
  }


}
"""


GITHUB = """
query getUserProfile($username: String!) {
  user(login: $username) {

    login
    name
    avatarUrl
    bio

    followers {
      totalCount
    }

    following {
      totalCount
    }

    # Total public repositories
    repoCount: repositories(privacy: PUBLIC) {
      totalCount
    }

    # Contribution graph
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            contributionLevel
          }
        }
      }
    }

    # Top repositories
    topRepositories: repositories(
      first: 100
      privacy: PUBLIC
      ownerAffiliations: OWNER
      orderBy: {
        field: STARGAZERS
        direction: DESC
      }
    ) {
      nodes {
        name
        description
        url
        stargazerCount
        forkCount

        primaryLanguage {
          name
          color
        }

        languages(
          first: 10
          orderBy: {
            field: SIZE
            direction: DESC
          }
        ) {
          edges {
            size
            node {
              name
              color
            }
          }
        }
      }
    }
  }
# PRs Merged
  mergedPRs: search(
    query: "is:pr is:merged author:$username"
    type: ISSUE
    first: 1
  ) {
    issueCount
  }
}
"""