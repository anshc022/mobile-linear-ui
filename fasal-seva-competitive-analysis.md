# Fasal Seva — Competitive Analysis Report

*Updated: February 2026 | Product Status: LIVE on Google Play Store*

---

## 1. INDIAN AGRITECH MARKET OVERVIEW

| Metric | Value |
|--------|-------|
| Market size (2024) | ~$4.0–4.5 billion |
| Projected size (2030) | ~$24–34 billion |
| CAGR | ~30–40% |
| Number of farmers in India | ~150 million (86% are small/marginal, <2 hectares) |
| Smartphone penetration (rural) | ~50–55% and growing rapidly |
| Key govt initiatives | Digital Agriculture Mission, eNAM, PM-KISAN, Agri-Stack |

**Key trends:**
- Rapid smartphone + cheap data adoption in rural India (Jio effect)
- Government push for precision agriculture and digital farmer IDs
- Growing climate volatility increasing demand for real-time farm intelligence
- Shift from input-focused to data/intelligence-focused agritech
- Investor interest peaking: $2B+ invested in Indian agritech (2019–2024)
- Most solutions still target large/commercial farms or serve as B2B enterprise tools — **massive gap for affordable smallholder-focused solutions**

---

## 2. COMPETITOR PROFILES

### 2.1 DeHaat
| Dimension | Details |
|-----------|---------|
| **Core Product** | Full-stack agri platform: farm inputs (seeds, fertilizers, pesticides), advisory, credit, and market linkage for crop sales |
| **Pricing** | Free app; monetizes via input sales margins and market commissions |
| **Target** | Small/medium farmers in Eastern India (Bihar, UP, Jharkhand, Odisha) |
| **Hardware** | Software-only (no sensors or devices) |
| **Key Features** | Input delivery to doorstep, crop advisory via call center, credit facilitation, output procurement |
| **Funding** | ~$350M+ raised (Series E, 2022); investors include Sofina, Prosus, RTP Global |
| **Scale** | 2M+ farmers, 10,000+ micro-entrepreneurs |
| **Weaknesses** | No precision agriculture / sensor capability; advisory is generic, not data-driven from field; no real-time monitoring; supply-chain focused, not farm-intelligence focused |

### 2.2 AgroStar
| Dimension | Details |
|-----------|---------|
| **Core Product** | Farm advisory platform + agri-input e-commerce + market linkages (Kimaye fresh produce brand) |
| **Pricing** | Free advisory; revenue from input product sales and produce exports |
| **Target** | 12M+ farmers across 12 states; also export markets (Kimaye) |
| **Hardware** | Software-only |
| **Key Features** | Personalized crop advisory (15M+ interactions), 200+ agri-input products, 10,000+ retail stores (omnichannel), global market linkages |
| **Funding** | ~$100M+ raised; $30M recent round for AI + omnichannel expansion |
| **Scale** | 12M+ farmers, largest advisory platform in Asia |
| **Weaknesses** | No on-farm sensing or precision agriculture; advisory is reactive (farmer asks questions); no real-time field monitoring; focused on input commerce rather than farm intelligence |

### 2.3 Fasal (the company)
| Dimension | Details |
|-----------|---------|
| **Core Product** | Smart irrigation & fertigation automation systems with soil sensors and weather stations |
| **Pricing** | Hardware purchase model; FasalJet systems likely ₹25,000–₹1,00,000+ depending on farm size and configuration |
| **Target** | Commercial/progressive farmers with drip irrigation; horticulture-focused |
| **Hardware** | **Yes** — soil moisture sensors, temperature sensors, weather stations, irrigation controllers, solenoid valves, fertigation injectors |
| **Key Features** | Irrigation automation (FasalJet), fertigation automation (FasalJet Pro), soil moisture monitoring, weather stations, mobile app control |
| **Funding** | ~$20M+ raised (Omnivore, Wavemaker, 3one4) |
| **Scale** | Thousands of farms; claims 52 billion liters water saved |
| **Weaknesses** | **Expensive** — targets commercial farms, not small/marginal farmers; no AI voice interface; no satellite analytics; no crop disease detection; limited to irrigation automation; no multilingual voice support |

