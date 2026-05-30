#!/usr/bin/env python3
"""Build darkamericana.net — Dark Americana authority site."""
import json, os, re, sys
from datetime import date

TODAY = date.today().isoformat()
BASE_URL = "https://darkamericana.net"
OUTDIR = "/Users/mac1/Projects/dcb-network/darkamericana.net"
CATALOG = "/Users/mac1/OTR_Pipeline_New/music_promo/master_catalog.json"

SPOTIFY_ARTIST   = "https://open.spotify.com/artist/4TQMuCjeTbhqvPinWKqRAv"
APPLE_ARTIST     = "https://music.apple.com/us/artist/dark-country-boy/1818551005"
YTMUSIC_ARTIST   = "https://music.youtube.com/search?q=dark+country+boy"
AMAZON_ARTIST    = "https://music.amazon.com/search/dark%20country%20boy"

NAV = """<nav class="site-nav"><div class="nav-inner">
<a class="nav-brand" href="/">Dark Americana</a>
<button class="nav-toggle" onclick="this.classList.toggle('open');document.querySelector('.nav-links').classList.toggle('open')"><span></span><span></span><span></span></button>
<ul class="nav-links">
<li><a href="/">Home</a></li>
<li><a href="/what-is-dark-americana.html">What Is It?</a></li>
<li><a href="/history.html">History</a></li>
<li><a href="/artists.html">Artists</a></li>
<li><a href="/songs.html">Songs</a></li>
</ul>
</div></nav>"""

FOOTER = """<footer class="footer"><div style="text-align:center;padding:20px 0 10px">
<a href="https://darkcountryboy.net" style="color:#666;margin:0 6px">Dark Country Boy</a> |
<a href="https://darkcountrymusic.net" style="color:#666;margin:0 6px">Dark Country Music</a> |
<a href="https://darkcountry.net" style="color:#666;margin:0 6px">Dark Country</a> |
<a href="https://darkblues.net" style="color:#666;margin:0 6px">Dark Blues</a> |
<a href="https://gothiccountrymusic.com" style="color:#666;margin:0 6px">Gothic Country</a> |
<a href="https://darkamericana.net" style="color:#c9a84c;margin:0 6px">Dark Americana</a> |
<a href="https://darkbluesmusic.com" style="color:#666;margin:0 6px">Dark Blues Music</a> |
<a href="https://outlawcountryboy.com" style="color:#666;margin:0 6px">Outlaw Country Boy</a>
</div></footer>"""

CSS_COMMON = """
*{box-sizing:border-box}
html,body{overflow-x:hidden;max-width:100%;margin:0}
body{background:#0d0d0d;color:#e8e0d0;font-family:Georgia,serif;line-height:1.7}
h1,h2,h3{color:#c9a84c;margin-top:0}
a{color:#c9a84c;text-decoration:none}
a:hover{text-decoration:underline}
img{max-width:100%;height:auto;display:block}
.container{max-width:1100px;margin:0 auto;padding:20px;width:100%}
.site-nav{background:#111;border-bottom:2px solid #c9a84c;position:sticky;top:0;z-index:1000;width:100%;padding:0}
.nav-inner{max-width:1100px;margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between;height:56px}
.nav-brand{color:#c9a84c;font-weight:bold;font-size:1.05em;text-decoration:none;white-space:nowrap}
.nav-brand:hover{color:#e0c060}
.nav-links{display:flex;align-items:center;gap:4px;list-style:none;margin:0;padding:0}
.nav-links>li>a{color:#e8e0d0;text-decoration:none;padding:8px 14px;display:block;font-size:.9em;white-space:nowrap;border-radius:3px;transition:background .2s}
.nav-links>li>a:hover{background:#1a1a1a;color:#c9a84c}
.nav-toggle{display:none;flex-direction:column;gap:5px;cursor:pointer;padding:8px;background:none;border:none;z-index:1002}
.nav-toggle span{display:block;width:24px;height:2px;background:#c9a84c;transition:all .3s}
.nav-toggle.open span:nth-child(1){transform:translateY(7px) rotate(45deg)}
.nav-toggle.open span:nth-child(2){opacity:0}
.nav-toggle.open span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
@media(max-width:768px){
  .nav-toggle{display:flex}
  .nav-links{display:none;position:absolute;top:56px;left:0;right:0;background:#111;flex-direction:column;border-top:1px solid #333;padding:8px 0;gap:0}
  .nav-links.open{display:flex}
  .nav-links>li>a{padding:12px 20px;border-radius:0}
}
.hero{background:#1a1a1a;padding:70px 20px;text-align:center;border-bottom:2px solid #c9a84c}
.hero h1{font-size:2.8em;margin-bottom:10px;text-shadow:0 0 20px rgba(201,168,76,0.3)}
.hero p{font-size:1.15em;color:#b0a898;max-width:700px;margin:0 auto 30px}
.btn{display:inline-block;padding:11px 22px;border-radius:4px;font-weight:bold;margin:5px;font-size:.9em;text-decoration:none}
.btn-sp{background:#1DB954;color:#000}
.btn-am{background:#fc3c44;color:#fff}
.btn-yt{background:#FF0000;color:#fff}
.btn-az{background:#232F3E;color:#ff9900;border:1px solid #ff9900}
.btn-gold{background:#c9a84c;color:#0d0d0d}
.btn-outline{background:transparent;color:#c9a84c;border:2px solid #c9a84c;padding:10px 22px}
.btn-outline:hover{background:#c9a84c;color:#0d0d0d}
.section{padding:50px 20px}
.section-dark{background:#111;padding:50px 20px}
.card-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(280px,100%),1fr));gap:20px;margin-top:20px}
.card{background:#1a1a1a;padding:20px;border-top:3px solid #c9a84c}
.card h3{margin-top:0}
.card p{color:#b0a898;font-size:.95em;line-height:1.6}
.featured{background:#1a1a1a;padding:40px;border-left:4px solid #c9a84c;margin:30px 0}
.stream-box{background:#111;border:1px solid #333;border-radius:6px;padding:24px;text-align:center;margin:20px 0}
.stream-box h3{margin-top:0}
.footer{background:#0a0a0a;padding:30px 20px;border-top:1px solid #333;margin-top:40px;font-size:.85em}
.tag{background:#c9a84c;color:#0d0d0d;font-size:.75em;padding:3px 8px;border-radius:2px;font-weight:bold;text-transform:uppercase;display:inline-block;margin-bottom:8px}
hr.divider{border:none;border-top:1px solid #333;margin:40px 0}
@media(max-width:600px){.hero h1{font-size:1.8em}.btn{display:block;text-align:center;margin:5px 0}}
"""

