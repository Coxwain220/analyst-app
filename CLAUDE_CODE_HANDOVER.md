# AI Rowing Coach App - Complete Handover to Claude Code

**Date:** January 23, 2026  
**From:** Claude (Assistant)  
**To:** Claude Code  
**User:** Rispy (John Eller)  

---

## 🎯 PROJECT MISSION

Build a **native iOS/Android rowing coach app** that connects to Concept2 PM5 rowing machines and heart rate monitors via Bluetooth to provide:
- Real-time workout tracking
- AI-powered coaching
- Training plan generation
- Performance analytics
- Cloud-synced workout history

**Critical Context:** User is **not a developer** - needs clear, step-by-step guidance with no assumed technical knowledge.


I have provided a handover document. Your first task is to index the project.

Read v1.html to understand the current Web Bluetooth logic.

Read CAPACITOR_CONVERSION_GUIDE.md.

Create a new file called index.html that implements the Capacitor Bluetooth changes while keeping the UI and Firebase logic identical.

Do not delete v1.html; we will keep it as a backup.

For prototype and testing the target device is an iPhone 12 Mini running iOS 26.2

You have full permission to run npm, npx, git, and eas commands, but it must explain the command first before hitting "Enter." This ensures I learn the workflow while you do the work.


---

## 📍 CURRENT STATUS - WHERE WE ARE NOW

### ✅ COMPLETED WORK

**Development Environment:**
- Windows PC (ARM64 architecture)
- Node.js v24.13.0 installed
- Git v2.52.0 installed
- Visual Studio Code installed
- EAS CLI installed
- Project location: `C:\rowing-coach-app`

**Accounts & Services:**
- GitHub: Coxwain220/rowing-coach-native
- Expo/EAS: aifitness account
- Ionic Appflow: Connected to GitHub
- Firebase: ai-fitness-app-c5307 (cloud storage active)
- Apple Developer: Enrollment submitted this morning (awaiting 24-48hr approval)

Desktop Hardware	Ryzen 7 7800X3D, 64GB RAM, Windows 11

**Capacitor Project Structure:**
```
C:\rowing-coach-app/
├── www/
│   └── index.html (needs to be updated with v1.html)
├── ios/
│   └── App/
│       └── App/
│           └── Info.plist (configured with Bluetooth permissions)
├── node_modules/
├── capacitor.config.json
├── app.json
├── eas.json
├── package.json
└── package-lock.json
```

**Installed Packages:**
- @capacitor/core
- @capacitor/cli
- @capacitor/ios
- @capacitor-community/bluetooth-le (v8.0.0)
- expo-dev-client

### 🔄 CURRENT BLOCKER

**Apple Developer Account Approval** - waiting 24-48 hours  
**Once approved:** Can build iOS app via Ionic Appflow

---

## 📱 APP FEATURES - CURRENT v1.html

**Latest version:** `v1.html` (3735 lines)  
**Status:** Web Bluetooth version (working in Bluefy browser)  
**Needs:** Conversion to Capacitor native Bluetooth

### Core Features Built:

1. **Dashboard (5 Swipeable Views)**
   - All Data view (metrics grid)
   - Force Curve visualization
   - Paceboat comparison
   - Pace bar chart
   - Large print mode

2. **Manual Workout Builder**
   - Single Distance mode
   - Single Time mode (5min, 30min, etc.)
   - Single Calorie mode
   - Fixed Intervals (6x500m, etc.)
   - Variable Intervals (custom sets)
   - Global Targets: Split pace, Pacer, Stroke rate, HR zones

3. **Review Screen**
   - Workout summary display
   - Mode, total time/distance
   - Interval breakdown
   - Target metrics
   - Start/Back buttons

4. **Workout Timer**
   - ✅ Countdown timer (5:00 → 0:00)
   - ✅ Waits for first stroke to start
   - ✅ Coach messages with progress
   - ✅ Auto-saves to history when complete
   - ✅ Interval rest periods
   - Manual "Start" button for testing

5. **Heart Rate Monitor Screen**
   - Live BPM display (72pt font)
   - Zone visualization (Z1-Z5)
   - Real-time graph
   - Avg/Max/Min stats
   - Direct HRM connection button

