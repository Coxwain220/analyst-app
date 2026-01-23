# v1.6 → Capacitor Native Conversion Guide

## Overview
This guide shows EXACTLY what to change in your v1.6 production HTML to make it work as a native iOS app with Capacitor Bluetooth.

---

## STEP 1: Add Capacitor Script Tag

**Location:** Right after `<title>AI Rowing Coach v1.6</title>` (around line 6)

**ADD THIS:**
```html
<!-- Capacitor Core -->
<script src="capacitor.js"></script>
```

---

## STEP 2: Initialize Capacitor Bluetooth

**Location:** Inside the `AIRowingCoach` class `init()` method (around line 1670)

**ADD THIS** at the start of `async init()`:
```javascript
async init() {
    // Initialize Capacitor Bluetooth
    if (window.Capacitor && window.Capacitor.Plugins.BleClient) {
        try {
            await window.Capacitor.Plugins.BleClient.initialize();
            console.log('✓ Capacitor Bluetooth initialized');
        } catch (e) {
            console.warn('Bluetooth init:', e);
        }
    }
    
    // ... rest of your existing init() code ...
```

---

## STEP 3: Replace connectPM5() Function

**Location:** Around line 2560 (search for `async connectPM5()`)

**REPLACE THE ENTIRE FUNCTION** with:

```javascript
async connectPM5() {
    const btn = document.getElementById('pm5ConnectBtn');
    const status = document.getElementById('pm5Status');
    const indicator = document.getElementById('pm5Indicator');
    
    const btnSettings = document.getElementById('pm5ConnectBtnSettings');
    const statusSettings = document.getElementById('pm5StatusSettings');
    const indicatorSettings = document.getElementById('pm5IndicatorSettings');
    
    if (btn) {
        btn.disabled = true;
        btn.textContent = 'Connecting...';
    }
    if (btnSettings) {
        btnSettings.disabled = true;
        btnSettings.textContent = 'Connecting...';
    }
    if (status) status.textContent = 'Searching for PM5...';
    if (statusSettings) statusSettings.textContent = 'Searching for PM5...';
    
    try {
        console.log('🔍 Requesting PM5...');
        
        // Use Capacitor Bluetooth LE plugin
        const { BleClient } = window.Capacitor.Plugins;
        
        const device = await BleClient.requestDevice({
            services: [PM5_SERVICE_UUID],
            optionalServices: []
        });
        
        console.log(`✓ Device: ${device.name || device.deviceId}`);
        if (status) status.textContent = `Connecting to ${device.name || 'PM5'}...`;
        if (statusSettings) statusSettings.textContent = `Connecting to ${device.name || 'PM5'}...`;
        
        await BleClient.connect(device.deviceId);
        console.log('✓ PM5 connected');
        
        this.pm5Device = device;
        
        // Start notifications
        await BleClient.startNotifications(
            device.deviceId,
            PM5_SERVICE_UUID,
            PM5_CHARACTERISTIC_UUID,
            (value) => this.handlePM5Data(value)
        );
        
        console.log('✓ PM5 notifications started');
        
        if (status) status.textContent = `Connected: ${device.name || 'PM5'}`;
        if (statusSettings) statusSettings.textContent = `Connected: ${device.name || 'PM5'}`;
        if (indicator) indicator.style.background = '#00FF99';
        if (indicatorSettings) indicatorSettings.style.background = '#00FF99';
        
        if (btn) {
            btn.textContent = 'Disconnect';
            btn.disabled = false;
            btn.onclick = () => this.disconnectPM5();
        }
        if (btnSettings) {
            btnSettings.textContent = 'Disconnect';
            btnSettings.disabled = false;
            btnSettings.onclick = () => this.disconnectPM5();
        }
        
        this.showToast('PM5 connected!', 'success');
    } catch (error) {
        console.error('❌ PM5 error:', error);
        if (status) status.textContent = 'Connection failed';
        if (statusSettings) statusSettings.textContent = 'Connection failed';
        if (indicator) indicator.style.background = '#FF4444';
        if (indicatorSettings) indicatorSettings.style.background = '#FF4444';
        
        if (btn) {
            btn.textContent = 'Retry';
            btn.disabled = false;
        }
        if (btnSettings) {
            btnSettings.textContent = 'Retry';
            btnSettings.disabled = false;
        }
        
        this.showToast('PM5 connection failed: ' + error.message, 'error');
    }
}
```

---

## STEP 4: Replace disconnectPM5() Function

**Location:** Right after `connectPM5()` (around line 2610)

**REPLACE WITH:**

```javascript
async disconnectPM5() {
    if (!this.pm5Device) return;
    
    try {
        const { BleClient } = window.Capacitor.Plugins;
        await BleClient.disconnect(this.pm5Device.deviceId);
        this.pm5Device = null;
        
        const status = document.getElementById('pm5Status');
        const indicator = document.getElementById('pm5Indicator');
        const btn = document.getElementById('pm5ConnectBtn');
        const statusSettings = document.getElementById('pm5StatusSettings');
        const indicatorSettings = document.getElementById('pm5IndicatorSettings');
        const btnSettings = document.getElementById('pm5ConnectBtnSettings');
        
        if (status) status.textContent = 'Not connected';
        if (statusSettings) statusSettings.textContent = 'Not connected';
        if (indicator) indicator.style.background = '#666';
        if (indicatorSettings) indicatorSettings.style.background = '#666';
        
        if (btn) {
            btn.textContent = 'Connect PM5';
            btn.onclick = () => this.connectPM5();
        }
        if (btnSettings) {
            btnSettings.textContent = 'Connect PM5';
            btnSettings.onclick = () => this.connectPM5();
        }
        
        this.showToast('PM5 disconnected', 'success');
    } catch (error) {
        console.error('❌ Disconnect error:', error);
    }
}
```

