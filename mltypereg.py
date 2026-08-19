from manim import *
import asyncio
from pathlib import Path
from pydub import AudioSegment
import edge_tts

# ================================
# 📱 CONFIG
# ================================
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 8
config.frame_height = 14.22

BG = "#0f172a"

# ================================
# 🎙 AUDIO SETUP
# ================================
ROOT = Path(__file__).parent
AUDIO_DIR = ROOT / "audio"
AUDIO_DIR.mkdir(exist_ok=True)

narration = [
    "नमस्कार दोस्तों, PostNetwork Academy में आपका स्वागत है।",

    "आज हम multiple feature regression problem समझेंगे।",

    "यह एक house price dataset है जिसमें area, bedrooms और age features हैं।",

    "पहले कुछ houses के prices already known हैं।",

    "आखिरी house का price हमें predict करना है।",

    "क्योंकि output continuous value है, यह regression problem है।",

    "model इन तीन features के आधार पर price predict करता है।"
]

# ================================
# 🔊 AUDIO FUNCTIONS
# ================================
def get_duration(file):
    try:
        return AudioSegment.from_file(file).duration_seconds
    except:
        return 2

def generate_audio(text, filename):
    path = AUDIO_DIR / filename

    if path.exists():
        return str(path)

    async def run():
        tts = edge_tts.Communicate(text, "hi-IN-MadhurNeural")
        await tts.save(str(path))

    asyncio.run(run())
    return str(path)

audio_files = []
durations = []

for i, text in enumerate(narration):
    f = generate_audio(text, f"audio_{i}.wav")
    audio_files.append(f)
    durations.append(get_duration(f))

# ================================
# 🎬 MAIN SCENE
# ================================
class MultiFeatureRegression(Scene):
    def construct(self):

        self.camera.background_color = BG

        # =========================
        # 🎓 BRAND
        # =========================
        brand = Text("PostNetwork Academy", font_size=30, color=BLUE).to_edge(UP)
        intro = Text("Multiple Linear Regression", font_size=34, color=YELLOW)

        self.add_sound(audio_files[0])
        self.play(FadeIn(brand))
        self.wait(durations[0] * 0.7)

        self.add_sound(audio_files[1])
        self.play(Write(intro))
        self.wait(durations[1])
        self.play(FadeOut(intro))

        # =========================
        # 📊 DATASET TABLE
        # =========================
        data = [
            ["Area", "Bedrooms", "Age", "Price"],
            ["1000", "2", "5", "40"],
            ["1200", "3", "10", "50"],
            ["1500", "3", "15", "60"],
            ["1800", "4", "20", "70"],
            ["2000", "4", "25", "80"],
            ["1300", "3", "12", "?"]
        ]

        table = Table(data, include_outer_lines=True).scale(0.5)

        self.add_sound(audio_files[2])
        self.play(Create(table))
        self.wait(durations[2])

        # =========================
        # ✅ KNOWN DATA
        # =========================
        self.add_sound(audio_files[3])

        known_rows = VGroup(*[
            table.get_rows()[i]
            for i in range(1, 6)
        ])

        self.play(known_rows.animate.set_color(GREEN))
        self.wait(durations[3])

        # =========================
        # ❓ UNKNOWN ROW
        # =========================
        self.add_sound(audio_files[4])

        unknown = table.get_rows()[6]
        self.play(unknown.animate.set_color(YELLOW))

        predict_text = Text("Predict Price ?", font_size=32).next_to(table, DOWN)
        self.play(Write(predict_text))

        self.wait(durations[4])

        # =========================
        # 📈 REGRESSION EXPLANATION
        # =========================
        self.add_sound(audio_files[5])

        eq = Text(
            "y = w1·Area + w2·Bedrooms + w3·Age + b",
            font_size=22,
            color=YELLOW
        ).to_edge(UP-2)

        self.play(Write(eq))
        self.wait(durations[5])

        # =========================
        # 🎯 PREDICTION
        # =========================
        self.add_sound(audio_files[6])

        result_cell = table.get_cell((7, 4))
        predicted = Text("55", color=GREEN).move_to(result_cell)

        self.play(Transform(result_cell, predicted))

        self.wait(durations[6])

        # =========================
        # CLEANUP
        # =========================
        self.play(FadeOut(table, predict_text, eq, brand))