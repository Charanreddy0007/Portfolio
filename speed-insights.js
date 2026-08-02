/**
 * Vercel Speed Insights Integration
 * Initializes web vitals tracking for the portfolio site
 */
import { injectSpeedInsights } from '@vercel/speed-insights';

// Initialize Speed Insights
// This will track Core Web Vitals (LCP, FID, CLS, etc.) and send them to Vercel
injectSpeedInsights({
  debug: false, // Set to true for development debugging
});
