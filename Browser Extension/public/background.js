chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "openManager",
    title: "Open Password Manager",
    contexts: ["all"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "openManager") {
    chrome.action.openPopup();
  }
});
