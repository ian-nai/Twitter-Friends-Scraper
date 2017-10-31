import time
import tweepy
import csv
import os

# Enter your own Consumer Key, Consumer Secret, Access Token, and Access Token Secret here.
auth = tweepy.OAuthHandler('consumer_key', 'consumer_secret')
auth.set_access_token('access_token', 'access_token_secret')

def friends_getter(): 
    
    print "Please enter the screen name of the user whose info you'd like to scrape."
    username_input = raw_input("Screen name: ")
    
    api = tweepy.API(auth)

    # Get the User object for twitter...
    user = api.get_user(username_input)

    print user.screen_name
    print user.followers_count
    ids = []
    for page in tweepy.Cursor(api.friends, screen_name=username_input).pages():
        ids.extend(page)
        time.sleep(30)

    print len(ids)

    usernames = []
    users = tweepy.Cursor(api.friends, screen_name=username_input).items()
    for u in users:
        print u.screen_name
        usernames.extend([u.screen_name])
        
    while True:
        try:
            user = next(users)
        except tweepy.TweepError:
            time.sleep(60*15)
            user = next(users)
        except StopIteration:
            break
        print "@" + user.screen_name
    
    save_file = raw_input("Save the list of friends in a .csv? Type 'y' for yes and 'n' for no.")
    if save_file == "y":
        with open(username_input + ".csv", "w") as f:
            wr = csv.writer(f, delimiter="\n")
            wr.writerow(usernames)
            print "File saved!"
            run_oncemore = raw_input("Scrape another user's friends?")
            if run_oncemore == "y":
                friends_getter()
            if run_oncemore == "n":
                print "Bye!"
                exit(0)           
    if save_file == "n":
        run_again = raw_input("Scrape another user's friends?")
        if run_again == "y":
            friends_getter()
        if run_again == "n":
            print "Bye!"
            exit(0)
                    
friends_getter()
