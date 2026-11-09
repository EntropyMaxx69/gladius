const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('overlayBridge', {
  onHud: cb => ipcRenderer.on('hud', (e, state) => cb(state)),
});
