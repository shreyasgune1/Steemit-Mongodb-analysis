#!/usr/bin/python3

import datetime
import shelve
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

shelf = shelve.open("/steemdata/utopian-io.shelf")
posts = shelf['posts']
comments = shelf['comments']
shelf.close()

def sort_by_value(dict, reverse=False):
    return sorted(dict.items(), key=lambda k: (k[1], k[0]), reverse=reverse)

def increment_kv(dict, key, increment=1):
    if not key in dict:
        dict[key] = 0
    dict[key] += increment


nposts_type = {}
nposts_author = {}
nposts_tag = {}
nposts_date = {}
nposts_app_date = {}
body_lengths = {}

for post in posts:
    meta = post['json_metadata']
    app = meta['app']
    type = "None"
    if 'type' in meta:
        type = meta['type']
        
    increment_kv(nposts_type, type)
    increment_kv(nposts_author, post['author'])

    tags = set(meta['tags']) # set removes duplicates
    for tag in tags:
        increment_kv(nposts_tag, tag)

    date = post['created'].date()
    increment_kv(nposts_date, date)
    if "utopian" in app:
        increment_kv(body_lengths, type, len(post['body']))
        increment_kv(nposts_app_date, date)

avg_len = {}
for post_type in body_lengths:
    avg_len[post_type] = int(body_lengths[post_type]/nposts_type[post_type])


xFmt = mdates.DateFormatter('%m/%d')

##############################################
# Number of posts per day
##############################################
ann_utopian = datetime.datetime(2017, 9, 26, 10, 2, 0, 0)
ann_getting_serious = datetime.datetime(2017, 10, 14, 22, 58, 0, 0)
ann_busy_org = datetime.datetime(2017, 10, 17, 9, 52, 0, 0)
ann_400k_sp = datetime.datetime(2017, 10, 19, 15, 10, 0, 0)
ann_bot = datetime.datetime(2017, 10, 22, 8, 12, 0, 0)


plt.figure(figsize=(12, 6))
plt.grid()
dates = [mdates.date2num(x) + 0.5 for x in sorted(nposts_date.keys())]
nposts = [nposts_date[key] for key in sorted(nposts_date.keys())]
plt.bar(dates, nposts, label="Posts with tag 'utopian-io'")

dates = [mdates.date2num(x) + 0.5 for x in sorted(nposts_app_date.keys())]
nposts = [nposts_app_date[key] for key in sorted(nposts_app_date.keys())]
plt.bar(dates, nposts, color='r', label="Posts from utopian-io app")
plt.axvline(mdates.date2num(ann_utopian), color='green', linestyle='dashed', linewidth=2, label="[ANN] Utopian")
plt.axvline(mdates.date2num(ann_getting_serious), color='orange', linestyle='dashed', linewidth=2, label="[ANN] Getting Serious")
plt.axvline(mdates.date2num(ann_busy_org), color='blue', linestyle='dashed', linewidth=2, label="[ANN] Double Rewards")
plt.axvline(mdates.date2num(ann_400k_sp), color='red', linestyle='dashed', linewidth=2, label="[ANN] 400k SP")
plt.axvline(mdates.date2num(ann_bot), color='black', linestyle='dashed', linewidth=2, label="[ANN] Utopian Bot")

plt.gcf().autofmt_xdate()
plt.gca().xaxis.set_major_formatter(xFmt)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))
plt.legend(loc=2)
plt.title("Number of contributions per day (Sept. 26th - Oct. 28th 2017)")
plt.xlabel("Date")
plt.ylabel("Contributions per day")
plt.figtext(0.99, 0.01, "@crokkon", horizontalalignment="right", verticalalignment="bottom")
plt.savefig('/steemdata/contributions_per_day.png')

