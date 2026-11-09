// Gladius – Desktop-Hauptprozess (Electron)
// Hauptfenster: die Trainings-App. Overlay: transparentes, klick-durchlässiges Vollbild-HUD,
// das immer über allen anderen Fenstern liegt (YouTube, Netflix, Browser im Vollbild …).
const { app, BrowserWindow, ipcMain, globalShortcut, screen, powerSaveBlocker } = require('electron');
const path = require('path');

let win = null, overlay = null, overlayOn = false, overlayReady = false, btCallback = null, psb = null;

if (!app.requestSingleInstanceLock()) app.quit();
app.on('second-instance', () => { if (win) { if (win.isMinimized()) win.restore(); win.focus(); } });

function createMain() {
  win = new BrowserWindow({
    width: 1320, height: 900, minWidth: 900, minHeight: 600,
    backgroundColor: '#0d1014', title: 'Gladius', autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true, nodeIntegration: false,
      backgroundThrottling: false            // läuft ungebremst weiter, auch minimiert oder verdeckt
    }
  });
  win.loadFile(path.join(__dirname, 'app', 'index.html'));

  // Bluetooth-Geräteauswahl: Electron hat keinen eigenen Dialog – die App zeigt die Liste selbst an
  win.webContents.on('select-bluetooth-device', (event, devices, callback) => {
    event.preventDefault();
    btCallback = callback;
    win.webContents.send('bt-devices', devices.map(d => ({ id: d.deviceId, name: d.deviceName || 'Unbekanntes Gerät' })));
  });

  win.on('closed', () => { win = null; if (overlay) overlay.destroy(); app.quit(); });
}

function createOverlay() {
  overlayReady = false;
  overlay = new BrowserWindow({
    transparent: true, frame: false, show: false, backgroundColor: '#00000000',
    resizable: false, movable: false, minimizable: false, maximizable: false, fullscreenable: false,
    skipTaskbar: true, focusable: false, hasShadow: false, alwaysOnTop: true,
    webPreferences: {
      preload: path.join(__dirname, 'overlay-preload.js'),
      contextIsolation: true, nodeIntegration: false, backgroundThrottling: false
    }
  });
  overlay.setAlwaysOnTop(true, 'screen-saver');          // höchste Ebene – auch über Vollbild-Videos
  overlay.setIgnoreMouseEvents(true);                    // Klicks gehen durch auf das Fenster darunter
  overlay.setVisibleOnAllWorkspaces(true, { visibleOnFullScreen: true });
  overlay.webContents.once('did-finish-load', () => { overlayReady = true; if (overlayOn) showOverlay(); });
  overlay.loadFile(path.join(__dirname, 'app', 'overlay.html'));
  overlay.on('closed', () => { overlay = null; overlayOn = false; notifyOverlay(); });
}

function showOverlay() {
  // Auf dem Bildschirm einblenden, auf dem gerade die Maus ist
  const d = screen.getDisplayNearestPoint(screen.getCursorScreenPoint());
  overlay.setBounds(d.bounds);
  overlay.showInactive();                                // ohne dem Video den Fokus zu stehlen
  overlay.setAlwaysOnTop(true, 'screen-saver');
  overlay.moveTop();
}

function setOverlay(on) {
  overlayOn = on;
  if (on) {
    if (!overlay) createOverlay();
    else if (overlayReady) showOverlay();
  } else if (overlay) {
    overlay.hide();
  }
  notifyOverlay();
}
const notifyOverlay = () => { if (win) win.webContents.send('overlay-state', overlayOn); };
const sendCmd = c => { if (win) win.webContents.send('cmd', c); };

ipcMain.on('overlay-toggle', () => setOverlay(!overlayOn));
ipcMain.on('overlay-set', (e, on) => setOverlay(!!on));
ipcMain.on('hud-update', (e, state) => { if (overlay && overlayOn && overlayReady) overlay.webContents.send('hud', state); });
ipcMain.on('bt-select', (e, id) => { if (btCallback) { const cb = btCallback; btCallback = null; cb(id || ''); } });
ipcMain.on('ride-active', (e, on) => {
  // Bildschirm während einer Fahrt nicht abschalten
  if (on && psb === null) psb = powerSaveBlocker.start('prevent-display-sleep');
  if (!on && psb !== null) { powerSaveBlocker.stop(psb); psb = null; }
});

// Globale Tastenkürzel – funktionieren auch, wenn YouTube & Co. im Vordergrund sind
const SHORTCUTS = {
  'CommandOrControl+Alt+H': () => setOverlay(!overlayOn),
  'CommandOrControl+Shift+Up': () => sendCmd('gear+'),
  'CommandOrControl+Shift+Down': () => sendCmd('gear-'),
  'CommandOrControl+Alt+P': () => sendCmd('pause'),
  'CommandOrControl+Alt+N': () => sendCmd('skip'),
};
function registerShortcuts() {
  const failed = [];
  for (const [acc, fn] of Object.entries(SHORTCUTS)) { try { if (!globalShortcut.register(acc, fn)) failed.push(acc); } catch (e) { failed.push(acc); } }
  if (failed.length && win) win.webContents.once('did-finish-load', () => win.webContents.send('shortcut-failed', failed));
}

app.whenReady().then(() => { createMain(); registerShortcuts(); });
app.on('will-quit', () => globalShortcut.unregisterAll());
app.on('window-all-closed', () => app.quit());
