from auditory.audio_asset import AudioAsset
import pygame

class Mixer:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        
        self.sfx_volume = 0.8
        self.bgm_volume = 0.5
        
        self.current_track = None
        self.next_track = None
        self.is_fading = False

    def play_sfx(self, sfx_name):
        if sfx_name in AudioAsset.sfx_cache:
            sound = AudioAsset.sfx_cache[sfx_name]
            sound.set_volume(self.sfx_volume)
            sound.play()

    def play_music(self, track_name, fade_ms=1000):
        if track_name not in AudioAsset.bgm_paths or track_name == self.current_track:
            print("PLAY MUSIC DID NOT CONTINUE")
            return

        if not pygame.mixer.music.get_busy():
            self._change_music(track_name)
        else:
            self.next_track = track_name
            self.is_fading = True
            pygame.mixer.music.fadeout(fade_ms)

    def _change_music(self, track_name):
        self.current_track = track_name
        pygame.mixer.music.load(AudioAsset.bgm_paths[track_name])
        pygame.mixer.music.set_volume(self.bgm_volume)
        pygame.mixer.music.play(-1)  # Loop infinitely
        self.next_track = None
        self.is_fading = False

    def update(self):
        if self.is_fading and not pygame.mixer.music.get_busy():
            if self.next_track:
                self._change_music(self.next_track)