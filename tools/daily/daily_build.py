# -*- coding: utf-8 -*-
"""Build all 50 Makor dailies: cards (both formats), landing pages, src/data/daily.js,
and a SQL file inserting the 45 new comms.daily_pool rows. Verse text is verbatim
BSB loaded from match50.json (produced from the study JSONs). No em or en dashes."""
import json, os, base64, re, sys
sys.path.insert(0, "/sessions/epic-ecstatic-babbage/mnt/outputs")
import gen_cards as gc

REPO = "/sessions/epic-ecstatic-babbage/mnt/makor"
OUT  = "/sessions/epic-ecstatic-babbage/mnt/outputs"
SITE = "https://makor.co.za"
EXISTING = {"genesis-1-1", "psalm-36-9", "john-1-1", "isaiah-55-1", "lamentations-3-22"}

match = {m["ref"]: m for m in json.load(open(f"{OUT}/match50.json")) if m.get("ok")}

def daily_slug(ref):
    book, cv = ref.rsplit(" ", 1)
    ch = cv.split(":")[0]
    v = cv.split(":")[1].split("-")[0]
    return book.lower().replace(" ", "-") + f"-{ch}-{v}"

WRITEUPS = {
 "Genesis 1:1": [
  "Seven Hebrew words open the whole Bible, and everything after them leans back on this one line.",
  "The word for created here is bara. In the Hebrew Scriptures it is a work only ever done by God; no one else is ever its subject. And the name for God, Elohim, is full and majestic. Before the world is set in order, before it falls, before a single promise is made, the first thing we are told is who stands behind it all. He is the source.",
  "This is where Makor begins, because it is where God begins: not with us, but with Him. Come and sit with the beginning."],
 "Psalm 36:9": [
  "David has just looked hard at the human heart with no fear of God in it, and found it a dry, self-flattering thing.",
  "Then his eyes lift. With You, he says, is the fountain of life. The Hebrew word is mekor, the same word that gives Makor its name: not a tank we fill, but a spring that rises from God Himself and never runs dry. And in Your light we see light; we do not see anything truly until He shines.",
  "Everything living, everything true, has one source. Come and drink from it."],
 "Psalm 19:1": [
  "Before a single word of Scripture is read, the sky is already preaching.",
  "David looks up and hears a sermon with no sound in it: sun, moon, and stars telling, day after day, that Someone made them and that He is glorious. Creation is God's first witness, and no one on earth is out of earshot.",
  "Lift your eyes today. The heavens are still declaring; the only question is whether we are listening."],
 "Jeremiah 2:13": [
  "This is the verse that gives Makor its name, and it comes as an indictment.",
  "God names two evils in one breath: His people walked away from Him, the fountain of living water, and then dug their own cracked cisterns that cannot even hold what little they catch. Every idol is a leaking tank we somehow prefer to a spring that never runs dry.",
  "Come back to the fountain. It is still flowing, and it was never the water that failed."],
 "Revelation 22:1": [
  "The Bible opens with a garden and a river, and it ends with a city and a river.",
  "At the very last, an angel shows John a river of the water of life, clear as crystal, flowing straight from the throne of God and of the Lamb. The thirst that runs through the whole story is finally, endlessly satisfied at its source.",
  "This is where it is all going: to the fountain, unhidden at last."],
 "Lamentations 3:22-23": [
  "These famous words were written from the ashes of a fallen city, not from a mountaintop.",
  "The man who wrote them had watched Jerusalem burn. And still he says: the LORD's mercies never fail; they are new every morning. Not that the pain was small, but that God's mercy was newer than each day's grief. Whatever you wake to, His mercy got there first.",
  "This morning, His mercy is new again."],
 "Psalm 103:8": [
  "This is God describing Himself, in the same words He first spoke to Moses on the mountain.",
  "Compassionate and gracious, slow to anger, overflowing with loving devotion. Not slow to love and quick to anger, as we so often imagine Him, but the reverse. His patience with us is not reluctance; it is His nature.",
  "Whatever you carried into today, He is slower to anger than you fear and richer in mercy than you hope."],
 "Psalm 86:15": [
  "David is in trouble and surrounded, and he steadies himself on who God is.",
  "You, O Lord, are a compassionate and gracious God, slow to anger, abounding in loving devotion and faithfulness. He does not talk himself into calm; he preaches God's own character back to himself and lets it hold him.",
  "When the ground shakes, say God's name back to yourself. It bears the weight."],
 "Zephaniah 3:17": [
  "A book heavy with warning ends with something almost too good to say out loud.",
  "The LORD your God is among you, mighty to save; and this mighty God rejoices over His people with gladness, quiets them with His love, and sings over them. The Judge of all the earth is also the One who sings over the people He has saved.",
  "You are not merely tolerated by God. You are sung over."],
 "Psalm 30:5": [
  "Grief is real, and this verse does not pretend otherwise.",
  "His anger is fleeting, His favor lasts a lifetime; weeping may stay the night, but joy comes in the morning. The night is not denied; it is given a boundary. Morning is coming, and it belongs to Him.",
  "If you are in the long night, hold on. Joy has an appointment with you at dawn."],
 "Proverbs 3:5-6": [
  "The hardest words here are the small ones: with all your heart, and lean not.",
  "Trust the LORD completely and stop leaning on your own understanding; in all your ways acknowledge Him, and He will make your paths straight. It is not the promise of an easy road, but of a guided one.",
  "Bring Him the decision you are turning over today. Lean on Him instead of on the ceiling above your bed."],
 "Psalm 23:1": [
  "Five words carry more comfort than most whole books: the LORD is my shepherd.",
  "If He is the shepherd, then I am not the one who has to find the pasture, fight the wolf, or know the way home. I shall not want, not because I have everything, but because I have Him.",
  "Let Him be the shepherd today. You were never meant to be both the sheep and the one who carries the flock."],
 "Psalm 46:1": [
  "This is the psalm behind the old hymn A Mighty Fortress, and it was written for shaking ground.",
  "God is our refuge and strength, an ever-present help in times of trouble. Not a help that arrives late, but one already present before the trouble began; not distant strength, but a refuge you can run inside.",
  "Whatever is giving way around you, run to the One who does not move."],
 "Isaiah 41:10": [
  "Fear gets four answers in a single verse, and not one of them is try harder.",
  "Do not fear, for I am with you; do not be dismayed, for I am your God. I will strengthen you and help you and uphold you with My righteous right hand. The cure for fear is not a feeling; it is a Person who is with you.",
  "You are held by a hand stronger than whatever is frightening you."],
 "Matthew 6:33": [
  "Jesus has just told anxious people to look at the birds and the flowers.",
  "Then He gives the reordering that changes everything: seek first the kingdom of God and His righteousness, and all these things will be added to you. Put God first, and the very things you were anxious about are handed back as gifts rather than idols.",
  "What are you seeking first today? Put His kingdom there, and watch the rest fall into place."],
 "Philippians 4:6-7": [
  "Paul writes this from prison, which is worth remembering.",
  "Be anxious for nothing, but in everything, by prayer with thanksgiving, tell God what you need; and the peace of God, which surpasses all understanding, will guard your heart. The instruction is not to feel calm but to pray, and the peace is God's gift, not your achievement.",
  "Turn the thing you are gripping into a prayer, and let His peace stand guard where the worry used to be."],
 "1 Peter 5:7": [
  "Peter writes to scattered, suffering Christians and hands them one small verb: cast.",
  "Cast all your anxiety on Him, because He cares for you. Not manage it, not hide it, but throw it onto Someone strong enough to hold it, and for this reason: He actually cares about you.",
  "Name the weight you are carrying and hand it over. He is not too busy, and you were never meant to hold it."],
 "John 1:1": [
  "John opens his Gospel with the very words that open the Bible: in the beginning.",
  "He wants you to hear the echo. The One who spoke the world into being in Genesis is here given a name and a face: the Word, who was with God and was God. The voice at creation was Christ, and nothing that exists came from anywhere else.",
  "The source has a face, and it is Jesus."],
 "John 3:16": [
  "The most familiar verse in the Bible is still the deepest.",
  "God so loved the world that He gave His one and only Son, so that everyone who believes in Him will not perish but have eternal life. The measure of the love is the size of the gift: not advice, not a second chance, but His own Son.",
  "This is how loved you are. Believe it, and live."],
 "John 14:6": [
  "The disciples are afraid and feeling lost, and Jesus does not hand them a map.",
  "He says, I am the way and the truth and the life; no one comes to the Father except through Me. He does not point down the road; He is the road. He does not merely teach the truth; He is it.",
  "You do not need to find the way. You need to follow the One who is the way."],
 "Isaiah 9:6": [
  "Seven hundred years before Bethlehem, Isaiah names the coming King.",
  "Unto us a child is born, unto us a son is given, and the government will rest on His shoulders: Wonderful Counselor, Mighty God, Everlasting Father, Prince of Peace. The child in the manger is the Mighty God, and the weight of the world rests on shoulders that can bear it.",
  "The names are all His. Bring Him whatever needs a Wonderful Counselor and a Prince of Peace."],
 "Isaiah 53:5": [
  "This was written centuries before the cross, and it reads like an eyewitness account.",
  "He was pierced for our transgressions, crushed for our iniquities; the punishment that brought us peace was upon Him, and by His wounds we are healed. Every clause is a substitution: our sin, His wounds; our peace, His punishment.",
  "The wounds that heal you are not your own. They are His, and they were for you."],
 "Colossians 1:16-17": [
  "Paul is describing the Christ that some wanted to reduce to one power among many.",
  "In Him all things were created, in heaven and on earth, visible and invisible; He is before all things, and in Him all things hold together. The One who made everything is also the One keeping it from flying apart, this very moment included.",
  "The world is not held together by luck, and not by you. It is held by Him."],
 "Hebrews 1:3": [
  "How can we see the invisible God? Hebrews answers in one line.",
  "The Son is the radiance of God's glory and the exact representation of His nature, and He upholds all things by His powerful word. To look at Jesus is to see the very light of God, and the hand that made the universe is the hand that holds it up.",
  "You want to know what God is like. Look long at His Son."],
 "Isaiah 55:1": [
  "Just after Isaiah sings of the Servant who was pierced for our transgressions, God flings the doors open and starts calling into the street.",
  "Come, all you who are thirsty. And then, strangely, come and buy, you who have no money. The price has already been paid; the wine and milk are handed over without cost. This is grace doing its own arithmetic.",
  "The only thing you need bring is your thirst. Come."],
 "John 4:14": [
  "Jesus says this to a tired woman at a well in the heat of the day.",
  "Whoever drinks the water I give will never thirst; it will become in him a spring of water welling up to eternal life. He is not offering another bucket for the old well, but a spring set inside the person, rising from within.",
  "The thing you keep going back to the well for, He wants to become a spring inside you. Come and drink."],
 "John 7:37-38": [
  "On the last and greatest day of the feast, Jesus stands up and shouts an invitation.",
  "If anyone is thirsty, let him come to Me and drink; whoever believes in Me, rivers of living water will flow from within him. The thirst is not a problem to hide but the very thing that qualifies you to come.",
  "Come thirsty. He turns the ones who drink into rivers for others."],
 "Matthew 11:28": [
  "Jesus does not call the impressive; He calls the tired.",
  "Come to Me, all you who are weary and burdened, and I will give you rest. The only entry requirement is exhaustion, and the gift is not a lighter load carried alone but rest found in Him.",
  "If you are worn out, you are exactly who He is talking to. Come."],
 "John 8:12": [
  "In a world that often feels dark, Jesus makes a staggering claim about Himself.",
  "I am the light of the world; whoever follows Me will never walk in darkness but will have the light of life. He does not merely light the path; He is the light, and following Him is how you leave the dark behind.",
  "Stop straining to see in the dark. Follow the Light and walk."],
 "Psalm 119:105": [
  "This verse tells you how much light Scripture gives, and it is honest about it.",
  "Your word is a lamp to my feet and a light to my path. Not a floodlight over the whole journey, but a lamp for the next step and the stretch of road just ahead. Enough to walk by, not enough to remove the need for trust.",
  "You may not see the whole way. Open the Word, take the next step in its light, and keep walking."],
 "Isaiah 40:8": [
  "Everything around us is fading, and Isaiah does not soften it.",
  "The grass withers and the flowers fall, but the word of our God stands forever. Empires, headlines, and our own strength are all grass; only one thing outlasts the wind, and it is what God has said.",
  "Build your life on the one thing that will still be standing. His word does not wither."],
 "Hebrews 4:12": [
  "The Bible is not a dead book about God; it is God's living voice.",
  "The word of God is living and active, sharper than any double-edged sword, cutting deep enough to judge the thoughts and intentions of the heart. When you read it, it reads you.",
  "Come to Scripture ready to be searched. It is alive, and it means to reach the heart."],
 "2 Timothy 3:16": [
  "Paul tells us where Scripture comes from and what it is for.",
  "All Scripture is God-breathed and useful for teaching, rebuking, correcting, and training in righteousness. It is not merely words about God; it is words from Him, given to shape a whole life.",
  "Let it teach you, and let it correct you. It was breathed out by God for exactly that."],
 "Joshua 1:8": [
  "Joshua is about to lead a nation, and God's first counsel is not about strategy.",
  "Keep this Book of the Law on your lips; meditate on it day and night, so that you may do all that is written in it. The way to a life that holds is not more willpower but a mind soaked in God's word.",
  "Give it a place in your day. What you meditate on is what you become."],
 "Isaiah 40:31": [
  "This is God's word to a people worn down and out of strength.",
  "Those who wait upon the LORD will renew their strength; they will soar on wings like eagles, run and not grow weary, walk and not faint. The strength is not summoned from within; it is renewed by waiting on Him.",
  "If you are running on empty, stop striving and wait on Him. He renews what you cannot."],
 "Joshua 1:9": [
  "Three times God tells Joshua to be strong, and here He gives the reason.",
  "Be strong and courageous; do not be afraid or discouraged, for the LORD your God is with you wherever you go. The courage is not self-generated bravado; it rests entirely on the fact of His presence.",
  "Wherever today takes you, He goes with you. That is enough to be brave."],
 "Philippians 4:13": [
  "This famous line is not about winning; Paul wrote it about contentment in plenty and in need.",
  "I can do all things through Christ who gives me strength. Full or hungry, comfortable or in want, he had learned that the strength to be content in any of it came from One outside himself.",
  "Whatever today asks of you, you do not face it on your own strength. His is enough."],
 "Psalm 27:1": [
  "David asks a question, then answers his own fear with it.",
  "The LORD is my light and my salvation, whom shall I fear? The LORD is the stronghold of my life, of whom shall I be afraid? If God is your light and your fortress, fear runs out of ground to stand on.",
  "Name your fear, then set it beside this: the LORD is my light. Whom shall I fear?"],
 "2 Corinthians 12:9": [
  "Paul begged three times for his thorn to be removed, and God said no, with a reason.",
  "My grace is sufficient for you, for My power is perfected in weakness. The thorn stayed, but so did the grace; and the weakness Paul hated became the very place God's power showed clearest.",
  "Your weakness is not disqualifying you. It may be the place His power is about to be seen."],
 "Psalm 121:1-2": [
  "A traveler looks up at the hills, unsure whether help or danger waits there.",
  "I lift up my eyes to the hills; where does my help come from? My help comes from the LORD, the Maker of heaven and earth. Not from the mountains or the idols on them, but from the One who made them.",
  "Lift your eyes higher than the hills today. Your help has a name."],
 "Proverbs 9:10": [
  "Wisdom does not begin where we expect, with cleverness or experience.",
  "The fear of the LORD is the beginning of wisdom, and knowledge of the Holy One is understanding. To rightly know anything, you must first rightly know God; reverence is the doorway, not the reward.",
  "Start today where wisdom starts: in awe of the One who made you."],
 "Micah 6:8": [
  "God cuts through every religious performance and says what He is really after.",
  "He has shown you what is good: to act justly, to love mercy, and to walk humbly with your God. Not grand offerings, but a just hand, a merciful heart, and a humble walk beside Him.",
  "You do not have to guess what God wants of you today. Do justice, love mercy, walk humbly."],
 "Ecclesiastes 3:1": [
  "The Preacher has been chasing meaning, and comes back with a steadying truth.",
  "To everything there is a season, and a time for every purpose under heaven. Nothing in your life is random or wasted; each season has its place under the ordering hand of God.",
  "Whatever season you are in, it has a time and a purpose. It will not last forever, and it is not outside His hand."],
 "Romans 12:2": [
  "After eleven chapters of mercy, Paul turns to how mercy remakes a life.",
  "Do not be conformed to this world, but be transformed by the renewing of your mind, so that you can discern the good and perfect will of God. Change starts not with behavior but with a mind made new.",
  "The world is always pressing you into its mold. Let God renew your mind instead, and you will begin to see straight."],
 "Matthew 5:16": [
  "Jesus has just called His people the light of the world, and light is not made to be hidden.",
  "Let your light shine before others, that they may see your good deeds and glorify your Father in heaven. The point of the shining is not your reputation but the Father's glory; good works are lamps pointing home.",
  "Let today's small, visible goodness point past you to Him."],
 "Ephesians 2:8-9": [
  "Paul states the heart of the gospel in a single sentence, and leaves us nothing to boast about.",
  "By grace you have been saved, through faith, and this is not from yourselves; it is the gift of God, not by works, so that no one can boast. Salvation is received, not earned; a gift, not a wage.",
  "Stop trying to earn what has already been given. Receive it, and let the boasting be His."],
 "Romans 8:28": [
  "This is not a promise that everything is good, but that God is at work in everything.",
  "We know that God works all things together for the good of those who love Him, who are called according to His purpose. Even the hard and senseless-seeming things are being woven, by Him, toward a good He has purposed.",
  "Whatever is in your hands today, it is not outside His weaving. Trust the Weaver."],
 "Romans 15:13": [
  "Paul ends a long argument not with a command but with a blessing.",
  "May the God of hope fill you with all joy and peace as you trust in Him, so that you may overflow with hope by the power of the Holy Spirit. Hope here is not wishful thinking but a fullness God pours in as we trust Him.",
  "Ask the God of hope to fill you today, until hope spills over the edges."],
 "Revelation 21:4": [
  "At the end of the story, God stoops down to do something tender.",
  "He will wipe away every tear from their eyes, and there will be no more death or mourning or crying or pain, for the old order has passed away. Not just an end to tears, but God Himself wiping them away.",
  "Every grief you carry has an expiry date. He is coming to wipe the last tear Himself."],
 "1 Peter 1:3": [
  "Peter opens his letter to suffering believers with praise, not pity.",
  "Blessed be the God and Father of our Lord Jesus Christ, who by His great mercy has given us new birth into a living hope through the resurrection of Jesus from the dead. The hope is called living because the One it rests on is alive.",
  "Your hope is not a wish; it is anchored in an empty tomb. Live today as one born into it."],
}

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{ref} · Scripture of the day · Makor</title>
<meta name="description" content="{verse}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Makor">
<meta property="og:title" content="{ref}">
<meta property="og:description" content="{verse}">
<meta property="og:image" content="https://makor.co.za/daily/{slug}-share.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="https://makor.co.za/daily/{slug}/">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://makor.co.za/daily/{slug}-share.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&display=swap" rel="stylesheet">
<style>
  :root{{--ink:#0E2A2E;--water:#0F6C6C;--light:#B8862F;--cream:#F4EEDF;--muted:#9BB0AD;}}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:radial-gradient(circle at 50% 30%, #12363B 0%, #0E2A2E 55%, #0A2023 100%);
    color:var(--cream);font-family:'Newsreader',Georgia,serif;min-height:100vh;
    padding:44px 20px 60px;-webkit-font-smoothing:antialiased}}
  main{{max-width:640px;margin:0 auto;text-align:center}}
  .wordmark{{font-family:'Fraunces',serif;font-weight:600;letter-spacing:.5em;font-size:20px;color:var(--water);padding-left:.5em}}
  .rule{{width:64px;height:1px;background:var(--light);opacity:.5;margin:16px auto 12px}}
  .eyebrow{{font-style:italic;color:var(--muted);font-size:16px;margin-bottom:28px}}
  .card{{width:100%;height:auto;border-radius:12px;display:block;margin:0 auto 34px;box-shadow:0 20px 50px -24px rgba(0,0,0,.6)}}
  .verse{{font-family:'Fraunces',serif;font-weight:400;font-size:26px;line-height:1.45;color:var(--cream);margin:0 auto 10px;max-width:560px}}
  .ref{{font-family:'Fraunces',serif;font-weight:500;letter-spacing:.2em;font-size:15px;color:var(--light);margin-bottom:32px}}
  .writeup{{text-align:left;max-width:560px;margin:0 auto 36px}}
  .writeup p{{font-size:18px;line-height:1.7;color:#E7E0CF;margin-bottom:18px}}
  .btn{{display:block;max-width:420px;width:100%;margin:0 auto 14px;padding:15px 24px;border-radius:8px;border:0;cursor:pointer;
    font-family:'Fraunces',serif;font-weight:500;font-size:17px;text-decoration:none;text-align:center}}
  a.btn{{line-height:1.2}}
  .primary{{background:var(--light);color:#0A2023}}
  .share{{background:var(--water);color:#fff}}
  footer{{margin-top:44px;color:var(--muted);font-size:13px;line-height:1.7}}
  footer a{{color:var(--water);text-decoration:none}}
</style>
</head>
<body>
<main>
  <div class="wordmark">MAKOR</div>
  <div class="rule"></div>
  <div class="eyebrow">Scripture of the day</div>
  <img class="card" src="data:image/png;base64,{b64}" alt="{ref} scripture card">
  <p class="verse">{verse}</p>
  <p class="ref">{ref}</p>
  <div class="writeup">{writeup_html}</div>
  <a class="btn primary" href="{study_url}">Read the full study</a>
  <button class="btn share" type="button" onclick="makorShare()">Share</button>
  <footer>Makor &middot; <a href="https://makor.co.za">makor.co.za</a><br>Every study an act of discipleship.</footer>
</main>
<script>
async function makorShare(){{
  var url="https://makor.co.za/daily/{slug}/";
  var text={share_text_js};
  var imgUrl="https://makor.co.za/daily/{slug}.png";
  try{{
    if(navigator.canShare){{
      try{{
        var r=await fetch(imgUrl); var b=await r.blob();
        var f=new File([b],"{slug}.png",{{type:"image/png"}});
        if(navigator.canShare({{files:[f]}})){{ await navigator.share({{files:[f],text:text+"\\n\\n"+url}}); return; }}
      }}catch(e){{}}
    }}
    if(navigator.share){{ await navigator.share({{title:"Makor",text:text,url:url}}); return; }}
  }}catch(e){{ return; }}
  try{{ await navigator.clipboard.writeText(text+"\\n\\n"+url); alert("Link copied. Paste it anywhere to share."); }}
  catch(e){{ window.prompt("Copy this link to share:", url); }}
}}
</script>
</body>
</html>
"""

def esc_attr(s):
    return s.replace('"', "&quot;")

def dashguard(s, where):
    assert "—" not in s and "–" not in s, f"DASH in {where}: {s[:80]}"

order = json.load(open(f"{OUT}/match50.json"))
daily_entries = []
pool_rows = []
made = 0
for m in order:
    ref = m["ref"]
    slug = daily_slug(ref)
    verse = gc._clean(m["verse"])
    study_url_abs = m["url"]
    study_url_rel = study_url_abs.replace(SITE, "")
    writeup = WRITEUPS[ref]
    for p in writeup: dashguard(p, ref)
    dashguard(verse, ref)
    # cards
    gc.render_vertical(verse, ref).save(f"{REPO}/public/daily/{slug}.png")
    gc.render_share(verse, ref).save(f"{REPO}/public/daily/{slug}-share.png")
    # page
    with open(f"{REPO}/public/daily/{slug}.png", "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    writeup_html = "".join(f"<p>{p}</p>" for p in writeup)
    share_text_js = json.dumps('"' + verse + '" (' + ref + ')')
    html = PAGE.format(ref=esc_attr(ref), verse=esc_attr(verse), slug=slug,
                       study_url=study_url_abs, b64=b64, writeup_html=writeup_html,
                       share_text_js=share_text_js)
    dashguard(html.replace(b64, ""), f"page {slug}")
    os.makedirs(f"{REPO}/public/daily/{slug}", exist_ok=True)
    with open(f"{REPO}/public/daily/{slug}/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    daily_entries.append({"slug": slug, "ref": ref, "verse": verse, "story": writeup, "studyUrl": study_url_rel})
    if slug not in EXISTING:
        pool_rows.append({"slug": slug, "ref": ref, "verse_text": verse, "writeup_html": writeup_html,
                          "writeup_txt": "\n\n".join(writeup), "study_url": study_url_abs,
                          "daily_page_url": f"{SITE}/daily/{slug}/", "image_path": f"/daily/{slug}.png",
                          "og_image_path": f"/daily/{slug}-share.png"})
    made += 1

# write daily.js
lines = ["// Verse of the day rotation. These entries mirror the hand made daily share",
         "// pages under public/daily/. The app picks one per calendar day so that the",
         "// verse in the app matches the daily in rotation for that date. Generated from",
         "// the 50 verse pool; verse text is verbatim BSB pulled from the study JSON.",
         "",
         "export const dailyEntries = ["]
for i, e in enumerate(daily_entries):
    comma = "," if i < len(daily_entries) - 1 else ""
    obj = ("  {\n"
           f"    slug: {json.dumps(e['slug'])},\n"
           f"    ref: {json.dumps(e['ref'])},\n"
           f"    verse: {json.dumps(e['verse'])},\n"
           f"    story: {json.dumps(e['story'], ensure_ascii=False)},\n"
           f"    studyUrl: {json.dumps(e['studyUrl'])}\n"
           f"  }}{comma}")
    lines.append(obj)
lines.append("];")
djs = "\n".join(lines) + "\n"
dashguard(djs, "daily.js")
with open(f"{REPO}/src/data/daily.js", "w", encoding="utf-8") as f:
    f.write(djs)

# SQL for the 45 new pool rows
def sq(s): return "'" + s.replace("'", "''") + "'"
sql = ["-- Insert the 45 new daily_pool rows (the 5 already present are left untouched)."]
for r in pool_rows:
    sql.append(
      "insert into comms.daily_pool (slug, ref, verse_text, writeup_html, writeup_txt, study_url, daily_page_url, image_path, og_image_path, active) values ("
      f"{sq(r['slug'])}, {sq(r['ref'])}, {sq(r['verse_text'])}, {sq(r['writeup_html'])}, {sq(r['writeup_txt'])}, {sq(r['study_url'])}, {sq(r['daily_page_url'])}, {sq(r['image_path'])}, {sq(r['og_image_path'])}, true);")
with open(f"{OUT}/pool_insert.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(sql) + "\n")

print(f"built {made} dailies; {len(pool_rows)} new pool rows; daily.js has {len(daily_entries)} entries")
