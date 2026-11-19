"""French helpers for Tiny French (YouTube): which words are French, so French is spoken by a character and English by the narrator."""
import re

ACCENTS = set("áéíóúüñ¿¡")
FR_WORDS = set("""el la los las un una unos unas de del al y o pero que qué quién cómo cuándo dónde cuánto cuánta por para con sin sobre
yo tú vos usted él ella nosotros ustedes ellos ellas me te se nos mi mis tus su sus este esta esto eso ese esa aquí allí ahí muy más menos
sí hola adiós gracias favor perdón disculpe buenos buenas días tardes noches mucho gusto encantado encantada bienvenido bienvenida
soy eres es somos son estoy estás está están tengo tienes tiene tenemos quiero quieres quiere puedo puedes puede voy vas va vamos hay
llamo llamas casa agua café comida cuenta baño calle tienda hablo hablas habla vivo vives vive hace hacer cuesta cuestan cuánto""".split())
EN_WORDS = set("""the a an is are am was were be been to of and or but not it this that these those you your he she we they my his her our their
what who how when where why do does did say says said means mean word words phrase phrases sentence listen repeat try answer question correct
wrong right quiz lesson example examples remember note tip good great nice please thanks thank welcome hello hi bye for in on at with from""".split())
KNOWN = set()          # French words seen in the script itself (filled by learn())
_WORD = re.compile(r"[\wÀ-ÿŒœ]+(?:['’][\wÀ-ÿŒœ]+)*", re.U)


def words(text):
    out = []
    for w in _WORD.findall(text.lower()):
        out.append(w.replace("’", "'"))
        if "'" in w or "’" in w:                      # l'eau -> l, eau
            out.extend(p for p in re.split(r"['’]", w) if p)
    return out


def learn(text):
    """Remember the words of a French line so later mixed text (quiz options, explanations) is read in the right voice."""
    for w in words(text):
        if len(w) > 2 or w in FR_WORDS:
            KNOWN.add(w)


def pron(_text):
    """No automatic pronunciation line for French (add a third part to a line if you want one)."""
    return ""


def is_french(text, default=False):
    toks = words(text)
    if not toks:
        return False
    fr = sum(1 for t in toks if t in FR_WORDS or t in KNOWN or any(ch in ACCENTS for ch in t))
    en = sum(1 for t in toks if t in EN_WORDS and t not in KNOWN)
    if fr > en:
        return True
    if en > fr:
        return False
    return default


_QUOTED = re.compile(r"(«[^»]+»|“[^”]+”|\"[^\"]+\"|(?<![\w])'[^']+'(?![\w]))")


def split_runs(text, default=False):
    """-> [(run, is_french)]. «guillemets» always force French; other quoted bits and the text around them are classified."""
    runs = []
    for k, piece in enumerate(_QUOTED.split(text)):
        if not piece or not piece.strip():
            continue
        if k % 2:
            forced = piece[0] == "«"
            inner = piece[1:-1].strip()
            runs.append((inner, True if forced else is_french(inner, default=default)))
        else:
            runs.append((piece.strip(), is_french(piece)))
    merged = []
    for r, f in runs:                     # join neighbours with the same language
        if merged and merged[-1][1] == f:
            merged[-1] = (merged[-1][0] + " " + r, f)
        else:
            merged.append((r, f))
    return merged


def options_default(question):
    """Quiz options are French unless the question asks what a French word means."""
    return not re.search(r"\b(what does|what do|in english|translate)\b", question or "", re.I)
