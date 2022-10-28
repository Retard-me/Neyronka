
from speechkit import Session, SpeechSynthesis
import pyaudio


oauth_token = "y0_AgAAAABTNQHKAATuwQAAAADRBGuqjqv4X8bbTiGwnkMdZcZqn-sLqWA"
catalog_id = "b1gfbvk423a8ui4lg9m9"

# Экземпляр класса `Session` можно получать из разных данных
session = Session.from_yandex_passport_oauth_token(oauth_token, catalog_id)

# Создаем экземляр класса `SpeechSynthesis`, передавая `session`,
# который уже содержит нужный нам IAM-токен
# и другие необходимые для API реквизиты для входа
synthesizeAudio = SpeechSynthesis(session)

# Метод `.synthesize()` позволяет синтезировать речь и сохранять ее в файл
synthesizeAudio.synthesize(
    'out.wav', text='Привет мир!',
    voice='oksana', format='lpcm', sampleRateHertz='16000'
)

# `.synthesize_stream()` возвращает объект типа `io.BytesIO()` с аудиофайлом
audio_data = synthesizeAudio.synthesize_stream(
		text='Привет мир, а в особенности, Привет Ася, Привет Аня, Привет Рома!',
    voice='oksana', format='lpcm', sampleRateHertz='16000'
)


def pyaudio_play_audio_function(audio_data, num_channels=1,
                                sample_rate=16000, chunk_size=4000) -> None:
    """
    Воспроизводит бинарный объект с аудио данными в формате lpcm (WAV)

    :param bytes audio_data: данные сгенерированные спичкитом
    :param integer num_channels: количество каналов, спичкит генерирует
        моно дорожку, поэтому стоит оставить значение `1`
    :param integer sample_rate: частота дискретизации, такая же
        какую вы указали в параметре sampleRateHertz
    :param integer chunk_size: размер семпла воспроизведения,
        можно отрегулировать если появится потрескивание
    """
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=num_channels,
        rate=sample_rate,
        output=True,
        frames_per_buffer=chunk_size
    )

    try:
        for i in range(0, len(audio_data), chunk_size):
            stream.write(audio_data[i:i + chunk_size])
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


sample_rate = 16000  # частота дискретизации должна
# совпадать при синтезе и воспроизведении

# Воспроизводим синтезированный файл
pyaudio_play_audio_function(audio_data, sample_rate=sample_rate)