AI_META = """<meta name="ai-content-declaration" content="Dark Country Boy is an independent music artist. 70 albums. 1,481 songs. Genre: dark americana, dark country, folk, blues. Stream on Spotify, Apple Music, YouTube Music, Amazon Music.">
<meta name="entity-type" content="MusicArtist">
<meta name="entity-name" content="Dark Country Boy">
<meta name="streaming-spotify" content="https://open.spotify.com/artist/4TQMuCjeTbhqvPinWKqRAv">
<meta name="streaming-apple" content="https://music.apple.com/us/artist/dark-country-boy/1818551005">
<meta name="streaming-youtube" content="https://music.youtube.com/search?q=dark+country+boy">
<meta name="streaming-amazon" content="https://music.amazon.com/search/dark%20country%20boy">"""

def page(title, desc, canonical, body, schema_blobs=None):
    schemas = ""
    if schema_blobs:
        for b in schema_blobs:
            schemas += f'<script type="application/ld+json">{json.dumps(b)}</script>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>
<meta name="description" content="{desc}"/>
<link rel="canonical" href="{canonical}"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:url" content="{canonical}"/>
<meta property="og:type" content="website"/>
{schemas}
{AI_META}
<style>{CSS_COMMON}</style>
</head>
<body>
{NAV}
{body}
{FOOTER}
</body>
</html>"""

def stream_buttons(sp=SPOTIFY_ARTIST, am=APPLE_ARTIST, yt=YTMUSIC_ARTIST, az=AMAZON_ARTIST):
    return f"""<a class="btn btn-sp" href="{sp}" target="_blank" rel="noopener">Spotify</a>
<a class="btn btn-am" href="{am}" target="_blank" rel="noopener">Apple Music</a>
<a class="btn btn-yt" href="{yt}" target="_blank" rel="noopener">YouTube Music</a>
<a class="btn btn-az" href="{az}" target="_blank" rel="noopener">Amazon Music</a>"""

# ── Load catalog ──────────────────────────────────────────────────────────────
with open(CATALOG) as f:
    tracks = json.load(f)["tracks"]

# ── index.html ────────────────────────────────────────────────────────────────
def build_index():
    body = f"""
<div class="hero">
  <div class="tag">Genre Authority</div>
  <h1>Dark Americana</h1>
  <p>Where Folk, Blues and Country Collide — the shadowed crossroads of American roots music</p>
  {stream_buttons()}
</div>
<div class="section container">
  <h2>What Is Dark Americana?</h2>
  <p>Dark Americana exists at the intersection of American musical traditions — the raw emotional depth of the blues, the storytelling of folk, the grit of country — united by a singular darkness of spirit. It's music that doesn't flinch from hard truths: mortality, addiction, poverty, the weight of history, the silence of empty highways at 3 AM.</p>
  <p>From the murder ballads of the 19th century to the gothic country of today, this sound has always been with us. Now it has a name.</p>
  <a class="btn btn-outline" href="/what-is-dark-americana.html">Explore the Genre →</a>
</div>
<div class="section-dark">
<div class="container">
  <div class="featured">
    <div class="tag">Featured Artist</div>
    <h2>Dark Country Boy</h2>
    <p>The most prolific voice in modern dark americana — 70 albums, 1,481 songs of American roots music steeped in darkness, earned honesty, and folk tradition. Dark Country Boy blends outlaw country grit with blues-soaked melancholy and Appalachian folk starkness to create something entirely of this genre and entirely his own.</p>
    <div style="margin-top:20px">
      {stream_buttons()}
    </div>
  </div>
