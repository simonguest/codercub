# Skill: Create Jupyter K-12 Notebook

You are creating a `.ipynb` notebook for the **Jupyter K-12** platform — a browser-based Jupyter client for K-12 students that runs Python via Pyodide (in-browser, no server). This skill covers all platform-specific extensions beyond standard `.ipynb` format.

## Notebook file format

A K-12 notebook is a standard `.ipynb` JSON file (`nbformat: 4`). Always write the JSON manually using the `Write` tool — **never use `NotebookEdit`**, which writes `source` as a plain string and breaks the parser. Every `source` field must be an **array of strings** (one string per line, with `\n` at the end of each line except the last).

```json
{
  "nbformat": 4,
  "nbformat_minor": 5,
  "metadata": {
    "title": "Lesson 1: Hello World",
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    }
  },
  "cells": []
}
```

---

## Notebook metadata extensions

### Title

```json
"metadata": {
  "title": "Lesson 4: Variables and Data Flow"
}
```

Falls back to filename if absent. Always set a descriptive title.

### Folder

Places the notebook in a pseudo-folder hierarchy shown in the app index:

```json
"metadata": {
  "folder": "/unit1/lessons"
}
```

Folders are derived at runtime from this field — no independent folder objects exist.

### Globals

Named values substituted at runtime using `{{VARIABLE}}` syntax in markdown and code cells. Supports per-locale overrides:

```json
"metadata": {
  "globals": {
    "STUDENT_NAME": {
      "default": "Rylee",
      "hi-IN": "Aditi",
      "ja-JP": "Daichi"
    },
    "FAVORITE_FOOD": {
      "default": "Pizza",
      "hi-IN": "Puri"
    }
  }
}
```

Use globals in cell source: `Hello, {{STUDENT_NAME}}!`

---

## Standard cell types

### Markdown cell

```json
{
  "cell_type": "markdown",
  "id": "cell-intro",
  "metadata": {},
  "source": [
    "## Welcome to Python\n",
    "\n",
    "In this lesson you will learn about **variables**."
  ]
}
```

### Code cell

```json
{
  "cell_type": "code",
  "execution_count": null,
  "id": "cell-hello",
  "metadata": {},
  "outputs": [],
  "source": [
    "name = 'World'\n",
    "print(f'Hello, {name}!')"
  ]
}
```

---

## Platform-specific cell types

These are activated by the `tags` array in `cell.metadata`.

### Video cell (`raw` + `"video"` tag)

```json
{
  "cell_type": "raw",
  "id": "cell-intro-video",
  "metadata": {
    "tags": ["video"]
  },
  "source": [
    "{ \"url\": \"https://example.com/lesson.mp4\", \"controls\": true }"
  ]
}
```

`controls: true` shows the playback controls bar; `false` hides it (good for short looping demos).

### Journal cell (`markdown` + `"journal"` tag)

A post-it style editable note where students write observations. Renders as markdown in read-only mode; double-click or pencil icon enters edit mode.

```json
{
  "cell_type": "markdown",
  "id": "cell-journal",
  "metadata": {
    "tags": ["journal"]
  },
  "source": [
    "Write your thoughts here..."
  ]
}
```

### CFU — Check for Understanding (`raw` + `"cfu"` tag)

Interactive quiz cells. Three question types: `freeform`, `multiple_choice`, `true_false`. Always initialise `submitted_answer` to `""`.

**Freeform** — case-insensitive, whitespace-trimmed comparison:

```json
{
  "cell_type": "raw",
  "id": "cell-cfu-1",
  "metadata": { "tags": ["cfu"] },
  "source": [
    "{\n",
    "  \"question_type\": \"freeform\",\n",
    "  \"question\": \"In what year was Python created?\",\n",
    "  \"answer\": \"1991\",\n",
    "  \"submitted_answer\": \"\"\n",
    "}"
  ]
}
```

**Multiple choice** — `answer` is the matching `key` value:

```json
{
  "cell_type": "raw",
  "id": "cell-cfu-2",
  "metadata": { "tags": ["cfu"] },
  "source": [
    "{\n",
    "  \"question_type\": \"multiple_choice\",\n",
    "  \"question\": \"Which is not a Python data type?\",\n",
    "  \"options\": [\n",
    "    { \"key\": \"a\", \"text\": \"int\" },\n",
    "    { \"key\": \"b\", \"text\": \"str\" },\n",
    "    { \"key\": \"c\", \"text\": \"char\" },\n",
    "    { \"key\": \"d\", \"text\": \"float\" }\n",
    "  ],\n",
    "  \"answer\": \"c\",\n",
    "  \"submitted_answer\": \"\"\n",
    "}"
  ]
}
```

