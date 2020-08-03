from VedioGenerator import VedioGenerator
from Subspeak import Subspeak

sub = Subspeak()


def get_video(text):
    audio, subtitle = sub.get_file(text)
    video = VedioGenerator(audio, subtitle, auto=1)
    return video


def txt_modify(text):
    text = str(text)
    text.replace('\n', '')
    return text


if __name__ == '__main__':
    with open('text.txt', 'r', encoding='Utf-8') as f:
        text = f.read()
    text = txt_modify(text)
    video = get_video(text)
    print(video)
