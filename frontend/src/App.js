import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [issueKey, setIssueKey] = useState('KAN-4');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleGenerateTests = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(
        'http://localhost:8000/generate-tests',
        { jira_issue_key: issueKey },
        { headers: { 'Content-Type': 'application/json' } }
      );

      if (response.data.error) {
        setError(response.data.error);
      } else {
        setResult(response.data);
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Error generating tests');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="header">
        <h1>Q360 - Agentic AI Test Platform</h1>
        <p>AI-Powered Test Generation from Jira Stories</p>
      </header>

      <main className="container">
        {/* Input Section */}
        <section className="input-section">
          <form onSubmit={handleGenerateTests}>
            <div className="form-group">
              <label htmlFor="issueKey">Jira Issue Key:</label>
              <input
                type="text"
                id="issueKey"
                value={issueKey}
                onChange={(e) => setIssueKey(e.target.value)}
                placeholder="e.g., KAN-4"
                disabled={loading}
              />
              <button type="submit" disabled={loading} className="btn-primary">
                {loading ? 'Generating Tests...' : 'Generate Tests'}
              </button>
            </div>
          </form>
        </section>

        {/* Error Section */}
        {error && (
          <section className="error-section">
            <h3>Error</h3>
            <p>{error}</p>
          </section>
        )}

        {/* Results Section */}
        {result && !error && (
          <section className="results-section">
            {/* Story Info */}
            <div className="story-info">
              <h2>{result.story_summary}</h2>
              <p className="issue-key">Issue: {result.jira_issue_key}</p>
            </div>

            {/* Test Cases */}
            {result.test_cases && result.test_cases.length > 0 && (
              <div className="test-cases-section">
                <h3>Generated Test Cases ({result.test_cases.length})</h3>
                <div className="test-cases-list">
                  {result.test_cases.map((tc, idx) => (
                    <div key={idx} className="test-case-card">
                      <div className="test-case-header">
                        <span className="test-id">{tc.test_id}</span>
                        <span className={`test-type ${tc.test_type}`}>
                          {tc.test_type.toUpperCase()}
                        </span>
                        <span className={`priority ${tc.priority}`}>
                          {tc.priority.toUpperCase()}
                        </span>
                      </div>
                      <h4>{tc.title}</h4>
                      <p className="description">{tc.description}</p>
                      <div className="steps">
                        <strong>Steps:</strong>
                        <ol>
                          {tc.steps.map((step, i) => (
                            <li key={i}>{step}</li>
                          ))}
                        </ol>
                      </div>
                      <div className="expected-result">
                        <strong>Expected Result:</strong>
                        <p>{tc.expected_result}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Test Data */}
            {result.test_data && result.test_data.length > 0 && (
              <div className="test-data-section">
                <h3>Generated Test Data ({result.test_data.length})</h3>
                <div className="test-data-list">
                  {result.test_data.reduce((acc, td) => {
                    const existing = acc.find(
                      (group) => group.field === td.field_name
                    );
                    if (existing) {
                      existing.data.push(td);
                    } else {
                      acc.push({ field: td.field_name, data: [td] });
                    }
                    return acc;
                  }, []).map((group, idx) => (
                    <div key={idx} className="test-data-field">
                      <h4>{group.field}</h4>
                      <div className="test-data-items">
                        {group.data.map((td, i) => (
                          <div key={i} className="test-data-item">
                            <span className={`category ${td.test_category}`}>
                              {td.test_category}
                            </span>
                            <span className="value">{td.sample_value}</span>
                            <span className="type">({td.data_type})</span>
                            <span className="constraints">
                              {td.constraints}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Summary */}
            <div className="summary">
              <h3>Summary</h3>
              <p>
                Generated <strong>{result.test_cases?.length || 0}</strong> test
                cases and <strong>{result.test_data?.length || 0}</strong> test
                data points for this story.
              </p>
            </div>
          </section>
        )}

        {/* Empty State */}
        {!result && !error && !loading && (
          <section className="empty-state">
            <p>Enter a Jira issue key and click "Generate Tests" to get started</p>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
