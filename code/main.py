import pygame
import random
import csv
import arabic_reshaper
from bidi.algorithm import get_display
import cv2
import mediapipe as mp
from os.path import join

# === Pygame و MediaPipe ===
pygame.init()
WIDTH, HEIGHT = 1280, 720
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🖐️ Hand-Controlled Educational Space Shooter")
clock = pygame.time.Clock()

# Persian Font
font = pygame.font.Font("font/Vazir.ttf", 30)

# === بLoad images ===
player_img = pygame.image.load("images/player.png").convert_alpha()
meteor_img = pygame.image.load("images/meteor.png").convert_alpha()
# Can change meteor'sixe in case you need
# meteor_img = pygame.transform.scale(meteor_img, (120, 40))

# === MediaPipe Setup ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
cap = cv2.VideoCapture(0)

def render_farsi_text(text, font, color=(255, 255, 255)):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return font.render(bidi_text, True, color)

def load_words():
    with open("data/Multiplication Table.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

words = load_words()
current_word = random.choice(words)

# === detection fist ===
def is_fist(hand_landmarks):
    tips_ids = [mp_hands.HandLandmark.INDEX_FINGER_TIP,
                mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                mp_hands.HandLandmark.RING_FINGER_TIP,
                mp_hands.HandLandmark.PINKY_TIP]
    dips_ids = [mp_hands.HandLandmark.INDEX_FINGER_DIP,
                mp_hands.HandLandmark.MIDDLE_FINGER_DIP,
                mp_hands.HandLandmark.RING_FINGER_DIP,
                mp_hands.HandLandmark.PINKY_DIP]
    for tip_id, dip_id in zip(tips_ids, dips_ids):
        if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[dip_id].y:
            return False
    return True

# === detection v pos===
def is_v_sign(hand_landmarks):
    tip_ids = {
        'index': mp_hands.HandLandmark.INDEX_FINGER_TIP,
        'middle': mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        'ring': mp_hands.HandLandmark.RING_FINGER_TIP,
        'pinky': mp_hands.HandLandmark.PINKY_TIP
    }
    dip_ids = {
        'index': mp_hands.HandLandmark.INDEX_FINGER_DIP,
        'middle': mp_hands.HandLandmark.MIDDLE_FINGER_DIP,
        'ring': mp_hands.HandLandmark.RING_FINGER_DIP,
        'pinky': mp_hands.HandLandmark.PINKY_DIP
    }

    index_open = hand_landmarks.landmark[tip_ids['index']].y < hand_landmarks.landmark[dip_ids['index']].y
    middle_open = hand_landmarks.landmark[tip_ids['middle']].y < hand_landmarks.landmark[dip_ids['middle']].y
    ring_closed = hand_landmarks.landmark[tip_ids['ring']].y >= hand_landmarks.landmark[dip_ids['ring']].y
    pinky_closed = hand_landmarks.landmark[tip_ids['pinky']].y >= hand_landmarks.landmark[dip_ids['pinky']].y

    return index_open and middle_open and ring_closed and pinky_closed

# === Get hand info===
def get_hand_info():
    ret, frame = cap.read()
    if not ret:
        return None, False, None, None
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        index = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        x = int(index.x * WIDTH)
        y = int(index.y * HEIGHT)
        return (x, y), is_fist(hand), rgb, hand
    return None, False, rgb, None

# === Classes===
class Meteor:
    def __init__(self, x, y, word_dict):
        self.rect = meteor_img.get_rect(topleft=(x, y))
        self.word_dict = word_dict
        self.speed = 200

    def move(self, dt):
        self.rect.y += self.speed * dt

    def draw(self):
        
        win.blit(meteor_img, self.rect)
        text = render_farsi_text(self.word_dict["answer"], font)
        text_x = self.rect.centerx - text.get_width() // 2
        text_y = self.rect.centery - text.get_height() // 2
        win.blit(text, (text_x, text_y))

def generate_meteors(current_word):
    options = [current_word]
    while len(options) < 3:
        w = random.choice(words)
        if w["answer"] not in [o["answer"] for o in options]:
            options.append(w)
    random.shuffle(options)
    return [Meteor(200 + i * 300, 0, w) for i, w in enumerate(options)]

# Sounds
laser_sound = pygame.mixer.Sound(join("audio", "laser.wav"))
explosion_sound = pygame.mixer.Sound(join("audio", "explosion.wav"))

# === Prepare Game===
meteors = []
bullets = []
score = 0
run = True
can_shoot = True
shoot_timer = 0
cooldown = 0.4
game_started = False

player_rect = player_img.get_rect(center=(WIDTH//2, HEIGHT - 100))

# === Game loop===
while run:
    dt = clock.tick(60) / 1000
    win.fill((20, 0, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    hand_pos, fist, camera_frame, hand_landmarks = get_hand_info()

    # Start Scene
    if not game_started:
        start_text = render_farsi_text("برای شروع بازی علامت V دست را نشان دهید", font, (255, 255, 255))
        win.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2 - 40))
        if hand_pos:
            player_rect.center = hand_pos
        win.blit(player_img, player_rect)

        if camera_frame is not None:
            cam_surface = pygame.surfarray.make_surface(camera_frame)
            cam_surface = pygame.transform.rotate(cam_surface, -90)
            cam_surface = pygame.transform.flip(cam_surface, True, False)
            small = pygame.transform.scale(cam_surface, (160, 120))
            win.blit(small, (10, HEIGHT - 130))

        pygame.display.update()

        if hand_landmarks and is_v_sign(hand_landmarks):
            game_started = True
            meteors = generate_meteors(current_word)
        continue  

    # Control player
    if hand_pos:
        player_rect.center = hand_pos

    if not can_shoot:
        shoot_timer += dt
        if shoot_timer >= cooldown:
            can_shoot = True
            shoot_timer = 0

    if fist and can_shoot and hand_pos:
        bullets.append(pygame.Rect(player_rect.centerx - 5, player_rect.top, 10, 20))
        laser_sound.play()
        can_shoot = False

   
    win.blit(player_img, player_rect)

    # Show question in top
    english_text = font.render(current_word['question'], True, (255, 255, 0))
    text_rect = english_text.get_rect(center=(WIDTH // 2, 50))
    win.blit(english_text, text_rect)

    # Bullets
    for bullet in bullets[:]:
        bullet.y -= int(800 * dt)
        pygame.draw.rect(win, (255, 255, 0), bullet)
        if bullet.bottom < 0:
            bullets.remove(bullet)

    # Meteors
    meteors_to_remove = []
    bullets_to_remove = []

    for meteor in meteors:
        meteor.move(dt)
        meteor.draw()

        if meteor.rect.top > HEIGHT and meteor.word_dict == current_word:
            game_started = False  # Game is over
            meteors = []
            bullets = []
            current_word = random.choice(words)
            score = 0

        for bullet in bullets:
            if meteor.rect.colliderect(bullet):
                if meteor.word_dict == current_word:
                    score += 1
                    current_word = random.choice(words)
                    meteors = generate_meteors(current_word)
                else:
                    score -= 1
                    game_started = False
                    meteors = []
                    bullets = []
                    current_word = random.choice(words)
                bullets_to_remove.append(bullet)
                meteors_to_remove.append(meteor)
                explosion_sound.play()

    for m in meteors_to_remove:
        if m in meteors:
            meteors.remove(m)
    for b in bullets_to_remove:
        if b in bullets:
            bullets.remove(b)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(score_text, (WIDTH - 200, 20))

    # Camera
    if camera_frame is not None:
        cam_surface = pygame.surfarray.make_surface(camera_frame)
        cam_surface = pygame.transform.rotate(cam_surface, -90)
        cam_surface = pygame.transform.flip(cam_surface, True, False)
        small = pygame.transform.scale(cam_surface, (160, 120))
        win.blit(small, (10, HEIGHT - 130))

    pygame.display.update()

cap.release()
pygame.quit()
