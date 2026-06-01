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

Files in `/sample_files/` are pre-loaded at startup. Current files: `cat.png`, `chime.wav`.

```python
import audio

audio.play('/sample_files/chime.wav')           # blocks until done
await audio.play_async('/sample_files/chime.wav')  # returns immediately (must use await)
```

Supported formats: WAV, MP3, OGG, M4A, FLAC.

### `graphics` — canvas drawing

```python
import graphics

c = graphics.canvas()               # auto-size (full cell width, 4:3)
c = graphics.canvas(640, 480)       # explicit pixels

# Draw an image file
graphics.draw_image(c, '/sample_files/cat.png')

# Access HTML Canvas 2D context methods via DOMProxy (snake_case → camelCase)
ctx = c.get_context('2d')
ctx.fill_style = 'red'
ctx.fill_rect(10, 10, 100, 50)
```

### `cv` — webcam and computer vision

```python
import cv

canvas = cv.get_canvas()                              # auto-sized
canvas = cv.get_canvas(width, height)                 # explicit pixels
camera = cv.start_camera(canvas)                      # starts webcam feed

detector = cv.start_face_detector(camera)             # BlazeFace
detector = cv.start_object_detector(camera)           # EfficientDet-Lite0
detector = cv.start_object_detector(camera, delegate="GPU")

detections = detector.get_detections()
# Each detection: {"type": "face"|"<label>", "x": int, "y": int, "w": int, "h": int, "confidence": float}

canvas.draw_bounding_boxes(detections)
camera.stop()
detector.stop()
```

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
