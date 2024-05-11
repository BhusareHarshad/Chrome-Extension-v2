import './App.css'
import summaryLogo from './assets/summary.png'
 

function Summary(){
  const getPageHTML = () => {
    return document.documentElement.outerHTML;
  };

  function summarizePage(){
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const tab = tabs?.[0];
      console.log(tab)
      if (tab) {
        chrome.scripting.executeScript({
          target: { tabId: tab.id || 1},
          func: getPageHTML,
        }, (results) => {
          const htmlContent = results?.[0]?.result;
          if (htmlContent) {
            console.log(htmlContent)
            //sendDataToBackend(htmlContent);
          } else {
            console.error('Failed to retrieve HTML content');
          }
        });
      } else {
        console.error('No active tab found');
      }
    });
  }

  return (
    <>
    <div>
      <img src={summaryLogo} className="logo"/>
    </div>
    <div className='card'>
      <button onClick={summarizePage}>
        Summarize
      </button>
    </div>
    </>
  )
}

export default Summary