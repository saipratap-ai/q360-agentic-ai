import React, { useState, useEffect } from 'react';
import './App.css';

// Icons as simple SVG components
const Icons = {
  Dashboard: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>,
  TestGen: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="1"/><path d="M9 14l2 2 4-4"/></svg>,
  Automation: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/><line x1="12" y1="2" x2="12" y2="22"/></svg>,
  Analytics: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>,
  Jira: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="3"/><path d="M12 1v6m0 6v6m-7-7h6m6 0h6"/></svg>,
  Settings: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 012.83-2.83l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z"/></svg>,
  Traceability: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>,
  Execution: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>,
  Chevron: () => <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="9 18 15 12 9 6"/></svg>,
  Check: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="20 6 9 17 4 12"/></svg>,
  Clock: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>,
  Alert: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>,
};

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Auto-detect API URL: same origin for production, localhost:8001 for local dev
  const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:8001'
    : '';

  // Test Generation State
  const [projects, setProjects] = useState([]);
  const [issues, setIssues] = useState([]);
  const [selectedProject, setSelectedProject] = useState('');
  const [selectedIssue, setSelectedIssue] = useState('');
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(null);
  const [testCases, setTestCases] = useState([]);
  const [testData, setTestData] = useState([]);
  const [storyInfo, setStoryInfo] = useState(null);
  const [dataSource, setDataSource] = useState({ projects: 'loading', issues: 'loading' }); // 'real' | 'mock' | 'loading'
  const [jiraConnected, setJiraConnected] = useState(null); // null = checking, true/false

  // Mock data fallbacks
  const mockProjects = [
    { key: 'KAN', name: 'QA Testing', type: 'software' },
    { key: 'SAM1', name: '(Example) Billing System Dev', type: 'software' }
  ];
  const mockIssuesMap = {
    KAN: [
      { key: 'KAN-10', summary: 'User Login Feature', status: 'Ready for QA', type: 'Story' },
      { key: 'KAN-11', summary: 'User Registration Flow', status: 'In Progress', type: 'Story' },
      { key: 'KAN-12', summary: 'Password Reset Feature', status: 'To Do', type: 'Story' },
    ],
    SAM1: [
      { key: 'SAM1-1', summary: 'Invoice Generation System', status: 'Ready for QA', type: 'Story' },
      { key: 'SAM1-2', summary: 'Payment Processing', status: 'In Progress', type: 'Story' },
    ]
  };

  // Fetch REAL projects from API on mount
  useEffect(() => {
    fetch(`${API_URL}/api/jira/projects`)
      .then(res => {
        if (!res.ok) throw new Error('API unavailable');
        return res.json();
      })
      .then(data => {
        setProjects(data.projects);
        setDataSource(prev => ({ ...prev, projects: 'real' }));
        setJiraConnected(true);
        if (data.projects.length > 0) {
          setSelectedProject(data.projects[0].key);
        }
      })
      .catch(() => {
        console.log('[Q360] API unavailable, using mock data');
        setProjects(mockProjects);
        setDataSource(prev => ({ ...prev, projects: 'mock' }));
        setJiraConnected(false);
        setSelectedProject('KAN');
      });
  }, []);

  // Fetch REAL issues when project changes
  useEffect(() => {
    if (!selectedProject) return;

    fetch(`${API_URL}/api/jira/issues?project=${selectedProject}`)
      .then(res => {
        if (!res.ok) throw new Error('API unavailable');
        return res.json();
      })
      .then(data => {
        setIssues(data.issues);
        setDataSource(prev => ({ ...prev, issues: 'real' }));
        if (data.issues.length > 0) {
          setSelectedIssue(data.issues[0].key);
        }
      })
      .catch(() => {
        const mock = mockIssuesMap[selectedProject] || [];
        setIssues(mock);
        setDataSource(prev => ({ ...prev, issues: 'mock' }));
        if (mock.length > 0) setSelectedIssue(mock[0].key);
      });
  }, [selectedProject]);

  const mockTestCases = [
    {
      test_id: 'TC-001', title: 'Valid user login with correct credentials',
      description: 'Verify that a registered user can successfully log in with valid email and password',
      test_type: 'positive', priority: 'high',
      steps: ['Navigate to login page', 'Enter valid email: test@example.com', 'Enter valid password: Password123!', 'Click Login button', 'Wait for dashboard redirect'],
      expected_result: 'User is authenticated and redirected to the main dashboard'
    },
    {
      test_id: 'TC-002', title: 'Login with invalid password',
      description: 'Verify proper error handling when user enters incorrect password',
      test_type: 'negative', priority: 'high',
      steps: ['Navigate to login page', 'Enter valid email: test@example.com', 'Enter invalid password: WrongPass!', 'Click Login button'],
      expected_result: 'Error message "Invalid credentials" displayed, user stays on login page'
    },
    {
      test_id: 'TC-003', title: 'Login with empty email field',
      description: 'Verify client-side validation prevents empty email submission',
      test_type: 'negative', priority: 'medium',
      steps: ['Navigate to login page', 'Leave email field empty', 'Enter password: Password123!', 'Click Login button'],
      expected_result: 'Validation error "Email is required" appears'
    },
    {
      test_id: 'TC-004', title: 'Login with SQL injection in email',
      description: 'Verify security against SQL injection attacks in login form',
      test_type: 'edge', priority: 'high',
      steps: ['Navigate to login page', "Enter email: ' OR 1=1 --", 'Enter password: anything', 'Click Login button'],
      expected_result: 'Input is sanitized, error message shown, no data breach'
    },
    {
      test_id: 'TC-005', title: 'Session timeout after inactivity',
      description: 'Verify user session expires after configured idle timeout',
      test_type: 'edge', priority: 'medium',
      steps: ['Login with valid credentials', 'Wait for session timeout period (30 min)', 'Attempt to navigate to a protected page'],
      expected_result: 'User is redirected to login page with "Session expired" message'
    },
  ];

  const mockTestData = [
    { field_name: 'Email', test_category: 'valid', sample_value: 'john.doe@example.com', data_type: 'string', constraints: 'Registered user, valid format' },
    { field_name: 'Email', test_category: 'valid', sample_value: 'admin@healthcare.org', data_type: 'string', constraints: 'Admin role, corporate domain' },
    { field_name: 'Email', test_category: 'invalid', sample_value: 'not-an-email', data_type: 'string', constraints: 'Missing @ and domain' },
    { field_name: 'Email', test_category: 'invalid', sample_value: '@empty-local.com', data_type: 'string', constraints: 'Empty local part' },
    { field_name: 'Email', test_category: 'boundary', sample_value: 'a@b.co', data_type: 'string', constraints: 'Minimum valid length' },
    { field_name: 'Email', test_category: 'boundary', sample_value: `${'a'.repeat(64)}@${'b'.repeat(63)}.com`, data_type: 'string', constraints: 'Maximum length (RFC 5321)' },
    { field_name: 'Password', test_category: 'valid', sample_value: 'Secure@Pass123', data_type: 'string', constraints: '14 chars, mixed case, number, special' },
    { field_name: 'Password', test_category: 'invalid', sample_value: '1234', data_type: 'string', constraints: 'Below minimum 8 chars' },
    { field_name: 'Password', test_category: 'boundary', sample_value: 'Ab1!Ab1!', data_type: 'string', constraints: 'Exactly 8 chars (minimum)' },
  ];

  const handleGenerateTests = async (e) => {
    e.preventDefault();
    setLoading(true);
    setProgress(null);
    setTestCases([]);
    setTestData([]);
    setStoryInfo(null);

    // Try REAL API first (streaming)
    try {
      const response = await fetch(`${API_URL}/api/generate-tests/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ jira_issue_key: selectedIssue })
      });

      if (response.ok && response.headers.get('content-type')?.includes('text/event-stream')) {
        // REAL STREAMING from backend
        console.log('[Q360] Using REAL API streaming');
        const fullText = await response.text();
        console.log('[Q360] Stream received, length:', fullText.length);

        // Parse all SSE events from the response
        const sseLines = fullText.split('\n');
        for (const line of sseLines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.type === 'status') {
                setProgress({ message: data.message });
              } else if (data.type === 'story') {
                const issue = issues.find(i => i.key === selectedIssue);
                setStoryInfo({
                  key: data.data.key, summary: data.data.summary,
                  status: issue?.status || 'Ready for QA', type: issue?.type || 'Story'
                });
              } else if (data.type === 'progress') {
                setProgress({ message: data.message });
              } else if (data.type === 'test_case') {
                setTestCases(prev => [...prev, data.data]);
              } else if (data.type === 'test_data') {
                setTestData(prev => [...prev, data.data]);
              } else if (data.type === 'complete') {
                setProgress(null);
              } else if (data.type === 'error') {
                throw new Error(data.message);
              }
            } catch (parseErr) {
              if (parseErr.message && !parseErr.message.includes('Unexpected')) throw parseErr;
              console.log('[Q360] Parse skip:', line.substring(0, 50));
            }
          }
        }
        setProgress(null);
        setLoading(false);
        return; // Success with real API
      }
    } catch (apiError) {
      console.log('[Q360] API unavailable, falling back to mock:', apiError.message);
    }

    // FALLBACK: Mock streaming
    const steps = [
      { msg: 'Connecting to Jira API...', delay: 600 },
      { msg: 'Fetching story details & acceptance criteria...', delay: 800 },
      { msg: 'AI Agent analyzing requirements...', delay: 1200 },
      { msg: 'Generating test scenarios...', delay: 800 },
    ];

    for (const step of steps) {
      setProgress({ message: step.msg });
      await new Promise(r => setTimeout(r, step.delay));
    }

    const issue = issues.find(i => i.key === selectedIssue);
    setStoryInfo({
      key: selectedIssue,
      summary: issue?.summary || 'Feature',
      status: issue?.status || 'Ready for QA',
      type: issue?.type || 'Story'
    });

    for (let i = 0; i < mockTestCases.length; i++) {
      setProgress({ message: `Generating test case ${i + 1} of ${mockTestCases.length}...` });
      await new Promise(r => setTimeout(r, 700));
      setTestCases(prev => [...prev, mockTestCases[i]]);
    }

    setProgress({ message: 'Generating test data variants...' });
    await new Promise(r => setTimeout(r, 500));

    for (let i = 0; i < mockTestData.length; i++) {
      setProgress({ message: `Creating test data ${i + 1} of ${mockTestData.length}...` });
      await new Promise(r => setTimeout(r, 400));
      setTestData(prev => [...prev, mockTestData[i]]);
    }

    setProgress(null);
    setLoading(false);
  };

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Icons.Dashboard },
    { id: 'generate', label: 'Test Generation', icon: Icons.TestGen },
    { id: 'automation', label: 'Automation', icon: Icons.Automation },
    { id: 'execution', label: 'Execution', icon: Icons.Execution },
    { id: 'analytics', label: 'Analytics', icon: Icons.Analytics },
    { id: 'traceability', label: 'Traceability', icon: Icons.Traceability },
    { id: 'settings', label: 'Settings', icon: Icons.Settings },
  ];

  // Dashboard metrics
  const dashboardMetrics = {
    totalTests: 247,
    automated: 189,
    passed: 203,
    failed: 12,
    pending: 32,
    coverage: 87,
    automationRate: 76,
  };

  const recentActivity = [
    { action: 'Test cases generated', detail: 'KAN-10: User Login Feature', time: '2 min ago', status: 'success' },
    { action: 'Automation script created', detail: 'TC-001 to TC-005 Selenium scripts', time: '15 min ago', status: 'success' },
    { action: 'Execution completed', detail: 'Regression Suite - Sprint 14', time: '1 hr ago', status: 'warning' },
    { action: 'Defect auto-created', detail: 'KAN-45: Login timeout not handled', time: '2 hrs ago', status: 'error' },
    { action: 'Test cases synced to qTest', detail: '12 test cases pushed', time: '3 hrs ago', status: 'success' },
  ];

  const renderDashboard = () => (
    <div className="page-content">
      <div className="page-header">
        <div>
          <h2>Dashboard</h2>
          <p className="page-subtitle">Real-time QA metrics and activity overview</p>
        </div>
        <div className="header-actions">
          <span className="live-badge">LIVE</span>
          <span className="date-badge">Sprint 14 &middot; Jun 2026</span>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon blue"><Icons.TestGen /></div>
          <div className="metric-info">
            <span className="metric-value">{dashboardMetrics.totalTests}</span>
            <span className="metric-label">Total Test Cases</span>
          </div>
        </div>
        <div className="metric-card">
          <div className="metric-icon green"><Icons.Check /></div>
          <div className="metric-info">
            <span className="metric-value">{dashboardMetrics.passed}</span>
            <span className="metric-label">Passed</span>
          </div>
        </div>
        <div className="metric-card">
          <div className="metric-icon red"><Icons.Alert /></div>
          <div className="metric-info">
            <span className="metric-value">{dashboardMetrics.failed}</span>
            <span className="metric-label">Failed</span>
          </div>
        </div>
        <div className="metric-card">
          <div className="metric-icon yellow"><Icons.Clock /></div>
          <div className="metric-info">
            <span className="metric-value">{dashboardMetrics.pending}</span>
            <span className="metric-label">Pending</span>
          </div>
        </div>
      </div>

      {/* Progress Bars */}
      <div className="dashboard-row">
        <div className="dashboard-card">
          <h3>Test Coverage</h3>
          <div className="progress-ring-container">
            <div className="progress-ring">
              <svg viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="50" fill="none" stroke="rgba(99,102,241,0.1)" strokeWidth="10"/>
                <circle cx="60" cy="60" r="50" fill="none" stroke="#6366f1" strokeWidth="10"
                  strokeDasharray={`${dashboardMetrics.coverage * 3.14} 314`}
                  strokeLinecap="round" transform="rotate(-90 60 60)"/>
              </svg>
              <div className="ring-value">{dashboardMetrics.coverage}%</div>
            </div>
            <div className="ring-details">
              <div className="ring-detail-item"><span className="dot green"></span>Covered: {dashboardMetrics.coverage}%</div>
              <div className="ring-detail-item"><span className="dot red"></span>Uncovered: {100 - dashboardMetrics.coverage}%</div>
            </div>
          </div>
        </div>

        <div className="dashboard-card">
          <h3>Automation Rate</h3>
          <div className="progress-ring-container">
            <div className="progress-ring">
              <svg viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="50" fill="none" stroke="rgba(139,92,246,0.1)" strokeWidth="10"/>
                <circle cx="60" cy="60" r="50" fill="none" stroke="#8b5cf6" strokeWidth="10"
                  strokeDasharray={`${dashboardMetrics.automationRate * 3.14} 314`}
                  strokeLinecap="round" transform="rotate(-90 60 60)"/>
              </svg>
              <div className="ring-value">{dashboardMetrics.automationRate}%</div>
            </div>
            <div className="ring-details">
              <div className="ring-detail-item"><span className="dot purple"></span>Automated: {dashboardMetrics.automated}</div>
              <div className="ring-detail-item"><span className="dot gray"></span>Manual: {dashboardMetrics.totalTests - dashboardMetrics.automated}</div>
            </div>
          </div>
        </div>

        <div className="dashboard-card full-width">
          <h3>Recent Activity</h3>
          <div className="activity-list">
            {recentActivity.map((item, idx) => (
              <div key={idx} className="activity-item">
                <div className={`activity-dot ${item.status}`}></div>
                <div className="activity-content">
                  <span className="activity-action">{item.action}</span>
                  <span className="activity-detail">{item.detail}</span>
                </div>
                <span className="activity-time">{item.time}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const renderTestGeneration = () => (
    <div className="page-content">
      <div className="page-header">
        <div>
          <h2>AI Test Generation</h2>
          <p className="page-subtitle">Generate test cases from Jira stories using AI agents</p>
        </div>
      </div>

      {/* Source Selection */}
      <div className="card">
        <div className="card-header">
          <h3>Source Selection</h3>
          <div className="source-badges">
            <span className={`source-indicator ${dataSource.projects}`}>
              Projects: {dataSource.projects === 'real' ? 'LIVE' : dataSource.projects === 'mock' ? 'MOCK' : '...'}
            </span>
            <span className={`source-indicator ${dataSource.issues}`}>
              Issues: {dataSource.issues === 'real' ? 'LIVE' : dataSource.issues === 'mock' ? 'MOCK' : '...'}
            </span>
          </div>
        </div>
        <form onSubmit={handleGenerateTests}>
          <div className="source-grid">
            <div className="field">
              <label>Project</label>
              <select value={selectedProject} onChange={e => setSelectedProject(e.target.value)} disabled={loading}>
                {projects.map(p => <option key={p.key} value={p.key}>{p.key} - {p.name}</option>)}
              </select>
            </div>
            <div className="field">
              <label>Issue</label>
              <select value={selectedIssue} onChange={e => setSelectedIssue(e.target.value)} disabled={loading}>
                {issues.map(i => <option key={i.key} value={i.key}>{i.key} - {i.summary}</option>)}
              </select>
            </div>
            <div className="field">
              <label>&nbsp;</label>
              <button type="submit" disabled={loading} className="btn-generate">
                {loading ? (
                  <><span className="btn-spinner"></span> Generating...</>
                ) : (
                  <><Icons.TestGen /> Generate Tests</>
                )}
              </button>
            </div>
          </div>
        </form>
      </div>

      {/* Agent Pipeline Progress */}
      {progress && (
        <div className="card agent-progress">
          <div className="agent-pipeline">
            <div className="pipeline-step active">
              <div className="pipeline-dot"><span className="pulse"></span></div>
              <span>{progress.message}</span>
            </div>
          </div>
        </div>
      )}

      {/* Story Info */}
      {storyInfo && (
        <div className="card story-card">
          <div className="story-header">
            <div className="story-meta">
              <span className="story-key">{storyInfo.key}</span>
              <span className={`story-status ${storyInfo.status.replace(/\s/g, '-').toLowerCase()}`}>{storyInfo.status}</span>
              <span className="story-type">{storyInfo.type}</span>
            </div>
            <h3>{storyInfo.summary}</h3>
          </div>
          {(testCases.length > 0 || testData.length > 0) && (
            <div className="story-stats">
              <div className="story-stat">
                <span className="story-stat-value">{testCases.length}</span>
                <span className="story-stat-label">Test Cases</span>
              </div>
              <div className="story-stat">
                <span className="story-stat-value">{testData.length}</span>
                <span className="story-stat-label">Data Points</span>
              </div>
              <div className="story-stat">
                <span className="story-stat-value">{testCases.filter(t => t.test_type === 'positive').length}</span>
                <span className="story-stat-label">Positive</span>
              </div>
              <div className="story-stat">
                <span className="story-stat-value">{testCases.filter(t => t.test_type === 'negative').length}</span>
                <span className="story-stat-label">Negative</span>
              </div>
              <div className="story-stat">
                <span className="story-stat-value">{testCases.filter(t => t.test_type === 'edge').length}</span>
                <span className="story-stat-label">Edge</span>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Test Cases Table */}
      {testCases.length > 0 && (
        <div className="card">
          <div className="card-header">
            <h3>Generated Test Cases</h3>
            <div className="card-actions">
              <button className="btn-outline">Export CSV</button>
              <button className="btn-outline">Sync to qTest</button>
              <button className="btn-outline btn-approve">Approve All</button>
            </div>
          </div>
          <div className="test-table">
            <div className="table-header">
              <span className="col-id">ID</span>
              <span className="col-title">Title</span>
              <span className="col-type">Type</span>
              <span className="col-priority">Priority</span>
              <span className="col-status">Status</span>
              <span className="col-actions">Actions</span>
            </div>
            {testCases.map((tc, idx) => (
              <TestCaseRow key={idx} tc={tc} />
            ))}
          </div>
        </div>
      )}

      {/* Test Data */}
      {testData.length > 0 && (
        <div className="card">
          <div className="card-header">
            <h3>Generated Test Data</h3>
            <button className="btn-outline">Export</button>
          </div>
          <div className="data-table">
            <div className="data-table-header">
              <span>Field</span>
              <span>Category</span>
              <span>Sample Value</span>
              <span>Type</span>
              <span>Constraints</span>
            </div>
            {testData.map((td, idx) => (
              <div key={idx} className="data-table-row fade-in">
                <span className="data-field">{td.field_name}</span>
                <span><span className={`badge ${td.test_category}`}>{td.test_category}</span></span>
                <span className="data-value">{td.sample_value}</span>
                <span className="data-type">{td.data_type}</span>
                <span className="data-constraint">{td.constraints}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Completion */}
      {testCases.length > 0 && testData.length > 0 && !loading && (
        <div className="completion-banner">
          <Icons.Check />
          <span>Generation complete &mdash; {testCases.length} test cases and {testData.length} data points ready for review</span>
        </div>
      )}
    </div>
  );

  const renderPlaceholder = (title, desc) => (
    <div className="page-content">
      <div className="page-header">
        <div>
          <h2>{title}</h2>
          <p className="page-subtitle">{desc}</p>
        </div>
      </div>
      <div className="placeholder-card">
        <div className="placeholder-icon">
          {title === 'Automation' && <Icons.Automation />}
          {title === 'Execution' && <Icons.Execution />}
          {title === 'Analytics' && <Icons.Analytics />}
          {title === 'Traceability' && <Icons.Traceability />}
          {title === 'Settings' && <Icons.Settings />}
        </div>
        <h3>{title} Module</h3>
        <p>This module is under development. It will include full {title.toLowerCase()} capabilities as defined in the Q360 PRD.</p>
        <span className="coming-soon">Coming in Phase 2</span>
      </div>
    </div>
  );

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard': return renderDashboard();
      case 'generate': return renderTestGeneration();
      case 'automation': return renderPlaceholder('Automation', 'Selenium & Rest Assured script generation');
      case 'execution': return renderPlaceholder('Execution', 'CI/CD pipeline integration & parallel execution');
      case 'analytics': return renderPlaceholder('Analytics', 'Test coverage, defect density & performance insights');
      case 'traceability': return renderPlaceholder('Traceability', 'Requirement to defect mapping & RTM');
      case 'settings': return renderPlaceholder('Settings', 'Integrations, user management & configuration');
      default: return renderDashboard();
    }
  };

  return (
    <div className="app-layout">
      {/* Mobile Overlay */}
      {mobileMenuOpen && <div className="mobile-overlay" onClick={() => setMobileMenuOpen(false)}></div>}

      {/* Sidebar */}
      <aside className={`sidebar ${sidebarCollapsed ? 'collapsed' : ''} ${mobileMenuOpen ? 'mobile-open' : ''}`}>
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <div className="logo-mark">Q3</div>
            {!sidebarCollapsed && <span className="logo-text">Q360</span>}
          </div>
          <button className="collapse-btn" onClick={() => setSidebarCollapsed(!sidebarCollapsed)}>
            <Icons.Chevron />
          </button>
        </div>

        <nav className="sidebar-nav">
          {navItems.map(item => (
            <button
              key={item.id}
              className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
              onClick={() => { setActiveTab(item.id); setMobileMenuOpen(false); }}
              title={sidebarCollapsed ? item.label : ''}
            >
              <item.icon />
              {!sidebarCollapsed && <span>{item.label}</span>}
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          {!sidebarCollapsed && (
            <div className="user-info">
              <div className="user-avatar">QA</div>
              <div className="user-details">
                <span className="user-name">QA Engineer</span>
                <span className="user-role">Platform User</span>
              </div>
            </div>
          )}
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {/* Top Bar */}
        <header className="topbar">
          <div className="topbar-left">
            <button className="hamburger" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
              <span></span><span></span><span></span>
            </button>
            <div className="breadcrumb">
              <span>Q360</span>
              <Icons.Chevron />
              <span className="breadcrumb-active">{navItems.find(n => n.id === activeTab)?.label}</span>
            </div>
          </div>
          <div className="topbar-right">
            <div className={`data-source-badge ${jiraConnected ? 'real' : 'mock'}`}>
              {jiraConnected === null ? 'Checking...' : jiraConnected ? 'LIVE DATA' : 'MOCK DATA'}
            </div>
            <div className="integration-status">
              <span className={`int-dot ${jiraConnected ? 'online' : 'offline'}`}></span>
              <span>Jira</span>
            </div>
            <div className="integration-status">
              <span className="int-dot offline"></span>
              <span>qTest</span>
            </div>
            <div className="integration-status">
              <span className="int-dot offline"></span>
              <span>Jenkins</span>
            </div>
          </div>
        </header>

        {/* Page Content */}
        {renderContent()}
      </main>
    </div>
  );
}

function TestCaseRow({ tc }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className={`table-row-wrapper fade-in ${expanded ? 'expanded' : ''}`}>
      <div className="table-row" onClick={() => setExpanded(!expanded)}>
        <span className="col-id"><span className="id-badge">{tc.test_id}</span></span>
        <span className="col-title">{tc.title}</span>
        <span className="col-type"><span className={`badge ${tc.test_type}`}>{tc.test_type}</span></span>
        <span className="col-priority"><span className={`badge priority-${tc.priority}`}>{tc.priority}</span></span>
        <span className="col-status"><span className="badge pending">Pending Review</span></span>
        <span className="col-actions">
          <button className="icon-btn approve-btn" title="Approve" onClick={e => e.stopPropagation()}>
            <Icons.Check />
          </button>
          <span className={`expand-icon ${expanded ? 'rotated' : ''}`}><Icons.Chevron /></span>
        </span>
      </div>
      {expanded && (
        <div className="row-detail">
          <p className="detail-desc">{tc.description}</p>
          <div className="detail-columns">
            <div className="detail-col">
              <h4>Steps</h4>
              <ol>
                {tc.steps.map((s, i) => <li key={i}>{s}</li>)}
              </ol>
            </div>
            <div className="detail-col">
              <h4>Expected Result</h4>
              <p className="expected">{tc.expected_result}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
