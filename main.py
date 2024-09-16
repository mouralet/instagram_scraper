import instaloader
import csv
import time
import threading
from datetime import datetime

data_limite = datetime(2024, 1, 1)

instagram = instaloader.Instaloader()
instagram.load_session_from_file('your_username')

dados = []

csvfile = open('file.csv', 'a', encoding='utf-8')
writer = csv.writer(csvfile)
writer.writerow(['numero_post', 'username', 'likes', 'views', 'data',
                'link_post', 'imagem', 'descricao_post', 'comentarios'])

def get_posts_by_username(username):
    numero_post = 0
    for post in instaloader.Profile.from_username(instagram.context, username).get_posts():
        time.sleep(10)
        numero_post += 1
        if post.date > data_limite and numero_post > 4:
            break
        substring = "the_keyword_you_want_to_collect_info"
        if post.caption is not None and substring in post.caption.lower():
            comentarios = []
            for comment in post.get_comments():
                comentarios.append(comment.text)
            descricao_formatada = post.caption.replace('\n', ' ') if post.caption else ''
            dado = {
                "username": post.owner_username,
                "likes": post.likes,
                "views": post.video_view_count,
                "data": post.date.strftime("%m/%d/%Y"),
                "link_post": post.shortcode,
                "imagem": post.url,
                "descricao_post": descricao_formatada,
                "comentarios": comentarios,
                "contagem_comentarios": post.comments
            }
            comentarios_formatados = [comentario.replace('\n', ' ') for comentario in comentarios]
            with lock:
                for comentario in comentarios_formatados:
                    writer.writerow([numero_post, dado['username'], dado['likes'], dado['views'], dado['data'],
                                     dado['link_post'], dado['imagem'], dado['descricao_post'], comentario])
    print('Finalizado usuário: ' + username)

lock = threading.Lock()
usernames = ["the_username_you_want_to_collect_info"]

threads = []
for username in usernames:
    thread = threading.Thread(target=get_posts_by_username, args=[username])
    threads.append(thread)

while len(threads) > 10:
    threads.remove(threads[0])

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

csvfile.close()
print('Finalizado!')
