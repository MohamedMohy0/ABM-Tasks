import asyncio
from patchright.async_api import async_playwright

# https://drive.google.com/file/d/1dUI9hZCl81RHnTbj3u2RtSd1kKUVzy_Z/view?usp=sharing
# Drive Video Link

async def bypass_with_token(token):

    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            channel="chrome",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800}
        )
        
        page = await context.new_page()
        sitekey = "0x4AAAAAAB4f8DxT2p1q1sgQ"
        await page.add_init_script(f"""
        // Block Turnstile entirely
        Object.defineProperty(window, 'turnstile', {{
            get: function() {{
                return {{
                    render: function(container, params) {{
                        console.log('Turnstile blocked');
                        
                        // Create token input
                        let input = document.querySelector('[name="cf-turnstile-response"]');
                        if (!input) {{
                            input = document.createElement('input');
                            input.type = 'hidden';
                            input.name = 'cf-turnstile-response';
                            document.body.appendChild(input);
                        }}
                        
                        return 'blocked';
                    }},
                    execute: function() {{ return Promise.resolve(); }},
                    reset: function() {{}}
                }};
            }},
            configurable: true
        }});
        
        // Block network requests
        const originalFetch = window.fetch;
        window.fetch = function(...args) {{
            if (args[0] && args[0].includes('challenges.cloudflare.com')) {{
                return Promise.reject();
            }}
            return originalFetch.apply(this, args);
        }};
        
        // Block scripts
        new MutationObserver(function(mutations) {{
            mutations.forEach(function(mutation) {{
                mutation.addedNodes.forEach(function(node) {{
                    if (node.nodeName === 'SCRIPT' && node.src && node.src.includes('turnstile')) {{
                        node.remove();
                    }}
                }});
            }});
        }}).observe(document.documentElement, {{ childList: true, subtree: true }});
        """)
        await page.goto("https://cd.captchaaiplus.com/turnstile.html", wait_until="domcontentloaded")
        await asyncio.sleep(2)
        has_iframe = await page.evaluate("""
            () => !!document.querySelector('iframe[src*="challenges"]')
        """)
        if not has_iframe:
            print("Captcha successfully blocked")        
        await page.evaluate("""
            (token) => {
                // Find or create token input
                let input = document.querySelector('[name="cf-turnstile-response"]');
                
                if (!input) {
                    input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'cf-turnstile-response';
                    document.body.appendChild(input);
                }
                
                input.value = token;
                console.log('Token injected');
            }
        """, token)
        token_value = await page.evaluate("document.querySelector('[name=\"cf-turnstile-response\"]')?.value")
        await asyncio.sleep(2)        
        submit_clicked = await page.evaluate("""
            () => {
                const submitBtn = document.querySelector('input[type="submit"], button[type="submit"]');
                if (submitBtn) {
                    submitBtn.click();
                    return true;
                }
                return false;
            }
        """)


        await asyncio.sleep(10)
        await browser.close()
        return True

async def main():
        token = input("\nToken: ").strip()
        if token:
            await bypass_with_token(token)

asyncio.run(main())