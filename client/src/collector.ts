import axios from 'axios';
import { StatisticsData, StatCollectorConfig } from './types';

export class StatCollector {
  private config: StatCollectorConfig;
  private startTime: number;
  private maxScrollDepth: number;
  private visitorId: string;
  private worker?: ServiceWorker;

  constructor(config: StatCollectorConfig) {
    this.config = {
      endpoint: 'https://api.statcollector.com/v1',
      debug: false,
      ...config,
    };
    this.startTime = Date.now();
    this.maxScrollDepth = 0;
    this.visitorId = this.getVisitorId();
    this.initializeCollector();
  }

  private getVisitorId(): string {
    const stored = localStorage.getItem('sc_visitor_id');
    if (stored) return stored;

    const newId = crypto.randomUUID();
    localStorage.setItem('sc_visitor_id', newId);
    return newId;
  }

  private async initializeCollector(): Promise<void> {
    this.attachEventListeners();
    await this.registerServiceWorker();
  }

  private attachEventListeners(): void {
    window.addEventListener('scroll', this.handleScroll.bind(this));
    window.addEventListener('beforeunload', this.handleUnload.bind(this));
  }

  private async registerServiceWorker(): Promise<void> {
    if ('serviceWorker' in navigator) {
      try {
        const registration = await navigator.serviceWorker.register('/sw.js');
        this.worker = registration.active || null;
      } catch (error) {
        this.logError('Failed to register service worker', error);
      }
    }
  }

  private handleScroll(): void {
    const scrollDepth = this.calculateScrollDepth();
    this.maxScrollDepth = Math.max(this.maxScrollDepth, scrollDepth);
  }

  private calculateScrollDepth(): number {
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight;
    const scrollTop = window.scrollY;
    return Math.round((scrollTop / (documentHeight - windowHeight)) * 100);
  }

  private async handleUnload(): Promise<void> {
    const statistics = this.collectStatistics();
    await this.sendStatistics(statistics);
  }

  private collectStatistics(): StatisticsData {
    return {
      url: window.location.href,
      userAgent: navigator.userAgent,
      referrer: document.referrer,
      screenWidth: window.screen.width,
      screenHeight: window.screen.height,
      language: navigator.language,
      isMobile: /Mobile|Android|iOS/.test(navigator.userAgent),
      scrollDepth: this.maxScrollDepth,
      timeOnPage: Math.round((Date.now() - this.startTime) / 1000),
      clientTimestamp: new Date().toISOString(),
      visitorId: this.visitorId,
    };
  }

  private async sendStatistics(data: StatisticsData): Promise<void> {
    try {
      if (navigator.onLine) {
        await this.sendToAPI(data);
      } else {
        this.storeOffline(data);
      }
    } catch (error) {
      this.logError('Failed to send statistics', error);
      this.storeOffline(data);
    }
  }

  private async sendToAPI(data: StatisticsData): Promise<void> {
    await axios.post(`${this.config.endpoint}/statistics`, data, {
      headers: {
        'X-API-Key': this.config.apiKey,
      },
    });
  }

  private storeOffline(data: StatisticsData): void {
    const offlineData = JSON.parse(
      localStorage.getItem('sc_offline_data') || '[]'
    );
    offlineData.push(data);
    localStorage.setItem('sc_offline_data', JSON.stringify(offlineData));
  }

  private logError(message: string, error: unknown): void {
    if (this.config.debug) {
      console.error(`[StatCollector] ${message}:`, error);
    }
    if (this.config.reportingEndpoint) {
      this.reportError(message, error);
    }
  }

  private async reportError(message: string, error: unknown): Promise<void> {
    try {
      await axios.post(
        this.config.reportingEndpoint!,
        {
          message,
          error: String(error),
          timestamp: new Date().toISOString(),
          userAgent: navigator.userAgent,
          url: window.location.href,
        },
        {
          headers: {
            'X-API-Key': this.config.apiKey,
          },
        }
      );
    } catch (e) {
      if (this.config.debug) {
        console.error('[StatCollector] Failed to report error:', e);
      }
    }
  }
}