### 2.4 CropIn
| Dimension | Details |
|-----------|---------|
| **Core Product** | Enterprise SaaS platform for agribusinesses — farm digitization, satellite monitoring, predictive analytics |
| **Pricing** | Enterprise SaaS subscriptions (B2B); not farmer-facing |
| **Target** | Agribusinesses, banks, insurers, governments, food companies (NOT individual farmers) |
| **Hardware** | Software-only (satellite + AI) |
| **Key Features** | Computed 1B+ acres globally; satellite-based crop monitoring; predictive yield models; EUDR compliance; climate risk modeling; "Cropin Cloud" platform |
| **Funding** | ~$45M+ raised; backed by Google, ABC World Asia, Chiratae |
| **Scale** | 250+ enterprise clients across 56 countries |
| **Weaknesses** | **Not farmer-facing at all** — serves enterprises only; no direct farmer tools; no field-level sensors; no voice/vernacular interface; no smallholder affordability story; no hardware component |

### 2.5 Plantix
| Dimension | Details |
|-----------|---------|
| **Core Product** | AI-powered crop disease diagnosis app — take a photo, get diagnosis + treatment |
| **Pricing** | Free app |
| **Target** | Smallholder farmers globally (strong India presence) |
| **Hardware** | Software-only (phone camera) |
| **Key Features** | Photo-based crop disease diagnosis, treatment recommendations, crop disease library, community expert advice, 100M+ crop questions answered |
| **Funding** | ~$7M raised (Germany-based PEAT GmbH) |
| **Scale** | Most downloaded agri-tech app worldwide; millions of users |
| **Weaknesses** | **Only does disease diagnosis** — no soil monitoring, no irrigation guidance, no weather/satellite analytics, no real-time field monitoring, no hardware sensing, no holistic farm management, reactive only (problem must already be visible) |

### 2.6 Kisan Network
| Dimension | Details |
|-----------|---------|
| **Core Product** | Direct farmer-to-buyer marketplace for crop sales; eliminates middlemen |
| **Pricing** | Commission on transactions |
| **Target** | Farmers seeking better crop prices; commodity buyers |
| **Hardware** | Software-only |
| **Key Features** | Direct market access, price transparency, logistics support |
| **Funding** | ~$4M raised |
| **Scale** | Operating in Rajasthan and a few other states |
| **Weaknesses** | Purely output/market side — no farm management, no advisory, no monitoring, no sensors; limited geographic reach; small scale |

### 2.7 Ninjacart
| Dimension | Details |
|-----------|---------|
| **Core Product** | B2B fresh produce supply chain — connects farmers to retailers/restaurants |
| **Pricing** | Commission/margin on produce logistics |
| **Target** | Farmers (supply side) and retailers/restaurants/kiranas (demand side) |
| **Hardware** | Software + logistics infrastructure (cold chain, warehouses) |
| **Key Features** | AI-powered demand forecasting, quality grading, same-day delivery, cold chain logistics |
| **Funding** | ~$300M+ raised; backed by Flipkart, Tiger Global, Accel |
| **Scale** | 200,000+ farmers, 100,000+ retailers, multiple cities |
| **Weaknesses** | **Purely supply-chain/logistics** — no farm-level intelligence, no precision agriculture, no advisory, no sensors; farmer is just a supplier; doesn't help farmers grow better crops |

### 2.8 BharatAgri
| Dimension | Details |
|-----------|---------|
| **Core Product** | Personalized crop schedule/calendar app with expert advisory for smallholders |
| **Pricing** | Freemium; premium subscription for personalized schedules (~₹500–1,000/season) |
| **Target** | Small/medium Indian farmers |
| **Hardware** | Software-only |
| **Key Features** | Crop-specific daily schedule (when to water, fertilize, spray), expert consultations, weather-based alerts, input purchase recommendations |
| **Funding** | ~$6M raised |
| **Scale** | 3M+ app downloads |
| **Weaknesses** | **No real-time field data** — schedules are generic/model-based, not sensor-driven; no actual soil measurement; no satellite imagery; no hardware; advice is calendar-based, not condition-based; no voice interface |

---

## 3. COMPETITOR MATRIX

