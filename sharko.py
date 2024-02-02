import tkinter as tk
import random
import os
import pygame


class Sharko:
    WINDOW_SIZE = "357x342"
    ANIMATION_DELAY = 500
    TALKING_ANIMATION_DELAY = 10000
    IDLE_ANIMATION_DELAY = 25000
    GREETING_ANIMATION_DELAY = 8000
    REMOVAL_ANIMATION_DELAY = 5000


    IMAGES_PATH = "assets/sharko/"
    TALKING_SENTENCES_PATH = "assets/sentences/talking/"
    GREETING_SENTENCES_PATH = "assets/sentences/greeting/"
    REMOVAL_SENTENCES_PATH = "assets/sentences/removal/"
    END_TALKING_SOUND = "assets/sounds/end_talking.mp3"
    START_TALKING_SOUND = "assets/sounds/start_talking.mp3"
    GREETING_SOUND = "assets/sounds/greeting.mp3"


    def __init__(self, image_path, talking_path, greeting_path, removal_path):
        self.window = tk.Tk()
        self.current_state = 'greeting'
        self.sound_enabled = True
        pygame.init()
        self.sound_file = self.GREETING_SOUND
        self.frame = 0
        self.min_volume = 0.1
        self.load_images(image_path, talking_path, greeting_path, removal_path)
        self.create_gui()
        self.animate()
        self.sounds(self.sound_file)
        self.window.after(self.GREETING_ANIMATION_DELAY, self.idle_state)
        self.window.after(self.GREETING_ANIMATION_DELAY + self.IDLE_ANIMATION_DELAY + self.TALKING_ANIMATION_DELAY, self.idle_state)
        self.sound_paths = [self.END_TALKING_SOUND, self.START_TALKING_SOUND, self.GREETING_SOUND]
        self.sounds_group = [pygame.mixer.Sound(path) for path in self.sound_paths]
        self.window.mainloop()


    def load_images(self, image_path, talking_path, greeting_path, removal_path):
        self.IMAGES_PATH = image_path
        self.TALKING_SENTENCES_PATH = talking_path
        self.GREETING_SENTENCES_PATH = greeting_path
        self.REMOVAL_SENTENCES_PATH = removal_path

        self.states = {
            'idle': [tk.PhotoImage(file=os.path.join(self.IMAGES_PATH, 'idle1.png')),
                     tk.PhotoImage(file=os.path.join(self.IMAGES_PATH, 'idle2.png'))],

            'talking': [],

            'greeting': [tk.PhotoImage(file=os.path.join(self.GREETING_SENTENCES_PATH, '1.png')),
                         tk.PhotoImage(file=os.path.join(self.GREETING_SENTENCES_PATH, '1a.png'))],

            'removal': [],
        }


    def create_gui(self):
        self.label = tk.Label(self.window, bd=0, bg='#2a2d2a')
        self.label.configure(image=self.states['idle'][0])
        self.label.image = self.states['idle'][0]
        self.label.pack()

        self.menu = tk.Menu(self.window, tearoff=0)
        self.rotate_menu = tk.Menu(self.window, tearoff=0)
        self.rotate_menu.add_command(label='Rotate (right)', command=self.rotate_left)
        self.rotate_menu.add_command(label='Rotate (left)', command=self.rotate_right)
        self.menu.add_cascade(label='Rotate', menu=self.rotate_menu)
        self.menu.add_command(label='Sounds (Off/On)', command=self.sounds_logics)
        self.menu.add_command(label='Close', command=self.close_command)

        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.wm_attributes('-transparentcolor', '#2a2d2a')
        self.window.geometry(self.WINDOW_SIZE)

        self.label.bind("<ButtonPress-2>", self.move1)
        self.label.bind("<B2-Motion>", self.move2)
        self.label.bind("<Double-Button-2>", lambda event: self.menu.post(event.x_root, event.y_root))


    def animate(self):
        state_images = self.states[self.current_state]
        self.frame = (self.frame + 1) % len(state_images)
        self.label.configure(image=state_images[self.frame])
        self.label.image = state_images[self.frame]

        self.window.after(self.ANIMATION_DELAY, self.animate)


    def clear_talking(self):
        self.states['talking'] = []


    def move1(self, event):
        self.x = event.x
        self.y = event.y


    def move2(self, event):
        x = self.window.winfo_pointerx() - self.x
        y = self.window.winfo_pointery() - self.y
        self.window.geometry(f"+{x}+{y}")


    def new_state(self, new_state):
        self.current_state = new_state


    def talking_state(self):
        if self.current_state == 'idle':
            self.add_talking_sentences()
            self.new_state('talking')
            sound_file = self.START_TALKING_SOUND
            self.sounds(sound_file)

        self.window.after(self.TALKING_ANIMATION_DELAY, self.idle_state)


    def idle_state(self):
        if self.current_state == 'talking' or self.current_state == 'greeting':
            self.new_state('idle')
            self.clear_talking()
            sound_file = self.END_TALKING_SOUND
            self.sounds(sound_file)

        self.window.after(self.IDLE_ANIMATION_DELAY, self.talking_state)


    def add_talking_sentences(self):
        sentences_folder = os.path.join(os.getcwd(), self.TALKING_SENTENCES_PATH)
        if os.path.exists(sentences_folder):
            filenames = [f for f in os.listdir(sentences_folder) if 'a' not in f]
            if filenames:
                random_sentence = random.choice(filenames)
                sentence1 = os.path.join(sentences_folder, random_sentence)
                sentence2 = sentence1[:-4] + 'a' + sentence1[-4:]
                self.states['talking'].extend([tk.PhotoImage(file=sentence1), tk.PhotoImage(file=sentence2)])

    
    def add_removal_sentences(self):
        sentences_folder = os.path.join(os.getcwd(), self.REMOVAL_SENTENCES_PATH)
        if os.path.exists(sentences_folder):
            filenames = [f for f in os.listdir(sentences_folder) if 'a' not in f]
            if filenames:
                random_sentence = random.choice(filenames)
                sentence1 = os.path.join(sentences_folder, random_sentence)
                sentence2 = sentence1[:-4] + 'a' + sentence1[-4:]
                self.states['removal'].extend([tk.PhotoImage(file=sentence1), tk.PhotoImage(file=sentence2)])


    def close_command(self):
        if self.current_state == 'greeting' or self.current_state == 'idle' or self.current_state == 'talking':
            self.add_removal_sentences()
            self.new_state('removal')
        if self.current_state == 'removal':
            pass
        
        self.window.after(self.REMOVAL_ANIMATION_DELAY, Sharko.exit)
        
        
    def exit():
        os._exit(0)


    def restart_application(self, new_image_path, new_talking_path, new_greeting_path, new_removal_path):
        self.window.destroy()
        Sharko(new_image_path, new_talking_path, new_greeting_path, new_removal_path)
    

    def rotate_right(self):

        new_image_path = "assets/mirror_sharko/"
        new_talking_path = "assets/mirror_sentences/talking/"
        new_greeting_path = "assets/mirror_sentences/greeting/"
        new_removal_path = "assets/mirror_sentences/removal/"

        self.restart_application(new_image_path, new_talking_path, new_greeting_path, new_removal_path)
        

    def rotate_left(self):
        new_image_path = "assets/sharko/"
        new_talking_path = "assets/sentences/talking/"
        new_greeting_path = "assets/sentences/greeting/"
        new_removal_path = "assets/sentences/removal/"

        self.restart_application(new_image_path, new_talking_path, new_greeting_path, new_removal_path)


    def sounds(self, sound_file):
        pygame.mixer.init()
        pygame.mixer.music.load(sound_file)
        if self.sound_enabled:
            pygame.mixer.music.set_volume(1.0)
        else:
            pygame.mixer.music.set_volume(0.0)
        pygame.mixer.music.play()

    
    def sounds_logics(self):
        self.sound_enabled = not self.sound_enabled
        if not self.sound_enabled:
            for sound in self.sounds_group:
                sound.set_volume(0.0)  
        else:
            for sound in self.sounds_group:
                sound.set_volume(1.0) 

        

sharko = Sharko("assets/sharko/",
                "assets/sentences/talking/",
                "assets/sentences/greeting/",
                "assets/sentences/removal/")


sharko.window.mainloop()

