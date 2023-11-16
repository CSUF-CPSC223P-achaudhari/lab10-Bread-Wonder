import threading
import json
import time 

def read_inventory(file_path='inventory.dat'):
    with open(file_path, 'r') as file:
        inventory_data = json.load(file)
    return inventory_data

def bot_fetcher(item_list, cart, lock):
    for item in item_list:
        item_number, item_description, seconds = item
        time.sleep(seconds)
        with lock:
            cart.append([item_number, item_description])

def bot_clerk(items):
    inventory = read_inventory()

    cart = []
    lock = threading.Lock()

    robot_fetcher_lists = [[], [], []]

    for i in range(len(items)):
        robot_fetcher_lists[i % 3].append([items[i], inventory[items[i]][0], inventory[items[i]][1]])

    f_list = []
    for fetcher_list in robot_fetcher_lists:
        ff_list = threading.Thread(target=bot_fetcher, args=(fetcher_list, cart, lock))
        f_list.append(ff_list)
        ff_list.start()

    for ff_list in f_list:
        ff_list.join()

    return cart