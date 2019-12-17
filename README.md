# Itslearning-anti-surveillance
### A tool to single handedly render the teachers' spying features useless.
## Inner workings
 Scan for availible subjects/courses
 Create a map of every availible resource the student has access to
 Induvidually visit every element (GET)

# Purpose
## Problems
 An it's learning teacher can see when their students last saw their uploaded "resource"
 Teachers are able to see exactly what items a certain student access at any moment
## Solution
 Visit every resource at once (using this tool) to render the "last seen" data for teachers useless

## Usage
```
python itslearning.py <ASP.NET_SessionId>
```
 The argument seen above is the session cookie that ties this session instance to your account.
 You can aquire the cookie by logging into it's learning and opening the "Storage" section of the F12 menu

## Requirements
```
faker
bs4
requests
progressbar2
argparse
```
