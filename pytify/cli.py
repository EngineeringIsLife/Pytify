#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytifylib
from strategy import get_pytify_class_by_platform
from menu import Menu
import argparse
import sys
import curses


class App:
    def __init__(self):
        self.pytify = get_pytify_class_by_platform()()

        self.run()

    def menu(self, list):
        self.list = list

        curses.wrapper(self.menu_items)

    def menu_items(self, stdscreen):
        curses.curs_set(0)

        main_menu = Menu(self.list, stdscreen)
        main_menu.display()

    def run(self):
        parser = argparse.ArgumentParser(description='Spotify remote')

        parser.add_argument('-n', help='for next song', action='store_true')
        parser.add_argument('-p', help='for previous song', action='store_true')
        parser.add_argument('-pp', help='for play and pause song', action='store_true')
        parser.add_argument('-s', help='stop music', action='store_true')

        args = parser.parse_args()

        if args.n:
            self.pytify.next()

        elif args.p:
            self.pytify.prev()

        elif args.pp:
            self.pytify.play_pause()

        elif args.s:
            self.pytify.stop()

        else:
            self.interaction()

    def intro(self):
        print('################################################')
        print('#         ____ _  _ ____ __ ____ _  _          #')
        print('#        (  _ ( \/ (_  _(  (  __( \/ )         #')
        print('#         ) __/)  /  )(  )( ) _) )  /          #')
        print('#        (__) (__/  (__)(__(__) (__/           #')
        print('#                 by bjarneo                   #')
        print('#    <http://www.github.com/bjarneo/Pytify>    #')
        print('################################################')

    def _get_input(self, message):
        if sys.version_info >= (3,0):
            result = input(message + '\n> ')
        else:
            result = raw_input(message + '\n> ')
        return result

    def interaction(self):
        self.intro()

        while 1:
            search = False
            search_type = self._get_input('Are you searching for (p)laylist or (a)rtist/(s)ong?')
            if search_type in 'asAS':
                search_input = self._get_input('What artist / song are you searching for?')
                if search_input:
                    search = self.pytify.search_song(search_input)

            elif search_type in 'pP':
                search_input = self._get_input('What playlist are you searching for?')
                if search_input:
                    search = self.pytify.search_playlist(search_input)

            if search is not False:
                self.menu(list=self.pytify.list())
                print "Liste: ", list


def main():
    try:
        App()

    except KeyboardInterrupt:
        print('\n Closing application...\n')

if __name__ == "__main__":
    main()