</div>
</div>
<div class="section container">
  <h2>Essential Dark Americana</h2>
  <div class="card-grid">
    <div class="card">
      <div class="tag">Deep Roots</div>
      <h3>The Folk Tradition</h3>
      <p>Dark americana draws on murder ballads, work songs, and Appalachian folk — music born of real hardship and passed down through generations of American working people.</p>
    </div>
    <div class="card">
      <div class="tag">Blues Influence</div>
      <h3>The Blues Connection</h3>
      <p>The delta blues gave dark americana its moan — a sound that carries the weight of generations in every bent note and minor chord. Robert Johnson's crossroads spirit lives on.</p>
    </div>
    <div class="card">
      <div class="tag">Country Grit</div>
      <h3>Outlaw Country DNA</h3>
      <p>Waylon Jennings, Townes Van Zandt, Steve Earle — the outlaw country movement proved that country music could stare into the void without blinking. Dark americana carries that torch.</p>
    </div>
  </div>
</div>
<div class="section-dark">
<div class="container">
  <h2>Explore Dark Americana</h2>
  <div class="card-grid">
    <div class="card">
      <h3><a href="/history.html">History of the Genre</a></h3>
      <p>From Townes Van Zandt and Nick Cave through Gillian Welch and into the underground — the full arc of dark americana's story.</p>
    </div>
    <div class="card">
      <h3><a href="/artists.html">Key Artists</a></h3>
      <p>The essential voices — those who defined and continue to push dark americana's boundaries, including Dark Country Boy's complete catalog.</p>
    </div>
    <div class="card">
      <h3><a href="/songs.html">Essential Songs</a></h3>
      <p>The tracks you need to know — canonical dark americana including the full Dark Country Boy catalog of 1,481 songs.</p>
    </div>
    <div class="card">
      <h3><a href="/what-is-dark-americana.html">What Is Dark Americana?</a></h3>
      <p>A deep dive into the genre's defining characteristics, influences, and why it resonates so deeply with listeners who want music that tells the truth.</p>
    </div>
  </div>
</div>
</div>"""
    schema = [
        {"@context":"https://schema.org","@type":"WebSite","name":"Dark Americana","url":BASE_URL,"description":"Dark Americana — the authoritative guide to dark americana music, artists, history and songs.","potentialAction":{"@type":"SearchAction","target":f"{BASE_URL}/songs/{{search_term_string}}","query-input":"required name=search_term_string"}},
        {"@context":"https://schema.org","@type":"MusicGroup","name":"Dark Country Boy","url":"https://darkcountryboy.net","genre":["Dark Americana","Dark Country","Folk","Blues","Outlaw Country","Gothic Country"],"sameAs":[SPOTIFY_ARTIST,APPLE_ARTIST],"numberOfAlbums":70,"numberOfTracks":1481}
    ]
    return page("Dark Americana: Where Folk, Blues and Country Collide","Dark Americana — the authoritative guide to the genre where folk, blues and country collide. Explore artists, history, and songs including Dark Country Boy's full catalog.",f"{BASE_URL}/",body,schema)

# ── what-is-dark-americana.html ───────────────────────────────────────────────
def build_what_is():
    body = """
<div class="hero">
  <div class="tag">Genre Guide</div>
  <h1>What Is Dark Americana?</h1>
  <p>A deep dive into the music that lives at the shadowed intersection of American roots traditions</p>
