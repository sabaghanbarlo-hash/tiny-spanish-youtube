# Tiny Spanish: YouTube

Script in, finished Spanish-learning video out, with **Emma, Mateo, Cami and Santi**. Free: GitHub Actions + Microsoft Edge neural voices + Pillow/resvg + ffmpeg. Cloned from the Tiny French YouTube system (`tiny-french-youtube`) with a Spanish language layer and a new cast. Sister system: `tiny-spanish-instagram` (Reels).

## Three kinds of video
| Kind | Script goes in | Made by | Workflow |
|---|---|---|---|
| Lesson (landscape, ~3 min): dialogue, vocabulary, grammar, quiz | `lessons/` | `lesson.py` | Render video |
| Animated story (landscape): characters walk, act and talk, then vocab, grammar, quiz | `stories/` | `story/lesson.py` | Render story |
| Short (vertical, <60 s): hook, 3 phrases, ending | `shorts/` | `short.py` | Make Short |

Actions -> pick the workflow -> run with the script file name. The MP4 goes to `docs/videos/`. The `docs/index.html` page (GitHub Pages) is the studio: paste a script, press a button. It needs a fine-grained GitHub token saved in your browser, set up inside the page.

## Publishing
`schedule.json` lists what goes out and when (UTC). **Scheduled publish** uploads each item as private with a publish time (`upload.py`, YouTube Data API), `set-thumbnails` adds thumbnails, and `crosspost-reels` can send Shorts to Instagram. Needs these repo secrets: `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN` (same names as the French project). Set `"paused": true` to stop everything.

## Script format
```
title: Introducing Yourself
episode: ES1
scene: cafe
cast: Emma, Mateo        # optional: any two of Emma, Mateo, Cami, Santi (left, right)

[story]
Mateo: ¡Hola! ¿Cómo te llamas? | Hi! What's your name? | KOH-moh teh YAH-mahs
Emma: Me llamo Emma. | My name is Emma.
[vocab]
vocab: me llamo | my name is | meh YAH-moh
example: Me llamo Emma. | My name is Emma.
[grammar]
grammar: Soy de + place | Use soy de to say where you are from.
example: Soy de México. | I'm from Mexico.
[quiz]
quiz: Question? | Option A | Option B | Option C | B | Explanation
[ending]
Emma and Mateo: ¡Hasta pronto! | See you soon!
```
Lines are `Spanish | English | pronunciation (optional)`. Stories add stage directions (`> Emma enters left`, `@scene cafe`): see `story/DIRECTING.md`, and give `story/DIRECTOR_PROMPT.md` to an AI to write them. Validate scripts with `python tools/validate_script.py <file>`.

Local test: `pip install -r requirements.txt` (+ ffmpeg, fonts-dejavu-core), then `python lesson.py lessons/01-introducing-yourself.txt --dummy-audio --preview out/` (no voices, one PNG per section).

## Cast
`config/characters.json` and `docs/CHARACTER_BIBLE.md`. Portraits are drawn in `tinyvideo.py` (`render_char`), full-body story characters in `story/rigsvg.py` (`_es`). Voices: es-US-Paloma (Emma), es-MX-Jorge (Mateo), es-CO-Salome (Cami), es-CO-Gonzalo (Santi). Spanish vocabulary and examples are spoken by the right-hand character (Mateo by default).

## Not ported yet
The Paris-only backgrounds of the French project (café terrace, Eiffel Tower, market): `spanish_places.py` is the empty hook for Spanish ones (plaza, mercado, taquería ...). The French course-art scripts (`course_art*.py`). Voices have only been tested with test tones here; the first Actions run uses the real voices.
