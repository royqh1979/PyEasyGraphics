import pygame

__all__ = [
    'load_music', 'close_music', 'play_music',
    'pause_music', 'unpause_music', 'stop_music',
    'queue_music', 'is_music_playing', 'get_music_pos',
    'get_music_volume', 'set_music_pos', 'set_music_volume',
    'fade_out_music',
]

_mixer_inited = False


def load_music(filename: str) -> None:
    """
    Load a music file for playback.

    If music playback device is note initialized, it will be initialized automatically.

    Use play_music() to play the music.

    :param filename: the music file to play
    """
    global _mixer_inited
    if not _mixer_inited:
        pygame.mixer.init()
        _mixer_inited = True
    pygame.mixer.music.load(filename)


def pause_music() -> None:
    """
    Pause the music playback.
    """
    pygame.mixer.music.pause()


def unpause_music() -> None:
    """
    Unpause the music playback.
    """
    pygame.mixer.music.unpause()


def stop_music() -> None:
    """
    Stop the music playback.
    """
    pygame.mixer.music.stop()


def play_music(loops: int = 0, start: float = 0.0) -> None:
    """
    Play the music.

    :param loops: loops. 0 means no loop
    :param start: start position of the music
    """
    pygame.mixer.music.play(loops, start)


def queue_music(filename: str):
    """
    Add music to the playing queue.

    :param filename: the music file to be queued.
    """
    pygame.mixer.music.queue(filename)


def set_music_volume(volume: int):
    """
    Set volume of the music playback.

    :param volume: volume of the playback
    """
    pygame.mixer.music.set_volume(volume)


def get_music_volume() -> int:
    """
    Return the music playback volume.

    :return: the playback volume.
    """
    return pygame.mixer.music.get_volume()


def is_music_playing() -> bool:
    """
    Get if the music is playing.

    :return: True if is playing, False if is not.
    """
    return pygame.mixer.music.get_busy()


def set_music_pos(pos: float):
    """
    Set current music play position.

    :param pos: the position to set.
    """
    pygame.mixer.music.set_pos()


def get_music_pos() -> float:
    """
    Get current music playback position .

    :return: current position
    """
    return pygame.mixer.music.get_pos()


def fade_out_music(time: float):
    """
    Fade out and stop the music.

    :param time: fade out time (in milliseconds)
    """
    pygame.mixer.music.fadeout(time)


def close_music():
    """
    Close the music playback device.

    """
    _mixer_inited = False
    pygame.mixer.quit()
