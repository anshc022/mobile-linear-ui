const puppeteer = require('puppeteer');

(async () => {
  try {
    const browser = await puppeteer.launch({
      headless: "new",
      args: [
        '--no-sandbox', 
        '--disable-setuid-sandbox', 
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--no-zygote',
        '--single-process'
      ]
    });
    const page = await browser.newPage();
    page.setDefaultNavigationTimeout(30000);

    // 1. Search Google for "Mandi Bhav WhatsApp Group Link"
    const query = "Mandi Bhav Indian Farmer WhatsApp Group Link 2026";
    console.log(`🔍 Searching Google for: ${query}`);
    
    await page.goto(`https://www.google.com/search?q=${encodeURIComponent(query)}`, { waitUntil: 'networkidle2' });
    
    // 2. Extract top result URLs (excluding Google own links)
    const searchResults = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('a'))
            .map(a => a.href)
            .filter(href => href && href.startsWith('http') && !href.includes('google.com') && !href.includes('google.co'));
    });
    
    console.log(`Found ${searchResults.length} potential sources.`);
    
    const waLinks = new Set();
    
    // 3. Visit top 2 results deeply
    const targets = searchResults.slice(0, 2); 
    
    for (const url of targets) {
        console.log(`\n📄 Scraping: ${url}`);
        try {
            const tempPage = await browser.newPage();
            await tempPage.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
            
            await tempPage.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
            
            // Look for chat.whatsapp.com links
            const links = await tempPage.evaluate(() => {
                return Array.from(document.querySelectorAll('a'))
                    .map(a => a.href)
                    .filter(href => href && href.includes('chat.whatsapp.com'));
            });
            
            console.log(`   found ${links.length} WhatsApp links.`);
            links.forEach(l => waLinks.add(l));
            
            await tempPage.close();
        } catch (e) {
            console.log(`   ❌ Failed: ${e.message}`);
        }
    }
    
    console.log('\n✅ --- HARVEST COMPLETE ---');
    const finalLinks = Array.from(waLinks);
    console.log(JSON.stringify(finalLinks, null, 2));
    
    await browser.close();
  } catch (err) {
    console.error('🔥 Critical Error:', err);
    process.exit(1);
  }
})();
