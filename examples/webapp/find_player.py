import soco

def find_speaker_with_music(current_speaker=None):
    # If the current speaker is playing, don't search for another one.
    if current_speaker:
        if current_speaker.get_current_transport_info()['current_transport_state'] == 'PLAYING':
            return current_speaker

    # Since the current speaker wasn't playing, try to discover another one
    speakers = soco.discover(allow_network_scan=True)
    if speakers:
        for speaker in speakers:
            state = speaker.get_current_transport_info()['current_transport_state']
            if state == 'PLAYING':
                return speaker
    # No player found
    return None

if __name__ == '__main__':
    print(find_speaker_with_music())