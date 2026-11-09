// Brücke zwischen Gladius (Webseite) und dem Desktop-Hauptprozess
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('gladiusDesktop', {
  isDesktop: true,
  hud: state => ipcRenderer.send('hud-update', state),
  toggleOverlay: () => ipcRenderer.send('overlay-toggle'),
  setOverlay: on => ipcRenderer.send('overlay-set', on),
  onOverlayState: cb => ipcRenderer.on('overlay-state', (e, on) => cb(on)),
  onCommand: cb => ipcRenderer.on('cmd', (e, c) => cb(c)),
  onBtDevices: cb => ipcRenderer.on('bt-devices', (e, list) => cb(list)),
  selectBt: id => ipcRenderer.send('bt-select', id),
  rideActive: on => ipcRenderer.send('ride-active', on),
  onShortcutFailed: cb => ipcRenderer.on('shortcut-failed', (e, list) => cb(list)),
  mediaKey: k => ipcRenderer.send('media-key', k),
  platform: process.platform,
});