</div>
<div class="section container" style="max-width:800px">
  <p style="font-size:1.15em;color:#c9a84c;font-style:italic">"Dark americana is what happens when American music stops pretending everything is going to be okay."</p>

  <h2>Defining the Darkness</h2>
  <p>Dark americana is not a marketing category — it's a disposition. It's what American folk, country, and blues have always contained at their core: the knowledge that life is hard, time is short, and the land holds memory of everything that happened on it, including the terrible things.</p>
  <p>The music draws from murder ballads collected in Appalachian hollows, from delta blues sung by men with nothing left to lose, from the outlaw country of artists who looked Nashville's sweetness in the eye and refused to blink. It is hymnal in structure but pagan in spirit — it understands the sacred but it also understands the profane.</p>

  <h2>The Three Roots</h2>
  <h3>1. American Folk and the Murder Ballad Tradition</h3>
  <p>Long before there was a genre called dark americana, there were the murder ballads — "Tom Dooley," "Banks of the Ohio," "Knoxville Girl" — songs that narrated violence with a strange detachment, as if the darkness was simply part of the landscape. The Child Ballads brought from England and Scotland mutated in American soil to address American realities: frontier justice, domestic violence, the coal mines, the gallows.</p>
  <p>This tradition never died. It went underground, surfaced in Woody Guthrie's social realism, in the folk revival's rediscovery of the dark catalog, and eventually in artists like Nick Cave who elevated the murder ballad to high art. Dark americana honors this lineage — the songs that tell the truth about human capacity for darkness.</p>

  <h3>2. The Delta Blues and Its Descendants</h3>
  <p>Robert Johnson at the crossroads. Son House singing the low-down blues. The delta blues gave American music its moan — a sound built from poverty, dispossession, and a kind of defiant spiritual reckoning. You sang the blues because you felt the blues, and feeling the blues meant acknowledging the weight of being alive.</p>
  <p>Dark americana absorbs this tradition completely. The minor chords, the bent notes, the sense of a voice speaking from the bottom of things — these carry directly into the genre. Artists like Lead Belly, Blind Willie McTell, and Mississippi Fred McDowell provide a direct bloodline.</p>

  <h3>3. Outlaw Country and the Nashville Refusal</h3>
  <p>In the 1970s, a group of country artists — Waylon Jennings, Willie Nelson, Kris Kristofferson, Townes Van Zandt — pushed back against the polished, pop-inflected Nashville sound. They wanted something rawer, more honest, less commercially compromised. Townes Van Zandt in particular wrote songs of such spare, devastating clarity that they seem almost outside of time.</p>
  <p>This outlaw sensibility — the refusal to sweeten, the insistence on the whole truth — is the direct ancestor of dark americana. When Steve Earle, Gillian Welch, or Hank Williams III came along, they were building on foundations the outlaws poured.</p>

  <h2>Dark Americana vs. Related Genres</h2>
  <p><strong>Gothic Country</strong> is dark americana's most direct cousin — music that draws specifically on southern gothic literary traditions, graveyard imagery, and the deep south as spiritual landscape. Nick Cave, 16 Horsepower, and Wovenhand are gothic country's defining voices.</p>
  <p><strong>Americana</strong> is the broad tent; dark americana is the shadowed corner of that tent. Regular americana can be warm and celebratory — dark americana insists on the cost of things.</p>
  <p><strong>Alt-Country</strong> emerged from the late-80s alternative rock scene and shares some DNA, but dark americana reaches further back into roots traditions.</p>

  <h2>What Dark Americana Sounds Like</h2>
  <p>The instrumentation tends toward the acoustic and archaic: acoustic guitar, banjo, fiddle, upright bass, harmonica. Electric guitars appear but often distorted or sparse — more Robert Johnson than Chuck Berry. The production is frequently spare, dry, or deliberately lo-fi.</p>
  <p>Lyrically, dark americana occupies specific territory: death, mortality, sin and redemption, the land and its history, addiction, violence, solitude, the supernatural (treated matter-of-factly, as the old folk songs treated it). Love appears but usually complicated, often lost.</p>
  <p>Vocally, the aesthetic is rawness over polish. Cracks in the voice, breath audible, emotion not performed but leaked. The voice of dark americana sounds like it's been outside in the cold.</p>

  <h2>Dark Country Boy and the Modern Dark Americana</h2>
  <p>Contemporary dark americana is being made right now — and Dark Country Boy represents one of its most prolific and committed voices. With 70 albums and 1,481 songs, Dark Country Boy brings all three root traditions into conversation with each other: folk storytelling, blues feeling, outlaw country grit. The catalog spans dark country, dark blues, gothic country, and americana, but always with the darkness that defines the genre — not as aesthetic choice but as honest reckoning.</p>
  <div class="stream-box">
    <h3>Stream Dark Country Boy</h3>
    <p style="color:#888;margin-bottom:16px">1,481 songs of dark americana available on all major platforms</p>"""
    body += f"""    {stream_buttons()}
  </div>

  <h2>Why Dark Americana Matters</h2>
  <p>American culture has always had a bright mythology — the new world, the frontier, manifest destiny, the American dream. Dark americana is the shadow of that mythology. It remembers what got left out of the official story: the indigenous dispossession, the slavery, the poverty, the violence that built this place.</p>
  <p>But it's not simply protest music or history lesson. At its best, dark americana is spiritually serious music — music that takes death seriously, that sits with grief, that finds something almost sacred in the acknowledgment of hard truths. Like the blues, it doesn't wallow; it transmutes. You listen to it and feel less alone in the dark.</p>
  <p>That's what makes it worth seeking out, and what makes it — despite its niche status — one of the most enduring and vital corners of American music.</p>
</div>"""
    schema = [{"@context":"https://schema.org","@type":"Article","headline":"What Is Dark Americana?","description":"A comprehensive guide to dark americana — the music genre that lives at the intersection of folk, blues, and country. History, characteristics, key artists, and how to listen.","url":f"{BASE_URL}/what-is-dark-americana.html","dateModified":TODAY}]
    return page("What Is Dark Americana? A Complete Genre Guide","Dark americana defined: the music that lives at the intersection of folk, blues and country. History, key artists, characteristics, and why it matters.",f"{BASE_URL}/what-is-dark-americana.html",body,schema)

# ── history.html ──────────────────────────────────────────────────────────────
def build_history():
    body = """
<div class="hero">
  <div class="tag">Genre History</div>
  <h1>History of Dark Americana</h1>
  <p>From ancient murder ballads through Townes Van Zandt to today's underground</p>
