#!/usr/bin/env python3
"""
Script to convert v1.html to index.html with Capacitor Bluetooth changes
Version 3 - Safe line-by-line processing
"""

# Read the entire v1.html file
with open('/home/user/analyst-app/v1.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Original file: {len(lines)} lines")

# CHANGE 1: Add Capacitor script after line 6 (after title)
for i, line in enumerate(lines):
    if '<title>AI Rowing Coach v1.6</title>' in line:
        lines.insert(i + 1, '    <!-- Capacitor Core -->\n')
        lines.insert(i + 2, '    <script src="capacitor.js"></script>\n')
        print(f"✓ Added Capacitor script at line {i+1}")
        break

# CHANGE 2: Add Capacitor Bluetooth initialization at start of AIRowingCoach init() method
# Find the AIRowingCoach class first, then find its init() method
in_airowingcoach = False
for i, line in enumerate(lines):
    if 'class AIRowingCoach {' in line:
        in_airowingcoach = True
    elif in_airowingcoach and 'async init() {' in line:
        # Insert after this line
        capacitor_init = """                // Initialize Capacitor Bluetooth
                if (window.Capacitor && window.Capacitor.Plugins.BleClient) {
                    try {
                        await window.Capacitor.Plugins.BleClient.initialize();
                        console.log('✓ Capacitor Bluetooth initialized');
                    } catch (e) {
                        console.warn('Bluetooth init:', e);
                    }
                }

"""
        lines.insert(i + 1, capacitor_init)
        print(f"✓ Added Capacitor Bluetooth init at line {i+1}")
        break

def find_function_range(lines, start_idx, func_signature):
    """Find the complete range of a function including all its braces"""
    brace_count = 0
    started = False

    for i in range(start_idx, len(lines)):
        line = lines[i]

        if func_signature in line:
            started = True

        if started:
            # Count braces on this line
            brace_count += line.count('{')
            brace_count -= line.count('}')

            if brace_count == 0 and started:
                return start_idx, i + 1  # Return range including this line

    return start_idx, start_idx + 1

def replace_function_safely(lines, func_name, new_code):
    """Safely replace a function by finding it and replacing exact range"""
    replacements = 0
    i = 0
    while i < len(lines):
        line = lines[i]

        # Check if this line contains the function signature
        if func_name in line and line.strip().startswith(('async ' + func_name, func_name)):
            # Find the complete function range
            start_idx = i
            end_idx = i + 1
            brace_count = 0
            started = False

            for j in range(i, len(lines)):
                if '{' in lines[j] or '}' in lines[j]:
                    if not started:
                        started = True
                    brace_count += lines[j].count('{')
                    brace_count -= lines[j].count('}')

                    if brace_count == 0 and started:
                        end_idx = j + 1
                        break

            # Replace the function
            indent = len(line) - len(line.lstrip())
            indented_code = '\n'.join(' ' * indent + l if l.strip() else l for l in new_code.split('\n'))
            lines[start_idx:end_idx] = [indented_code + '\n']
            replacements += 1
            print(f"✓ Replaced {func_name} at line {start_idx} (removed {end_idx - start_idx} lines)")
            i = start_idx + 1
        else:
            i += 1

    return replacements

# CHANGE 3: Replace connectPM5() function
connectPM5_new = """async connectPM5() {
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
}"""

replace_function_safely(lines, 'async connectPM5()', connectPM5_new)

# CHANGE 4: Replace disconnectPM5() function
disconnectPM5_new = """async disconnectPM5() {
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
}"""

replace_function_safely(lines, 'disconnectPM5()', disconnectPM5_new)

# CHANGE 5: Replace connectHRM() function
connectHRM_new = """async connectHRM() {
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
}"""

replace_function_safely(lines, 'async connectHRM()', connectHRM_new)

# CHANGE 6: Replace disconnectHRM() function
disconnectHRM_new = """disconnectHRM() {
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
}"""

# Note: disconnectHRM needs to be async for await
disconnectHRM_new_async = """async disconnectHRM() {
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
}"""

replace_function_safely(lines, 'disconnectHRM()', disconnectHRM_new_async)

# CHANGE 7: Replace connectHRMDirect() function
connectHRMDirect_new = """async connectHRMDirect() {
const HRM_SERVICE = 0x180D;
const HRM_CHARACTERISTIC = 0x2A37;

const btn = document.getElementById('hrmConnectButton');
const statusText = document.getElementById('hrmStatusText');
const statusDesc = document.getElementById('hrmStatusDesc');

btn.disabled = true;
btn.textContent = 'Connecting...';
statusText.textContent = 'Connecting...';

try {
    console.log('🔍 Requesting HRM...');

    const { BleClient } = window.Capacitor.Plugins;

    const device = await BleClient.requestDevice({
        services: [HRM_SERVICE],
        optionalServices: []
    });

    console.log(`✓ Device: ${device.name || device.deviceId}`);
    statusDesc.textContent = `Connecting to ${device.name || 'HRM'}...`;

    await BleClient.connect(device.deviceId);
    console.log('✓ HRM connected');

    this.hrmDevice = device;

    await BleClient.startNotifications(
        device.deviceId,
        HRM_SERVICE,
        HRM_CHARACTERISTIC,
        (value) => this.handleHRMDataDirect(value)
    );

    console.log('✓ HRM notifications started');

    statusText.textContent = `Connected: ${device.name || 'HRM'}`;
    statusDesc.textContent = 'Receiving heart rate data';
    btn.textContent = 'Disconnect';
    btn.disabled = false;
    btn.onclick = () => this.disconnectHRMDirect();

    // Show live display and graph
    document.getElementById('hrmLiveDisplay').style.display = 'block';
    document.getElementById('hrmGraphContainer').style.display = 'block';

    // Initialize canvas
    this.initHRMCanvas();

    this.showToast('HRM connected!', 'success');
} catch (error) {
    console.error('❌ HRM error:', error);
    statusText.textContent = 'Connection Failed';
    statusDesc.textContent = error.message;
    btn.textContent = 'Retry';
    btn.disabled = false;

    this.showToast('HRM connection failed: ' + error.message, 'error');
}
}"""

replace_function_safely(lines, 'async connectHRMDirect()', connectHRMDirect_new)

# Also replace disconnectHRMDirect
disconnectHRMDirect_new = """disconnectHRMDirect() {
if (!this.hrmDevice) return;

try {
    const { BleClient } = window.Capacitor.Plugins;
    await BleClient.disconnect(this.hrmDevice.deviceId);

    this.hrmDevice = null;
    this.hrmCharacteristic = null;
    this.hrHistory = [];
    this.currentHR = 0;

    document.getElementById('hrmStatusText').textContent = 'Not Connected';
    document.getElementById('hrmStatusDesc').textContent = 'Connect your Polar/Garmin/Wahoo HRM';
    document.getElementById('hrmLiveDisplay').style.display = 'none';
    document.getElementById('hrmGraphContainer').style.display = 'none';

    const btn = document.getElementById('hrmConnectButton');
    btn.textContent = 'Connect Heart Rate Monitor';
    btn.onclick = () => this.connectHRMDirect();

    this.showToast('HRM disconnected', 'success');
} catch (error) {
    console.error('❌ Disconnect error:', error);
}
}"""

# Need async version
disconnectHRMDirect_new_async = """async disconnectHRMDirect() {
if (!this.hrmDevice) return;

try {
    const { BleClient } = window.Capacitor.Plugins;
    await BleClient.disconnect(this.hrmDevice.deviceId);

    this.hrmDevice = null;
    this.hrmCharacteristic = null;
    this.hrHistory = [];
    this.currentHR = 0;

    document.getElementById('hrmStatusText').textContent = 'Not Connected';
    document.getElementById('hrmStatusDesc').textContent = 'Connect your Polar/Garmin/Wahoo HRM';
    document.getElementById('hrmLiveDisplay').style.display = 'none';
    document.getElementById('hrmGraphContainer').style.display = 'none';

    const btn = document.getElementById('hrmConnectButton');
    btn.textContent = 'Connect Heart Rate Monitor';
    btn.onclick = () => this.connectHRMDirect();

    this.showToast('HRM disconnected', 'success');
} catch (error) {
    console.error('❌ Disconnect error:', error);
}
}"""

replace_function_safely(lines, 'disconnectHRMDirect()', disconnectHRMDirect_new_async)

# Write the new index.html file
with open('/home/user/analyst-app/index.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"\n✓ Successfully created index.html ({len(lines)} lines)")
print("\nAll Capacitor Bluetooth changes applied!")

# Verify
nav_bluetooth_count = sum(1 for line in lines if 'navigator.bluetooth' in line)
ble_client_count = sum(1 for line in lines if 'BleClient' in line)
print(f"\n⚠️  navigator.bluetooth references remaining: {nav_bluetooth_count}")
print(f"✓ BleClient references: {ble_client_count}")
