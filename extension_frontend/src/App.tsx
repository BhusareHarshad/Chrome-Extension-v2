import { useState } from 'react';
import './App.css';
import summaryLogo from './assets/summary.png';
import axios from 'axios';

function Summary() {
  const [loading, setLoading] = useState(false);
  const [summaryData, setSummaryData] = useState('');

  const getPageHTML = () => {
    return document.documentElement.outerHTML;
  };

  function getTabId(tab: any) {
    return tab.id;
  }

  async function sendDataToBackend(htmlContent: String) {
    try {
      setLoading(true);
      const response = await axios.post('http://127.0.0.1:8000/summarize', {
        htmldata: htmlContent,
      });
      const extractedData = response.data.data;
      setSummaryData(extractedData); // Assuming the response contains summary data
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  }

  function summarizePage() {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const tab = tabs?.[0];
      if (tab) {
        chrome.scripting.executeScript(
          {
            target: { tabId: getTabId(tab) },
            func: getPageHTML,
          },
          (results) => {
            const htmlContent = results?.[0]?.result;
            if (htmlContent) {
              sendDataToBackend(htmlContent);
            } else {
              console.error('Failed to retrieve HTML content');
            }
          }
        );
      } else {
        console.error('No active tab found');
      }
    });
  }

  return (
    <>
      <div>
        <img src={summaryLogo} className="logo" alt="Summary Logo" />
      </div>
      <div className='card'>
        <button onClick={summarizePage} disabled={loading}>
          {loading ? 'Loading...' : 'Summarize'}
        </button>
        {summaryData && (
          <div className="summary-data">
            <h2>Summary</h2>
            <p>{summaryData}</p>
          </div>
        )}
      </div>
    </>
  );
}

export default Summary;
