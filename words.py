#!/usr/bin/env python
#coding=utf-8
"""
words.py - Phenny module for "Don't complete the Word"
Copyright 2012, Mark Scala
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""
import re
import random

pattern = re.compile('[abcdefghijklmnopqrstuvwxyz]')

# dictionary = open('/usr/share/dict/american-english-insane').readlines()
dictionary = open('/usr/share/dict/american-english').readlines()
dictionary = [x.strip() for x in dictionary if x[0] not in list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')]

players = [] # at least two players.
word = random.choice(list('abcdefghijklmnopqrstuvwxyz'))
challenge_time = None
game_on = 0
score = {} # nick:score

def display_rules(phenny, input):
    phenny.say('Go away!')

def join(phenny, input):
    global game_on
    global players
    if game_on == 1:
        phenny.say("I'm sorry, %s, but it's too late for you to join." % input.nick)
        return None
    if len(players) == 0:
        phenny.say("No one has offered a game, %s. Try '.word!'" % input.nick)
        return None
    phenny.say("%s has joined! We have a game!" % input.nick)
    players.append(input.nick)
    game_on = 1
    advance_turn(phenny,input)
join.commands = ['join!', 'join']

def word_challenge(phenny, input):
    global players
    players.append(input.nick)
    phenny.say("%s offers a game of \"Don't Complete The Word!\"" % input.nick)
    phenny.say("The rules are simple, but you can see them with the .wrules command.")
    phenny.say("'.join' to join.")
word_challenge.commands = ['word!', 'words!', 'start-words']

def replay(phenny,input):
    phenny.say("%s, we're waiting!" % players[0])

def next_letter(phenny, input):
    if input.nick != players[0]:
        phenny.say("%s, wait your turn to play!" % input.nick)
        replay(phenny,input)
        return None
    if len(players) < 2:
        phenny.say("%s, we need at least one more player." % input.nick)
        return None
    global word
    letter = input.group(2)
    if len(letter) == 1 and pattern.match(letter):
        word += letter
        res = test_word(word)
        if res == 1:
            phenny.say("%s, you numbskull! %s is a word! Look it up! You lose!" % (input.nick, word))
            cleanup()
        elif res == 2:
            phenny.say("Aaargh! %s, you ignominious wretch! %s cannot be extended to make ANY word! You lose!" % (input.nick, word))
            cleanup()
        else:
            advance_turn(phenny,input)
    else:
        phenny.say("%s, that is not a legal letter. Recall your abc's and select a letter from the alphabet, in lower case, please!" % input.nick)
next_letter.commands = ['try']

def cleanup():
    global word
    global players
    global game_on
    global score
    try:
        if players[1] in score.keys():
            score[player[1]] += 1
        else:
            score.setdefault(player[1],1)
    except:
        pass
    game_on = 0
    word = random.choice(list('abcdefghijklmnopqrstuvwxyz'))
    players = []

def show_score(phenny,input):
    global score
    try:
        for player in score.keys():
            phenny.say("%s has won %d games" % (player, score[player]))
    except:
        pass
show_score.commands = ['word-rank', 'wrank']

def check_candidate(wd):
    pattern = re.compile(wd)
    for w in dictionary:
        if pattern.match(w):
            return True
    else:
        return False

def test_word(w):
    "FIXME: iterating through the dictionary twice is not good."
    if w in dictionary:
        return 1
    elif not check_candidate(w):
        return 2
    else:
        return 0

def advance_turn(phenny, input):
    global players
    players = players[1:] + players[:1]
    phenny.say("%s, it's your turn." % players[0])
    phenny.say("Extend  '%s'  by one letter (which could make a word) without forming a dictionary word." % word)

if __name__ == '__main__':
    print __doc__.strip()
