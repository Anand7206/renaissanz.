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

hero_slides_data_str = f"""// Hero Slider Data Array (6 slides total with closure-safe fallback)
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

# Native slides in index.html with global HERO_SLIDES_DATA indexing
native_slides_new = f"""              <div class="hero-slide active" role="group" aria-roledescription="slide" aria-label="Slide 1 of 6">
                <div class="slide-ribbon">NOMINATIONS OPEN</div>
                <img src="./assets/hero/hero-01.jpg" onerror="if(!this.dataset.fb){{this.dataset.fb='1';this.src=HERO_SLIDES_DATA[0].fallback;}}" alt="Renaissanz NextGen Leader Award Edition 5 trophy presentation with celebrity guest Tejasswi Prakash" class="slide-img fit-cover" width="1000" height="1250" loading="eager" fetchpriority="high">
              </div>
              <div class="hero-slide" role="group" aria-roledescription="slide" aria-label="Slide 2 of 6">
                <img src="./assets/hero/hero-02.jpg" onerror="if(!this.dataset.fb){{this.dataset.fb='1';this.src=HERO_SLIDES_DATA[1].fallback;}}" alt="Renaissanz NextGen Leader Award Edition 6 official poster featuring celebrity guest Vaani Kapoor" class="slide-img fit-contain" width="1000" height="1250" loading="eager" fetchpriority="high">
              </div>"""

# JS slide rendering code using DOM element and closure-safe onerror
js_render_code = """    HERO_SLIDES_DATA.forEach((slide, idx) => {
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
      imgEl.width = 1000;
      imgEl.height = 1250;
      if (isEager) {
        imgEl.loading = 'eager';
        imgEl.setAttribute('fetchpriority', 'high');
      } else {
        imgEl.loading = 'lazy';
        imgEl.setAttribute('decoding', 'async');
      }

      imgEl.onerror = () => {
        if (!imgEl.dataset.fb && slide.fallback) {
          imgEl.dataset.fb = '1';
          imgEl.src = slide.fallback;
        }
      };

      slideEl.appendChild(imgEl);
      sliderTrack.appendChild(slideEl);"""

# Update index.html
with open(index_path, 'r', encoding='utf-8') as fp:
    html = fp.read()

# Update HERO_SLIDES_DATA block
start_tag = "// Hero Slider Data Array"
end_tag = "];"
start_pos = html.find(start_tag)
if start_pos != -1:
    end_pos = html.find(end_tag, start_pos) + len(end_tag)
    html = html[:start_pos] + hero_slides_data_str + html[end_pos:]

# Update native slides HTML
start_native = '<div class="hero-slide active"'
end_native = '</div>\n            </div>'
start_n_pos = html.find(start_native)
if start_n_pos != -1:
    end_n_pos = html.find(end_native, start_n_pos)
    html = html[:start_n_pos] + native_slides_new + html[end_n_pos:]

# Update JS loop in index.html
start_loop = "HERO_SLIDES_DATA.forEach((slide, idx) => {"
end_loop = "sliderTrack.appendChild(slideEl);"
start_l_pos = html.find(start_loop)
if start_l_pos != -1:
    end_l_pos = html.find(end_loop, start_l_pos) + len(end_loop)
    html = html[:start_l_pos] + js_render_code + html[end_l_pos:]

with open(index_path, 'w', encoding='utf-8') as fp:
    fp.write(html)
print("index.html updated successfully!")

# Update assets/js/main.js
with open(js_path, 'r', encoding='utf-8') as fp:
    js_content = fp.read()

start_pos = js_content.find(start_tag)
if start_pos != -1:
    end_pos = js_content.find(end_tag, start_pos) + len(end_tag)
    js_content = js_content[:start_pos] + hero_slides_data_str + js_content[end_pos:]

start_l_pos = js_content.find(start_loop)
if start_l_pos != -1:
    end_l_pos = js_content.find(end_loop, start_l_pos) + len(end_loop)
    js_content = js_content[:start_l_pos] + js_render_code + js_content[end_l_pos:]

with open(js_path, 'w', encoding='utf-8') as fp:
    fp.write(js_content)
print("assets/js/main.js updated successfully!")
