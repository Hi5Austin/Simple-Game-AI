
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from random import *
import sys
import os

def random_game():
    global driver
    file_counter = 0
    file_counter += 1
    f = file('data/'+str(file_counter)+'.txt','w')
    #sequence = ''
    keys_dict = {Keys.RIGHT:2,Keys.DOWN:4,Keys.UP:3,Keys.LEFT:1}
    keys = [Keys.RIGHT,Keys.DOWN,Keys.UP,Keys.LEFT]
    driver.get("http://gabrielecirulli.github.io/2048/")
    game = driver.find_element_by_xpath('/html/body')

    running = True
    score = 0

    while running:
        key = choice(keys)
        key_sym = keys_dict[key]
        #sequence += (key_sym)
        game.send_keys(key)
        score = driver.find_elements_by_class_name('score-container')[0].text.split('\n')[0]

        f.write(str(key_sym)+',')
        f.write(str(score))
        f.write('\n')

        over = driver.find_elements_by_xpath("//*[contains(text(), 'Game over!')]")
        if (len(over) != 0):
            running = False
            driver.refresh()

def find_best():
    best_file = ''
    best_score = 0
    os.chdir('data')
    for name in os.listdir('./'):
        f = open(name,'r')
        lines = f.readlines()
        last_line = lines[-1]
        data = last_line.split(',')
        score = int(data[1][:-1])
        if(score > best_score):
              best_score = score
              best_file = name
    f = open(best_file,'r')
    lines = f.readlines()
    seq = ''
    for line in lines:
        seq += line[0]
    return [seq,best_score]

def train(seq,s_score):
    global driver
    score = s_score
    game = driver.find_element_by_xpath('/html/body')
    keys_dict = {'2':Keys.RIGHT,'4':Keys.DOWN,'3':Keys.UP,'1':Keys.LEFT}
    new_seq = ''
    while True:
        for i in range(len(seq)):
            chance = choice([1,2,3,4])
            if(choice == 4):
                new_seq += choice(['1','2','3','4'])
            new_seq += seq[i]
        for char in new_seq:
            game.send_keys(keys_dict[char])
        new_score = driver.find_elements_by_class_name('score-container')[0].text.split('\n')[0]
        restart_button = driver.find_elements_by_class_name('restart-button')[0].click()
        if new_score > score:
            seq = new_seq
            score = new_score

run = True
if(run):
    driver = webdriver.Firefox()
    num_random = int(sys.argv[1])

    for i in range(num_random):
        random_game()
    data = find_best()
    best_sequence = data[0]
    best_score = data[1]
    train(best_sequence,best_score)