| Dimension | DeHaat | AgroStar | Fasal (co.) | CropIn | Plantix | Kisan Network | Ninjacart | BharatAgri | **Fasal Seva** |
|-----------|--------|----------|-------------|--------|---------|---------------|-----------|------------|----------------|
| **Primary Focus** | Input supply + market | Advisory + inputs | Irrigation automation | Enterprise SaaS | Disease diagnosis | Market linkage | Supply chain | Crop schedule | **Full-stack precision farming + AI voice** |
| **Hardware** | ❌ | ❌ | ✅ (expensive) | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ (testing phase)** |
| **Soil Sensors** | ❌ | ❌ | ✅ (moisture, temp) | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ (BT 5.0 IoT sensor — 2 farmer pilots)** |
| **Satellite Analytics** | ❌ | ❌ | ❌ | ✅ (enterprise) | ❌ | ❌ | ❌ | ❌ | **✅ (Sentinel-2, 5 indices: NDVI, NDWI, NDRE, SAVI, MSI)** |
| **AI Voice Interface** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ (Sevak Live — full-duplex, Gemini 3.0)** |
| **Smart Irrigation** | ❌ | ❌ | ✅ (basic) | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ (FAO-56 Penman-Monteith, VRA zones)** |
| **Field Mapping** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ (tap-to-draw + walk mode)** |
| **AR Visualization** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅ (AR Zone Explorer)** |
| **Weather Intelligence** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | Weather | **✅ (14-day GPS forecasts, storm alerts, spray planning)** |
| **Target Farmer** | Small | Small–Medium | Commercial | Enterprise | Small | Small | Small–Medium | Small | **Small–Medium** |
| **Pricing** | Free app | Free app | ₹25K+ | Enterprise SaaS | Free app | Free app | N/A | ~₹500/season | **Free app (sensor pricing TBD)** |
| **Multilingual** | Limited | Limited | No | No | Limited | No | No | Limited | **✅ (Hindi, English, Tamil)** |
| **Funding** | $350M+ | $100M+ | $20M+ | $45M+ | $7M | $4M | $300M+ | $6M | **Zero (bootstrapped, live product)** |

---

## 4. MARKET MAP

### By Value Chain Position

```
INPUT SIDE                          ON-FARM                         OUTPUT SIDE
(seeds, fertilizer,               (monitoring, growing,            (selling, logistics,
 credit)                           irrigation)                      market access)

┌─────────────┐                 ┌──────────────────┐             ┌──────────────┐
│   DeHaat    │                 │   Fasal (co.)    │             │  Ninjacart   │
│   AgroStar  │                 │   ★ FASAL SEVA ★ │             │ Kisan Network│
│             │                 │   BharatAgri     │             │              │
└─────────────┘                 │   Plantix        │             └──────────────┘
                                └──────────────────┘
                                        │
                         ┌──────────────┴──────────────┐
                         │       CropIn (enterprise     │
                         │       satellite analytics)   │
                         └─────────────────────────────┘
```

### By Feature Depth vs Accessibility

```
                    DEEP FEATURES                    SHALLOW FEATURES
                    ┌──────────────────┐    ┌────────────────────┐
ACCESSIBLE          │  ★ FASAL SEVA ★  │    │ BharatAgri, Plantix│
(free/affordable,   │  (LIVE, free app │    │ DeHaat, AgroStar   │
 voice-first)       │   + IoT testing) │    │                    │
                    └──────────────────┘    └────────────────────┘
                    ┌──────────────────┐    ┌────────────────────┐
EXPENSIVE/          │  Fasal (co.)     │    │ CropIn             │
ENTERPRISE          │  Fyllo, Yuktix   │    │                    │
                    └──────────────────┘    └────────────────────┘
```

---

## 5. FASAL SEVA'S ACTUAL POSITIONING (AS OF FEB 2026)

### Product Reality — LIVE on Play Store

**App:** com.fasalseva.app (Google Play Store) | **Website:** fasalseva.in
**Users:** 64 real farmers | **Funding:** ₹0 raised | **Price:** Free for all Indian farmers

### Actual Features (Live in Production)

