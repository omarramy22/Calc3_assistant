// background.js

chrome.runtime.onInstalled.addListener((details) => {
  console.log('Calc3 Assistant installed');

  if (details.reason === 'install') {
    chrome.storage.local.set({
      'calc3_settings': {
        'keepActive': true,
        'autoSave': true,
        'theme': 'light'
      }
    });
  }
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'saveCalculation') {
    chrome.storage.local.get(['calc3_history'], (result) => {
      const history = result.calc3_history || [];
      history.push({
        timestamp: Date.now(),
        operation: request.operation,
        input: request.input,
        result: request.result
      });

      if (history.length > 50) {
        history.splice(0, history.length - 50);
      }

      chrome.storage.local.set({ 'calc3_history': history });
    });
    sendResponse({ status: 'saved' });
  }
  
  return true;
});