**True/False** — `answer` is `"True"` or `"False"`:

```json
{
  "cell_type": "raw",
  "id": "cell-cfu-3",
  "metadata": { "tags": ["cfu"] },
  "source": [
    "{\n",
    "  \"question_type\": \"true_false\",\n",
    "  \"question\": \"Python is a compiled language.\",\n",
    "  \"answer\": \"False\",\n",
    "  \"submitted_answer\": \"\"\n",
    "}"
  ]
}
```

Optional CFU fields:
- `"animation": false` — suppresses confetti on correct answer (useful when many CFU cells appear close together)
- `"i18n"` — per-locale overrides for `question`, `options`, `answer` (see i18n section below)

---

## Form fields (Google Colab `#@param` compatible)

Interactive widgets in code cells. Students change values using sliders, dropdowns, or checkboxes without editing code.

```python
AGE = 51 #@param
TEMPERATURE = 1.0 #@param {type:"slider", min:0, max:2, step:0.1}
MODEL = "small" #@param ["small", "medium", "large"]
IS_ENABLED = True #@param {type:"boolean"}
```

---

## Built-in Python modules

These modules are always available without `pip install`.

### `audio` — play sound files

Files in `/sample_files/` are pre-loaded at startup.

- **Images:** `abstract.jpg`, `cat.jpg`, `city.jpg`, `codercub.jpg`, `dog.jpg`, `earth.jpg`, `fabric.jpg`, `forest.jpg`, `undersea.jpg`
- **Sounds:** `clang.wav`, `coin_pickup.wav`, `correct.wav`, `door.wav`, `gameover.wav`, `incorrect.wav`, `laser.wav`, `pop.wav`, `thud.wav`, `wood.wav`, `zap.wav`
- **Music:** `music_ambience.wav`, `music_bach.wav`, `music_sibelius.wav`

```python
import audio

audio.play('/sample_files/correct.wav')           # blocks until done
await audio.play_async('/sample_files/correct.wav')  # returns immediately (must use await)

# Note names: letter + optional accidental (# or b) + octave, e.g. "C4", "F#3", "Bb5"
audio.play_note('C4', 0.5)                   # single note, blocks until done
audio.play_note(['C4', 'E4', 'G4'], 1.0)     # chord (list of note names)
await audio.play_note_async('A4', 0.25)      # non-blocking

audio.play_notes([                           # sequence of (note, duration) tuples
    ('C4', 0.4), ('E4', 0.4), ('G4', 0.4),
    (['C4', 'E4', 'G4'], 1.0),               # chord in a sequence
])
await audio.play_notes_async(melody)         # non-blocking sequence

audio.speak("Hello, world!")                          # blocks until speech finishes
audio.speak("G'day!", voice=audio.Voice.EN_AU.FEMALE) # with a specific voice
await audio.speak_async("This doesn't block.")        # fire and forget

# Available Voice constants (all have .FEMALE and .MALE):
# Voice.EN_US  Voice.EN_GB  Voice.EN_AU
# Voice.FR_FR  Voice.DE_DE  Voice.ES_ES  Voice.IT_IT  Voice.PT_BR
# Voice.JA_JP  Voice.ZH_CN  Voice.KO_KR  Voice.HI_IN  Voice.AR_SA
```

Supported formats: WAV, MP3, OGG, M4A, FLAC.

### `graphics` — canvas drawing

```python
import graphics

c = graphics.canvas()               # auto-size (full cell width, 4:3)
c = graphics.canvas(640, 480)       # explicit pixels

# Draw an image file
graphics.draw_image(c, '/sample_files/cat.jpg')

# Access HTML Canvas 2D context methods via DOMProxy (snake_case → camelCase)
ctx = c.get_context('2d')
ctx.fill_style = 'red'
ctx.fill_rect(10, 10, 100, 50)
```

### `cv` — webcam and computer vision

All detectors accept an optional `delegate="GPU"` argument (default). Falls back to CPU automatically with a printed warning if GPU is unavailable.

**Setup:**

```python
import cv
import graphics

canvas = graphics.canvas()           # auto-sized (full cell width, 4:3)
canvas = graphics.canvas(640, 480)   # explicit pixels
camera = cv.start_camera(canvas)     # starts webcam feed; canvas is optional (headless camera)
```

**Face detection** (BlazeFace):

```python
detector = cv.start_face_detector(camera)
detections = detector.get_detections()
# Each detection: {"type": "face", "x": int, "y": int, "w": int, "h": int, "confidence": float}
canvas.draw_bounding_boxes(detections)
detector.stop()
```