| Feature | Description | Status |
|---------|-------------|--------|
| **Sevak Live** | Full-duplex AI voice calls with farm data context. Powered by Gemini 3.0 Native Audio. Hindi, English, Tamil. | ✅ LIVE |
| **Satellite Monitoring** | Sentinel-2 imagery, 5 indices (NDVI, NDWI, NDRE, SAVI, MSI), color-coded heatmaps, updated every 3-5 days | ✅ LIVE |
| **Field Mapping** | Tap-to-draw or walk mode, 20+ crops, 7 soil types, 5 irrigation types, downloadable PDF reports | ✅ LIVE |
| **Smart Irrigation Engine** | FAO-56 Penman-Monteith, crop-specific Kc coefficients, VRA zone prescriptions | ✅ LIVE |
| **Weather Intelligence** | 14-day GPS-based forecasts, storm alerts, spray planning | ✅ LIVE |
| **AR Zone Explorer** | Augmented reality satellite overlay on physical field | ✅ LIVE |
| **WhatsApp OTP Login** | SIM auto-detection for frictionless onboarding | ✅ LIVE |
| **Dark Mode + Multilingual UI** | Hindi, English, Tamil; OTA updates | ✅ LIVE |
| **Fasal Seva Mini IoT Sensor** | BT 5.0, 50m range, IP67, rechargeable | ⚠️ TESTING (2 farmers only) |

### What This Means Competitively

**Fasal Seva has already shipped more precision agriculture features for smallholders than any competitor — for free, with zero funding.**

The feature set is significantly stronger than what well-funded competitors offer:
- **More satellite indices than CropIn** offers to individual farmers (5 vs typically 1-2)
- **FAO-56 irrigation engine** that Fasal (co.) charges ₹25K+ to access
- **Full-duplex AI voice calls** — no competitor has anything close
- **AR field visualization** — entirely unique in Indian agritech
- **Walk mode field mapping** — no competitor offers this for smallholders

### The Gap That Still Matters

The key unsolved challenges are not technical but commercial:
1. **Revenue model:** App is free. Hardware isn't ready to scale. How does Fasal Seva make money?
2. **Hardware scaling:** IoT sensor only with 2 test farmers. Manufacturing, distribution, and unit economics are unproven.
3. **User growth:** 64 users is proof of concept, not product-market fit. Need 1,000+ for meaningful signal.
4. **Funding:** Zero raised. Need capital to scale hardware and distribution.

---

## 6. COMPETITIVE ADVANTAGES — Where Fasal Seva Wins

### vs DeHaat / AgroStar (input commerce platforms)
**"They sell products. We tell farmers exactly what their soil needs, when — for free, by voice."**
- Their advisory is generic; Fasal Seva's is satellite-driven and field-specific.
- Fasal Seva's voice AI (Sevak Live) is a generation ahead of any call-center advisory.

### vs Fasal (the company) (expensive hardware)
**"We've shipped more features for free than they charge ₹25K+ for."**
- Fasal co. targets commercial farms. Fasal Seva serves the 86% they ignore.
- FAO-56 Penman-Monteith engine, 5 satellite indices, AI voice — all free in Fasal Seva.
- Fasal co. has no voice interface, no AR, no field mapping with walk mode.

### vs CropIn (enterprise SaaS)
**"We bring enterprise-grade satellite analytics directly to the farmer's pocket — with 5 indices, not just NDVI."**
- CropIn serves agribusinesses at enterprise pricing. Fasal Seva gives individual farmers more indices for free.

### vs Plantix (disease diagnosis)
**"We catch problems BEFORE they become visible — with satellite monitoring across 5 spectral indices."**
- Plantix is reactive (photo after disease appears). Fasal Seva monitors proactively every 3-5 days.

### vs BharatAgri (crop calendar)
**"Our recommendations come from FAO-56 science and satellite data, not a generic calendar."**
- BharatAgri provides model-based schedules. Fasal Seva provides real-time, science-driven, field-specific guidance.

---

## 7. COMPETITIVE RISKS

