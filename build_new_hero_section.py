import os
import base64
import re

hero_dir = r"C:\Users\anand singh\.gemini\antigravity\scratch\renaissanz-nextgen-award\assets\hero"
index_path = r"C:\Users\anand singh\.gemini\antigravity\scratch\renaissanz-nextgen-award\index.html"
js_path = r"C:\Users\anand singh\.gemini\antigravity\scratch\renaissanz-nextgen-award\assets\js\main.js"

slides_config = [
    {
        'key': 'hero-02.jpg',
        'rel': './assets/hero/hero-02.jpg',
        'type': 'poster',
        'caption': 'UPCOMING • Edition 6 • with Vaani Kapoor • 14 Dec 2026',
        'ribbon': 'UPCOMING EDITION',
        'alt': 'Renaissanz NextGen Leader Award Edition 6 official poster featuring celebrity guest Vaani Kapoor'
    },
    {
        'key': 'hero-01.jpg',
        'rel': './assets/hero/hero-01.jpg',
        'type': 'photo',
        'caption': 'Edition 5 • Memories • with Tejasswi Prakash',
        'ribbon': 'NOMINATIONS OPEN',
        'alt': 'Renaissanz NextGen Leader Award Edition 5 trophy presentation with celebrity guest Tejasswi Prakash'
    },
    {
        'key': 'hero-03.jpg',
        'rel': './assets/hero/hero-03.jpg',
        'type': 'photo',
        'caption': 'Edition 5 • Memories • with Ekta Kapoor',
        'ribbon': 'EDITION 5',
        'alt': 'Renaissanz NextGen Leader Award Edition 5 trophy presentation moment with Ekta Kapoor'
    },
    {
        'key': 'hero-05.jpg',
        'rel': './assets/hero/hero-05.jpg',
        'type': 'photo',
        'caption': 'Edition 4 • Memories • with Shehnaaz Gill',
        'ribbon': 'EDITION 4',
        'alt': 'Renaissanz NextGen Leader Award Edition 4 award presentation moment with Shehnaaz Gill'
    },
    {
        'key': 'hero-06.jpg',
        'rel': './assets/hero/hero-06.jpg',
        'type': 'photo',
        'caption': 'Honouring Achievers • Shamita Shetty',
        'ribbon': 'PAST HIGHLIGHTS',
        'alt': 'Certificate presentation moment on stage with celebrity guest Shamita Shetty'
    },
    {
        'key': 'hero-08.jpg',
        'rel': './assets/hero/hero-08.jpg',
        'type': 'photo',
        'caption': 'SammRenaissance Fashion Show • Runway',
        'ribbon': 'FASHION RUNWAY',
        'alt': 'SammRenaissance fashion runway moment at past award edition'
    }
]

# Read base64 strings
for s in slides_config:
    p = os.path.join(hero_dir, s['key'])
    with open(p, 'rb') as fp:
        s['b64'] = "data:image/jpeg;base64," + base64.b64encode(fp.read()).decode('utf-8')

# Construct Native HTML for all 6 slides in track
native_track_html = []
for idx, s in enumerate(slides_config):
    active_cls = "active" if idx == 0 else ""
    fit_cls = "slide-img fit-contain" if s['type'] == 'poster' else "slide-img fit-cover"
    ribbon_html = f'<div class="slide-ribbon">{s["ribbon"]}</div>' if s.get('ribbon') else ''
    
    slide_html = f"""              <div class="hero-slide {active_cls}" role="group" aria-roledescription="slide" aria-label="Slide {idx + 1} of {len(slides_config)}">
                {ribbon_html}
                <img src="{s['b64']}" data-src="{s['rel']}" alt="{s['alt']}" class="{fit_cls}" width="800" height="1000" loading="{'eager' if idx <= 1 else 'lazy'}">
              </div>"""
    native_track_html.append(slide_html)

full_native_track = "\n".join(native_track_html)

# Build JavaScript array string for HERO_SLIDES_DATA
js_slides_list = []
for s in slides_config:
    js_slides_list.append(f"""  {{
    image: '{s["b64"]}',
    rel: '{s["rel"]}',
    type: '{s["type"]}',
    caption: '{s["caption"]}',
    ribbon: '{s["ribbon"]}',
    alt: '{s["alt"]}'
  }}""")