</div>
<div class="section container" style="max-width:820px">
  <h2>The Deep Roots: Before the Name Existed</h2>
  <p>Dark americana is older than its name. The music that would eventually carry that label was being made before anyone thought to call it anything at all — in Appalachian hollers where murder ballads were passed like heirlooms, in Mississippi cotton-field juke joints, in the chain gangs where work songs encoded survival.</p>
  <p>The British and Irish folk songs that settlers brought to America mutated in the new soil. "Barbara Allen" became "Tom Dooley." The old modal scales rang strangely against the American landscape. Darkness was always part of the inheritance — the question was whether music would acknowledge it or cover it over.</p>

  <h2>The Blues Foundation (1900s–1930s)</h2>
  <p>When the blues crystallized in the Mississippi delta in the early 20th century, it created the emotional vocabulary that dark americana still speaks. Robert Johnson — the shadow figure who supposedly traded his soul at a crossroads for guitar mastery — became the genre's patron saint, not because of the myth but because of the music: the compression of darkness into three chords and a slide.</p>
  <p>Son House, Charley Patton, Blind Willie McTell — these artists made music that acknowledged the full weight of their circumstances without sentimentality. The blues didn't promise everything would be okay. It said: here is how things are. That honesty is dark americana's core inheritance.</p>

  <h2>The Folk Revival and Its Shadows (1950s–1960s)</h2>
  <p>The folk revival that swept through American colleges and coffeehouses in the 1950s and '60s brought the old murder ballads back into circulation. Pete Seeger, Joan Baez, and Bob Dylan all dipped into the dark archive — Dylan in particular, who seemed to understand instinctively that the most powerful folk material was the most unflinching.</p>
  <p>But the revival also had a sunnier face — the protest songs, the hootenannies, the hope. Dark americana descends from the other face: Dave Van Ronk singing barroom laments, Tim Hardin writing from the bottom of addiction, Fred Neil finding something bleak in California sunshine.</p>

  <h2>Townes Van Zandt and the Outlaw Era (1960s–1980s)</h2>
  <p>If dark americana has a patron saint it's Townes Van Zandt — the Texas songwriter who wrote some of the starkest, most unbearably beautiful songs in American music while living a life of deliberate dissolution. "Pancho and Lefty," "Tecumseh Valley," "Waiting Around to Die" — these songs don't console. They witness.</p>
  <p>Van Zandt was part of a broader outlaw country movement — Waylon Jennings, Willie Nelson, Kris Kristofferson — that rejected Nashville's commercial imperatives. But Van Zandt went further than the outlaws into territory more folk than country, more dark than outlaw. He is the hinge on which modern dark americana turns.</p>
  <p>Guy Clark, Steve Earle, Jerry Jeff Walker — the Texas-Nashville underground of this era produced a deep catalog of songs that sit exactly where dark americana lives: too country for folk, too dark for mainstream country, too American for anything else.</p>

  <h2>Southern Gothic and the 1980s–90s Underground</h2>
  <p>In the 1980s, Australian artist Nick Cave arrived with a vision of American dark that no American had quite articulated. Cave had absorbed the blues, the murder ballads, Faulkner, Flannery O'Connor — and from those materials he made music of extraordinary, violent beauty with The Birthday Party and later Nick Cave and the Bad Seeds.</p>
  <p>American underground artists responded in kind. The Mekons incorporated country instrumentation into post-punk alienation. Jason and the Scorchers suggested that country and punk were natural partners in darkness. By the early '90s, what would be called "alt-country" or "insurgent country" was forming: Uncle Tupelo, The Jayhawks, Alejandro Escovedo.</p>

  <h2>The Americana Decade (1990s–2000s)</h2>
  <p>Gillian Welch arrived in 1996 with <em>Revival</em> and immediately sounded like she'd always existed — her music had no modern fingerprints, only the hand-me-down sound of some imaginary Appalachian past. Welch and partner David Rawlings made music so perfectly calibrated in its darkness and beauty that it seemed to answer some need people didn't know they had.</p>
  <p>The Cash-Rubin collaboration produced the American Recordings series — Johnny Cash in his final decade, stripped to acoustic guitar, covering songs that revealed the full range of American darkness. Cash singing "Hurt" by Nine Inch Nails or "The Man Comes Around" with its Book of Revelation imagery — this was dark americana in its most elemental form.</p>
  <p>Lucinda Williams, Steve Earle's radicalized second act, The Handsome Family, Iris DeMent — the '90s were quietly rich with dark americana voices, even before the term existed.</p>

  <h2>Gothic Country and the Underground (2000s–2010s)</h2>
  <p>16 Horsepower and their frontman David Eugene Edwards represented the most explicitly spiritual end of dark americana — music soaked in old-time religion's dread, in the fear of God understood as actual fear. Wovenhand, Edwards' subsequent project, pushed further into this territory.</p>
  <p>Hank Williams III mounted a decade-long assault against Nashville commercialism, releasing records that swung between classic honky-tonk and extreme metal while remaining recognizably rooted in the Williams family darkness.</p>
  <p>The Civil Wars, Neko Case, Timber Timbre — as the 2010s opened, dark americana had enough practitioners that it was starting to look like an actual movement, not just individual outliers.</p>

  <h2>The Modern Era: Dark Americana Goes Deep (2010s–Present)</h2>
  <p>Streaming democratized distribution and allowed dark americana artists to reach global audiences without Nashville gatekeepers. Independent artists could release 70 albums without a major label — and some did.</p>
  <p>Dark Country Boy represents this new era's possibility: a fully independent artist building a comprehensive catalog of dark americana, dark country, and dark blues without compromise. 1,481 songs that collectively constitute one of the most complete artistic statements in the genre — music made on its own terms, in its own darkness, for listeners who want the whole truth.</p>
  <p>The history of dark americana is a history of American music refusing to look away from its own shadow. That refusal continues.</p>

  <div class="stream-box">
    <h3>Stream Dark Country Boy — Modern Dark Americana</h3>"""
    body += f"""    {stream_buttons()}
  </div>