**Object detection** (EfficientDet-Lite0, 80 COCO classes):

```python
detector = cv.start_object_detector(camera)
detections = detector.get_detections()
# Each detection: {"type": "<label>", "x": int, "y": int, "w": int, "h": int, "confidence": float}
canvas.draw_bounding_boxes(detections)
detector.stop()
```

**Pose landmarker** (MediaPipe Pose, 33 landmarks):

```python
detector = cv.start_pose_detector(camera)              # num_poses=1 default
detector = cv.start_pose_detector(camera, num_poses=2) # detect up to 2 people
poses = detector.get_detections()
# poses is a list of poses; each pose is a list of 33 landmark dicts:
# {"x": int, "y": int, "z": float, "visibility": float}
# Index landmarks with cv.POSE constants:
left_elbow = poses[0][cv.POSE.LEFT_ELBOW]
canvas.draw_poses(poses)
detector.stop()
```

Available `cv.POSE` landmarks: `NOSE`, `LEFT_EYE_INNER`, `LEFT_EYE`, `LEFT_EYE_OUTER`, `RIGHT_EYE_INNER`, `RIGHT_EYE`, `RIGHT_EYE_OUTER`, `LEFT_EAR`, `RIGHT_EAR`, `MOUTH_LEFT`, `MOUTH_RIGHT`, `LEFT_SHOULDER`, `RIGHT_SHOULDER`, `LEFT_ELBOW`, `RIGHT_ELBOW`, `LEFT_WRIST`, `RIGHT_WRIST`, `LEFT_PINKY`, `RIGHT_PINKY`, `LEFT_INDEX`, `RIGHT_INDEX`, `LEFT_THUMB`, `RIGHT_THUMB`, `LEFT_HIP`, `RIGHT_HIP`, `LEFT_KNEE`, `RIGHT_KNEE`, `LEFT_ANKLE`, `RIGHT_ANKLE`, `LEFT_HEEL`, `RIGHT_HEEL`, `LEFT_FOOT_INDEX`, `RIGHT_FOOT_INDEX`.

**Gesture recognition** (MediaPipe Gesture Recognizer, 21 hand landmarks):

```python
detector = cv.start_gesture_detector(camera)               # num_hands=2 default
detector = cv.start_gesture_detector(camera, num_hands=1)
detections = detector.get_detections()
# Each detection: {"gesture": str, "confidence": float, "handedness": "Left"|"Right",
#                  "landmarks": [{"x": int, "y": int, "z": float}, ...]}  # 21 landmarks
# Gesture values: "None", "Closed_Fist", "Open_Palm", "Pointing_Up",
#                 "Thumb_Down", "Thumb_Up", "Victory", "ILoveYou"
thumb_tip = detections[0]["landmarks"][cv.HAND.THUMB_TIP]
canvas.draw_hands(detections)
detector.stop()
```

Available `cv.HAND` landmarks: `WRIST`, `THUMB_CMC`, `THUMB_MCP`, `THUMB_IP`, `THUMB_TIP`, `INDEX_FINGER_MCP`, `INDEX_FINGER_PIP`, `INDEX_FINGER_DIP`, `INDEX_FINGER_TIP`, `MIDDLE_FINGER_MCP`, `MIDDLE_FINGER_PIP`, `MIDDLE_FINGER_DIP`, `MIDDLE_FINGER_TIP`, `RING_FINGER_MCP`, `RING_FINGER_PIP`, `RING_FINGER_DIP`, `RING_FINGER_TIP`, `PINKY_MCP`, `PINKY_PIP`, `PINKY_DIP`, `PINKY_TIP`.

**Image segmentation** (MediaPipe Selfie Multi-Class):

```python
segmenter = cv.start_segmenter(camera)
segments = segmenter.get_segments()  # list of class names visible in the frame
# e.g. ["background", "hair", "clothes"]

# Paint a segment class with a solid colour
cv.color_segment(canvas, segmenter, cv.SEGMENT.HAIR, "#ff69b4", opacity=0.6)

# Replace a segment with an image, clipped to the segment shape
cv.apply_image_to_segment(canvas, segmenter, cv.SEGMENT.BACKGROUND, "/sample_files/cat.jpg", opacity=0.9)

segmenter.stop()
```

Available `cv.SEGMENT` classes: `BACKGROUND`, `HAIR`, `BODY_SKIN`, `FACE_SKIN`, `CLOTHES`, `OTHERS`.

**Capturing a still frame:**

```python
jpeg_data_url = cv.capture_frame(camera)
# Returns "data:image/jpeg;base64,..." — suitable for passing to a VLM API as an image input.
# The camera must have produced at least one frame before calling this.
```

