# HandShootMath
Educational hand-gesture-controlled game for learning multiplication using Pygame &amp; MediaPipe.


# 🖐️ HandShootMath - Hand-Controlled Space Shooter for Learning Multiplication Table

A creative educational game built with **Pygame**, **MediaPipe**, and **OpenCV**, where players shoot meteors by controlling their hand in front of a webcam to learn the **multiplication table** in a fun and interactive way.

---

## 🎮 Game Description

**HandShootMath** is a hand-gesture-controlled educational space shooter game that helps children (or anyone!) practice and learn multiplication tables. Players use the **V sign** to start the game and **make a fist to shoot**. Meteors fall from the sky with Persian words on them, and the player must shoot the correct translation of the English word shown at the top.

The game ends if:
- You shoot the wrong word,
- Or the correct meteor reaches the bottom of the screen.

---
## ✋ Game Controls

Gesture	Action
✌️ V Sign	Start Game
✊ Fist	Shoot Laser
🖐️ Move Hand	Move Player

## 🎥 Demo Video

You can watch a short demo of the system in action here:  
👉 [Click to watch the demo video](Demo.mp4)

## 🧠 Learning Goals

- Learn and reinforce **multiplication table** in both Questions and Answers.
- Improve **hand-eye coordination**.
- Explore **hand tracking and gesture recognition** using AI (MediaPipe).
- Enhance **motivation for learning math** through gamification.

---

## 🛠️ Technologies Used

- 🐍 Python 3.12
- 🎮 Pygame (for game engine)
- 🎥 OpenCV (for camera feed)
- 🧠 MediaPipe (for hand tracking)
- 📁 CSV file for word data

---

## 📂 Folder Structure

HandShootMath/
│
├── code/
│ └── main.py
├── images/
│ ├── player.png
│ └── meteor.png
│
├── audio/
│ ├── laser.wav
│ └── explosion.wav
│
├── font/
│ └── Vazir.ttf
│
├── data/
│ └── Multiplication Table.csv
│
├── Demo.mp4
└── README.md

---

## 📦 How to Run

1. Clone the repository:

git clone https://github.com/your-username/HandShootMath.git
cd HandShootMath

2. Install dependencies:

pip install pygame opencv-python mediapipe arabic-reshaper python-bidi

3. Make sure your webcam is working and then run the game:

python main.py


🧪 Example CSV Format (Multiplication Table.csv)

question,answer
2x2,
3x4,12
5x5,25


🌟 Future Ideas
Add multiplayer or leaderboard support.
Add more levels and vocabulary categories (e.g., English numbers, animals, etc.).
Support left-handed players.
Add score saving or user profiles.

💬 Feedback
Feel free to open issues or pull requests. Contributions are welcome!

