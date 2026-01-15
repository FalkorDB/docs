import React, { useState } from 'react';
import clsx from 'clsx';
import { ThemeClassNames } from '@docusaurus/theme-common';
import { useDoc } from '@docusaurus/plugin-content-docs/client';
import EditThisPage from '@theme/EditThisPage';
import TagsListInline from '@theme/TagsListInline';
import styles from './styles.module.css';

function BackToTopButton() {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <button 
      onClick={scrollToTop}
      className={styles.backToTop}
      aria-label="Back to top"
      title="Back to top"
    >
      ↑ Back to top
    </button>
  );
}

function WasThisHelpful() {
  const [feedback, setFeedback] = useState<'yes' | 'no' | null>(null);

  const handleFeedback = (helpful: 'yes' | 'no') => {
    setFeedback(helpful);
    
    const feedbackData = {
      helpful,
      page: window.location.pathname,
      timestamp: new Date().toISOString(),
      url: window.location.href,
    };

    // 1. Send to Google Tag Manager (if configured)
    if (typeof window !== 'undefined' && (window as any).dataLayer) {
      (window as any).dataLayer.push({
        event: 'doc_feedback',
        feedback_type: helpful,
        page_path: feedbackData.page,
        feedback_value: helpful === 'yes' ? 1 : 0
      });
    }

    // 2. Send to Google Analytics directly (fallback)
    if (typeof window !== 'undefined' && (window as any).gtag) {
      (window as any).gtag('event', 'doc_feedback', {
        event_category: 'documentation',
        event_label: feedbackData.page,
        feedback_type: helpful,
        value: helpful === 'yes' ? 1 : 0
      });
    }

    // 3. Console log for debugging (can be removed in production)
    console.log('📊 Doc Feedback:', feedbackData);

    // 4. Optional: Send to your own backend endpoint
    // Uncomment and configure when ready:
    /*
    fetch('/api/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(feedbackData),
    }).catch(err => console.error('Failed to send feedback:', err));
    */

    // 5. Optional: Store in localStorage for analytics review
    try {
      const existingFeedback = JSON.parse(localStorage.getItem('doc_feedback') || '[]');
      existingFeedback.push(feedbackData);
      // Keep only last 50 entries
      if (existingFeedback.length > 50) {
        existingFeedback.shift();
      }
      localStorage.setItem('doc_feedback', JSON.stringify(existingFeedback));
    } catch (e) {
      // Silent fail for localStorage
    }
  };

  return (
    <div className={styles.feedbackContainer}>
      {feedback === null ? (
        <>
          <span className={styles.feedbackQuestion}>Was this page helpful?</span>
          <div className={styles.feedbackButtons}>
            <button
              onClick={() => handleFeedback('yes')}
              className={clsx(styles.feedbackButton, styles.feedbackYes)}
              aria-label="Yes, this page was helpful"
            >
              👍 Yes
            </button>
            <button
              onClick={() => handleFeedback('no')}
              className={clsx(styles.feedbackButton, styles.feedbackNo)}
              aria-label="No, this page was not helpful"
            >
              👎 No
            </button>
          </div>
        </>
      ) : (
        <div className={styles.feedbackThanks}>
          Thanks for your feedback! {feedback === 'yes' ? '😊' : 'We\'ll work on improving this page.'}
        </div>
      )}
    </div>
  );
}

export default function DocItemFooter(): React.ReactElement {
  const { metadata } = useDoc();
  const { editUrl, tags } = metadata;

  const canDisplayTagsRow = tags.length > 0;
  const canDisplayEditMetaRow = !!editUrl;

  const canDisplayFooter = canDisplayTagsRow || canDisplayEditMetaRow;

  if (!canDisplayFooter) {
    return (
      <footer className={clsx(ThemeClassNames.docs.docFooter, styles.docFooter)}>
        <WasThisHelpful />
        <div className={styles.footerActions}>
          <BackToTopButton />
        </div>
      </footer>
    );
  }

  return (
    <footer className={clsx(ThemeClassNames.docs.docFooter, styles.docFooter)}>
      {canDisplayTagsRow && (
        <div className={clsx('row margin-top--sm', ThemeClassNames.docs.docFooterTagsRow)}>
          <div className="col">
            <TagsListInline tags={tags} />
          </div>
        </div>
      )}
      {canDisplayEditMetaRow && (
        <div className={clsx('row', ThemeClassNames.docs.docFooterEditMetaRow)}>
          <div className="col">{editUrl && <EditThisPage editUrl={editUrl} />}</div>
        </div>
      )}
      <div className={styles.separator} />
      <WasThisHelpful />
      <div className={styles.footerActions}>
        <BackToTopButton />
      </div>
    </footer>
  );
}
