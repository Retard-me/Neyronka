from speechkit import Session, ShortAudioRecognition
import io
import wave
import pyaudio


oauth_token = "y0_AgAAAABTNQHKAATuwQAAAADRBGuqjqv4X8bbTiGwnkMdZcZqn-sLqWA"
catalog_id = "b1gfbvk423a8ui4lg9m9"

# Экземпляр класса `Session` можно получать из разных данных
session = Session.from_yandex_passport_oauth_token(oauth_token, catalog_id)

recognizeShortAudio = ShortAudioRecognition(session)

def record_audio(seconds, sample_rate,
                 chunk_size=4000, num_channels=1) -> bytes:
    """
    Записывает аудио данной продолжительности и возвращает бинарный объект с данными

    :param integer seconds: Время записи в секундах
    :param integer sample_rate: частота дискретизации, такая же
        какую вы указали в параметре sampleRateHertz
    :param integer chunk_size: размер семпла записи
    :param integer num_channels: количество каналов, в режимер синхронного
        распознавания спичкит принимает моно дорожку,
        поэтому стоит оставить значение `1`
    :return: Возвращает объект BytesIO с аудио данными в формате WAV
    :rtype: bytes
    """

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


sample_rate = 16000  # частота дискретизации должна
# совпадать при записи и распознавании

# Записываем аудио продолжительностью 3 секунды
data = record_audio(3, sample_rate)

# Отправляем на распознавание
text = recognizeShortAudio.recognize(
    data, format='lpcm', sampleRateHertz=sample_rate)
print(text)