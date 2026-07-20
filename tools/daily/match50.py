import json, os, re, glob

REPO = "/sessions/epic-ecstatic-babbage/mnt/makor"
STUDROOT = os.path.join(REPO, "src/content/studies")

# (n, ref-string, book-folder, chapter, [verses])
TARGETS = [
 (1,"Genesis 1:1","genesis",1,[1]),
 (2,"Psalm 36:9","psalms",36,[9]),
 (3,"Psalm 19:1","psalms",19,[1]),
 (4,"Jeremiah 2:13","jeremiah",2,[13]),
 (5,"Revelation 22:1","revelation",22,[1]),
 (6,"Lamentations 3:22-23","lamentations",3,[22,23]),
 (7,"Psalm 103:8","psalms",103,[8]),
 (8,"Psalm 86:15","psalms",86,[15]),
 (9,"Zephaniah 3:17","zephaniah",3,[17]),
 (10,"Psalm 30:5","psalms",30,[5]),
 (11,"Proverbs 3:5-6","proverbs",3,[5,6]),
 (12,"Psalm 23:1","psalms",23,[1]),
 (13,"Psalm 46:1","psalms",46,[1]),
 (14,"Isaiah 41:10","isaiah",41,[10]),
 (15,"Matthew 6:33","matthew",6,[33]),
 (16,"Philippians 4:6-7","philippians",4,[6,7]),
 (17,"1 Peter 5:7","1-peter",5,[7]),
 (18,"John 1:1","john",1,[1]),
 (19,"John 3:16","john",3,[16]),
 (20,"John 14:6","john",14,[6]),
 (21,"Isaiah 9:6","isaiah",9,[6]),
 (22,"Isaiah 53:5","isaiah",53,[5]),
 (23,"Colossians 1:16-17","colossians",1,[16,17]),
 (24,"Hebrews 1:3","hebrews",1,[3]),
 (25,"Isaiah 55:1","isaiah",55,[1]),
 (26,"John 4:14","john",4,[14]),
 (27,"John 7:37-38","john",7,[37,38]),
 (28,"Matthew 11:28","matthew",11,[28]),
 (29,"John 8:12","john",8,[12]),
 (30,"Psalm 119:105","psalms",119,[105]),
 (31,"Isaiah 40:8","isaiah",40,[8]),
 (32,"Hebrews 4:12","hebrews",4,[12]),
 (33,"2 Timothy 3:16","2-timothy",3,[16]),
 (34,"Joshua 1:8","joshua",1,[8]),
 (35,"Isaiah 40:31","isaiah",40,[31]),
 (36,"Joshua 1:9","joshua",1,[9]),
 (37,"Philippians 4:13","philippians",4,[13]),
 (38,"Psalm 27:1","psalms",27,[1]),
 (39,"2 Corinthians 12:9","2-corinthians",12,[9]),
 (40,"Psalm 121:1-2","psalms",121,[1,2]),
 (41,"Proverbs 9:10","proverbs",9,[10]),
 (42,"Micah 6:8","micah",6,[8]),
 (43,"Ecclesiastes 3:1","ecclesiastes",3,[1]),
 (44,"Romans 12:2","romans",12,[2]),
 (45,"Matthew 5:16","matthew",5,[16]),
 (46,"Ephesians 2:8-9","ephesians",2,[8,9]),
 (47,"Romans 8:28","romans",8,[28]),
 (48,"Romans 15:13","romans",15,[13]),
 (49,"Revelation 21:4","revelation",21,[4]),
 (50,"1 Peter 1:3","1-peter",1,[3]),
]

TOKEN = re.compile(r"\{\{[^|]+\|([^}]*)\}\}")
def clean(t):
    return TOKEN.sub(r"\1", t)

def load_book(folder):
    studies=[]
    for p in glob.glob(os.path.join(STUDROOT, folder, "*.json")):
        try:
            d=json.load(open(p))
        except Exception as e:
            continue
        vmap={}
        for u in d.get("text",{}).get("units",[]):
            for v in u.get("verses",[]):
                vmap[(v.get("chapter"), v.get("n"))]=v.get("text","")
        studies.append({
            "path":p,
            "slug":d.get("section",{}).get("slug"),
            "title":d.get("section",{}).get("title"),
            "thesis":d.get("section",{}).get("thesis"),
            "passageRef":d.get("section",{}).get("passageRef"),
            "book":d.get("book"),
            "vmap":vmap,
        })
    return studies

cache={}
results=[]
missing=[]
for n,ref,folder,ch,verses in TARGETS:
    if folder not in cache:
        cache[folder]=load_book(folder)
    hit=None
    for s in cache[folder]:
        if all((ch,v) in s["vmap"] for v in verses):
            hit=s; break
    if not hit:
        # fallback: study containing the first verse
        for s in cache[folder]:
            if (ch,verses[0]) in s["vmap"]:
                hit=s; break
    if not hit:
        missing.append((n,ref,folder))
        results.append({"n":n,"ref":ref,"ok":False})
        continue
    text=" ".join(clean(hit["vmap"][(ch,v)]) for v in verses if (ch,v) in hit["vmap"])
    slug=hit["slug"]; bslug=folder
    url=f"https://makor.co.za/{bslug}/{slug}/"
    results.append({"n":n,"ref":ref,"ok":True,"slug":slug,"title":hit["title"],
                    "thesis":hit["thesis"],"url":url,"verse":text,"passageRef":hit["passageRef"]})

print("MATCHED", sum(1 for r in results if r.get("ok")), "of", len(TARGETS))
if missing:
    print("MISSING:")
    for m in missing: print("  ", m)
print()
for r in results:
    if r.get("ok"):
        print(f'{r["n"]:>2}. {r["ref"]:<20} -> {r["url"]}')
        print(f'      title: {r["title"]}  (passageRef {r["passageRef"]})')
        print(f'      verse: {r["verse"][:110]}')
    else:
        print(f'{r["n"]:>2}. {r["ref"]:<20} -> NOT FOUND')

json.dump(results, open("/sessions/epic-ecstatic-babbage/mnt/outputs/match50.json","w"), indent=1, ensure_ascii=False)
print("\nwrote match50.json")
