# -*- coding: utf-8 -*-
import requests
import sys

class SearchRequest:
    # Api url
    url = ''

    # hold received items
    _items = {}

    # history of last requests
    _history = []

    # limit output songs
    _limit = 15

    # Search for item
    def search(self, query):
        try:
            search = '+'.join(query.split())
            url = self.url % (search, self._limit)

            try:
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

            self.set_items(data=response.json())

            return True
        except StandardError:
            print('Search went wrong? Please try again.')

            return False

    def set_items(data):
        raise NotImplementedError()

    def get_items(self):
        return self._items

    def list(self):
        raise NotImplementedError()


class SearchPlaylist(SearchRequest):
    # Api url
    url = 'https://api.spotify.com/v1/search?q=%s&type=playlist&limit=%d'

    def set_items(self, data):
        for index, playlist in enumerate(data['playlists']['items']):
            #print "Rohdaten: ", playlist

            playlist_name = playlist['name'][:30].encode('utf-8')

            self._items[index + 1] = {
                'href':playlist['uri'],
                'name':playlist_name,
                'tracks':playlist['tracks']['total']
            }

    def list(self):
        list = []
        space = '{0:3} | {1:45} | {2:10}'
        list.append(space.format('#', 'Name', 'Tracks'))
        list.append(space.format(
            '-' * 3,
            '-' * 45,
            '-' * 10
        ))

        for i in self.get_items():
            list.append(space.format(
                '%d.' % i,
                '%s' % self.get_items()[i]['name'],
                '%d' % self.get_items()[i]['tracks']
            ))

        return list


class SearchSongs(SearchRequest):
    # Api url
    url = 'https://api.spotify.com/v1/search?q=%s&type=track,artist&limit=%d'

    def set_items(self, data):
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

            self._items[index + 1] = {
                'href': song['uri'],
                'artist': artist_name,
                'song': song_name,
                'album': album_name
            }

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

        for i in self.get_items():
            list.append(space.format(
                '%d.' % i,
                '%s' % self.get_items()[i]['artist'],
                '%s' % self.get_items()[i]['song'],
                '%s' % self.get_items()[i]['album']
            ))

        return list



# Fetch songs with spotify api
class Pytifylib:

    search_pl = SearchPlaylist()
    search_so = SearchSongs()
    search = search_pl

    def _get_item_uri_at_index(self, index):
        return str(self.search._items[index]['href'])

    def search_playlist(self, request):
        self.search = self.search_pl
        return self.search.search(request)

    def search_song(self, request):
        self.search = self.search_so
        return self.search.search(request)
    #def _get_song_name_at_index(self, index):
        #return str('%s - %s' % (self._songs[index]['artist'], self._songs[index]['song']))

    def list(self):
        return self.search.list()

    def listen(self, index):
        raise NotImplementedError()

    def print_history(self):
        if len(self.search._history) > 5:
            self.search._history.pop(0)

        print('\nLast five search results:')

        for item in self.search._history:
            print(item)

    def next(self):
        raise NotImplementedError()

    def prev(self):
        raise NotImplementedError()

    def play_pause(self):
        raise NotImplementedError()

    def pause(self):
        raise NotImplementedError()

