from __future__ import print_function

from speechkit import Session, ShortAudioRecognition

import pyaudio
import wave

# Токены для подключения к Yandex Speechkit
oauth_token = "y0_AgAAAABTNQHKAATuwQAAAADRBGuqjqv4X8bbTiGwnkMdZcZqn-sLqWA"
catalog_id = "b1gfbvk423a8ui4lg9m9"

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Ссылка на API гугл-календаря
SCOPES = ['https://www.googleapis.com/auth/calendar']

import pythonnet
import io
import clr
import os.path
import datetime

pathDLL = "C:/Users/ASUS/source/repos/Hors-master/bin/debug/netstandard2.0/Hors.dll"
clr.AddReference(pathDLL)

import Hors
from System import DateTime





# Подключение библиотеки парсинга даты и времени из текста, написанной на С#




# Экземпляр класса `Session` можно получать из разных данных
session = Session.from_yandex_passport_oauth_token(oauth_token, catalog_id)

recognizeShortAudio = ShortAudioRecognition(session)

# Записывает аудио данной продолжительности и возвращает бинарный объект с данными
def record_audio(seconds, sample_rate, chunk_size=4000, num_channels=1) -> bytes:
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=num_channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size
    )
    frames = []
    try:
        for i in range(0, int(sample_rate / chunk_size * seconds)):
            data = stream.read(chunk_size)
            frames.append(data)
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

    container = io.BytesIO()
    wf = wave.open(container, 'wb')
    wf.setnchannels(num_channels)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    container.seek(0)
    return container


sample_rate = 16000  # Частота дискретизации должна
# Совпадать при записи и распознавании

# Записываем аудио продолжительностью 3 секунды
data = record_audio(3, sample_rate)

# Отправляем на распознавание
recognized_text = recognizeShortAudio.recognize(
    data, format='lpcm', sampleRateHertz=sample_rate)

print(recognized_text)

today = DateTime.Now

# Парсинг даты и времени из распознанного текста
parser = Hors.HorsTextParser()
result = parser.Parse(recognized_text, today, 4)

# print(result.Text)

# Результат парсинга
fdate = result.Dates[0]

print(fdate.DateFrom.ToString("yyyy'-'MM'-'dd'T'HH':'mm':'ss'+'05:00"))
# print(fdate.DateTo.ToString("yyyy'-'MM'-'dd'T'HH':'mm':'ss'+'05:00"))

def main():
    creds = None
    # Файл token.json хранит токен пользователя для доступа
    # Файл создается автоматически при первой авторизации, после чего,
    # он обновляется
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Если файл token.json пуст, то программа перенаправляет пользователя
    # на страницу авторизации
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Сохранение данных для повторного использования
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Вызов API гугл-календаря
        event = {
            'summary': result.Text,
            'location': '',
            'description': '',
            'start': {
                'dateTime': fdate.DateFrom.ToString("yyyy'-'MM'-'dd'T'HH':'mm':'ss'+'05:00"),
                'timeZone': 'Asia/Yekaterinburg',
            },
            'end': {
                'dateTime': fdate.DateTo.ToString("yyyy'-'MM'-'dd'T'HH':'mm':'ss'+'05:00"),
                'timeZone': 'Asia/Yekaterinburg',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=1'
            ],
            'attendees': [
                {'email': 'renarddapinder@gmail.com'},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
# [END calendar_quickstart]