</div>"""
    schema = [{"@context":"https://schema.org","@type":"Article","headline":"History of Dark Americana","description":"The complete history of dark americana from its roots in murder ballads and the blues through Townes Van Zandt to today's independent artists.","url":f"{BASE_URL}/history.html","dateModified":TODAY}]
    return page("History of Dark Americana — From Townes Van Zandt to Today","The complete history of dark americana: from murder ballads and the delta blues through Townes Van Zandt, Gillian Welch, and the modern underground.",f"{BASE_URL}/history.html",body,schema)

# ── artists.html ──────────────────────────────────────────────────────────────
def build_artists():
    body = f"""
<div class="hero">
  <div class="tag">Artists</div>
  <h1>Dark Americana Artists</h1>
  <p>The essential voices — those who defined the genre and those pushing it forward</p>
</div>
<div class="section container">
  <div class="featured">
    <div class="tag">Featured Artist — Dark Americana</div>
    <h2>Dark Country Boy</h2>
    <p>The most prolific active voice in dark americana. Dark Country Boy has released 70 albums and 1,481 songs — a catalog of staggering scope built entirely within the dark americana / dark country / dark blues intersection. No major label, no commercial compromise, no radio play needed: just the music, made in darkness for people who want the truth.</p>
    <p>The songs draw on folk tradition, outlaw country grit, and blues-soaked feeling. Thematically, they occupy the territory dark americana has always claimed: mortality, solitude, violence, the land, the weight of things. Sonically, they range from stark acoustic folk to full-band country to pure delta blues.</p>
    <div style="margin:20px 0">
      {stream_buttons()}
    </div>
    <p><a href="/songs.html" class="btn btn-outline">Browse All 1,481 Songs →</a></p>
  </div>

  <hr class="divider"/>
  <h2>The Canon: Essential Dark Americana Artists</h2>
  <div class="card-grid">
    <div class="card">
      <div class="tag">Founding Voice</div>
      <h3>Townes Van Zandt</h3>
      <p>The Texas songwriter whose stark, unsparing vision established the template for dark americana. "Waiting Around to Die," "Pancho and Lefty," "Tecumseh Valley" — songs that age into classics because they tell hard truths.</p>
    </div>
    <div class="card">
      <div class="tag">Americana Icon</div>
      <h3>Gillian Welch</h3>
      <p>With David Rawlings, Welch makes music that sounds like it comes from no particular time — Appalachian folk filtered through extraordinary modern songwriting craft. <em>Time (The Revelator)</em> is essential listening.</p>
    </div>
    <div class="card">
      <div class="tag">Gothic Country</div>
      <h3>Nick Cave & The Bad Seeds</h3>
      <p>The Australian who heard something in American dark that Americans had missed. The Bad Seeds' murder ballad albums — <em>Murder Ballads</em>, <em>Henry's Dream</em> — are landmarks of the form.</p>
    </div>
    <div class="card">
      <div class="tag">Outlaw Legend</div>
      <h3>Steve Earle</h3>
      <p>Earle's arc from commercial country to political folk to bluegrass to whatever he is now covers most of the dark americana map. <em>Guitar Town</em>, <em>Train a Comin'</em>, <em>El Corazón</em> — a catalog of consistent dark brilliance.</p>
    </div>
    <div class="card">
      <div class="tag">Dark Country</div>
      <h3>Hank Williams III</h3>
      <p>Grandson of the legend, Hank III built a career on refusing everything Nashville offered. His records swing between classic honky-tonk darkness and extreme noise while remaining rooted in the Williams family legacy of honest misery.</p>
    </div>
    <div class="card">
      <div class="tag">Southern Gothic</div>
      <h3>16 Horsepower</h3>
      <p>David Eugene Edwards built one of dark americana's most spiritually intense catalogs — music soaked in biblical dread, Appalachian imagery, and the terror of genuine religious feeling. "Parttime Man," "Black Soul Choir" — essential.</p>
    </div>
    <div class="card">
      <div class="tag">Alt-Country Roots</div>
      <h3>Uncle Tupelo</h3>
      <p>Jeff Tweedy and Jay Farrar's band is where modern dark americana and alternative rock most productively collided. <em>No Depression</em> named a genre; <em>March 16-20, 1992</em> showed what dark country could be.</p>
    </div>
    <div class="card">
      <div class="tag">Blues Foundation</div>
      <h3>Robert Johnson</h3>
      <p>The mythic crossroads figure of the delta blues is dark americana's deepest root. Johnson's 29 recorded songs contain everything the genre would later say — about desire, darkness, the devil, the road, and what waits at the end of it.</p>
    </div>
    <div class="card">
      <div class="tag">Folk Dark</div>
      <h3>The Handsome Family</h3>
      <p>Brett and Rennie Sparks make murder-tinged folk that tips into genuine unease — dark humor and genuine darkness in equal measure. "Far From Any Road" brought them to mainstream attention. Their full catalog rewards the dark-minded listener.</p>
    </div>
    <div class="card">
      <div class="tag">Modern Voice</div>
      <h3>Neko Case</h3>
      <p>Case's solo catalog — particularly <em>Fox Confessor Brings the Flood</em> and <em>Middle Cyclone</em> — places her squarely in dark americana territory: voice of unsettling clarity, lyrics that find violence and wonder in the natural world.</p>
    </div>
    <div class="card">
      <div class="tag">Louisiana Dark</div>
      <h3>Lucinda Williams</h3>
      <p>Williams' rootsy sound comes directly from the Louisiana and Texas landscapes — her music has the smell of bayou and honky-tonk, the weight of hard experience. <em>Car Wheels on a Gravel Road</em> is the genre's southern chapter.</p>
    </div>
    <div class="card">
      <div class="tag">Canadian Dark</div>
      <h3>Timber Timbre</h3>
      <p>Taylor Kirk's project proves dark americana's reach beyond the American south — Canadian forests and winter light informing music that sounds like it was made in a haunted house. Gothic atmosphere at its finest.</p>
    </div>
  </div>
