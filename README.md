# Itslearning-anti-surveillance
### A tool to render teachers' spying features useless
## Inner workings
```
 Scan for availible subjects/courses
 Create a map of every availible resource the student has access to
 Induvidually visit every element (GET)
 
 Elements include tasks, links, documents, PDFs, etc
```

# Purpose
## Problems
 An it's learning teacher can see when their students last saw their uploaded "resource".
 Teachers are able to see exactly what items a certain student access at any moment.
## Solution
 Visit every resource at once (using this tool) to render the "last seen" data for teachers useless.

## Usage
```
usage: itslearning.py [-h] [-s STARREDONLY] [-d DELAY] session

positional arguments:
  session               ASP.NET_SessionId

optional arguments:
  -h, --help            show this help message and exit
  -s STARREDONLY, --starredOnly STARREDONLY
                        Wether to only scan the subjects marked as * in it's learning
  -d DELAY, --delay DELAY
                        Delay in minutes

```
 The argument seen above is the session cookie that ties this session instance to your account.
 You can aquire the cookie by logging into it's learning and opening the "Storage" section of the F12 menu.

## Requirements (PIP available)
```
faker
bs4
requests
progressbar2
argparse
```
