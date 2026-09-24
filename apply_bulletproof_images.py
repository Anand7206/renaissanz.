import os
import base64

hero_dir = r"C:\Users\anand singh\.gemini\antigravity\scratch\renaissanz-nextgen-award\assets\hero"
index_path = r"C:\Users\anand singh\.gemini\antigravity\scratch\renaissanz-nextgen-award\index.html"
js_path = r"C:\Users\anand singh\.gemini\antigravity\scratch\renaissanz-nextgen-award\assets\js\main.js"

files = {
    'hero-01': 'hero-01.webp',
    'hero-02': 'hero-02.webp',
    'hero-03': 'hero-03.webp',
    'hero-05': 'hero-05.webp',
    'hero-06': 'hero-06.webp',
    'hero-08': 'hero-08.webp'
}

b64 = {}
for k, v in files.items():
    p = os.path.join(hero_dir, v)
    with open(p, 'rb') as fp:
        b64[k] = "data:image/webp;base64," + base64.b64encode(fp.read()).decode('utf-8')

hero_slides_data_str = f"""// Hero Slider Data Array (6 slides total with 100% fail-safe fallback)
const HERO_SLIDES_DATA = [
  {{
    image: './assets/hero/hero-01.jpg',
    fallback: '{b64["hero-01"]}',
    type: 'photo',
    caption: 'Edition 5 • Memories • with Tejasswi Prakash',
    ribbon: 'NOMINATIONS OPEN',
    alt: 'Renaissanz NextGen Leader Award Edition 5 trophy presentation with celebrity guest Tejasswi Prakash'
  }},
  {{
    image: './assets/hero/hero-02.jpg',
    fallback: '{b64["hero-02"]}',
    type: 'poster',
    caption: 'UPCOMING • Edition 6 • with Vaani Kapoor • 14 Dec 2026',
    alt: 'Renaissanz NextGen Leader Award Edition 6 official poster featuring celebrity guest Vaani Kapoor'
  }},
  {{
    image: './assets/hero/hero-03.jpg',
    fallback: '{b64["hero-03"]}',
    type: 'photo',
    caption: 'Edition 5 • Memories • with Ekta Kapoor',
    alt: 'Renaissanz NextGen Leader Award Edition 5 trophy presentation moment with Ekta Kapoor'
  }},
  {{
    image: './assets/hero/hero-05.jpg',
    fallback: '{b64["hero-05"]}',
    type: 'photo',
    caption: 'Edition 4 • Memories • with Shehnaaz Gill',
    alt: 'Renaissanz NextGen Leader Award Edition 4 award presentation moment with Shehnaaz Gill'
  }},
  {{
    image: './assets/hero/hero-06.jpg',
    fallback: '{b64["hero-06"]}',
    type: 'photo',
    caption: 'Honouring Achievers • Shamita Shetty',
    alt: 'Certificate presentation moment on stage with celebrity guest Shamita Shetty'
  }},
  {{
    image: './assets/hero/hero-08.jpg',
    fallback: '{b64["hero-08"]}',
    type: 'photo',
    caption: 'SammRenaissance Fashion Show • Runway',
    alt: 'SammRenaissance fashion runway moment at past award edition'
  }}
];"""

# Read index.html
with open(index_path, 'r', encoding='utf-8') as fp:
    html = fp.read()

# Update background blur fallback
html = html.replace(
    "style=\"background-image: url('./assets/hero/hero-01.jpg');\"",
    f"style=\"background-image: url('./assets/hero/hero-01.jpg'), url('{b64['hero-01']}');\""
)

