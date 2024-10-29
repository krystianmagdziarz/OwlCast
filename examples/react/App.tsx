import { StatCollectorProvider } from './StatCollectorProvider';

function App() {
  return (
    <StatCollectorProvider apiKey="your-api-key">
      <div>Your app content</div>
    </StatCollectorProvider>
  );
}
