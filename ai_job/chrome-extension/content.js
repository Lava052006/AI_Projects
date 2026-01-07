// Job Scam Detector - Content Script
// Automatically detects and marks job posts on webpages

console.log('🎯 Job Detector Extension Loaded!');
console.log('Current URL:', window.location.href);
console.log('Page title:', document.title);
console.log("TrustHire content script loaded");


const API_BASE_URL = 'http://localhost:8000';
const EXTENSION_PREFIX = 'job-scam-detector';

// Configuration
// content.js - Extracts and analyzes jobs on LinkedIn
// content.js - LinkedIn Job Detector

class LinkedInJobDetector {
  constructor() {
    this.analyzedJobs = new Set();
    this.isProcessing = false;
    this.init();
  }

  init() {
    console.log('🔍 Initializing Job Detector...');
    
    // Wait for page to be ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.start());
    } else {
      this.start();
    }
  }

  start() {
    // Small delay to let LinkedIn render
    setTimeout(() => {
      this.scanForJobs();
      this.setupObserver();
    }, 2000);
  }

  scanForJobs() {
    console.log('📊 Scanning for jobs...');

    // LinkedIn job cards - multiple selectors for different layouts
    const selectors = [
      '.jobs-search-results__list-item',
      '.scaffold-layout__list-item',
      '.job-card-container',
      '.jobs-search-results-list__list-item'
    ];

    let jobCards = [];
    for (const selector of selectors) {
      const elements = document.querySelectorAll(selector);
      if (elements.length > 0) {
        jobCards = Array.from(elements);
        console.log(`✅ Found ${jobCards.length} jobs using selector: ${selector}`);
        break;
      }
    }

    if (jobCards.length === 0) {
      console.log('⚠️ No job cards found. Trying detailed view...');
      this.checkDetailedView();
      return;
    }

    // Analyze each job card
    jobCards.forEach((card, index) => {
      const jobId = this.getJobId(card, index);
      if (!this.analyzedJobs.has(jobId)) {
        console.log(`🔎 Analyzing job ${index + 1}/${jobCards.length}`);
        this.analyzeJobCard(card, jobId);
      }
    });
  }

  checkDetailedView() {
    // Check if we're on a detailed job view page
    const detailSelectors = [
      '.jobs-details',
      '.jobs-unified-top-card',
      '.job-view-layout'
    ];

    for (const selector of detailSelectors) {
      const detail = document.querySelector(selector);
      if (detail) {
        console.log('✅ Found detailed job view');
        this.analyzeDetailedJob(detail);
        return;
      }
    }

    console.log('❌ No jobs found on this page');
  }

  getJobId(element, index) {
    // Try to get job ID from link
    const link = element.querySelector('a[href*="/jobs/view/"]');
    if (link) {
      const match = link.href.match(/\/jobs\/view\/(\d+)/);
      if (match) return `job-${match[1]}`;
    }

    // Fallback to using element content hash
    const text = element.innerText.substring(0, 100);
    return `job-${text.replace(/\s/g, '-').substring(0, 50)}-${index}`;
  }

  analyzeJobCard(card, jobId) {
    try {
      // Extract job data
      const jobData = this.extractJobDataFromCard(card);
      
      if (!jobData.title) {
        console.log('⚠️ Could not extract job title, skipping');
        return;
      }

      console.log('📝 Job data extracted:', jobData);

      // Analyze the job
      const analysis = this.analyzeJob(jobData);
      console.log('📊 Analysis result:', analysis);

      // Mark as analyzed
      this.analyzedJobs.add(jobId);

      // Display indicator
      this.displayRiskBadge(card, analysis);

    } catch (error) {
      console.error('❌ Error analyzing job:', error);
    }
  }

  extractJobDataFromCard(card) {
    // Multiple selector options for different LinkedIn layouts
    const titleSelectors = [
      '.job-card-list__title',
      '.job-card-container__link',
      '.jobs-unified-top-card__job-title',
      '.artdeco-entity-lockup__title'
    ];

    const companySelectors = [
      '.job-card-container__company-name',
      '.job-card-container__primary-description',
      '.artdeco-entity-lockup__subtitle',
      '.jobs-unified-top-card__company-name'
    ];

    const locationSelectors = [
      '.job-card-container__metadata-item',
      '.artdeco-entity-lockup__caption',
      '.jobs-unified-top-card__bullet'
    ];

    const getTextFromSelectors = (selectors) => {
      for (const selector of selectors) {
        const element = card.querySelector(selector);
        if (element) return element.innerText.trim();
      }
      return '';
    };

    return {
      title: getTextFromSelectors(titleSelectors),
      company: getTextFromSelectors(companySelectors),
      location: getTextFromSelectors(locationSelectors),
      snippet: card.innerText.substring(0, 500)
    };
  }

  analyzeDetailedJob(detail) {
    try {
      const jobData = {
        title: detail.querySelector('.jobs-unified-top-card__job-title, .job-details-jobs-unified-top-card__job-title')?.innerText || '',
        company: detail.querySelector('.jobs-unified-top-card__company-name, .job-details-jobs-unified-top-card__company-name')?.innerText || '',
        location: detail.querySelector('.jobs-unified-top-card__bullet')?.innerText || '',
        description: detail.querySelector('.jobs-description-content__text, .jobs-description')?.innerText || ''
      };

      console.log('📝 Detailed job data:', jobData);

      const analysis = this.analyzeJob(jobData);
      console.log('📊 Analysis result:', analysis);

      this.displayRiskBadge(detail, analysis);

    } catch (error) {
      console.error('❌ Error analyzing detailed job:', error);
    }
  }

  analyzeJob(jobData) {
    // YOUR EXISTING AI LOGIC GOES HERE
    // For now, I'll create a rule-based system
    
    let score = 0;
    const flags = [];

    const fullText = `${jobData.title} ${jobData.company} ${jobData.location} ${jobData.description || jobData.snippet}`.toLowerCase();

    // Red flag checks
    if (fullText.includes('urgent') || fullText.includes('immediate')) {
      score += 15;
      flags.push('⚠️ Urgency pressure detected');
    }

    if (fullText.includes('no experience') && (fullText.includes('high salary') || fullText.includes('$'))) {
      score += 20;
      flags.push('💰 Unrealistic compensation for experience');
    }

    if (fullText.match(/\$\d{3,}.*per (day|hour)/)) {
      score += 15;
      flags.push('💵 Suspicious pay structure');
    }

    if (fullText.includes('pay to apply') || fullText.includes('application fee') || fullText.includes('training fee')) {
      score += 30;
      flags.push('🚨 Requests upfront payment');
    }

    if (fullText.includes('work from home') && fullText.includes('no experience') && fullText.includes('flexible')) {
      score += 10;
      flags.push('🏠 Too-good-to-be-true remote work');
    }

    if ((jobData.description || jobData.snippet).split(' ').length < 30) {
      score += 10;
      flags.push('📝 Very brief job description');
    }

    if (fullText.includes('crypto') || fullText.includes('bitcoin') || fullText.includes('forex')) {
      score += 15;
      flags.push('💱 High-risk financial sector');
    }

    if (fullText.includes('unlimited earning') || fullText.includes('be your own boss')) {
      score += 20;
      flags.push('⚡ MLM/pyramid scheme language');
    }

    // Company name checks
    if (!jobData.company || jobData.company.length < 3) {
      score += 15;
      flags.push('🏢 No clear company name');
    }

    return {
      score: Math.min(score, 100),
      level: this.getRiskLevel(score),
      flags: flags
    };
  }

  getRiskLevel(score) {
    if (score < 30) return 'low';
    if (score < 60) return 'medium';
    return 'high';
  }

  displayRiskBadge(element, analysis) {
    // Remove existing badge if present
    const existing = element.querySelector('.job-risk-badge-container');
    if (existing) existing.remove();

    // Create badge
    const badge = document.createElement('div');
    badge.className = 'job-risk-badge-container';

    const { score, level, flags } = analysis;

    let color, emoji, text;
    if (level === 'low') {
      color = '#10b981';
      emoji = '✓';
      text = 'Low Risk';
    } else if (level === 'medium') {
      color = '#f59e0b';
      emoji = '⚠';
      text = 'Medium Risk';
    } else {
      color = '#ef4444';
      emoji = '⚠';
      text = 'High Risk';
    }

    badge.innerHTML = `
      <div class="job-risk-badge" style="
        background: ${color};
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        position: absolute;
        top: 10px;
        right: 10px;
        z-index: 999;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        cursor: help;
      ">
        <span>${emoji}</span>
        <span>${text}</span>
        <span style="
          background: rgba(255,255,255,0.3);
          padding: 2px 6px;
          border-radius: 10px;
          font-size: 11px;
        ">${score}</span>
      </div>
    `;

    // Add tooltip with flags
    if (flags.length > 0) {
      badge.title = 'Red flags detected:\n' + flags.join('\n');
    }

    // Position it
    element.style.position = 'relative';
    element.appendChild(badge);

    console.log(`✅ Badge displayed for ${level} risk job (score: ${score})`);
  }

  setupObserver() {
    console.log('👁️ Setting up page observer...');

    // Watch for new jobs being loaded
    const observer = new MutationObserver(() => {
      if (!this.isProcessing) {
        this.isProcessing = true;
        setTimeout(() => {
          this.scanForJobs();
          this.isProcessing = false;
        }, 1000);
      }
    });

    // Observe the main content area
    const targetNode = document.querySelector('main') || document.body;
    observer.observe(targetNode, {
      childList: true,
      subtree: true
    });

    console.log('✅ Observer active');
  }
}

// Initialize the detector
const detector = new LinkedInJobDetector();