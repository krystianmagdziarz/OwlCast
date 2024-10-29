import React, { useEffect } from 'react';

interface StatCollectorProviderProps {
  apiKey: string;
  children: React.ReactNode;
}

export const StatCollectorProvider: React.FC<StatCollectorProviderProps> = ({ 
  apiKey, 
  children 
}) => {
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://cdn.statcollector.com/collector.js';
    script.async = true;
    script.onload = () => {
      window.StatCollector.init(apiKey);
    };
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, [apiKey]);

  return <>{children}</>;
};
