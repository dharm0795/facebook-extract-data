import json
import re
import requests
import csv
import facebook
import itertools
token=""
#to acess data from api
graph=facebook.GraphAPI(token)
myprofile=graph.get_object("me")
#to extract family operation
family=graph.get_object("me/family")
familymember=[]
for it in family['data']:
	familymember.append([it['name'],it['relationship']])
print(familymember)
#to extract list of freinds
friends=graph.get_connections(myprofile['id'],'friends')
with open('FamilyMembers.csv','wb') as file:
	fl=csv.writer(file,delimiter=',')
	fl.writerow(['Name','Relationship'])
	fl.writerows(familymember)
#print(friends)
#now extract import information about friends
listoffriends=[]
male=[]
female=[]
for each in friends['data']:
	post=graph.get_object(id=each['id'])
	try:
		pt=post['languages']
		#print(pt)
		lst=[]
		for ech in range(0,len(pt)):
			lst.append(pt[ech]['name'])
		print(lst)
		listoffriends.append([each['id'],each['name'],post['gender'],post['hometown']['name'],lst])
		if(post['gender']=="male"):
			male.append([each['id'],each['name'],post['gender'],post['hometown']['name'],lst])
		else:
			female.append([each['id'],each['name'],post['gender'],post['hometown']['name'],lst])
	except(Exception):
		listoffriends.append([each['id'],each['name'],post['gender'],post['hometown']['name'],"Not Available"])
		if(post['gender']=="male"):
			male.append([each['id'],each['name'],post['gender'],post['hometown']['name'],"Not Avaiable"])
		else:
			female.append([each['id'],each['name'],post['gender'],post['hometown']['name'],"Available"])

#to write data in file
with open('ListofFreinds.csv','wb') as file:
	fl=csv.writer(file,delimiter=',')
	fl.writerow(['ID','NAME','GENDER','Hometown','Language'])
	fl.writerows(listoffriends)
#group according to gender male
with open('MaleListofFreinds.csv','wb') as file:
	fl=csv.writer(file,delimiter=',')
	fl.writerow(['ID','NAME','GENDER','Hometown','Langauge'])
	fl.writerows(male)
#group according to gender female
with open('FEMaleListofFreinds.csv','wb') as file:
	fl=csv.writer(file,delimiter=',')
	fl.writerow(['ID','NAME','GENDER','Hometown'])
	fl.writerows(female)

#initally self admin groups
groups = graph.get_object("me/groups")
for group_id in groups['data']:
    list2=[] #stores the name of the person posting in the group and the text message posted.
    feed=graph.get_object(group_id['id'] + "/feed", page=True, retry=3, limit=500) #get feed of the group
    GroupMembers=graph.get_object(group_id['id'] + "/members", page=True, retry=3, limit=500) #get group members
    #print GroupMembers
    list3=[] #stores the name of the members of the group
    flag=0; #0 that the group has no admin otherwise 1
    for member in GroupMembers['data']:
        list3.append([member['name']])
        if(member['administrator']==True):
            flag=1
            administrator=member['name']
    for each2 in feed['data']:
        #print feed['data']
        try:
            list2.append([each2['from']['name'],each2['message']])
        except(Exception):
            print each2['from']['name'] #Exception caused when no text is posted but only image(s). Print the name of the defaulter

    with open('group'+group_id['id']+'.csv', 'wb') as fp: #groups are named with the id of the group.
        a = csv.writer(fp, delimiter=',')
        a.writerow(['group name',group_id['name']])
        if(flag==0):
            a.writerow(['administrator','None'])
        else:
            a.writerow(['administrator',administrator])
        a.writerow([])
        a.writerow(['Members'])
        a.writerows(list3)
        a.writerow([])

        a.writerow(['from_name','message'])
        a.writerows(list2) 
