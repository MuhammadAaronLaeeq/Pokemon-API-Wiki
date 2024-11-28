from cgitb import text
from ctypes.wintypes import UINT
from shutil import move
import requests
from requests import Session
from pprint import pprint as pp
import tkinter as tk
import ttkbootstrap as ttk

global uInput
global inputWidget

class PokemonClass():
    def __init__(self):
        self.e2 = 'https://pokeapi.co/api/v2/pokemon/'
        self.session = Session()


    def organizeMoves(self, Pokemon):
        url = self.e2 + Pokemon + '/'
        request = self.session.get(url)
        try:
            move_list_info = request.json()['moves']
            moves = []
            for i in range(len(move_list_info)):
                for j in range(len(move_list_info[i]['version_group_details'])):
                    d = {}
                    moves.append(d)
                    d['name'] = move_list_info[i]['move']['name']
                    d['game_version'] = move_list_info[i]['version_group_details'][j]['version_group']['name']
                    d['method'] = move_list_info[i]['version_group_details'][j]['move_learn_method']['name']
                    d['level'] = move_list_info[i]['version_group_details'][j]['level_learned_at']
    
            return moves

        except:
            return None


    def versionSelectMoveset(self, version, Pokemon):

        moves = self.organizeMoves(Pokemon)
        game_move_dict = {}
        version_list = []

        try:
            for i in range(len(moves)):
                version_list.append(moves[i]['game_version'])
                version_list = list(dict.fromkeys(version_list))
                game_move_dict[moves[i]['game_version']] = []
        
        except:
            return None
        try:
            for i in range(len(moves)):
                for j in version_list:
                    if moves[i]['game_version'] == j:
                        game_move_dict[j].append(moves[i])

            return game_move_dict[version]

        except:
            return None


    def displayMoveset(self,version,Pokemon, moves_y_n):
        if moves_y_n == True:
            dictionary = self.versionSelectMoveset(version, Pokemon)

            try:
                updated_dictionary = []
                for i in range(len(dictionary)):
                    arr = list(dictionary[i].values())
                    updated_dictionary.append(arr)

                updated_dictionary.sort(key=lambda x : x[0])
                print("\n {: <20} {: <20} {: <15}".format('Move', 'Method Used', 'Level Obtained') + '\n')
                for i in range(len(updated_dictionary)):
                    print("{: <20} {: <20} {: <15}".format(updated_dictionary[i][0],updated_dictionary[i][2],updated_dictionary[i][3]))

                return True

            except TypeError:
                print('Poke')
                return False

        else:
            True



def userInput():
    Pokemon = input('What Pokemon do you want information for? \n').lower()
    Version = input('For what version? \n').lower()
    word_list = Version.split()
    if len(word_list) == 2:
        Version = word_list[0] + '-' + word_list[1]

    return Pokemon, Version


def sendInfo():
    pokemon = inputWidget.get()
    print(uInput.get())



def inputWindow():
    window = tk.Tk()
    window.geometry('750x400')
    
    title = ttk.Label(master = window, text = 'Enter Pokemon', font = 'Calibri 24 bold')
    title.pack(pady=50)

    inputFrame = ttk.Frame(master = window)
    inputFrame.pack()

    uInput = tk.StringVar()
    inputWidget = ttk.Entry(master = inputFrame, textvariable = uInput)
    inputWidget.pack(pady=50)

    searchButton = ttk.Button(master = inputFrame, text = 'Search...', command = sendInfo)
    searchButton.pack()

    window.mainloop()




def main():
    Charmander = PokemonClass()
    Pokemon, Version = userInput()
    Charmander.displayMoveset(Version, Pokemon, True)

    #inputWindow()



main()