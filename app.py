# from flask import Flask, jsonify
# import yandex_music
# import os

# from yandex_music import Client

# client = Client().init()

# CHART_ID = 'world'
# TOKEN = os.environ.get('TOKEN')

# client = Client(TOKEN).init()
# chart = client.chart(CHART_ID).chart

# text = [f'🏆 {chart.title}', chart.description, '', 'Треки:']

# for track_short in chart.tracks:
#     track, chart= track_short.track, track_short.chart
#     artists = ''
#     if track.artists:
#         artists = ' - ' + ', '.join(artist.name for artist in track.artists)
        
#     if track.albums:
#         labels = []
#         for album in track.albums:
#             if hasattr(album, 'labels') and album.labels:  # Check if 'labels' exist
#                 labels.extend(label.name for label in album.labels)  # Extract names
                
#         if labels:
#             labels = ' - Лейбл ' + ', '.join(labels)
    
#     listeners = f' - Слушатели {chart.listeners}'

#     track_text = f'{track.title}{artists}{labels}{listeners}'

#     if chart.progress == 'down':
#         track_text = '🔻 ' + track_text
#     elif chart.progress == 'up':
#         track_text = '🔺 ' + track_text
#     elif chart.progress == 'new':
#         track_text = '🆕 ' + track_text
#     elif chart.position == 1:
#         track_text = '👑 ' + track_text
    
#     track_text = f'{chart.position} {track_text}'
#     text.append(track_text)
    

# print('\n'.join(text))

# app = Flask(__name__)

# def get_chart():
#     tracks = []
#     for track_short in chart.tracks:
#         track, chart= track_short.track, track_short.chart
#         # artists = ''
#         # if track.artists:
#         #     artists = ' - ' + ', '.join(artist.name for artist in track.artists)
        
#         if track.albums:
#             labels = []
#             for album in track.albums:
#                 if hasattr(album, 'labels') and album.labels:  # Check if 'labels' exist
#                     labels.extend(label.name for label in album.labels)  # Extract names
        
#         # listeners = f' - Слушатели {chart.listeners}'
        
#     tracks.append({
#             "title": track.title,
#             "artist": ", ".join(artist.name for artist in track.artists),
#             "link": f"https://music.yandex.ru/album/{track.albums[0].id}/track/{track.id}",
#             # "listeners": listeners,
#             # "cover": cover,
#             # "genres": genres,
#             "label": labels
#         })
    
#     return tracks

#     tracks = []
#     for track in chart:
#         # Проверка на наличие жанров
#         genres = [genre.title for genre in track.albums[0].genres] if track.albums[0].genres else ["Неизвестно"]

#         # Проверка на наличие лейбла
#         label = track.albums[0].labels[0] if track.albums[0].labels else "Неизвестный лейбл"

#         # Проверка на наличие обложки
#         cover = track.og_image.replace("%%", "200x200") if track.og_image else "https://via.placeholder.com/200"

#         # Количество слушателей (точных данных API НЕ ДАЁТ, используем `normalized_popularity`)
#         listeners = track.normalized_popularity if hasattr(track, "normalized_popularity") else 0

#         tracks.append({
#             "title": track.title,
#             "artist": ", ".join(artist.name for artist in track.artists),
#             "link": f"https://music.yandex.ru/album/{track.albums[0].id}/track/{track.id}",
#             "listeners": listeners,
#             "cover": cover,
#             "genres": genres,
#             "label": label
#         })
    
#     return tracks

# @app.route("/chart", methods=["GET"])
# def chart():
#     """Возвращает JSON с чартом"""
#     return jsonify(get_chart())

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, jsonify, render_template
import os
from yandex_music import Client

app = Flask(__name__)

TOKEN = os.environ.get('TOKEN')
CHART_ID = 'world'
client = Client(TOKEN).init()
chart = client.chart(CHART_ID).chart

def get_chart():
    tracks = []
    
    for track_short in chart.tracks:
        track, chart_data = track_short.track, track_short.chart
        
        # Получаем имя исполнителей
        artists = ", ".join(artist.name for artist in track.artists) if track.artists else "Неизвестно"
        
        # Получаем лейблы, если они есть
        labels = []
        if track.albums:
            for album in track.albums:
                if hasattr(album, 'labels') and album.labels:
                    labels.extend(label.name for label in album.labels)
        label = ", ".join(labels) if labels else "Неизвестный лейбл"
        
        # Слушатели
        listeners = chart_data.listeners if hasattr(chart_data, 'listeners') else 0
        
        # Генерация ссылки на трек
        track_link = f"https://music.yandex.ru/album/{track.albums[0].id}/track/{track.id}" if track.albums else ""
        
        # Обложка трека
        cover_url = track.cover_uri.replace("%%", "200x200") if track.cover_uri else "https://via.placeholder.com/200"
        
        tracks.append({
            "position": chart_data.position,
            "title": track.title,
            "artist": artists,
            "link": track_link,
            "listeners": listeners,
            "label": label,
            "cover": f"https://{cover_url}"  # Добавление корректного URL
        })
    
    return tracks

@app.route("/")
def home():
    return render_template("index.html")  # Serves the frontend

@app.route("/chart", methods=["GET"])
def chart_endpoint():
    """Возвращает JSON с чартом"""
    return jsonify(get_chart()), 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == "__main__":
    app.run(debug=True)