</div>"""
    schema = [{"@context":"https://schema.org","@type":"ItemList","name":"Dark Americana Artists","description":"The essential dark americana artists — the voices that defined and continue to define the genre.","url":f"{BASE_URL}/artists.html"}]
    return page("Dark Americana Artists — The Essential Voices","The key dark americana artists: Townes Van Zandt, Gillian Welch, Nick Cave, Dark Country Boy, and the voices that defined the genre.",f"{BASE_URL}/artists.html",body,schema)

# ── songs.html ────────────────────────────────────────────────────────────────
def build_songs_index():
    # Build a table of all tracks
    rows = ""
    for t in tracks:
        slug = t['trackSlug']
        name = t['trackName']
        album = t['albumName']
        rows += f'<tr><td><a href="/songs/{slug}.html">{name}</a></td><td style="color:#888;font-size:.85em">{album}</td></tr>\n'

    body = f"""
<div class="hero">
  <div class="tag">Song Catalog</div>
  <h1>Essential Dark Americana Songs</h1>
  <p>The Dark Country Boy catalog — 1,481 songs of dark americana, dark country, and dark blues</p>
  {stream_buttons()}
</div>
<div class="section container">
  <p>The full Dark Country Boy catalog represents one of the most comprehensive bodies of work in dark americana. Browse all 1,481 songs below, each with streaming links to Spotify, Apple Music, YouTube Music, and Amazon Music.</p>
  <div style="overflow-x:auto;margin-top:20px">
  <table style="width:100%;border-collapse:collapse">
  <thead><tr style="border-bottom:2px solid #c9a84c">
    <th style="text-align:left;padding:8px 12px;color:#c9a84c">Song</th>
    <th style="text-align:left;padding:8px 12px;color:#c9a84c">Album</th>
  </tr></thead>
  <tbody style="font-size:.9em">
  {rows}
  </tbody>
  </table>
  </div>
