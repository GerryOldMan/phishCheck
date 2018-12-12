#!/usr/bin/python
'''
Download database from phish tank
Check to find new phishing sites against old database
Check to see if new ones have https and record
Check to see if they have a target
'''

'''
Pickle the dictionaries to help load if script breaks
'''

#How do I track days, weeks, months, quarters?

#Set the imports
from urllib.request import urlopen
import json
import _pickle as pkl
import os
from datetime import datetime, timedelta

current = datetime.now()
previous_day = current - timedelta(days=1)

#Path for files
direct = str(current.strftime('%Y'))+'/'+current.strftime('%b')
path = str(current.strftime('%Y'))+'/'+current.strftime('%b')+'/'+current.strftime('%d')+current.strftime('%a')+'.pkl'
#previous days file
oldPath = str(previous_day.strftime('%Y'))+'/'+previous_day.strftime('%b')+'/'+previous_day.strftime('%d')+previous_day.strftime('%a')+'.pkl'

#Get the data from PhishTank

phishUrl = 'http://data.phishtank.com/data/online-valid.json'
response = urlopen(phishUrl)

data = json.load(response)
#Save the data to a pickle file
#First check that the folder exists and if not make it
os.makedirs(os.path.dirname(path), exist_ok=True)
pkl.dump(data, open(path,'wb'))

#Check old database to see if any new phishing sites

#Load the previous days data
oldData = pkl.load(open(oldPath,'rb'))

#Compare the two files for new sites.
additional = filter(lambda x:x not in data,oldData)

#Try to load Targets
try:
	targets = pkl.load(open(direct+'/targets.pkl','rb'))
except:
	targets = {}

#Add the new finds to the targets list.
for i in additional:
	if i['target'] in targets:
		targets[i['target']] += 1
	elif i['target'] != 'Other':
		targets[i['target']] = 1

#Save the new target pickle file
pkl.dump(targets, open(direct+'/targets.pkl','wb'))

#Sort the dictionary in to biggest to smallest
ordered_list = sorted(targets, key=targets.get, reverse=True)

#Then create html file
html = '''
<!DOCTYPE html>
<html lang="en">

  <head>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>BetterPassword - Most Phished Sites</title>

    <!-- Bootstrap core CSS -->
    <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom fonts for this template -->
    <link href="vendor/fontawesome-free/css/all.min.css" rel="stylesheet" type="text/css">
    <link href='https://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic' rel='stylesheet' type='text/css'>
    <link href='https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800' rel='stylesheet' type='text/css'>

    <!-- Custom styles for this template -->
    <link href="css/clean-blog.min.css" rel="stylesheet">

    <style>
      table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
      }
      th, td {
        padding: 15px;
      }
      </style>

  </head>

  <body>
    <div class="container">
      <div class="row">
        <div class="col-lg-8 col-md-10 mx-auto">
          <div class="post-heading">
            <h1>Most fake sites December</h1>
            <h2 class="subheading">These are the sites that have been most impersonated this month</h2>
          </div>

          <table >
            <tr>
              <th>Site</th>
              <th>Number</th>
            </tr>
            <tr>
              <th>%s</th>
              <th>%s</th>
            </tr>
			<tr>
				<th>%s</th>
				<th>%s</th>
			</tr>
			<tr>
              <th>%s</th>
              <th>%s</th>
            </tr>
			<tr>
				<th>%s</th>
				<th>%s</th>
			</tr>
			<tr>
				<th>%s</th>
				<th>%s</th>
			</tr>


          </table>
        </div>
      </div>
    </body>
	''' %(ordered_list[0], targets[ordered_list[0]],ordered_list[1], targets[ordered_list[1]],
	ordered_list[2], targets[ordered_list[2]],ordered_list[3], targets[ordered_list[3]],ordered_list[4], targets[ordered_list[4]])

f = open('sites.html','w')
f.write(html)
f.close()