##############################################
# Posts per category
##############################################
plt.figure(figsize=(12, 6))
plt.grid()
nposts_type_sorted = sort_by_value(nposts_type, reverse=True)
xticks = range(0, len(nposts_type))
num_posts = [x[1] for x in nposts_type_sorted]
xlabels = [x[0] for x in nposts_type_sorted]
plt.bar(xticks, num_posts)
plt.gca().xaxis.set_ticks(xticks)
plt.gca().set_xticklabels(xlabels)
plt.gcf().autofmt_xdate(rotation=45)
plt.title("Number of posts per utopian category")
plt.ylabel("Number of posts")
plt.figtext(0.99, 0.01, "@crokkon", horizontalalignment="right", verticalalignment="bottom")
plt.savefig("/steemdata/posts_per_category.png")

##############################################
# Contributions per author
##############################################
TOP=50
plt.figure(figsize=(12, 6))
plt.grid()
nauthors = len(nposts_author)
nposts_author_sorted = sort_by_value(nposts_author, reverse=True)
nposts = [x[1] for x in nposts_author_sorted][:TOP]
xticks = range(0, TOP)
xlabels = [x[0] for x in nposts_author_sorted][:TOP]
plt.bar(xticks, nposts)
plt.text(TOP/2, max(nposts)-1, "Total number of unique contributors: %d" % nauthors, \
         fontsize=12, bbox={'facecolor':'white'})
plt.gca().xaxis.set_ticks(xticks)
plt.gca().set_xticklabels(xlabels)
plt.gcf().autofmt_xdate(rotation=45)
plt.title("Number of contributions per user (Sept. 26th - Oct. 28th 2017)")
plt.ylabel("Number of contributions")
plt.figtext(0.99, 0.01, "@crokkon", horizontalalignment="right", verticalalignment="bottom")
plt.savefig("/steemdata/posts_per_author.png")

##############################################
# Average post length
##############################################
plt.figure(figsize=(12, 6))
plt.grid()
lengths = [avg_len[x] for x in avg_len]
xticks = range(0, len(avg_len))
xlabels = [x for x in avg_len]
plt.bar(xticks, lengths)
plt.gca().xaxis.set_ticks(xticks)
plt.gca().set_xticklabels(xlabels)
plt.gcf().autofmt_xdate(rotation=45)
plt.title("Average length of contributions (Sept. 26th - Oct. 28th 2017)")
plt.ylabel("Contribution body length (chars)")
plt.figtext(0.99, 0.01, "@crokkon", horizontalalignment="right", verticalalignment="bottom")
plt.savefig("/steemdata/contribution_lengths.png")


##############################################
# Number of comments with utopian app per day
##############################################
ncomments_date = {}
for comment in comments:
    date = comment['created'].date()
    increment_kv(ncomments_date, date)

plt.figure(figsize=(12, 6))
plt.grid()
dates = [mdates.date2num(x) + 0.5 for x in sorted(ncomments_date.keys())]
ncomments = [ncomments_date[key] for key in sorted(ncomments_date.keys())]
plt.bar(dates, ncomments, label="Comments with utopian app")

plt.axvline(mdates.date2num(ann_utopian), color='green', linestyle='dashed', linewidth=2, label="[ANN] Utopian")
plt.axvline(mdates.date2num(ann_getting_serious), color='orange', linestyle='dashed', linewidth=2, label="[ANN] Getting Serious")
plt.axvline(mdates.date2num(ann_busy_org), color='blue', linestyle='dashed', linewidth=2, label="[ANN] Double Rewards")
plt.axvline(mdates.date2num(ann_400k_sp), color='red', linestyle='dashed', linewidth=2, label="[ANN] 400k SP")
plt.axvline(mdates.date2num(ann_bot), color='black', linestyle='dashed', linewidth=2, label="[ANN] Utopian Bot")

plt.gcf().autofmt_xdate()
plt.gca().xaxis.set_major_formatter(xFmt)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))
plt.legend(loc=2)
plt.title("Number of comments with the utopian app per day (Sept. 26th - Oct. 28th 2017)")
plt.xlabel("Date")
plt.ylabel("Comments per day")
plt.figtext(0.99, 0.01, "@crokkon", horizontalalignment="right", verticalalignment="bottom")
plt.savefig('/steemdata/comments_per_day.png')