6. **Training Plan**
   - 4-week progressive program
   - Week-by-week breakdown
   - Clickable workout days
   - Plan overview with objectives
   - Status tracking (completed/pending)

7. **AI Chat**
   - Simulated AI coach responses
   - Quick reply buttons
   - Workout creation guidance
   - Training plan generation
   - Performance analysis

8. **History & Analytics**
   - Workout log with dates
   - CSV export functionality
   - Delete individual workouts
   - Total workouts/distance stats
   - Firebase cloud sync

9. **Settings**
   - User profile (name, age, weight)
   - HR zones configuration (max HR, Z1-Z5 ranges)
   - Device connections (PM5, HRM)
   - Firebase status display
   - CSV import

10. **Navigation**
    - Top nav: Settings, HR Mon, 2 TBD placeholders
    - Bottom nav: AI Chat, Row, Builder, Plan, History
    - Active state highlighting

### Firebase Integration:
- Anonymous authentication
- Cloud Firestore for workouts
- Profile storage
- Chat history sync
- Auto-save on workout completion

### Current Bluetooth (Web API):
- PM5 connection via `navigator.bluetooth.requestDevice()`
- HRM connection via standard Heart Rate Service
- Works in Bluefy browser on iOS
- **Problem:** Unreliable, app freezes

---

## 🚨 CRITICAL ISSUES TO FIX

### 1. **Bluetooth Conversion** (HIGHEST PRIORITY)
**Problem:** Web Bluetooth API is unreliable  
**Solution:** Convert to Capacitor Bluetooth LE plugin  
**Status:** Conversion guide created (see CAPACITOR_CONVERSION_GUIDE.md)

**What needs to change in v1.html:**
```javascript
// OLD (Web Bluetooth)
this.pm5Device = await navigator.bluetooth.requestDevice({
    filters: [{ services: [PM5_SERVICE_UUID] }]
});
const server = await this.pm5Device.gatt.connect();

// NEW (Capacitor)
const { BleClient } = window.Capacitor.Plugins;
await BleClient.initialize();
const device = await BleClient.requestDevice({
    services: [PM5_SERVICE_UUID]
});
await BleClient.connect(device.deviceId);
```

**Files to modify:**
- Add `<script src="capacitor.js"></script>` in `<head>`
- Replace `connectPM5()` function
- Replace `disconnectPM5()` function
- Replace `connectHRM()` function
- Replace `disconnectHRM()` function
- Replace `connectHRMDirect()` function

### 2. **Cloud Build Setup**
**Status:** Waiting on Apple Developer approval  
**Next steps when approved:**
1. Complete Ionic Appflow certificate setup
2. Trigger iOS build
3. Download .ipa file
4. Install on iPhone 12 Mini

---

## 🎨 DESIGN PHILOSOPHY

**IMPORTANT:** User has emphasized that **design will change significantly**. Current focus is on:
1. **Functionality first** - get features working
2. **Reliable Bluetooth** - stable PM5/HRM connections
3. **Gym testing** - validate in real environment
4. **Iterate on UX** - polish comes later