</div>"""
    schema = [{"@context":"https://schema.org","@type":"ItemList","name":"Dark Americana Songs","description":"Complete dark americana song catalog — Dark Country Boy's 1,481 songs of dark americana, dark country, and dark blues.","url":f"{BASE_URL}/songs.html","numberOfItems":len(tracks)}]
    return page(f"Dark Americana Songs — {len(tracks)} Tracks | Dark Country Boy","Browse all 1,481 dark americana songs by Dark Country Boy — stream on Spotify, Apple Music, YouTube Music and Amazon Music.",f"{BASE_URL}/songs.html",body,schema)

# ── individual song pages ─────────────────────────────────────────────────────
DARK_AMERICANA_ADJECTIVES = [
    "steeped in dark americana grit",
    "a dark americana journey through American roots music",
    "where folk tradition meets blues darkness",
    "outlaw country at its most uncompromising",
    "a dark country meditation on the American experience",
    "gothic americana with raw emotional depth",
    "rooted in the blues tradition and outlaw country spirit",
    "stark, honest dark americana storytelling",
    "a song that lives where folk, blues and country collide",
    "pure American roots darkness",
]

def song_desc(name, album):
    import hashlib
    h = int(hashlib.md5(name.encode()).hexdigest(), 16)
    adj = DARK_AMERICANA_ADJECTIVES[h % len(DARK_AMERICANA_ADJECTIVES)]
    return f"{name} by Dark Country Boy — {adj}. From the album {album}. Stream on all major platforms."

def build_song_page(t):
    slug = t['trackSlug']
    name = t['trackName']
    album = t['albumName']
    artwork = t.get('artworkUrl','')
    apple_url = t.get('appleMusicUrl','') or APPLE_ARTIST
    sp_url = t.get('spotifySearchUrl','') or SPOTIFY_ARTIST
    yt_url = t.get('youtubeMusicSearchUrl','') or YTMUSIC_ARTIST
    az_url = t.get('amazonMusicSearchUrl','') or AMAZON_ARTIST
    release = t.get('releaseDate','')

    desc = song_desc(name, album)
    canonical = f"{BASE_URL}/songs/{slug}.html"

    art_html = f'<img src="{artwork}" alt="{name} artwork" class="artwork" loading="lazy"/>' if artwork else ''

    body = f"""
<div class="hero" style="padding:40px 20px">
  {art_html}
  <h1 style="font-size:1.8em;margin-top:12px">{name}</h1>
  <p style="color:#888;margin-bottom:4px">Dark Country Boy</p>
  <p style="color:#666;font-size:.9em">Album: {album}{(' · ' + release[:4]) if release else ''}</p>
</div>
<div class="section container" style="max-width:700px">
  <div class="stream-box">
    <h3>Stream "{name}"</h3>
    <a class="btn btn-sp" href="{sp_url}" target="_blank" rel="noopener">Spotify</a>
    <a class="btn btn-am" href="{apple_url}" target="_blank" rel="noopener">Apple Music</a>
    <a class="btn btn-yt" href="{yt_url}" target="_blank" rel="noopener">YouTube Music</a>
    <a class="btn btn-az" href="{az_url}" target="_blank" rel="noopener">Amazon Music</a>
  </div>
  <p>{desc}</p>
  <p>Dark Country Boy is one of dark americana's most prolific independent artists — 70 albums, 1,481 songs that span dark country, dark blues, gothic country, and americana. No commercial compromise, no major label: just the music, made honestly.</p>
  <p><a href="/artists.html">About Dark Country Boy →</a></p>
  <p><a href="/songs.html">← All Songs</a></p>
</div>"""

    schema = [
        {"@context":"https://schema.org","@type":"MusicRecording","name":name,"url":canonical,"datePublished":release,"byArtist":{"@type":"MusicGroup","name":"Dark Country Boy","url":"https://darkcountryboy.net","sameAs":[SPOTIFY_ARTIST,APPLE_ARTIST]},"inAlbum":{"@type":"MusicAlbum","name":album},"sameAs":[apple_url,sp_url]},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE_URL},{"@type":"ListItem","position":2,"name":"Songs","item":f"{BASE_URL}/songs.html"},{"@type":"ListItem","position":3,"name":name,"item":canonical}]}
    ]
    return page(f"{name} — Dark Country Boy | Dark Americana",desc,canonical,body,schema)

# ── sitemap.xml ───────────────────────────────────────────────────────────────
def build_sitemap():
    urls = [BASE_URL+"/", BASE_URL+"/what-is-dark-americana.html", BASE_URL+"/history.html", BASE_URL+"/artists.html", BASE_URL+"/songs.html"]
    for t in tracks:
        urls.append(f"{BASE_URL}/songs/{t['trackSlug']}.html")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>")
    lines.append("</urlset>")
    return "\n".join(lines)

# ── MAIN ──────────────────────────────────────────────────────────────────────
print("Building main pages...")
os.makedirs(f"{OUTDIR}/songs", exist_ok=True)

with open(f"{OUTDIR}/index.html","w") as f: f.write(build_index())
with open(f"{OUTDIR}/what-is-dark-americana.html","w") as f: f.write(build_what_is())
with open(f"{OUTDIR}/history.html","w") as f: f.write(build_history())
with open(f"{OUTDIR}/artists.html","w") as f: f.write(build_artists())
with open(f"{OUTDIR}/songs.html","w") as f: f.write(build_songs_index())

with open(f"{OUTDIR}/CNAME","w") as f: f.write("darkamericana.net")
with open(f"{OUTDIR}/robots.txt","w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")
with open(f"{OUTDIR}/sitemap.xml","w") as f: f.write(build_sitemap())

print(f"Building {len(tracks)} song pages...")
for i, t in enumerate(tracks):
    with open(f"{OUTDIR}/songs/{t['trackSlug']}.html","w") as f:
        f.write(build_song_page(t))
    if (i+1) % 200 == 0:
        print(f"  {i+1}/{len(tracks)}")

print(f"Done! Total pages: {5 + len(tracks)}")
