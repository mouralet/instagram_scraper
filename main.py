import instaloader
import csv
import time
import threading
from datetime import datetime

limit_date = datetime(2023, 5, 1)
instagram = instaloader.Instaloader()
instagram.load_session_from_file('login_instagram')  # (login)
data_list = []
csvfile = open('arquivo.csv', 'a', encoding='utf-8')
writer = csv.writer(csvfile)
writer.writerow(['post_number', 'username', 'likes', 'views', 'date',
                'post_link', 'image', 'post_description', 'comments'])

def get_posts_by_username(username):
    post_number = 0 
    for post in instaloader.Profile.from_username(instagram.context, username).get_posts():
        time.sleep(10)
        post_number += 1  
        print('Post: ' + "https://www.instagram.com/p/" + post.shortcode)
        print(post_number)
        
        if post.date < limit_date and post_number > 4:
            print(
                "Data do post é menor que 01/01/2023 e número de post maior que 4. Parando a coleta.")
            break
        
        substring = "keyword"
        if post.caption is not None and substring in post.caption.lower():
            comments = []
            for comment in post.get_comments():
                comments.append(comment.text)
            
            formatted_description = post.caption.replace(
                '\n', ' ') if post.caption else ''
            data = {
                "username": post.owner_username,
                "likes": post.likes,
                "views": post.video_view_count,
                "date": post.date.strftime("%m/%d/%Y"),
                "post_link": "https://www.instagram.com/p/" + post.shortcode,
                "image": post.url,
                "post_description": formatted_description,
                "comments": comments,
                "comments_count": post.comments
            }

            formatted_comments = [comment.replace(
                '\n', ' ') for comment in comments]
            with lock:
                for comment in formatted_comments:
                    writer.writerow([post_number, data['username'], data['likes'], data['views'], data['date'],
                                    data['post_link'], data['image'], data['post_description'], comment])
        print('Finished user: ' + username)
    lock = threading.Lock()

usernames = ["usarname1", "username2", "username3"]

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

print('Completed!')