# Update native initial slides in HTML
native_slides_old = """              <div class="hero-slide active" role="group" aria-roledescription="slide" aria-label="Slide 1 of 6">
                <div class="slide-ribbon">NOMINATIONS OPEN</div>
                <img src="./assets/hero/hero-01.jpg" onerror="if(this.src.indexOf('.jpg')!==-1)this.src=this.src.replace('.jpg','.png');" alt="Renaissanz NextGen Leader Award Edition 5 trophy presentation with celebrity guest Tejasswi Prakash" class="slide-img fit-cover" width="1000" height="1250" loading="eager" fetchpriority="high">
              </div>
              <div class="hero-slide" role="group" aria-roledescription="slide" aria-label="Slide 2 of 6">
                <img src="./assets/hero/hero-02.jpg" onerror="if(this.src.indexOf('.jpg')!==-1)this.src=this.src.replace('.jpg','.png');" alt="Renaissanz NextGen Leader Award Edition 6 official poster featuring celebrity guest Vaani Kapoor" class="slide-img fit-contain" width="1000" height="1250" loading="eager" fetchpriority="high">
              </div>"""

native_slides_new = f"""              <div class="hero-slide active" role="group" aria-roledescription="slide" aria-label="Slide 1 of 6">
                <div class="slide-ribbon">NOMINATIONS OPEN</div>
                <img src="./assets/hero/hero-01.jpg" onerror="if(!this.dataset.fb){{this.dataset.fb='1';this.src='{b64["hero-01"]}';}}" alt="Renaissanz NextGen Leader Award Edition 5 trophy presentation with celebrity guest Tejasswi Prakash" class="slide-img fit-cover" width="1000" height="1250" loading="eager" fetchpriority="high">
              </div>
              <div class="hero-slide" role="group" aria-roledescription="slide" aria-label="Slide 2 of 6">
                <img src="./assets/hero/hero-02.jpg" onerror="if(!this.dataset.fb){{this.dataset.fb='1';this.src='{b64["hero-02"]}';}}" alt="Renaissanz NextGen Leader Award Edition 6 official poster featuring celebrity guest Vaani Kapoor" class="slide-img fit-contain" width="1000" height="1250" loading="eager" fetchpriority="high">
              </div>"""

html = html.replace(native_slides_old, native_slides_new)

# Update HERO_SLIDES_DATA block in index.html
start_tag = "// Hero Slider Data Array (6 slides total)"
end_tag = "];"
start_pos = html.find(start_tag)
if start_pos != -1:
    end_pos = html.find(end_tag, start_pos) + len(end_tag)
    html = html[:start_pos] + hero_slides_data_str + html[end_pos:]

# Update slide rendering img tag in index.html
old_img_render = """      <img src="${slide.image}" 
           onerror="if(this.src.indexOf('.jpg')!==-1){this.src=this.src.replace('.jpg','.png');}else if(this.src.indexOf('.png')!==-1){this.src=this.src.replace('.png','.webp');}"
           alt="${slide.alt}" 
           class="${imgClass}" 
           width="1000" height="1250"
           ${isEager ? 'loading="eager" fetchpriority="high"' : 'loading="lazy" decoding="async"'}>"""

new_img_render = """      <img src="${slide.image}" 
           onerror="if(!this.dataset.fb){this.dataset.fb='1';this.src=slide.fallback;}"
           alt="${slide.alt}" 
           class="${imgClass}" 
           width="1000" height="1250"
           ${isEager ? 'loading="eager" fetchpriority="high"' : 'loading="lazy" decoding="async"'}>"""

html = html.replace(old_img_render, new_img_render)

with open(index_path, 'w', encoding='utf-8') as fp:
    fp.write(html)
print("Updated index.html successfully!")

# Read main.js
with open(js_path, 'r', encoding='utf-8') as fp:
    js_content = fp.read()

start_pos = js_content.find(start_tag)
if start_pos != -1:
    end_pos = js_content.find(end_tag, start_pos) + len(end_tag)
    js_content = js_content[:start_pos] + hero_slides_data_str + js_content[end_pos:]

js_content = js_content.replace(old_img_render, new_img_render)

with open(js_path, 'w', encoding='utf-8') as fp:
    fp.write(js_content)
print("Updated assets/js/main.js successfully!")
