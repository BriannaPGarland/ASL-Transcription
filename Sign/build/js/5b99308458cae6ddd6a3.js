var {
  BrowserWindow,
  app
} = require('electron');

var path = require('path');

function createWindow() {
  var win = new BrowserWindow({
    width: 1200,
    height: 800,
    backgroundColor: "#757BC8",
    webPreferences: {
      nodeIntegration: false,
      worldSafeExecuteJavaScript: true,
      contextIsolation: true
    }
  });
  win.loadFile('index.html');
}

require('electron-reload')(__dirname, {
  electron: path.join(__dirname, 'node_modules', '.bin', 'electron')
});

app.whenReady().then(createWindow);