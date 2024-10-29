// Single Page Application integration
class SPAStatCollector {
    constructor(apiKey, options = {}) {
        this.previousPath = window.location.pathname;
        this.collector = new StatCollector(apiKey, options);
        
        // Handle route changes
        window.addEventListener('popstate', this.handleRouteChange.bind(this));
        
        // For frameworks using pushState
        const originalPushState = history.pushState;
        history.pushState = (...args) => {
            originalPushState.apply(history, args);
            this.handleRouteChange();
        };
    }
    
    handleRouteChange() {
        const currentPath = window.location.pathname;
        if (currentPath !== this.previousPath) {
            this.collector.trackPageView();
            this.previousPath = currentPath;
        }
    }
}

// Usage
const analytics = new SPAStatCollector('your-api-key', {
    debug: true
});
