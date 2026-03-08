// Open side panel when extension icon is clicked
chrome.action.onClicked.addListener((tab) => {
  chrome.sidePanel.open({ tabId: tab.id });
});

// Auto-open side panel for every tab
chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });
