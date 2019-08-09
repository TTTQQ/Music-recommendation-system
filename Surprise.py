import pickle
import os
from surprise import Reader, KNNBaseline
from surprise import Dataset
import surprise

# 重建歌单id到歌曲名的映射字典
fo = open("popular_playlist.pkl", "rb")
id_name_dic = pickle.load(fo, encoding='utf-8')
id_name_dic = pickle.load(open("popular_playlist.pkl", "rb"), encoding='utf-8')
print("加载歌单id到歌曲名的映射字典完成...")
# 重建歌单名到歌单id的映射字典
name_id_dic = {}
for playlist_id in id_name_dic:
    name_id_dic[id_name_dic[playlist_id]] = playlist_id
print("加载歌单名到歌单id的映射字典完成....")

file_path = os.path.expanduser('./popular_music_suprise_format.txt')
# 指定文件格式
reader = Reader(line_format='user item rating timestamp', sep=',')
# 从文件读取数据
music_data = Dataset.load_from_file(file_path, reader=reader)
# 计算歌曲和歌曲之间的相似度
print("构建数据集...")
trainset = music_data.build_full_trainset()
# # sim_options = {'name': 'pearson_baseline', 'user_based': False}
# print(id_name_dic.keys())
# print(trainset.n_items)
# print(trainset.n_users)
# print("开始训练模型...")
algo = KNNBaseline()
algo.fit(trainset)

current_palylist = list(name_id_dic.keys())[39]
print("歌单名称", current_palylist)
# 取出近邻
# 映射名字到id
playlist_id = name_id_dic[current_palylist]
print("歌单id", playlist_id)
# 取出来对应的内部user id => to_inner_uid
playlist_inner_id = algo.trainset.to_inner_uid(playlist_id)
print("内部id", playlist_inner_id)

playlist_neighbors = algo.get_neighbors(playlist_inner_id, k=10)

# 把歌曲id转换成歌曲名字
# to_raw_uid映射回去
playlist_neighbors = (algo.trainset.to_raw_uid(inner_id)
                      for inner_id in playlist_neighbors)
playlist_neighbors = (id_name_dic[playlist_id] for playlist_id in playlist_neighbors)

print("之前的啥：", playlist_neighbors)
print("和歌单《", current_palylist, "》最接近的10首歌单为：\n")
for playlist in playlist_neighbors:
    print(playlist, algo.trainset.to_inner_uid(name_id_dic[current_palylist]))


# 针对用户进行预测
song_id_name_dic = pickle.load(open("popular_song.pkl", "rb"), encoding='utf-8')
print("加载歌曲id到歌曲名的映射字典完成...")
song_name_id_dic = {}
for song_id in song_id_name_dic:
    song_name_id_dic[song_id_name_dic[song_id]] = song_id
print("加载歌曲名到歌曲id的映射字典完成...")
# 内部编码的4号用户
user_inner_id = 4
user_rating = trainset.ur[user_inner_id]
items = map(lambda x: x[0], user_rating)
for song in items:
    print(algo.predict(user_inner_id, song, r_ui=1),
          song_id_name_dic[algo.trainset.to_raw_iid(song)])
print("完成...")

# 模型存储
surprise.dump.dump('./recommendation.model', algo=algo)
# 可以用以下方式载入
algo = surprise.dump.load('./recommendation.model')


