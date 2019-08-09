#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import _pickle as pickle


def parse_song_line(in_line):
    data = json.loads(in_line)
    name = data['result']['name']
    tags = ",".join(data['result']['tags'])
    subscribed_count = data['result']['subscribedCount']
    if subscribed_count < 100:
        return False
    playlist_id = data['result']['id']
    song_info = ''
    songs = data['result']['tracks']
    for song in songs:
        try:
            song_info += "\t"+":::".join([str(song['id']),
                                          song['name'], song['artist'][0]['name'], str(song['popularity'])])
        except Exception as e:
            # print(e)
            # print('歌曲有误，错误格式')
            continue
        return name+"##"+tags+"##"+str(playlist_id)+"##"+str(subscribed_count)+song_info


def parse_file1(in_file, out_file):
    out = open(out_file, 'w')
    for line in open(in_file, encoding='utf-8'):
        result = parse_song_line(line)
        if result:
            out.write(result.encode('utf-8').strip()+"\n")
            # encode('utf-8').
    out.close()


parse_file1("./playlistdetail.all.json", "./163_music_playlist.txt")


# 解析成 user item rating timestamp行格式
def is_null(s):
    return len(s.split(",")) > 2


def parse_song_info(song_info):
    try:
        song_id, name, artist, popularity = song_info.split(":::")
        # return ",".join([song_id, name, artist, popularity])
        return ",".join([song_id, "1.0", '1300000'])
    except Exception as e:
        # print e
        # print song_info
        return ""


def parse_playlist_line(in_line):
    try:
        contents = in_line.strip().split("\t")
        name, tags, playlist_id, subscribed_count = contents[0].split("##")
        songs_info = map(lambda x: playlist_id + "," + parse_song_info(x), contents[1:])
        songs_info = filter(is_null, songs_info)
        return "\n".join(songs_info)
    except Exception as e:
        print(e)
        return False


def parse_file2(in_file, out_file):
    out = open(out_file, 'w')
    for line in open(in_file):
        result = parse_playlist_line(line)
        if result:
            out.write(result.encode('utf-8').strip() + "\n")
    out.close()


parse_file2("./163_music_playlist.txt", "./163_music_surprise_format.txt")


def parse_playlist_get_info(in_line, playlist_dic, song_dic):
    contents = in_line.strip().split("\t")
    name, tags, playlist_id, subscribed_count = contents[0].split("##")
    playlist_dic[playlist_id] = name
    for song in contents[1:]:
        try:
            song_id, song_name, artist, popularity = song.split(":::")
            song_dic[song_id] = song_name+"\t"+artist
        except:
            print("error format error")
            print(song + "\n")


def parse_file3(in_file, out_playlist, out_song):
    # 从歌单id到歌单名称的映射字典
    playlist_dic = {}
    # 从歌曲id到歌曲名称的映射字典
    song_dic = {}
    for line in open(in_file, encoding="ISO-8859-1"):
        parse_playlist_get_info(line, playlist_dic, song_dic)
    # 把映射字典保存在二进制文件中
    pickle.dump(playlist_dic, open(out_playlist, "wb"))
    # 可以通过playlist_dic = pickle.load(open("playlist.pk1", "rb"))
    pickle.dump(song_dic, open(out_song, "wb"))


parse_file3("./163_music_playlist.txt", "playlist.pkl", "song.pkl")
