from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import json
from collections import defaultdict

def is_light_color(color_str, threshold=240):
    try:
        numbers = re.findall(r'\d+', color_str)
        if len(numbers) >= 3:
            r, g, b = int(numbers[0]), int(numbers[1]), int(numbers[2])
            return (r >= threshold and g >= threshold and b >= threshold)
    except:
        pass
    return False

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

driver.get(r"https://egypt.blsspainglobal.com/Global/CaptchaPublic/GenerateCaptcha?data=4CDiA9odF2%2b%2bsWCkAU8htqZkgDyUa5SR6waINtJfg1ThGb6rPIIpxNjefP9UkAaSp%2fGsNNuJJi5Zt1nbVACkDRusgqfb418%2bScFkcoa1F0I%3d")


time.sleep(5)

visible_texts = []
target_number = None

try:
    box_labels = driver.find_elements(By.CLASS_NAME, "box-label")
    for box in box_labels:
        text = box.text.strip()
        if text:
            color = box.value_of_css_property("color")
            is_light = is_light_color(color, threshold=240)
            
            if not is_light:
                visible_texts.append(text)
                print(f"{text}")
                
except Exception as e:
    print(f"Error: {e}")

try:
    action_buttons = driver.find_elements(By.CLASS_NAME, "img-action-text")
    for button in action_buttons:
        text = button.text.strip()
        if text and text not in visible_texts:
            visible_texts.append(text)
            print(f"{text}")
except Exception as e:
    print(f"Error: {e}")


js_code = """
function getAllImagesData() {
    const images = document.querySelectorAll('img');
    const results = [];
    
    function getRealZIndex(el) {
        const style = window.getComputedStyle(el);
        let zIndex = style.zIndex;
        
        if (zIndex === 'auto' || zIndex === '') {
            let parent = el.parentElement;
            let depth = 0;
            while (parent && depth < 5) {
                const parentStyle = window.getComputedStyle(parent);
                if (parentStyle.position !== 'static' && parentStyle.zIndex !== 'auto') {
                    zIndex = parentStyle.zIndex;
                    break;
                }
                parent = parent.parentElement;
                depth++;
            }
        }
        
        if (zIndex === 'auto' || zIndex === '') {
            zIndex = '0';
        }
        
        return zIndex;
    }
    
    function getEffectivePosition(el) {
        const rect = el.getBoundingClientRect();
        
        if (rect.x === 0 && rect.y === 0 && rect.width === 0 && rect.height === 0) {
            const style = window.getComputedStyle(el);
            const top = style.top;
            const left = style.left;
            
            const topMatch = top.match(/(-?\d+)px/);
            const leftMatch = left.match(/(-?\d+)px/);
            
            if (topMatch && leftMatch) {
                return {
                    x: parseInt(leftMatch[1]) || 0,
                    y: parseInt(topMatch[1]) || 0,
                    width: parseInt(style.width) || 0,
                    height: parseInt(style.height) || 0
                };
            }
        }
        
        return {
            x: Math.round(rect.x),
            y: Math.round(rect.y),
            width: Math.round(rect.width),
            height: Math.round(rect.height)
        };
    }
    
    images.forEach((img, index) => {
        try {
            const pos = getEffectivePosition(img);
            const style = window.getComputedStyle(img);
            const zIndexComputed = getRealZIndex(img);
            const zNum = parseFloat(zIndexComputed) || 0;
            
            let allText = '';
            let parent = img.parentElement;
            let depth = 0;
            while (parent && depth < 3) {
                allText += parent.innerText + ' ';
                parent = parent.parentElement;
                depth++;
            }
            
            const numbers = allText.match(/\\b\\d{3}\\b/g);
            const uniqueNumbers = numbers ? [...new Set(numbers)] : [];
            
            const isVisible = style.display !== 'none' && 
                             style.visibility !== 'hidden' && 
                             parseFloat(style.opacity || 1) > 0;
            
            results.push({
                index: index + 1,
                src: img.src,
                base64: img.src.startsWith('data:image') ? img.src : null,
                class: img.className || '',
                id: img.id || '',
                
                z_index: zNum,
                
                position: {
                    x: pos.x,
                    y: pos.y,
                    width: pos.width,
                    height: pos.height
                },
                
                is_visible: isVisible,
                has_real_position: pos.x > 0 || pos.y > 0,
                has_size: pos.width > 0 && pos.height > 0,
                
                css: {
                    display: style.display,
                    visibility: style.visibility,
                    opacity: parseFloat(style.opacity) || 1,
                    position: style.position
                },
                
                numbers: uniqueNumbers
            });
            
        } catch (e) {
            results.push({
                index: index + 1,
                error: e.toString()
            });
        }
    });
    
    return results;
}
return getAllImagesData();
"""

all_images_data = driver.execute_script(js_code)
all_images_base64 = []
for img in all_images_data:
    if img.get('src') and img['src'].startswith('data:image'):
        all_images_base64.append({
            'index': img['index'],
            'base64': img['src'],
        })

with open('allimages.json', 'w', encoding='utf-8') as f:
    json.dump(all_images_base64, f, ensure_ascii=False, indent=2)




locations = defaultdict(list)
for img in all_images_data:
    if img.get('position') and (img['position']['x'] > 0 or img['position']['y'] > 0):
        x = round(img['position']['x'] / 10) * 10
        y = round(img['position']['y'] / 10) * 10
        key = f"({x},{y})"
        locations[key].append(img)

grid_images = []
for loc, imgs in locations.items():
    if imgs:
        best_img = max(imgs, key=lambda x: x.get('z_index', 0))
        grid_images.append(best_img)

valid_grid = [img for img in grid_images if img.get('position') and 
              (img['position']['x'] > 0 or img['position']['y'] > 0)]
valid_grid.sort(key=lambda x: (x['position']['y'], x['position']['x']))

visible_images = valid_grid[:9] if len(valid_grid) >= 9 else valid_grid
visible_images_base64 = []
for img in visible_images:
    if img.get('src') and img['src'].startswith('data:image'):
        visible_images_base64.append({
            'index': img['index'],
            'base64': img['src'],     
        })

with open('visible_images_only.json', 'w', encoding='utf-8') as f:
    json.dump(visible_images_base64, f, ensure_ascii=False, indent=2)

texts_data = {
    'visible_texts': visible_texts,
}

with open('visible_texts.json', 'w', encoding='utf-8') as f:
    json.dump(texts_data, f, ensure_ascii=False, indent=2)

time.sleep(500)
driver.quit()
