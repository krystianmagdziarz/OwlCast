export interface StatisticsData {
  url: string;
  userAgent: string;
  referrer?: string;
  screenWidth: number;
  screenHeight: number;
  language: string;
  isMobile: boolean;
  scrollDepth: number;
  timeOnPage: number;
  clientTimestamp: string;
  visitorId: string;
}

export interface StatCollectorConfig {
  apiKey: string;
  endpoint?: string;
  debug?: boolean;
  reportingEndpoint?: string;
}