**Current UI:**
- Dark theme (#000 background)
- Neon green accent (#00FF99)
- High contrast for gym visibility
- Large touch targets for sweaty thumbs
- Swipeable dashboard views

---

## 📊 USER DATA

### CSV Import Format:
User has Concept2 workout history in CSV format:
- Columns: Log ID, Date, Description, Work Time, Work Distance, Pace, Avg Watts, Avg Heart Rate, etc.
- Date format: DD/M/YYYY (e.g., "18/1/2026")
- Import working correctly in v1.html

### Sample Data:
- **Latest file:** concept2-season-2026_-_jan_21.csv
- ~52 workouts from recent training season
- Used for testing History screen
- Syncs to Firebase after import

---

## 🛠️ TECHNICAL STACK

**Frontend:**
- Single HTML file architecture
- Vanilla JavaScript (no frameworks)
- CSS Grid + Flexbox
- Firebase v10.8.0 (modular SDK)

**Native Layer (Capacitor):**
- @capacitor/core
- @capacitor/ios
- @capacitor-community/bluetooth-le v8.0.0

**Build Tools:**
- Capacitor CLI
- EAS CLI (Expo)
- Ionic Appflow (cloud builds)

**Services:**
- Firebase Firestore (workout storage)
- Firebase Auth (anonymous)
- GitHub (code hosting)

---

## 📋 GYM TEST REQUIREMENTS

User has **limited gym access** (few times per week). App MUST work reliably for:

**Test Workflow:**
1. Open app on iPhone
2. Settings → Connect PM5 (Concept2 rowing machine)
3. Settings → Connect HRM (chest strap)
4. Builder → Create 5-minute workout
5. Review → Start Row
6. **Wait for first stroke** (timer stays at 5:00)
7. Pull handle → Timer starts counting down (5:00 → 4:59...)
8. Complete workout → Auto-saves to History
9. History → Export CSV

**Success Criteria:**
- ✅ PM5 connects on first try
- ✅ HRM connects and shows live BPM
- ✅ Timer countdown works correctly
- ✅ Data saves to Firebase
- ✅ No app freezes or crashes

---

## 🗂️ FILE STRUCTURE

### Current GitHub Repository: `rowing-coach-native`

```
rowing-coach-native/
├── README.md
├── v1.html (3735 lines - CURRENT WORKING VERSION)
└── (other project files to be added)
```

### What Claude Code Needs:

1. **v1.html** - Current web version
2. **CAPACITOR_CONVERSION_GUIDE.md** - Bluetooth conversion instructions
3. **AI_Plan.docx** - Training plan architecture notes
4. **concept2-season-2026_-_jan_21.csv** - Sample workout data
5. **This handover document**

---

## 🎯 IMMEDIATE NEXT STEPS FOR CLAUDE CODE

### Phase 1: Bluetooth Conversion (NOW)

**Task:** Convert v1.html to use native Capacitor Bluetooth

**Steps:**
1. Read CAPACITOR_CONVERSION_GUIDE.md thoroughly
2. Take v1.html as base
3. Apply the 7 code changes outlined in guide:
   - Add Capacitor script tag
   - Initialize BleClient in init()
   - Replace connectPM5() with native version
   - Replace disconnectPM5() with native version
   - Replace connectHRM() with native version
   - Replace disconnectHRM() with native version
   - Update connectHRMDirect() with native version
4. Save as new file: `index.html`
5. Provide to user for testing

**Validation:**
- File should be ~3750 lines (similar to v1.html)
- Only Bluetooth code changed
- All other features preserved
- Firebase integration intact
- UI/UX identical

### Phase 2: Cloud Build (When Apple Approves)

**Task:** Guide user through Ionic Appflow build

**Prerequisites:**
- Apple Developer account active
- Sees "Certificates, Identifiers & Profiles" at developer.apple.com

**Steps:**
1. User opens Ionic Appflow
2. Selects build configuration
3. Chooses "Automatic Signing" or manual cert setup
4. Enters Apple ID credentials
5. Triggers build
6. Waits 15-20 minutes
7. Downloads .ipa file

### Phase 3: Gym Testing

**Task:** Support user during first gym test

**What to monitor:**
- PM5 connection success rate
- HRM connection reliability
- Timer behavior (wait for first stroke)
- Data accuracy in History
- Firebase sync verification

**What to fix:**
- Any Bluetooth disconnection issues
- Timer bugs
- Data not saving
- UI visibility problems in gym lighting

### Phase 4: Feature Development (After Stable Bluetooth)

**Backlog:**
- Real PM5 data parsing (currently placeholder)
- AI coaching (currently simulated)
- Advanced analytics
- Social features
- Training plan customization

---

## 🚫 WHAT NOT TO DO

**Do NOT change without user approval:**
- ❌ Overall UI design (colors, layout, navigation)
- ❌ Core feature set (Dashboard, Builder, Plan, etc.)
- ❌ Firebase configuration
- ❌ File architecture (stay single HTML for now)

**Do NOT assume technical knowledge:**
- ❌ Use terminal commands without explanation
- ❌ Reference unfamiliar dev concepts
- ❌ Skip validation steps
- ❌ Make changes without clear reasoning

**Do NOT add complexity:**
- ❌ Build systems or bundlers
- ❌ TypeScript conversion
- ❌ React/Vue/Angular frameworks
- ❌ Testing frameworks (not ready yet)

---

## 💬 COMMUNICATION STYLE WITH USER

**User Profile:**
- Non-developer
- Needs clear step-by-step instructions
- Appreciates directness over excessive praise
- Values functionality over polish (for now)
- Has limited gym testing time (high stakes)

**When Providing Instructions:**
1. ✅ Show exact commands to run
2. ✅ Explain what each step does
3. ✅ Provide validation checks
4. ✅ Anticipate common errors
5. ✅ Ask for confirmation before major changes

**When Things Break:**
1. ✅ Acknowledge the issue clearly
2. ✅ Explain root cause simply
3. ✅ Provide concrete fix
4. ✅ Offer alternative if needed
5. ✅ Learn from the mistake

---

## 📞 KEY CONTACT INFO

**User:** Rispy (John Eller)  
**Email:** ellertonoj@gmail.com  
**Phone:** iPhone 12 Mini (target device)  
**Location:** Singapore

**Accounts:**
- GitHub: Coxwain220
- Expo: aifitness
- Apple Developer: ellertonoj@gmail.com (pending approval)

---

## 📚 REFERENCE DOCUMENTS

**Available in outputs:**
1. `CAPACITOR_CONVERSION_GUIDE.md` - Bluetooth changes needed
2. `AI_Plan.docx` - Backend architecture notes
3. `concept2-season-2026_-_jan_21.csv` - Sample data

**In GitHub (`rowing-coach-native`):**
1. `v1.html` - Current working version (3735 lines)

**In Project Memory:**
- Full development history
- Past bugs and fixes
- User preferences and constraints
- Design decisions rationale

---

## 🎓 LEARNING FROM PAST MISTAKES

**What Went Wrong:**
1. **Initial Web Bluetooth approach** - Too unreliable, caused app freezes
2. **EAS build configuration issues** - Xcode scheme problems with Capacitor
3. **Multiple file location changes** - OneDrive sync caused issues
4. **Over-complicated connection code** - Tried too many fallback methods

**What Worked:**
1. **Simple, clear instructions** - User followed successfully
2. **Incremental feature building** - Dashboard → Builder → Timer
3. **Frequent validation** - "Does this work?" after each change
4. **Cloud build decision** - Avoids Mac hardware requirement
5. **Firebase integration** - Clean data abstraction layer

---

## 🔮 FUTURE VISION

**Short-term (Next 2 weeks):**
- Stable native iOS app
- Reliable PM5/HRM connections
- Accurate workout tracking
- Cloud-synced history

**Medium-term (Next month):**
- Real AI coaching (Claude API integration)
- Advanced analytics
- Social features (compare with friends)
- Training plan customization

**Long-term (3+ months):**
- Android version
- App Store submission
- Beta testing program
- Revenue model (freemium)

---

## ✅ SUCCESS DEFINITION

**This handover is successful if:**

1. ✅ Claude Code understands the full project context
2. ✅ Claude Code can continue development seamlessly
3. ✅ User gets a working native iOS app
4. ✅ PM5 Bluetooth connection is reliable in gym
5. ✅ User can test and provide feedback effectively

---

## 📝 FINAL NOTES FOR CLAUDE CODE

**You inherit:**
- A functional web app (v1.html)
- A non-technical user who needs guidance
- A critical blocker (Apple approval)
- A clear path forward (Bluetooth conversion)
- High stakes (limited gym testing opportunities)

**Your mission:**
1. Convert v1.html to native Capacitor Bluetooth
2. Ensure zero feature regression
3. Support user through first gym test
4. Iterate based on real-world feedback
5. Build toward production-ready app

**Remember:**
- User is waiting on Apple (24-48 hrs from Jan 23 morning)
- Design will change later (don't over-optimize UI now)
- Bluetooth reliability is THE critical success factor
- Clear communication > technical perfection

---

**Good luck! The user is counting on you. 🚣**

---

## 📎 ATTACHED FILES

1. `v1.html` - Current working version
2. `CAPACITOR_CONVERSION_GUIDE.md` - Bluetooth conversion steps
3. `AI_Plan.docx` - Architecture notes
4. `concept2-season-2026_-_jan_21.csv` - Sample workout data

**GitHub Repository:** https://github.com/Coxwain220/rowing-coach-native