**Stopping everything:**

```python
camera.stop()
```

### `scene3d` — interactive 3D scenes (BabylonJS)

```python
import scene3d, math

scene = scene3d.Scene()          # creates canvas + BabylonJS engine, shows output immediately
scene.set_sky("#87CEEB")         # background colour
scene.set_sky(scene3d.Sky.CLOUDS)  # HDR environment skybox (also drives PBR reflections)

ground = scene.set_ground(length=20, width=20)  # returns a Mesh
ground.set_material(scene3d.Material.Grass.Bright)
ground.set_tiling(10)            # repeat texture 10× across the ground

box = scene3d.Shapes.Box(width=1, height=1, depth=1)
box.set_position(0, 0.5, 0)
box.set_rotation(y=45)           # degrees; any combination of x, y, z
box.set_color("#cc4400")
box.set_texture('/sample_files/cat.jpg')   # file path from Pyodide FS
box.set_texture('data:image/png;base64,…') # data URL (e.g. from AI model)
box.set_scale(1, 2, 1)           # scale on each axis
box.set_material(scene3d.Material.Bricks.DarkClay)  # PBR material
box.set_glossiness(0.3)          # 0.0 = matte, 1.0 = mirror-like (PBR only)
box.on_click(lambda: box.set_color("#ff0000"))
scene.add(box)

sphere = scene3d.Shapes.Sphere(diameter=1, segments=16)
scene.add(sphere)

cylinder = scene3d.Shapes.Cylinder(diameter=1, height=2, tessellation=16)
scene.add(cylinder)

ctx = scene.get_context('2d')    # 2D overlay canvas for HUD drawing (supports standard Canvas2D methods)

t = 0.0

@scene.on_frame                  # called each render tick; dt = seconds since last frame
def animate(dt):
    global t
    t += dt
    box.set_position(0, 0.5 + math.sin(t * 2), 0)
    ctx.clear()
    ctx.fill_style = '#ffffff'
    ctx.fill_text(f'Time: {t:.1f}s', 10, 24)

scene.run()                      # blocks Python in event loop; Stop button works
```

**Shapes:** `Shapes.Box(width, height, depth)`, `Shapes.Sphere(diameter, segments)`, `Shapes.Cylinder(diameter, height, tessellation)`.

**Mesh methods:** `set_position(x, y, z)`, `set_rotation(x, y, z)` (degrees), `set_scale(x, y, z)`, `set_color(hex)`, `set_texture(source)`, `set_material(constant)`, `set_glossiness(value)`, `set_tiling(u, v=None)`, `on_click(fn)`. All keyword arguments default to 0 (or 1 for scale), so `set_rotation(y=45)` is valid. `set_ground` returns a `Mesh` so all these methods work on the ground too.

**Mesh getters:** `get_position()` → `(x, y, z)` tuple, `get_rotation()` → `(x, y, z)` tuple in degrees, `get_scale()` → `(x, y, z)` tuple, `get_color()` → hex string. Values are always in sync because every `set_*` call updates Python-side state immediately.

**`Group`:** groups multiple meshes so they move and rotate as a single unit. Child positions and rotations are relative to the group origin. Supports `set_position`, `set_rotation`, `set_scale`, `get_position`, `get_rotation`, `get_scale`. No appearance methods (`set_color`, `set_material`, etc.) — those belong on the individual child meshes.

```python
car = scene3d.Group()

body = scene3d.Shapes.Box(width=2, height=0.5, depth=1)
body.set_color('#cc2200')

wheel = scene3d.Shapes.Cylinder(diameter=0.4, height=0.15, tessellation=16)
wheel.set_rotation(z=90)
wheel.set_position(0.8, 0, 0.5)
wheel.set_color('#222222')

car.add(body)
car.add(wheel)
car.set_position(0, 0.5, 0)
scene.add(car)                   # adds the group + all children in one call

car.set_rotation(y=45)           # rotates the whole group
```

**`set_texture(source)`:** accepts a file path (e.g. `'/sample_files/cat.jpg'`), a `data:` URL, or a raw base64 string (assumed PNG). Setting a texture resets the color to white; call `set_color` after `set_texture` to apply a tint.

**`set_material(constant)`:** applies a PBR material (colour + normal + roughness) or simple diffuse texture. Available constants:

```python
# Bricks
box.set_material(scene3d.Material.Bricks.DarkClay)
box.set_material(scene3d.Material.Bricks.RoughStone)
# Carpet: BlueCheckerboard, BeigePattern
# Chip: CircuitGreen, CircuitRed, CircuitOrange, CircuitBlue
# Fabric: BurgundyRibbed, BlueQuilted, BlackTartan, RedBlueCheck, Denim
# Grass: Bright, Dark, Olive
# Gravel: LightGray, DarkGray
# Marble: Brown, Gray, Black, Charcoal
# Planets (simple): Earth, Jupiter, Mars, Mercury, Neptune, Saturn, Uranus, Venus, Moon
# Road: PatchedAsphalt, AsphaltEdges, Highway
# RoofingTiles: DarkSlate
# Snow: Fresh
# Sports (simple): Soccerball, Tennis
# Tiles: LimeGreen, GreenMosaic, WoodHexagon, Checkerboard
# Wood: Oak
# WoodFloor: PinePlanks
```

**`set_glossiness(value)`:** `0.0` = completely matte, `1.0` = mirror-like. Only affects PBR materials (set via `set_material`); no-ops on plain colour/texture meshes.

**`set_tiling(u, v=None)`:** repeats the texture `u` times horizontally and `v` vertically (`v` defaults to `u`). Persists across `set_material` calls. Essential for ground planes — without it a single tile stretches across the whole surface.

**`set_sky(color)`:** accepts a hex colour string (e.g. `"#87CEEB"`) or a `Sky` constant. When an env skybox is used, PBR materials automatically pick up IBL reflections.

```python
scene.set_sky(scene3d.Sky.CLOUDS)
scene.set_sky(scene3d.Sky.DEEP_SPACE)
scene.set_sky(scene3d.Sky.MODERN_BUILDINGS)
scene.set_sky(scene3d.Sky.ORLANDO_STADIUM)
scene.set_sky(scene3d.Sky.PURE_SKY)
```

**Scene defaults:** ArcRotateCamera (mouse orbit/zoom), HemisphericLight, dark background. BabylonJS loads lazily the first time `scene3d` is used.

**`ctx.clear()`** is a custom method that clears the full 2D overlay; all other standard Canvas2D methods work normally.

**`scene.run()`** must be the last call — it blocks Python in an event loop. The Stop button interrupts it within ~250 ms.

---

### Standard scientific libraries (available via Pyodide)

These do not need `micropip` — just `import` them:
- `numpy`, `pandas`, `matplotlib`, `scikit-learn`, `scipy`
- `openai` (via micropip if needed — check notebook context)

For any other package, use `import micropip; await micropip.install("package-name")` before importing.

---

## Cell IDs

Always set a meaningful `id` on each cell. IDs must be unique within the notebook. Use kebab-case prefixed by type:
- `cell-intro`, `cell-instructions` — markdown
- `cell-hello`, `cell-exercise-1` — code
- `cell-video-intro` — video
- `cell-journal-1` — journal
- `cell-cfu-1`, `cell-cfu-variables` — CFU

---

## Typical lesson structure

A well-structured K-12 lesson notebook follows this pattern:

1. **Video cell** — short intro video (optional)
2. **Markdown** — learning objective(s) for the lesson
3. **Markdown + Code pairs** — concept explanation followed by a runnable example
4. **Journal cell** — student reflection prompt
5. **Form-field code cell** — interactive experiment where students tweak parameters
6. **CFU cells** — 2–4 check-for-understanding questions at the end

Keep code cells short (under 20 lines). Prefer multiple small cells over one large one so students can run incrementally and see output after each step.

---

## "Open in Jupyter-K12" Badge

In the first markdown cell, after the heading and description, you should add an "Open in Jupyter-K12 badge", a self-referencing link to the hosted version of the notebook. This makes it easy for students to open notebooks from their CMS.

The structure of the href should include the simonguest/codercub repo and a link to the .ipynb file following the same path.

Example:

```
# Hello World Notebook!

This is an example of the Jupyter .ipynb document format

<a target="_blank" href="https://jupyter-k12.org?github=simonguest/codercub/blob/main/labs/02/notebooks/hello_world.ipynb">
  <img src="https://img.shields.io/badge/Open_in-Jupyter_K--12-blue" alt="Open In Jupyter K-12"/>
</a>
```

## Key rules

- **Always use `Write` (never `NotebookEdit`)** when creating or editing notebooks
- `source` must be an **array of strings**, each line ending with `\n` except the last
- `submitted_answer` in CFU cells must be `""` (never omit it)
- Set `cell.id` on every cell — use descriptive kebab-case names
- Set `metadata.title` in the notebook metadata
- `outputs` must be `[]` and `execution_count` must be `null` in all code cells
- Do not include a `language_info` key; the platform doesn't use it
- Use `{{VARIABLE}}` globals for any content that varies by locale or student context
- Add i18n overrides to markdown cells when the notebook targets multilingual classrooms
