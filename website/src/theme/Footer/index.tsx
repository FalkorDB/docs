import React from 'react';
import clsx from 'clsx';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './styles.module.css';

export default function Footer(): React.ReactElement {
  const { siteConfig } = useDocusaurusContext();
  const copyright = (siteConfig.themeConfig as any)?.footer?.copyright;

  return (
    <footer className={clsx('footer', styles.footer)}>
      <div className="container">
        <div className={styles.footerGrid}>
          <div className={styles.footerColumn}>
            <h3 className={styles.columnTitle}>RESOURCES</h3>
            <ul className={styles.linkList}>
              <li><a href="/">Documentation</a></li>
              <li><a href="https://www.falkordb.com/blog" target="_blank" rel="noopener noreferrer">Blog</a></li>
              <li><a href="https://www.falkordb.com/pricing" target="_blank" rel="noopener noreferrer">Pricing</a></li>
              <li><a href="https://www.falkordb.com/graph-size-calculator" target="_blank" rel="noopener noreferrer">Graph Size Calculator</a></li>
            </ul>
          </div>

          <div className={styles.footerColumn}>
            <h3 className={styles.columnTitle}>DEVELOPER</h3>
            <ul className={styles.linkList}>
              <li><a href="https://github.com/FalkorDB/FalkorDB" target="_blank" rel="noopener noreferrer">GitHub</a></li>
              <li><a href="https://github.com/FalkorDB/FalkorDB/tree/master/demo" target="_blank" rel="noopener noreferrer">Examples</a></li>
              <li><a href="https://github.com/FalkorDB/FalkorDB/issues" target="_blank" rel="noopener noreferrer">GitHub Issues</a></li>
              <li><a href="https://github.com/FalkorDB/FalkorDB/releases" target="_blank" rel="noopener noreferrer">Changelog</a></li>
            </ul>
          </div>

          <div className={styles.footerColumn}>
            <h3 className={styles.columnTitle}>COMMUNITY</h3>
            <ul className={styles.linkList}>
              <li><a href="https://discord.gg/ErBEqN9E" target="_blank" rel="noopener noreferrer">Discord</a></li>
              <li><a href="https://www.linkedin.com/company/falkordb" target="_blank" rel="noopener noreferrer">LinkedIn</a></li>
              <li><a href="https://app.falkordb.cloud" target="_blank" rel="noopener noreferrer">Try Cloud</a></li>
            </ul>
          </div>

          <div className={clsx(styles.footerColumn, styles.contactColumn)}>
            <h3 className={styles.columnTitle}>CONTACT</h3>
            <form 
              className={styles.contactForm} 
              action="https://formspree.io/f/xjggkpoy" 
              method="POST"
            >
              <input
                type="text"
                name="firstName"
                className={styles.formInput}
                placeholder="First Name"
                required
              />
              <input
                type="text"
                name="company"
                className={styles.formInput}
                placeholder="Company"
              />
              <input
                type="email"
                name="email"
                className={styles.formInput}
                placeholder="Email"
                required
              />
              <textarea
                name="message"
                className={styles.formTextarea}
                placeholder="Message"
                rows={2}
                required
              />
              <button type="submit" className={styles.submitBtn}>
                Send
              </button>
            </form>
          </div>
        </div>

        <div className={styles.footerBottom}>
          <div className={styles.copyright}>
            {copyright}
          </div>
        </div>
      </div>
    </footer>
  );
}
