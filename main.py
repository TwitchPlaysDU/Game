#Define the imports
import twitch
import keycommands
import mousecommands
import user_timestamp
import re
import time
import os
import csv
import math
import sys

t = twitch.Twitch()

usr = "USER"
key = "oauth:OAUTH"
t.twitch_connect(usr, key)

command_log = {}
command_cooldown = 1.5

users_chatting = {}
users_chatting_cooldown = 240

kick_vote_cooldown = 120
kick_votes = {}
quorum_part = 0.35
min_kick_votes = 3

timeouts = [1800, 3600, 18000, 86400, 604800]
timeout_history = {}
kick_cooldowns = {}
kick_cooldown = 600

if os.path.isfile('timeouts.txt'):
    with open('timeouts.txt') as f:
        rows = csv.reader(f,delimiter=",",lineterminator="\n")
        next(rows, None)
        for row in rows:
            timeout_history[row[0]] = row[1]
 
while True:
    new_messages = t.twitch_recieve_messages()
 
    if not new_messages:
        continue
    else:
        for message in new_messages:       
            msg_queue = []
            queue = False
            while True:
                if len(msg_queue) > 0:
                    msg = msg_queue.pop(0)
                elif queue:
                    break
                else:
                    msg = message['message'].lower()
                    queue = True
                    
                username = message['username'].lower()
                
                users_chatting[username]= time.time()
                
                msg = re.sub(' +', ' ', msg)
                
                c = msg.split()
                if len(c) == 2 and c[0] == 'kick':
                    if c[1][0] != '@':
                        c[1] = '@' + c[1]
                    if c[1] not in kick_cooldowns or time.time() - kick_cooldowns[c[1]] > kick_cooldown:
                        if c[1] in kick_votes:
                            found = False
                            after_timeout = True
                            for user in kick_votes[c[1]]:
                                if after_timeout and time.time() - user.time < kick_vote_cooldown:
                                    after_timeout = False
                                if not found and user.user == username:
                                    user.time = time.time()
                                    found = True
                                    #break
                            if not found:
                                kick_votes[c[1]].add(user_timestamp.UserTimestamp(username, time.time()))
                            if after_timeout:
                                t.message(usr, 'Vote to kick %s started. You have 120 seconds. Send kick %s to join the vote. At least a third of active players has to participate.' % (c[1], c[1]))
                        else:
                            kick_votes[c[1]] = {user_timestamp.UserTimestamp(username, time.time())}
                            t.message(usr, 'Vote to kick %s started. You have 120 seconds. Send kick %s to join the vote. At least a third of active players has to participate.' % (c[1], c[1]))
                            
                        votes = 0
                        for user in kick_votes[c[1]]:
                            if time.time() - user.time < kick_vote_cooldown:
                                votes += 1
                        quorum = 0
                        for user in users_chatting:
                            if time.time() - users_chatting[user] < users_chatting_cooldown:
                                quorum += 1
                        
                        print('Active users now: %d' % quorum)
                        quorum = max(min_kick_votes, int(math.ceil(quorum * quorum_part)))
                        
                        print('Vote to kick %s: %d/%d' % (c[1], votes, quorum))
                        #t.message(usr, 'Vote to kick %s: %d/%d' % (c[1], votes, quorum))
                        
                        if votes >= quorum:
                            timeout = timeouts[0]
                            if c[1] in timeout_history:
                                try: new_timeout = timeouts.index(int(timeout_history[c[1]])) + 1
                                except: new_timeout = 0
                                if new_timeout >= len(timeouts):
                                    timeout = -1
                                else:
                                    timeout = timeouts[new_timeout]
                                    
                            if timeout != -1:
                                t.timeout(usr, c[1], timeout)
                                timeout_history[c[1]] = timeout
                                t.message(usr, '%s was kicked for %d seconds! PJSalt' % (c[1], timeout))
                                print ('%s kicked.' % c[1])
                            else:
                                t.ban(usr, c[1])
                                t.message(usr, '%s was banned forever! PJSalt' % c[1])
                                print ('%s banned.' % c[1])
                            kick_votes.pop(c[1])
                            kick_cooldowns[c[1]] = time.time()
                            
                            with open("timeouts.txt","w+") as f:
                                writer = csv.writer(f,delimiter=",",lineterminator="\n")
                                writer.writerow(['username', 'duration'])
                                for u in timeout_history:
                                    writer.writerow([u, timeout_history[u]])
                    continue
                            
                        
                msg = re.sub(r"([^1-9 ])([1-9])", r"\1 \2", msg)
                msg = re.sub(r"([1-9])([a-z])", r"\1 \2", msg)
                 
                try:
                    if not command_log.has_key(msg) or time.time() - command_log[msg] > command_cooldown:                    
                        if not keycommands.command(msg) and not mousecommands.command(msg):
                            #msg = re.sub(r"( )([1-9])", r"\2", msg)
                            #msg_split = msg.split()
                            #if len(msg_split) > 1:
                                #msg_queue.extend(msg_split)
                            continue
                        
                        command_log[msg] = time.time()
                        print(username + ": " + msg.encode('utf-8'))
                    
                        time.sleep(0.2)
                except:
                    print(sys.exc_info()[0])