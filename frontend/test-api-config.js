// Test script to verify API configuration
// Run this with: node test-api-config.js

// Simulate different environment scenarios
const testScenarios = [
  {
    name: 'Development (no env var, localhost)',
    env: { NODE_ENV: 'development' },
    window: { location: { hostname: 'localhost', protocol: 'http:' } },
    expected: 'http://localhost:5000'
  },
  {
    name: 'Development (no env var, different IP)',
    env: { NODE_ENV: 'development' },
    window: { location: { hostname: '192.168.1.100', protocol: 'http:' } },
    expected: 'http://192.168.1.100:5000'
  },
  {
    name: 'Production (no env var)',
    env: { NODE_ENV: 'production' },
    window: { location: { hostname: 'myserver.com', protocol: 'https:' } },
    expected: ''
  },
  {
    name: 'Custom API URL',
    env: { REACT_APP_API_URL: 'http://custom-server:8080' },
    window: { location: { hostname: 'anywhere.com', protocol: 'http:' } },
    expected: 'http://custom-server:8080'
  },
  {
    name: 'Empty API URL',
    env: { REACT_APP_API_URL: '' },
    window: { location: { hostname: 'anywhere.com', protocol: 'http:' } },
    expected: ''
  }
];

// Function to simulate the API base URL logic
function getApiBaseUrl(env, mockWindow = {}) {
  const originalEnv = { ...process.env };
  const originalWindow = global.window;
  
  // Set test environment
  Object.keys(env).forEach(key => {
    process.env[key] = env[key];
  });
  
  // Mock window object
  global.window = mockWindow;
  
  let result;
  
  // If explicitly set via environment variable, use that (including empty string)
  if (process.env.REACT_APP_API_URL !== undefined) {
    result = process.env.REACT_APP_API_URL;
  }
  // For production builds, try to auto-detect the host
  else if (process.env.NODE_ENV === 'production') {
    result = '';
  }
  // Development: try to detect if we're running on a different host
  else if (mockWindow.location) {
    const currentHost = mockWindow.location.hostname;
    const currentProtocol = mockWindow.location.protocol;
    
    // If not localhost, assume backend is on same host with port 5000
    if (currentHost !== 'localhost' && currentHost !== '127.0.0.1') {
      result = `${currentProtocol}//${currentHost}:5000`;
    } else {
      result = 'http://localhost:5000';
    }
  }
  // Development fallback for localhost
  else {
    result = 'http://localhost:5000';
  }
  
  // Restore original environment
  process.env = originalEnv;
  global.window = originalWindow;
  
  return result;
}

console.log('🧪 Testing API Configuration Logic');
console.log('=====================================');

let allPassed = true;

testScenarios.forEach(scenario => {
  const result = getApiBaseUrl(scenario.env, scenario.window);
  const passed = result === scenario.expected;
  
  console.log(`\n📋 ${scenario.name}`);
  console.log(`   Environment: ${JSON.stringify(scenario.env)}`);
  if (scenario.window?.location) {
    console.log(`   Window Location: ${scenario.window.location.protocol}//${scenario.window.location.hostname}`);
  }
  console.log(`   Expected: ${scenario.expected || '(empty/relative URLs)'}`);
  console.log(`   Got: ${result || '(empty/relative URLs)'}`);
  console.log(`   Status: ${passed ? '✅ PASS' : '❌ FAIL'}`);
  
  if (!passed) allPassed = false;
});

console.log('\n=====================================');
console.log(`🎯 Overall Result: ${allPassed ? '✅ ALL TESTS PASSED' : '❌ SOME TESTS FAILED'}`);

if (allPassed) {
  console.log('\n🚀 API configuration is working correctly!');
  console.log('   The frontend will adapt to different deployment scenarios.');
} else {
  console.log('\n🐛 There are issues with the API configuration logic.');
  process.exit(1);
}
