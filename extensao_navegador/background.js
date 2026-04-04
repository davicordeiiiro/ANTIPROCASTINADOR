let endTime = 0;
let focusTech = '';
let focusMins = 0;
let allowedSites = [];

// Load Config
chrome.storage.local.get(['endTime', 'focusTech', 'focusMins', 'allowedSites'], (res) => {
  endTime = res.endTime || 0;
  focusTech = res.focusTech || '';
  focusMins = res.focusMins || 0;
  allowedSites = res.allowedSites || [];
});

// Message Handling
chrome.runtime.onMessage.addListener((req, sender, sendResponse) => {
  if (req.action === 'START_TIMER') {
    focusMins = req.mins;
    focusTech = req.tech;
    endTime = Date.now() + (req.mins * 60 * 1000);
    
    chrome.storage.local.set({ endTime, focusTech, focusMins });
    chrome.alarms.create('focustimer', { delayInMinutes: req.mins });
    
    sendResponse({ success: true, endTime });
  } 
  else if (req.action === 'STOP_TIMER') {
    endTime = 0;
    chrome.storage.local.set({ endTime: 0 });
    chrome.alarms.clear('focustimer');
    sendResponse({ success: true });
  } 
  else if (req.action === 'GET_STATE') {
    sendResponse({ endTime, focusTech, focusMins, allowedSites });
  } 
  else if (req.action === 'SET_SITES') {
    allowedSites = req.sites;
    chrome.storage.local.set({ allowedSites });
    sendResponse({ success: true });
  }
  return true;
});

// Alarm triggers when focus time is up
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'focustimer') {
    // Notification
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icon128.png',
      title: '🚀 Fim do Ciclo!',
      message: `Você concluiu ${focusMins} min em ${focusTech}.`
    });

    // Save history
    chrome.storage.local.get(['historico'], (res) => {
      let relatorio = res.historico || {};
      relatorio[focusTech] = (relatorio[focusTech] || 0) + focusMins;
      chrome.storage.local.set({ historico: relatorio, endTime: 0 });
    });

    endTime = 0;
  }
});

// Block distracting sites
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (endTime > Date.now() && changeInfo.url) {
    checkAndBlock(tabId, changeInfo.url);
  }
});

chrome.tabs.onActivated.addListener(activeInfo => {
  if (endTime > Date.now()) {
    chrome.tabs.get(activeInfo.tabId, (tab) => {
      if(tab.url) checkAndBlock(tab.id, tab.url);
    });
  }
});

function checkAndBlock(tabId, urlStr) {
  try {
    const url = new URL(urlStr);
    
    // Block ONLY http and https. Keep chrome://, edge://, file://, etc safe.
    if (url.protocol !== 'http:' && url.protocol !== 'https:') return;

    const hostname = url.hostname.toLowerCase();
    
    let isAllowed = false;
    for (const site of allowedSites) {
      const lowerSite = site.trim().toLowerCase();
      if (lowerSite && hostname.includes(lowerSite)) {
        isAllowed = true;
        break;
      }
    }

    if (!isAllowed) {
      const blockUrl = chrome.runtime.getURL(`block.html?domain=${encodeURIComponent(hostname)}&tech=${encodeURIComponent(focusTech)}`);
      chrome.tabs.update(tabId, { url: blockUrl });
    }
  } catch (e) {
    console.error("Invalid URL", e);
  }
}
