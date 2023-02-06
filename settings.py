with open('graphics/settings_for_game', 'r') as f:
    read_data = f.read()

WINDOW_WIDTH, WINDOW_HEIGHT, FRAMERATE = list(map(int, read_data.split()))