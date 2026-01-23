# Verification Example: connectPM5() Function

## BEFORE (v1.html - Web Bluetooth API)

```javascript
async connectPM5() {
    const btn = document.getElementById('pm5ConnectBtn');
    const status = document.getElementById('pm5Status');
    const indicator = document.getElementById('pm5Indicator');

    // Also update Settings card elements
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

        this.pm5Device = await navigator.bluetooth.requestDevice({  // ❌ Web Bluetooth
            filters: [{ services: [PM5_SERVICE_UUID] }]
        });

        console.log(`✓ Device: ${this.pm5Device.name}`);
        if (status) status.textContent = `Connecting to ${this.pm5Device.name}...`;
        if (statusSettings) statusSettings.textContent = `Connecting to ${this.pm5Device.name}...`;

        const server = await this.pm5Device.gatt.connect();  // ❌ GATT
        const service = await server.getPrimaryService(PM5_SERVICE_UUID);  // ❌ GATT
        this.pm5Characteristic = await service.getCharacteristic(PM5_CHARACTERISTIC_UUID);  // ❌ GATT

        await this.pm5Characteristic.startNotifications();  // ❌ Direct characteristic
        this.pm5Characteristic.addEventListener('characteristicvaluechanged', (e) => {  // ❌ Event listener
            this.handlePM5Data(e.target.value);
        });

        console.log('✓ PM5 connected');

        if (status) status.textContent = `Connected: ${this.pm5Device.name}`;
        if (statusSettings) statusSettings.textContent = `Connected: ${this.pm5Device.name}`;
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

## AFTER (index.html - Capacitor Bluetooth LE)

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
        const { BleClient } = window.Capacitor.Plugins;  // ✅ Capacitor

        const device = await BleClient.requestDevice({  // ✅ BleClient
            services: [PM5_SERVICE_UUID],
            optionalServices: []
        });

        console.log(`✓ Device: ${device.name || device.deviceId}`);
        if (status) status.textContent = `Connecting to ${device.name || 'PM5'}...`;
        if (statusSettings) statusSettings.textContent = `Connecting to ${device.name || 'PM5'}...`;

        await BleClient.connect(device.deviceId);  // ✅ Connect via plugin
        console.log('✓ PM5 connected');

        this.pm5Device = device;  // ✅ Store device object

        // Start notifications
        await BleClient.startNotifications(  // ✅ Plugin-managed notifications
            device.deviceId,
            PM5_SERVICE_UUID,
            PM5_CHARACTERISTIC_UUID,
            (value) => this.handlePM5Data(value)  // ✅ Callback function
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

## Key Differences

| Aspect | Web Bluetooth (v1.html) | Capacitor (index.html) |
|--------|------------------------|----------------------|
| Device Request | `navigator.bluetooth.requestDevice()` | `BleClient.requestDevice()` |
| Connection | `device.gatt.connect()` | `BleClient.connect(device.deviceId)` |
| Service Access | `server.getPrimaryService()` | Not needed - handled by plugin |
| Characteristic Access | `service.getCharacteristic()` | Not needed - handled by plugin |
| Notifications | `characteristic.startNotifications()` + event listener | `BleClient.startNotifications()` with callback |
| Device Reference | Stores GATT server | Stores device object with deviceId |
| Platform Support | Web browsers only | iOS, Android, Web |

## Benefits of Capacitor Version

1. **Native iOS Support** - Works on iPhone with native Bluetooth
2. **Simplified API** - No GATT layer management needed
3. **Consistent Behavior** - Same code works across platforms
4. **Better Error Handling** - Native error messages
5. **Background Support** - Can potentially run in background (iOS)
6. **App Store Compliant** - Can be published to Apple App Store
