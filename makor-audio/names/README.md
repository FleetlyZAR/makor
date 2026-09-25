# Names lexicon: how Makor audio says Hebrew, Aramaic and Greek words

Kokoro reads English well. It does not know most biblical names, or the
Hebrew, Aramaic and Greek words the studies transliterate (chesed, nachash,
toledot, agape). This folder holds the exact spoken form of every such word,
and the audio pipeline applies it automatically.

## Files

    harvest.py         collects every name and transliteration Makor speaks
    candidates.json    the harvest: word, kind, count, what Kokoro says today
    batches/           the harvest cut into review batches of 200
    reviewed/          one decision per word, per batch (written by review)
    overrides.json     hand edits on top of the reviews (add, replace, drop,
                       or "avoid" phrases where the word is plain English)
    build.py           validates the reviews and writes lexicon.json
    audit.py           lists entries that could override an English word
    lexicon.json       the finished lexicon the audio pipeline reads

## How it works

`generate_audio.mark_names()` wraps each lexicon word in misaki's inline
phoneme markup just before synthesis, for example
`[Zerubbabel](/zəɹˈʌbəbᵊl/)`. US voices (af_heart, am_michael) take the `us`
form, UK voices (bf_emma, bm_george) the `gb` form. A possessive
(Zerubbabel's) gets the right ending added. Names match case sensitively
(`Job` the man, never `job`); transliterations with `"case": "any"` also match
at the start of a sentence. The on-screen study is never changed.

## Refresh after new or edited studies

    cd makor-audio
    .venv/bin/python names/harvest.py      # new words go into new batches only
    # review each new batch into reviewed/ (see below)
    .venv/bin/python names/build.py        # validate and write lexicon.json
    .venv/bin/python names/audit.py        # check English collisions

Existing batches are never renumbered, so reviewed/ stays aligned. Do this
after each book is deepened, before its audio is rendered: new Go deeper text
brings new transliterations.

The venv is Python 3.12 with `kokoro`, `misaki[en]` and `espeak-ng` (Homebrew).

## Review rules (for people and agents)

For every row in a batch, write one decision to `reviewed/<same file name>`:

- `skip`: not a name or transliteration at all, an ordinary English word
  ("believers", "Meeting", "Then", "Hosts" in "LORD of Hosts").
- `ok`: `current_us` and `current_gb` are already right. Kokoro's own
  dictionary gets many common names right (Jesus, Moses, Jerusalem, Isaiah).
- `fix`: give `us`, `gb`, `say`, `lang` and `case`.

`say` is a readable guide for a human, capitals on the stressed syllable
(zuh-RUB-uh-bel). `lang` is Hebrew, Aramaic, Greek, Latin, Persian, Egyptian,
Akkadian or Other. `case` is `exact` for proper names and `any` for
transliterated words.

### Which pronunciation

- **Biblical proper names** (people, places, peoples, books): the standard
  English pulpit pronunciation of a good English Bible pronouncing dictionary,
  not modern Israeli Hebrew. Zerubbabel zuh-RUB-uh-bel, Abednego
  uh-BED-nih-go, Jehoshaphat jeh-HOSH-uh-fat, Mephibosheth meh-FIB-oh-sheth,
  Ahithophel uh-HITH-oh-fel, Habakkuk huh-BAK-uk, Melchizedek
  mel-KIZ-uh-dek, Job JOBE, Lot LOT. English convention reads biblical ch as
  k in names (Enoch EE-nuk, Baruch BAIR-uk, Malachi MAL-uh-kye).
- **Transliterated Hebrew and Aramaic words**: academic pronunciation. Chet
  and khaf (ch, kh, h with a dot) are the guttural `x` (chesed XEH-sed, ruach
  ROO-akh, nachash nah-KHASH). Tsade is `ts`. Stress is usually on the last
  syllable (qadosh kah-DOHSH, toledot toh-leh-DOHT), except segolates and
  similar forms stressed on the first (chesed, nephesh NEH-fesh, melech
  MEH-lekh, ebed EH-bed). An apostrophe for aleph or ayin is silent or a light
  break.
- **Transliterated Greek words**: the seminary (Erasmian) pronunciation.
  agape ah-GAH-pay, logos LOH-goss, pneuma PNYOO-mah, chi as `x`
  (charis KHAH-ris), ekklesia ek-klay-SEE-ah.

### Phoneme notation (misaki)

Consonants: b d f h j (y as in yes) k l m n p s t v w z ɡ ŋ ɹ ʃ ʒ ð θ ʤ (j in
jam) ʧ (ch in church), and `x` for the guttural (Bach). Vowels: i (fleece)
u (goose) ɑ (father) ɔ (thought) ɛ (dress) ɜ (nurse) ɪ (kit) ʊ (foot)
ʌ (strut) ə (schwa) ᵊ (light schwa, as in syllabic ᵊl). Diphthongs: A (face)
I (price) W (mouth) Y (choice).

US only: æ (trap), O (goat), ᵻ (reduced vowel), T (flapped t), ʔ.
GB only: a (trap), Q (goat), ɒ (lot), ː (length: iː uː ɑː ɔː ɜː).
So the US `ʤˈOb` is the GB `ʤˈQb`, and the US `hˈæbəkʊk` is the GB
`hˈabəkʊk`. GB drops r after a vowel unless a vowel follows (US `ɜɹ`, GB `ɜː`).

Stress marks go immediately before the stressed vowel, not at the start of the
syllable: `zəɹˈʌbəbᵊl`, `nˌɛbjəkədnˈɛzəɹ`. Every word of more than one
syllable needs one primary stress `ˈ`.

`build.py` rejects any symbol outside these sets and any missing stress.