---

## STEP 5: Replace connectHRM() Function

**Location:** Search for `async connectHRM()` (around line 2650)

**REPLACE THE ENTIRE FUNCTION** with:

```javascript
async connectHRM() {
    const HRM_SERVICE = 0x180D;
    const HRM_CHARACTERISTIC = 0x2A37;
    
    const btn = document.getElementById('hrmConnectBtn');
    const status = document.getElementById('hrmStatus');
    const indicator = document.getElementById('hrmIndicator');
    
    const btnSettings = document.getElementById('hrmConnectBtnSettings');
    const statusSettings = document.getElementById('hrmStatusSettings');
    const indicatorSettings = document.getElementById('hrmIndicatorSettings');
    
    if (btn) {
        btn.disabled = true;
        btn.textContent = 'Connecting...';
    }
    if (btnSettings) {
        btnSettings.disabled = true;
        btnSettings.textContent = 'Connecting...';
    }
    if (status) status.textContent = 'Connecting...';
    if (statusSettings) statusSettings.textContent = 'Connecting...';
    
    try {
        console.log('🔍 Requesting HRM...');
        
        const { BleClient } = window.Capacitor.Plugins;
        
        const device = await BleClient.requestDevice({
            services: [HRM_SERVICE],
            optionalServices: []
        });
        
        console.log(`✓ Device: ${device.name || device.deviceId}`);
        if (status) status.textContent = `Connecting to ${device.name || 'HRM'}...`;
        if (statusSettings) statusSettings.textContent = `Connecting to ${device.name || 'HRM'}...`;
        
        await BleClient.connect(device.deviceId);
        console.log('✓ HRM connected');
        
        this.hrmDevice = device;
        
        await BleClient.startNotifications(
            device.deviceId,
            HRM_SERVICE,
            HRM_CHARACTERISTIC,
            (value) => this.handleHRMData(value)
        );
        
        console.log('✓ HRM notifications started');
        
        if (status) status.textContent = `Connected: ${device.name || 'HRM'}`;
        if (statusSettings) statusSettings.textContent = `Connected: ${device.name || 'HRM'}`;
        if (indicator) indicator.style.background = '#ff6b6b';
        if (indicatorSettings) indicatorSettings.style.background = '#ff6b6b';
        
        if (btn) {
            btn.textContent = 'Disconnect';
            btn.disabled = false;
            btn.onclick = () => this.disconnectHRM();
        }
        if (btnSettings) {
            btnSettings.textContent = 'Disconnect';
            btnSettings.disabled = false;
            btnSettings.onclick = () => this.disconnectHRM();
        }
        
        this.showToast('HRM connected!', 'success');
    } catch (error) {
        console.error('❌ HRM error:', error);
        if (status) status.textContent = 'Connection failed';
        if (statusSettings) statusSettings.textContent = 'Connection failed';
        if (indicator) indicator.style.background = '#FF4444';
        if (indicatorSettings) indicatorSettings.style.background = '#FF4444';
        
        if (btn) {
            btn.textContent = 'Retry';
            btn.disabled = false;
        }
        if (btnSettings) {
            btnSettings.textContent = 'Retry';
            btnSettings.disabled = false;
        }
        
        this.showToast('HRM connection failed: ' + error.message, 'error');
    }
}
```

---

## STEP 6: Replace disconnectHRM() Function

**REPLACE WITH:**

```javascript
async disconnectHRM() {
    if (!this.hrmDevice) return;
    
    try {
        const { BleClient } = window.Capacitor.Plugins;
        await BleClient.disconnect(this.hrmDevice.deviceId);
        this.hrmDevice = null;
        
        const status = document.getElementById('hrmStatus');
        const indicator = document.getElementById('hrmIndicator');
        const btn = document.getElementById('hrmConnectBtn');
        const statusSettings = document.getElementById('hrmStatusSettings');
        const indicatorSettings = document.getElementById('hrmIndicatorSettings');
        const btnSettings = document.getElementById('hrmConnectBtnSettings');
        
        if (status) status.textContent = 'Not connected';
        if (statusSettings) statusSettings.textContent = 'Not connected';
        if (indicator) indicator.style.background = '#666';
        if (indicatorSettings) indicatorSettings.style.background = '#666';
        
        if (btn) {
            btn.textContent = 'Connect HRM';
            btn.onclick = () => this.connectHRM();
        }
        if (btnSettings) {
            btnSettings.textContent = 'Connect HRM';
            btnSettings.onclick = () => this.connectHRM();
        }
        
        this.showToast('HRM disconnected', 'success');
    } catch (error) {
        console.error('❌ Disconnect error:', error);
    }
}
```

---

## STEP 7: Also Update connectHRMDirect() 

**Location:** Search for `async connectHRMDirect()`

Apply the same Capacitor Bluetooth pattern as above.

---

## SUMMARY OF CHANGES

1. ✅ Add `<script src="capacitor.js"></script>` in `<head>`
2. ✅ Initialize BleClient in `init()`
3. ✅ Replace `navigator.bluetooth` with `BleClient`
4. ✅ Replace `device.gatt.connect()` with `BleClient.connect(device.deviceId)`
5. ✅ Replace `startNotifications` with `BleClient.startNotifications()`
6. ✅ Replace `disconnect()` with `BleClient.disconnect(device.deviceId)`

**Everything else stays EXACTLY the same!**

---

## After Making Changes

1. Save the file as `index.html`
2. Copy it to `C:\rowing-coach-app\www\index.html`
3. Run: `npx cap sync`
4. Wait for Apple Developer approval
5. Build on Ionic Appflow

**Then you'll have your full v1.6 app with native Bluetooth on iPhone!**