js_array_str = "// Hero Slider Data Array (Embedded Data URIs - Zero 404 Guaranteed)\nconst HERO_SLIDES_DATA = [\n" + ",\n".join(js_slides_list) + "\n];"

# Read index.html
with open(index_path, 'r', encoding='utf-8') as fp:
    html = fp.read()

# Replace Background Blur image
html = re.sub(
    r'id="hero-bg-blur"[^>]*style="[^"]*"',
    f'id="hero-bg-blur" class="hero-bg-blur" style="background-image: url(\'{slides_config[0]["b64"]}\');"',
    html
)

# Replace native hero slider track inner HTML
track_regex = r'(<div id="hero-slider-track" class="hero-slider-track">)(.*?)(</div>\s*</div>\s*<!-- Controls)'
match = re.search(track_regex, html, re.DOTALL)
if match:
    new_track_block = match.group(1) + "\n" + full_native_track + "\n            " + match.group(3)
    html = html[:match.start()] + new_track_block + html[match.end():]

# Replace HERO_SLIDES_DATA in index.html
start_tag = "// Hero Slider Data Array"
end_tag = "];"
start_pos = html.find(start_tag)
if start_pos != -1:
    end_pos = html.find(end_tag, start_pos) + len(end_tag)
    html = html[:start_pos] + js_array_str + html[end_pos:]

# Replace initHeroSlider rendering logic in index.html to use native DOM elements smoothly
js_loop_code = """    HERO_SLIDES_DATA.forEach((slide, idx) => {
      const slideEl = document.createElement('div');
      slideEl.className = `hero-slide ${idx === 0 ? 'active' : ''}`;
      slideEl.setAttribute('role', 'group');
      slideEl.setAttribute('aria-roledescription', 'slide');
      slideEl.setAttribute('aria-label', `Slide ${idx + 1} of ${totalSlides}`);

      const isEager = idx <= 1;
      const imgClass = slide.type === 'poster' ? 'slide-img fit-contain' : 'slide-img fit-cover';

      if (slide.ribbon) {
        const ribbonEl = document.createElement('div');
        ribbonEl.className = 'slide-ribbon';
        ribbonEl.textContent = slide.ribbon;
        slideEl.appendChild(ribbonEl);
      }

      const imgEl = document.createElement('img');
      imgEl.src = slide.image;
      imgEl.alt = slide.alt;
      imgEl.className = imgClass;
      imgEl.width = 800;
      imgEl.height = 1000;
      if (isEager) {
        imgEl.loading = 'eager';
      } else {
        imgEl.loading = 'lazy';
      }

      slideEl.appendChild(imgEl);
      sliderTrack.appendChild(slideEl);"""

start_loop = "HERO_SLIDES_DATA.forEach((slide, idx) => {"
end_loop = "sliderTrack.appendChild(slideEl);"
start_l_pos = html.find(start_loop)
if start_l_pos != -1:
    end_l_pos = html.find(end_loop, start_l_pos) + len(end_loop)
    html = html[:start_l_pos] + js_loop_code + html[end_l_pos:]

with open(index_path, 'w', encoding='utf-8') as fp:
    fp.write(html)
print("Updated index.html with native embedded slides successfully!")

# Update assets/js/main.js
with open(js_path, 'r', encoding='utf-8') as fp:
    js_content = fp.read()

start_pos = js_content.find(start_tag)
if start_pos != -1:
    end_pos = js_content.find(end_tag, start_pos) + len(end_tag)
    js_content = js_content[:start_pos] + js_array_str + js_content[end_pos:]

start_l_pos = js_content.find(start_loop)
if start_l_pos != -1:
    end_l_pos = js_content.find(end_loop, start_l_pos) + len(end_loop)
    js_content = js_content[:start_l_pos] + js_loop_code + js_content[end_l_pos:]

with open(js_path, 'w', encoding='utf-8') as fp:
    fp.write(js_content)
print("Updated assets/js/main.js successfully!")
