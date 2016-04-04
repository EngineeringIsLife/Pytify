# -*- coding: utf-8 -*-
import requests
import sys


# Fetch songs with spotify api
class Pytifylib:
    # Api url
    url = 'https://api.spotify.com/v1/search?q=%s&type=track,artist&limit=%d'
    url_playlist = 'https://api.spotify.com/v1/search?q=%s&type=playlist&limit=%d'

    # hold songs
    _songs = {}

    # hold playlists
    _playlists = {}

    # current mode (playlist or artist/song)
    _mode = 'p'

    # history
    _history = []

    # limit output songs
    _limit = 15

    # Search for song / album / artist
    def search(self, query):
        try:
            search = '+'.join(query.split())
            url = self.url % (search, self._limit)

            try:
                #print "Suche ", self.url % search
                response = requests.get(url)
            except requests.exceptions.Timeout:
                response = requests.get(url)
            except requests.exceptions.TooManyRedirects:
                print('Something wrong with your request. Try again.')

                return False
            except requests.exceptions.RequestException as e:
                print(e)
                sys.exit(1)

            self._history.append(query)

            self.set_songs(data=response.json())

            self._mode = 'a'

            return True
        except StandardError:
            print('Search went wrong? Please try again.')

            return False

    def search_playlist(self, query):
        try:
            search = '+'.join(query.split())
            url = self.url_playlist % (search, self._limit)
            print url
            try:
                response = requests.get(url)
            except requests.exceptions.Timeout:
                response = requests.get(url)
            except requests.exceptions.TooManyRedirecets:
                print('Something wrong with your requests. Try again.')
                return False
            except requests.exceptions.RequestException as e:
                print (e)
                sys.exit(1)

            self._history.append(query)
            self.set_playlists(data=response.json())
            self._mode = 'p'
            return True
        except StandardError:
            print('Search went wrong? Please try again.')
            return False

    def set_songs(self, data):
        for index, song in enumerate(data['tracks']['items']):
            if index == self._limit:
                break

            if sys.version_info >= (3, 0):
                artist_name = song['artists'][0]['name'][:25]
                song_name = song['name'][:30]
                album_name = song['album']['name'][:30]
            else:
                artist_name = song['artists'][0]['name'][:25].encode('utf-8')
                song_name = song['name'][:30].encode('utf-8')
                album_name = song['album']['name'][:30].encode('utf-8')

            self._songs[index + 1] = {
                'href': song['uri'],
                'artist': artist_name,
                'song': song_name,
                'album': album_name
            }

    def set_playlists(self, data):
        for index, playlist in enumerate(data['playlists']['items']):
            #print "Rohdaten: ", playlist

            playlist_name = playlist['name'][:30].encode('utf-8')

            self._playlists[index + 1] = {
                'href':playlist['uri'],
                'name':playlist_name,
                'tracks':playlist['tracks']['total']
            }

           
    def get_songs(self):
        return self._songs

    def get_playlists(self):
        return self._playlists

    # List all. Limit if needed
    def list(self):
        list = []
        space = '{0:3} | {1:25} | {2:30} | {3:30}'

        list.append(space.format('#', 'Artist', 'Song', 'Album'))

        # Just to make it pwitty
        list.append(space.format(
            '-' * 3,
            '-' * 25,
            '-' * 30,
            '-' * 30
        ))

        for i in self.get_songs():
            list.append(space.format(
                '%d.' % i,
                '%s' % self.get_songs()[i]['artist'],
                '%s' % self.get_songs()[i]['song'],
                '%s' % self.get_songs()[i]['album']
            ))

        return list

    def list_playlist(self):
        list = []
        space = '{0:3} | {1:45} | {2:10}'
        list.append(space.format('#', 'Name', 'Tracks'))
        list.append(space.format(
            '-' * 3,
            '-' * 45,
            '-' * 10
        ))

        for i in self.get_playlists():
            list.append(space.format(
                '%d.' % i,
                '%s' % self.get_playlists()[i]['name'],
                '%d' % self.get_playlists()[i]['tracks']
            ))

        return list

    def _get_song_uri_at_index(self, index):
        if self._mode is 'a':
            return str(self._songs[index]['href'])
        elif self._mode is 'p':
            return str(self._playlists[index]['href'])

    def _get_song_name_at_index(self, index):
        return str('%s - %s' % (self._songs[index]['artist'], self._songs[index]['song']))

    def listen(self, index):
        raise NotImplementedError()

    def print_history(self):
        if len(self._history) > 5:
            self._history.pop(0)

        print('\nLast five search results:')

        for song in self._history:
            print(song)

    def next(self):
        raise NotImplementedError()

    def prev(self):
        raise NotImplementedError()

    def play_pause(self):
        raise NotImplementedError()

    def pause(self):
        raise NotImplementedError()
