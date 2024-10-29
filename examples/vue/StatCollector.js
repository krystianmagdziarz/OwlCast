export default {
  install(app, options) {
    if (!options.apiKey) {
      console.error('StatCollector: API key is required');
      return;
    }

    const script = document.createElement('script');
    script.src = 'https://cdn.statcollector.com/collector.js';
    script.async = true;
    
    script.onload = () => {
      window.StatCollector.init(options.apiKey);
    };
    
    document.body.appendChild(script);
  }
};