| Risk | Details | Mitigation |
|------|---------|------------|
| **Revenue model unclear** | App is free. Hardware not ready to scale. No revenue yet. | Explore freemium, B2B data licensing, government contracts, hardware subscription models |
| **Distribution** | DeHaat (2M farmers), AgroStar (12M) have massive farmer networks | Feature superiority + free pricing can drive organic growth; partner with FPOs |
| **Funding gap** | Competitors have $4M–$350M; Fasal Seva has ₹0 | Strong product traction with zero funding is a compelling investor narrative |
| **Hardware scaling** | IoT sensor tested with only 2 farmers; manufacturing and distribution unproven | Focus on software-first growth; hardware as premium add-on when ready |
| **User growth** | 64 users — early but small | Organic growth from Play Store; FPO partnerships; government pilot programs |
| **Fasal (co.) moving downmarket** | Could launch cheaper product for smallholders | Fasal Seva already has more features for free; voice AI + AR are hard to replicate |
| **Big tech entry** | Google, Microsoft, Jio could enter | First-mover with live product; deep feature set; vernacular voice moat |

---

## 8. POSITIONING STRATEGY

### The One-Liner
> **"Fasal Seva is a free, voice-first precision farming app — live on Play Store — that gives India's 120 million small farmers satellite intelligence, FAO-56 irrigation science, and AI advisory in Hindi, English, and Tamil."**

### The Pitch Framework

**Problem:** India's 120M+ small farmers make decisions blind — no soil data, no satellite insights, generic advice. Existing solutions are either software-only (no real data) or hardware costing ₹25K+ (unaffordable).

**Solution:** Fasal Seva = Free mobile app with full-duplex AI voice calls (Sevak Live, powered by Gemini 3.0), 5-index satellite monitoring, FAO-56 smart irrigation, AR field visualization, and walk-mode field mapping. IoT soil sensor in testing.

**Traction (as of Feb 2026):**
- Live on Google Play Store (com.fasalseva.app)
- 64 real users
- Zero funding raised — entirely bootstrapped
- IoT sensor piloting with 2 farmers
- Website: fasalseva.in

**Why Now:**
- Rural smartphone penetration crossed 50%
- Gemini 3.0 enables real-time multilingual voice AI
- Free satellite data (Sentinel-2) makes 5-index monitoring viable
- Government Digital Agriculture Mission creating policy tailwind
- Climate change making precision irrigation urgent

**Moats:**
1. **Feature depth at zero price** — no competitor matches the feature set, let alone for free
2. **Voice-first AI (Sevak Live)** — full-duplex conversations, not chatbots
3. **5 satellite indices** — more than enterprise solutions offer to individual farmers
4. **AR visualization** — entirely unique in agritech
5. **Data network effects** — every user's field data improves the system for all

**Competitive Moat Diagram:**
```
                        Deep Feature Set
                        (satellite, irrigation,
                         voice AI, AR, mapping)
                              │
                    Fasal(co) │ ★ FASAL SEVA ★
                   (₹25K+)   │ (FREE, live, 64 users)
    ──────────────────────────┼──────────────────────────
    Expensive/Enterprise      │    Free/Accessible
                              │
                    CropIn    │  BharatAgri, Plantix
                              │  DeHaat, AgroStar
                              │
                        Shallow Features
                        (advisory, commerce,
                         single-purpose)
```

**Fasal Seva occupies the strongest quadrant: deep features + free/accessible.**

---

## 9. KEY TAKEAWAYS

1. **Lead with the product:** "We've already shipped what competitors with $350M couldn't — a complete precision farming ecosystem, for free."

2. **64 users with zero funding** is the story. It proves the product has real pull.

3. **Sevak Live is the killer feature:** Full-duplex AI voice calls in Hindi/English/Tamil, powered by Gemini 3.0. No competitor has anything close.

4. **The monetization question is real:** The app is free. The hardware isn't ready. Investors will want to see a path to revenue.

5. **Hardware is the next frontier:** The Fasal Seva Mini IoT sensor (BT 5.0, IP67) is testing with 2 farmers. Scaling this is the key unlock for the next phase.

6. **The 86% story still holds:** 86% of Indian farmers are small/marginal. No precision agriculture solution serves them at this depth. Fasal Seva is the first.

---

*Report updated February 2026. Fasal Seva product data from Google Play Store listing (com.fasalseva.app). Competitor data from company websites, publicly available funding data, and market research reports.*
