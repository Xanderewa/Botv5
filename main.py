
- src/App.jsx (from snapshot)
- src/index.css (from snapshot)
- tailwind.config.js (from snapshot)
- src/lib/kucoin.js (from snapshot)
- src/lib/indicators.js (from snapshot)
- src/lib/telegram.js (from snapshot)
- src/pages/Login.jsx (from snapshot)
- src/components/SignalCard.jsx (just wrote)
- src/components/TrackedPositions.jsx (just wrote)
- src/pages/Dashboard.jsx (just wrote)
- src/lib/signalTracker.js (just wrote)

I need to read:
- src/pages/Settings.jsx
- src/components/ControlBar.jsx
- src/components/ProtectedRoute.jsx
- src/lib/AuthContext.jsx
- src/api/base44Client.js
- src/main.jsx
- index.html
- src/lib/PageNotFound.jsx
- src/lib/utils.js
- src/lib/query-client.js
- src/components/ScrollToTop.jsx
- src/components/UserNotRegisteredError.jsx
- src/components/AuthLayout.jsx
- src/components/GoogleIcon.jsx
 read_file
Arguments:
{
  "file_path": "src/pages/Settings.jsx"
}
Result:
1: import React, { useState, useEffect } from "...

---

### read_file
Arguments:
{
  "file_path": "src/components/ControlBar.jsx"
}
Result:
1: import React from "react";
   2: import { Re...

---

### read_file
Arguments:
{
  "file_path": "src/components/ProtectedRoute.jsx"
}
Result:
1: import { useEffect } from 'react';
   2: imp...

---

### read_file
Arguments:
{
  "file_path": "src/lib/AuthContext.jsx"
}
Result:
1: import React, { createContext, useState, use...

---

### read_file
Arguments:
{
  "file_path": "src/api/base44Client.js"
}
Result:
1: import { createClient } from '@base44/sdk';
...

---

### read_file
Arguments:
{
  "file_path": "src/main.jsx"
}
Result:
1: import React from 'react'
   2: import React...

---

### read_file
Arguments:
{
  "file_path": "index.html"
}
Result:
1: <!doctype html>
   2: <html lang="en">
   3:...

---

### read_file
Arguments:
{
  "file_path": "src/lib/PageNotFound.jsx"
}
Result:
1: import { useLocation } from 'react-router-do...

---

### read_file
Arguments:
{
  "file_path": "src/lib/utils.js"
}
Result:
1: import { clsx } from "clsx"
   2: import { t...

---

### read_file
Arguments:
{
  "file_path": "src/lib/query-client.js"
}
Result:
1: import { QueryClient } from '@tanstack/react...

---

### read_file
Arguments:
{
  "file_path": "src/components/ScrollToTop.jsx"
}
Result:
1: import { useEffect } from "react";
   2: imp...

---

### read_file
Arguments:
{
  "file_path": "src/components/UserNotRegisteredError.jsx"
}
Result:
1: import React from 'react';
   2: 
   3: cons...

---

### read_file
Arguments:
{
  "file_path": "src/components/AuthLayout.jsx"
}
Result:
1: import React from "react";
   2: 
   3: expo...

---

### read_file
Arguments:
{
  "file_path": "src/components/GoogleIcon.jsx"
}
Result:
1: import React from "react";
   2: 
   3: expo...

[Reasoning]
Now let me also read the remaining auth pages and app-params.

### read_file
Arguments:
{
  "file_path": "src/lib/app-params.js"
}
Result:
1: const isNode = typeof window === 'undefined'...

---

### read_file
Arguments:
{
  "file_path": "src/pages/Register.jsx"
}
Result:
1: import React, { useState } from "react";
   ...

---

### read_file
Arguments:
{
  "file_path": "src/pages/ForgotPassword.jsx"
}
Result:
1: import React, { useState } from "react";
   ...

---

### read_file
Arguments:
{
  "file_path": "src/pages/ResetPassword.jsx"
}
Result:
1: import React, { useState } from "react";
   ...

Aquí está el código completo y final de la aplicación:

---

**index.html**
```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="https://base44.com/logo_v2.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="manifest" href="/manifest.json" />
    <title>CryptoSignal Bot</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

---

**src/main.jsx**
```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from '@/App.jsx'
import '@/index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <App />
)
```

---

**src/App.jsx**
```jsx
import { Toaster } from "@/components/ui/toaster"
import { QueryClientProvider } from '@tanstack/react-query'
import { queryClientInstance } from '@/lib/query-client'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import PageNotFound from './lib/PageNotFound';
import { AuthProvider, useAuth } from '@/lib/AuthContext';
import UserNotRegisteredError from '@/components/UserNotRegisteredError';
import ScrollToTop from './components/ScrollToTop';
import Dashboard from './pages/Dashboard';
import Settings from './pages/Settings';
import Login from './pages/Login';
import Register from './pages/Register';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';
import ProtectedRoute from '@/components/ProtectedRoute';
import { Navigate } from 'react-router-dom';

const AuthenticatedApp = () => {
  const { isLoadingAuth, isLoadingPublicSettings, authError, navigateToLogin } = useAuth();

  if (isLoadingPublicSettings || isLoadingAuth) {
    return (
      <div className="fixed inset-0 flex items-center justify-center">
        <div className="w-8 h-8 border-4 border-slate-200 border-t-slate-800 rounded-full animate-spin"></div>
      </div>
    );
  }

  if (authError) {
    if (authError.type === 'user_not_registered') {
      return <UserNotRegisteredError />;
    } else if (authError.type === 'auth_required') {
      navigateToLogin();
      return null;
    }
  }

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/reset-password" element={<ResetPassword />} />
      <Route element={<ProtectedRoute unauthenticatedElement={<Navigate to="/login" replace />} />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Route>
      <Route path="*" element={<PageNotFound />} />
    </Routes>
  );
};

function App() {
  return (
    <AuthProvider>
      <QueryClientProvider client={queryClientInstance}>
        <Router>
          <ScrollToTop />
          <AuthenticatedApp />
        </Router>
        <Toaster />
      </QueryClientProvider>
    </AuthProvider>
  )
}

export default App
```

---

**src/index.css**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 0 0% 3.9%;
    --card: 0 0% 100%;
    --card-foreground: 0 0% 3.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 0 0% 3.9%;
    --primary: 0 0% 9%;
    --primary-foreground: 0 0% 98%;
    --secondary: 0 0% 96.1%;
    --secondary-foreground: 0 0% 9%;
    --muted: 0 0% 96.1%;
    --muted-foreground: 0 0% 45.1%;
    --accent: 0 0% 96.1%;
    --accent-foreground: 0 0% 9%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 0 0% 98%;
    --border: 0 0% 89.8%;
    --input: 0 0% 89.8%;
    --ring: 0 0% 3.9%;
    --chart-1: 12 76% 61%;
    --chart-2: 173 58% 39%;
    --chart-3: 197 37% 24%;
    --chart-4: 43 74% 66%;
    --chart-5: 27 87% 67%;
    --radius: 0.5rem;
    --font-heading: ui-sans-serif, system-ui, sans-serif;
    --font-body: ui-sans-serif, system-ui, sans-serif;
    --font-display: ui-sans-serif, system-ui, sans-serif;
    --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    --sidebar-background: 0 0% 98%;
    --sidebar-foreground: 240 5.3% 26.1%;
    --sidebar-primary: 240 5.9% 10%;
    --sidebar-primary-foreground: 0 0% 98%;
    --sidebar-accent: 240 4.8% 95.9%;
    --sidebar-accent-foreground: 240 5.9% 10%;
    --sidebar-border: 220 13% 91%;
    --sidebar-ring: 217.2 91.2% 59.8%;
  }

  .dark {
    --background: 0 0% 3.9%;
    --foreground: 0 0% 98%;
    --card: 0 0% 3.9%;
    --card-foreground: 0 0% 98%;
    --popover: 0 0% 3.9%;
    --popover-foreground: 0 0% 98%;
    --primary: 0 0% 98%;
    --primary-foreground: 0 0% 9%;
    --secondary: 0 0% 14.9%;
    --secondary-foreground: 0 0% 98%;
    --muted: 0 0% 14.9%;
    --muted-foreground: 0 0% 63.9%;
    --accent: 0 0% 14.9%;
    --accent-foreground: 0 0% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 0 0% 98%;
    --border: 0 0% 14.9%;
    --input: 0 0% 14.9%;
    --ring: 0 0% 83.1%;
    --chart-1: 220 70% 50%;
    --chart-2: 160 60% 45%;
    --chart-3: 30 80% 55%;
    --chart-4: 280 65% 60%;
    --chart-5: 340 75% 55%;
    --sidebar-background: 240 5.9% 10%;
    --sidebar-foreground: 240 4.8% 95.9%;
    --sidebar-primary: 224.3 76.3% 48%;
    --sidebar-primary-foreground: 0 0% 100%;
    --sidebar-accent: 240 3.7% 15.9%;
    --sidebar-accent-foreground: 240 4.8% 95.9%;
    --sidebar-border: 240 3.7% 15.9%;
    --sidebar-ring: 217.2 91.2% 59.8%;
  }
}

@layer base {
  * {
    @apply border-border outline-ring/50;
  }

  body {
    @apply bg-background text-foreground font-body;
  }
}
```

---

**tailwind.config.js**
```js
/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: ["class"],
    content: ["./index.html", "./src/**/*.{ts,tsx,js,jsx}"],
  theme: {
  	extend: {
  		borderRadius: {
  			lg: 'var(--radius)',
  			md: 'calc(var(--radius) - 2px)',
  			sm: 'calc(var(--radius) - 4px)'
  		},
  		colors: {
  			background: 'hsl(var(--background))',
  			foreground: 'hsl(var(--foreground))',
  			card: {
  				DEFAULT: 'hsl(var(--card))',
  				foreground: 'hsl(var(--card-foreground))'
  			},
  			popover: {
  				DEFAULT: 'hsl(var(--popover))',
  				foreground: 'hsl(var(--popover-foreground))'
  			},
  			primary: {
  				DEFAULT: 'hsl(var(--primary))',
  				foreground: 'hsl(var(--primary-foreground))'
  			},
  			secondary: {
  				DEFAULT: 'hsl(var(--secondary))',
  				foreground: 'hsl(var(--secondary-foreground))'
  			},
  			muted: {
  				DEFAULT: 'hsl(var(--muted))',
  				foreground: 'hsl(var(--muted-foreground))'
  			},
  			accent: {
  				DEFAULT: 'hsl(var(--accent))',
  				foreground: 'hsl(var(--accent-foreground))'
  			},
  			destructive: {
  				DEFAULT: 'hsl(var(--destructive))',
  				foreground: 'hsl(var(--destructive-foreground))'
  			},
  			border: 'hsl(var(--border))',
  			input: 'hsl(var(--input))',
  			ring: 'hsl(var(--ring))',
  			chart: {
  				'1': 'hsl(var(--chart-1))',
  				'2': 'hsl(var(--chart-2))',
  				'3': 'hsl(var(--chart-3))',
  				'4': 'hsl(var(--chart-4))',
  				'5': 'hsl(var(--chart-5))'
  			},
  			sidebar: {
  				DEFAULT: 'hsl(var(--sidebar-background))',
  				foreground: 'hsl(var(--sidebar-foreground))',
  				primary: 'hsl(var(--sidebar-primary))',
  				'primary-foreground': 'hsl(var(--sidebar-primary-foreground))',
  				accent: 'hsl(var(--sidebar-accent))',
  				'accent-foreground': 'hsl(var(--sidebar-accent-foreground))',
  				border: 'hsl(var(--sidebar-border))',
  				ring: 'hsl(var(--sidebar-ring))'
  			}
  		},
  		fontFamily: {
  			heading: ['var(--font-heading)'],
  			body: ['var(--font-body)'],
  			display: ['var(--font-display)'],
  			mono: ['var(--font-mono)']
  		},
  		keyframes: {
  			'accordion-down': {
  				from: { height: '0' },
  				to: { height: 'var(--radix-accordion-content-height)' }
  			},
  			'accordion-up': {
  				from: { height: 'var(--radix-accordion-content-height)' },
  				to: { height: '0' }
  			}
  		},
  		animation: {
  			'accordion-down': 'accordion-down 0.2s ease-out',
  			'accordion-up': 'accordion-up 0.2s ease-out'
  		}
  	}
  },
  plugins: [require("tailwindcss-animate")],
}
```

---

**src/api/base44Client.js**
```js
import { createClient } from '@base44/sdk';
import { appParams } from '@/lib/app-params';

const { appId, token, functionsVersion, appBaseUrl } = appParams;

export const base44 = createClient({
  appId,
  token,
  functionsVersion,
  serverUrl: '',
  requiresAuth: false,
  appBaseUrl
});
```

---

**src/lib/app-params.js**
```js
const isNode = typeof window === 'undefined';
const windowObj = isNode ? { localStorage: new Map() } : window;
const storage = windowObj.localStorage;

const toSnakeCase = (str) => {
	return str.replace(/([A-Z])/g, '_$1').toLowerCase();
}

const getAppParamValue = (paramName, { defaultValue = undefined, removeFromUrl = false } = {}) => {
	if (isNode) {
		return defaultValue;
	}
	const storageKey = `base44_${toSnakeCase(paramName)}`;
	const urlParams = new URLSearchParams(window.location.search);
	const searchParam = urlParams.get(paramName);
	if (removeFromUrl) {
		urlParams.delete(paramName);
		const newUrl = `${window.location.pathname}${urlParams.toString() ? `?${urlParams.toString()}` : ""
			}${window.location.hash}`;
		window.history.replaceState({}, document.title, newUrl);
	}
	if (searchParam) {
		storage.setItem(storageKey, searchParam);
		return searchParam;
	}
	if (defaultValue) {
		storage.setItem(storageKey, defaultValue);
		return defaultValue;
	}
	const storedValue = storage.getItem(storageKey);
	if (storedValue) {
		return storedValue;
	}
	return null;
}

const getAppParams = () => {
	if (getAppParamValue("clear_access_token") === 'true') {
		storage.removeItem('base44_access_token');
		storage.removeItem('token');
	}
	return {
		appId: getAppParamValue("app_id", { defaultValue: import.meta.env.VITE_BASE44_APP_ID }),
		token: getAppParamValue("access_token", { removeFromUrl: true }),
		fromUrl: getAppParamValue("from_url", { defaultValue: window.location.href }),
		functionsVersion: getAppParamValue("functions_version", { defaultValue: import.meta.env.VITE_BASE44_FUNCTIONS_VERSION }),
		appBaseUrl: getAppParamValue("app_base_url", { defaultValue: import.meta.env.VITE_BASE44_APP_BASE_URL }),
	}
}

export const appParams = {
	...getAppParams()
}
```

---

**src/lib/query-client.js**
```js
import { QueryClient } from '@tanstack/react-query';

export const queryClientInstance = new QueryClient({
	defaultOptions: {
		queries: {
			refetchOnWindowFocus: false,
			retry: 1,
		},
	},
});
```

---

**src/lib/utils.js**
```js
import { clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs) {
  return twMerge(clsx(inputs))
}

export const isIframe = window.self !== window.top;
```

---

**src/lib/AuthContext.jsx**
```jsx
import React, { createContext, useState, useContext, useEffect } from 'react';
import { base44 } from '@/api/base44Client';
import { appParams } from '@/lib/app-params';
import { createAxiosClient } from '@base44/sdk/dist/utils/axios-client';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoadingAuth, setIsLoadingAuth] = useState(true);
  const [isLoadingPublicSettings, setIsLoadingPublicSettings] = useState(true);
  const [authError, setAuthError] = useState(null);
  const [authChecked, setAuthChecked] = useState(false);
  const [appPublicSettings, setAppPublicSettings] = useState(null);

  useEffect(() => {
    checkAppState();
  }, []);

  const checkAppState = async () => {
    try {
      setIsLoadingPublicSettings(true);
      setAuthError(null);
      
      const appClient = createAxiosClient({
        baseURL: `/api/apps/public`,
        headers: {
          'X-App-Id': appParams.appId
        },
        token: appParams.token,
        interceptResponses: true
      });
      
      try {
        const publicSettings = await appClient.get(`/prod/public-settings/by-id/${appParams.appId}`);
        setAppPublicSettings(publicSettings);
        
        if (appParams.token) {
          await checkUserAuth();
        } else {
          setIsLoadingAuth(false);
          setIsAuthenticated(false);
          setAuthChecked(true);
        }
        setIsLoadingPublicSettings(false);
      } catch (appError) {
        console.error('App state check failed:', appError);
        
        if (appError.status === 403 && appError.data?.extra_data?.reason) {
          const reason = appError.data.extra_data.reason;
          if (reason === 'auth_required') {
            setAuthError({ type: 'auth_required', message: 'Authentication required' });
          } else if (reason === 'user_not_registered') {
            setAuthError({ type: 'user_not_registered', message: 'User not registered for this app' });
          } else {
            setAuthError({ type: reason, message: appError.message });
          }
        } else {
          setAuthError({ type: 'unknown', message: appError.message || 'Failed to load app' });
        }
        setIsLoadingPublicSettings(false);
        setIsLoadingAuth(false);
      }
    } catch (error) {
      console.error('Unexpected error:', error);
      setAuthError({ type: 'unknown', message: error.message || 'An unexpected error occurred' });
      setIsLoadingPublicSettings(false);
      setIsLoadingAuth(false);
    }
  };

  const checkUserAuth = async () => {
    try {
      setIsLoadingAuth(true);
      const currentUser = await base44.auth.me();
      setUser(currentUser);
      setIsAuthenticated(true);
      setIsLoadingAuth(false);
      setAuthChecked(true);
    } catch (error) {
      console.error('User auth check failed:', error);
      setIsLoadingAuth(false);
      setIsAuthenticated(false);
      setAuthChecked(true);
      
      if (error.status === 401 || error.status === 403) {
        setAuthError({ type: 'auth_required', message: 'Authentication required' });
      }
    }
  };

  const logout = (shouldRedirect = true) => {
    setUser(null);
    setIsAuthenticated(false);
    
    if (shouldRedirect) {
      base44.auth.logout(window.location.href);
    } else {
      base44.auth.logout();
    }
  };

  const navigateToLogin = () => {
    base44.auth.redirectToLogin(window.location.href);
  };

  return (
    <AuthContext.Provider value={{ 
      user, 
      isAuthenticated, 
      isLoadingAuth,
      isLoadingPublicSettings,
      authError,
      appPublicSettings,
      authChecked,
      logout,
      navigateToLogin,
      checkUserAuth,
      checkAppState
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
```

---

**src/lib/PageNotFound.jsx**
```jsx
import { useLocation } from 'react-router-dom';
import { base44 } from '@/api/base44Client';
import { useQuery } from '@tanstack/react-query';

export default function PageNotFound({}) {
    const location = useLocation();
    const pageName = location.pathname.substring(1);

    const { data: authData, isFetched } = useQuery({
        queryKey: ['user'],
        queryFn: async () => {
            try {
                const user = await base44.auth.me();
                return { user, isAuthenticated: true };
            } catch (error) {
                return { user: null, isAuthenticated: false };
            }
        }
    });
    
    return (
        <div className="min-h-screen flex items-center justify-center p-6 bg-slate-50">
            <div className="max-w-md w-full">
                <div className="text-center space-y-6">
                    <div className="space-y-2">
                        <h1 className="text-7xl font-light text-slate-300">404</h1>
                        <div className="h-0.5 w-16 bg-slate-200 mx-auto"></div>
                    </div>
                    
                    <div className="space-y-3">
                        <h2 className="text-2xl font-medium text-slate-800">
                            Page Not Found
                        </h2>
                        <p className="text-slate-600 leading-relaxed">
                            The page <span className="font-medium text-slate-700">"{pageName}"</span> could not be found in this application.
                        </p>
                    </div>
                    
                    {isFetched && authData.isAuthenticated && authData.user?.role === 'admin' && (
                        <div className="mt-8 p-4 bg-slate-100 rounded-lg border border-slate-200">
                            <div className="flex items-start space-x-3">
                                <div className="flex-shrink-0 w-5 h-5 rounded-full bg-orange-100 flex items-center justify-center mt-0.5">
                                    <div className="w-2 h-2 rounded-full bg-orange-400"></div>
                                </div>
                                <div className="text-left space-y-1">
                                    <p className="text-sm font-medium text-slate-700">Admin Note</p>
                                    <p className="text-sm text-slate-600 leading-relaxed">
                                        This could mean that the AI hasn't implemented this page yet. Ask it to implement it in the chat.
                                    </p>
                                </div>
                            </div>
                        </div>
                    )}
                    
                    <div className="pt-6">
                        <button 
                            onClick={() => window.location.href = '/'} 
                            className="inline-flex items-center px-4 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 hover:border-slate-300 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-500"
                        >
                            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                            </svg>
                            Go Home
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}
```

---

**src/lib/kucoin.js**
```js
const KUCOIN_BASE = "https://api.kucoin.com/api/v1";

export const DEFAULT_PAIRS = [
  "BTC-USDT",
  "ETH-USDT",
  "SOL-USDT",
  "BNB-USDT",
  "XRP-USDT",
  "ADA-USDT",
  "DOGE-USDT",
  "AVAX-USDT",
  "LINK-USDT",
  "DOT-USDT",
];

export async function fetchCandles(symbol, type = "1hour") {
  const url = `${KUCOIN_BASE}/market/candles?type=${type}&symbol=${symbol}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${symbol}`);
  const json = await res.json();
  if (json.code !== "200000") throw new Error(json.msg || "KuCoin API error");

  const data = (json.data || []).slice().reverse();
  return data.map((item) => ({
    time: parseInt(item[0]),
    open: parseFloat(item[1]),
    close: parseFloat(item[2]),
    high: parseFloat(item[3]),
    low: parseFloat(item[4]),
    volume: parseFloat(item[5]),
    turnover: parseFloat(item[6]),
  }));
}

export async function fetch24hrStats(symbol) {
  const url = `${KUCOIN_BASE}/market/stats?symbol=${symbol}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${symbol} stats`);
  const json = await res.json();
  if (json.code !== "200000") throw new Error(json.msg || "KuCoin API error");
  return json.data;
}
```

---

**src/lib/indicators.js**
```js
export function calculateSMA(prices, period) {
  if (prices.length < period) return null;
  const slice = prices.slice(-period);
  return slice.reduce((a, b) => a + b, 0) / period;
}

export function calculateEMA(prices, period) {
  if (prices.length < period) return null;
  const k = 2 / (period + 1);
  let ema = prices.slice(0, period).reduce((a, b) => a + b, 0) / period;
  for (let i = period; i < prices.length; i++) {
    ema = prices[i] * k + ema * (1 - k);
  }
  return ema;
}

export function calculateEMAArray(prices, period) {
  if (prices.length < period) return [];
  const k = 2 / (period + 1);
  const result = [];
  let ema = prices.slice(0, period).reduce((a, b) => a + b, 0) / period;
  for (let i = period; i < prices.length; i++) {
    ema = prices[i] * k + ema * (1 - k);
    result.push(ema);
  }
  return result;
}

export function calculateRSI(prices, period = 14) {
  if (prices.length < period + 1) return 50;
  const changes = [];
  for (let i = 1; i < prices.length; i++) {
    changes.push(prices[i] - prices[i - 1]);
  }
  const gains = changes.map((c) => (c > 0 ? c : 0));
  const losses = changes.map((c) => (c < 0 ? -c : 0));
  let avgGain = gains.slice(0, period).reduce((a, b) => a + b, 0) / period;
  let avgLoss = losses.slice(0, period).reduce((a, b) => a + b, 0) / period;
  for (let i = period; i < changes.length; i++) {
    avgGain = (avgGain * (period - 1) + gains[i]) / period;
    avgLoss = (avgLoss * (period - 1) + losses[i]) / period;
  }
  if (avgLoss === 0) return 100;
  const rs = avgGain / avgLoss;
  return 100 - 100 / (1 + rs);
}

export function calculateMACD(prices) {
  if (prices.length < 35) return { macd: 0, signal: 0, histogram: 0 };
  const ema12 = calculateEMAArray(prices, 12);
  const ema26 = calculateEMAArray(prices, 26);
  const minLen = Math.min(ema12.length, ema26.length);
  const macdLine = [];
  for (let i = 0; i < minLen; i++) {
    macdLine.push(ema12[i] - ema26[i]);
  }
  const signalLine = calculateEMAArray(macdLine, 9);
  const macd = macdLine[macdLine.length - 1];
  const signal = signalLine[signalLine.length - 1] || 0;
  const histogram = macd - signal;
  return { macd, signal, histogram };
}

export function calculateBollingerBands(prices, period = 20, multiplier = 2) {
  if (prices.length < period) return { upper: 0, middle: 0, lower: 0 };
  const slice = prices.slice(-period);
  const sma = slice.reduce((a, b) => a + b, 0) / period;
  const variance = slice.reduce((a, b) => a + Math.pow(b - sma, 2), 0) / period;
  const stdDev = Math.sqrt(variance);
  return {
    upper: sma + multiplier * stdDev,
    middle: sma,
    lower: sma - multiplier * stdDev,
  };
}

export function calculateATR(candles, period = 14) {
  if (candles.length < period + 1) return 0;
  const trs = [];
  for (let i = 1; i < candles.length; i++) {
    const high = candles[i].high;
    const low = candles[i].low;
    const prevClose = candles[i - 1].close;
    const tr = Math.max(high - low, Math.abs(high - prevClose), Math.abs(low - prevClose));
    trs.push(tr);
  }
  const slice = trs.slice(-period);
  return slice.reduce((a, b) => a + b, 0) / slice.length;
}

export function calculateVolumeRatio(candles, period = 20) {
  if (candles.length < period + 1) return 1;
  const volumes = candles.map((c) => c.volume);
  const recent = volumes.slice(-period - 1, -1);
  const avgVol = recent.reduce((a, b) => a + b, 0) / period;
  if (avgVol === 0) return 1;
  return volumes[volumes.length - 1] / avgVol;
}

export function generateSignal(candles) {
  const prices = candles.map((c) => c.close);
  if (prices.length < 50) {
    const lastPrice = prices[prices.length - 1] || 0;
    return {
      type: "NEUTRAL",
      direction: null,
      rsi: 50,
      macd: { macd: 0, signal: 0, histogram: 0 },
      emaShort: lastPrice,
      emaLong: lastPrice,
      bollinger: { upper: 0, middle: 0, lower: 0 },
      price: lastPrice,
      atr: 0,
      tp: null,
      sl: null,
      strength: 0,
      volumeRatio: 1,
      reasons: ["Insufficient data — need at least 50 candles"],
    };
  }

  const rsi = calculateRSI(prices, 14);
  const macd = calculateMACD(prices);
  const emaShort = calculateEMA(prices, 9);
  const emaLong = calculateEMA(prices, 50);
  const bb = calculateBollingerBands(prices, 20, 2);
  const atr = calculateATR(candles, 14);
  const volumeRatio = calculateVolumeRatio(candles, 20);
  const currentPrice = prices[prices.length - 1];

  const prevMacd = calculateMACD(prices.slice(0, -1));
  const histRising = macd.histogram > prevMacd.histogram;
  const histFalling = macd.histogram < prevMacd.histogram;

  let longScore = 0;
  let shortScore = 0;
  const reasons = [];

  if (rsi < 30) {
    longScore += 2;
    reasons.push(`RSI oversold (${rsi.toFixed(1)})`);
  } else if (rsi < 40) {
    longScore += 1;
    reasons.push(`RSI near oversold (${rsi.toFixed(1)})`);
  }
  if (macd.histogram > 0 && histRising) {
    longScore += 1;
    reasons.push("MACD bullish & rising");
  }
  if (emaShort > emaLong) {
    longScore += 1;
    reasons.push("Uptrend (EMA9 > EMA50)");
  }
  if (currentPrice <= bb.lower * 1.005) {
    longScore += 1;
    reasons.push("Price at lower BB");
  }

  if (rsi > 70) {
    shortScore += 2;
    reasons.push(`RSI overbought (${rsi.toFixed(1)})`);
  } else if (rsi > 60) {
    shortScore += 1;
    reasons.push(`RSI near overbought (${rsi.toFixed(1)})`);
  }
  if (macd.histogram < 0 && histFalling) {
    shortScore += 1;
    reasons.push("MACD bearish & falling");
  }
  if (emaShort < emaLong) {
    shortScore += 1;
    reasons.push("Downtrend (EMA9 < EMA50)");
  }
  if (currentPrice >= bb.upper * 0.995) {
    shortScore += 1;
    reasons.push("Price at upper BB");
  }

  if (volumeRatio > 1.5) {
    longScore += 1;
    shortScore += 1;
    reasons.push(`High volume (${volumeRatio.toFixed(1)}x avg)`);
  }

  let type = "NEUTRAL";
  let direction = null;

  if (longScore >= 4 && longScore > shortScore + 1) {
    type = longScore >= 5 ? "STRONG_BUY" : "BUY";
    direction = "LONG";
  } else if (shortScore >= 4 && shortScore > longScore + 1) {
    type = shortScore >= 5 ? "STRONG_SELL" : "SELL";
    direction = "SHORT";
  }

  let tp = null;
  let sl = null;
  if (direction === "LONG") {
    sl = currentPrice - atr * 1.5;
    tp = currentPrice + atr * 3.0;
  } else if (direction === "SHORT") {
    sl = currentPrice + atr * 1.5;
    tp = currentPrice - atr * 3.0;
  }

  return {
    type,
    direction,
    rsi,
    macd,
    emaShort,
    emaLong,
    bollinger: bb,
    price: currentPrice,
    atr,
    tp,
    sl,
    strength: Math.max(longScore, shortScore),
    volumeRatio,
    reasons,
  };
}
```

---

**src/lib/telegram.js**
```js
export async function sendTelegramMessage(botToken, chatId, text, parseMode = "HTML") {
  const url = `https://api.telegram.org/bot${botToken}/sendMessage`;
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      chat_id: chatId,
      text,
      parse_mode: parseMode,
      disable_web_page_preview: true,
    }),
  });
  const json = await res.json();
  if (!json.ok) throw new Error(json.description || "Failed to send Telegram message");
  return json;
}

function formatPrice(price) {
  if (!price) return "N/A";
  if (price >= 1) return price.toLocaleString("en-US", { maximumFractionDigits: 2 });
  return price.toFixed(6);
}

export function formatSignalMessage(signal) {
  const arrows = {
    STRONG_BUY: "🟢🟢 <b>STRONG BUY — LONG</b>",
    BUY: "🟢 <b>BUY — LONG</b>",
    NEUTRAL: "⚪ <b>NEUTRAL</b>",
    SELL: "🔴 <b>SELL — SHORT</b>",
    STRONG_SELL: "🔴🔴 <b>STRONG SELL — SHORT</b>",
  };

  const pair = signal.pair.replace("-", "/");
  const entry = formatPrice(signal.price);
  const tp = formatPrice(signal.tp);
  const sl = formatPrice(signal.sl);
  const changeStr = signal.change24h >= 0 ? `+${signal.change24h.toFixed(2)}%` : `${signal.change24h.toFixed(2)}%`;
  const trendStr = signal.emaShort > signal.emaLong ? "Uptrend ↗" : "Downtrend ↘";
  const strengthBar = "🔥".repeat(Math.min(signal.strength, 5));

  const risk = signal.tp && signal.sl ? Math.abs(signal.price - signal.sl) : 0;
  const reward = signal.tp && signal.sl ? Math.abs(signal.tp - signal.price) : 0;
  const rr = risk > 0 ? (reward / risk).toFixed(1) : "N/A";

  const slPercent = signal.sl ? Math.abs((signal.sl - signal.price) / signal.price) * 100 : 0;
  let leverage = 10;
  if (slPercent > 0 && slPercent < 2) leverage = 20;
  else if (slPercent < 4) leverage = 10;
  else leverage = 5;

  let msg = `${arrows[signal.type]}  <b>${pair}</b>  <i>⚡ Futures</i>\n`;
  msg += `━━━━━━━━━━━━━━━━━━\n`;
  msg += `💰 Entry: <b>$${entry}</b>\n`;
  msg += `🎯 Take Profit: <b>$${tp}</b>\n`;
  msg += `🛑 Stop Loss: <b>$${sl}</b>\n`;
  msg += `📊 Risk:Reward = <b>1:${rr}</b>\n`;
  msg += `⚡ Suggested Leverage: <b>${leverage}x</b>\n`;
  msg += `━━━━━━━━━━━━━━━━━━\n`;
  msg += `📈 24h: ${changeStr} | RSI: ${signal.rsi.toFixed(1)}\n`;
  msg += `📏 Trend: ${trendStr}\n`;
  msg += `💪 Strength: ${strengthBar}\n`;
  msg += `━━━━━━━━━━━━━━━━━━\n`;
  msg += `<i>Reasons:</i>\n`;
  signal.reasons.forEach((r) => {
    msg += `  • ${r}\n`;
  });
  msg += `\n🕐 ${new Date().toLocaleString("en-US")}\n`;
  msg += `📡 KuCoin | ⚙️ Base44 Signal Bot\n`;
  msg += `⚠️ <i>Not financial advice. Trade at your own risk.</i>`;

  return msg;
}

export function formatTradeClosedMessage(signal) {
  const won = signal.status === "WON";
  const pair = signal.pair.replace("-", "/");
  const entry = formatPrice(signal.price);
  const closed = formatPrice(signal.closed_price);
  const pnl = signal.pnl_percent?.toFixed(2) || "0.00";
  const pnlStr = won ? `+${pnl}%` : `${pnl}%`;
  const emoji = won ? "✅" : "❌";
  const direction = signal.direction || "";
  const hitTarget = won ? "🎯 TP Hit!" : "🛑 SL Hit!";

  let msg = `${emoji} <b>TRADE ${won ? "WON 🎉" : "LOST"}</b> — ${pair} (${direction})\n`;
  msg += `━━━━━━━━━━━━━━━━━━\n`;
  msg += `💰 Entry: $${entry}\n`;
  msg += `${won ? "🎯" : "🛑"} Exit: $${closed}\n`;
  msg += `${hitTarget}\n`;
  msg += `📊 P&L: <b>${pnlStr}</b>\n`;
  msg += `━━━━━━━━━━━━━━━━━━\n`;
  msg += `🕐 ${new Date().toLocaleString("en-US")}`;

  return msg;
}

export async function testTelegramConnection(botToken, chatId) {
  const msg =
    "✅ <b>Bot Connected Successfully!</b>\n\n" +
    "Your futures trading signal bot is now active.\n\n" +
    "📡 Data source: KuCoin (free, unlimited)\n" +
    "🎯 Each signal includes TP, SL & leverage\n" +
    "📈 Signals are tracked until TP or SL is hit\n" +
    "🔔 You'll be notified when trades win or lose\n\n" +
    "🤖 Powered by Base44";
  return sendTelegramMessage(botToken, chatId, msg);
}
```

---

**src/lib/signalTracker.js**
```js
import { base44 } from "@/api/base44Client";
import { sendTelegramMessage, formatSignalMessage, formatTradeClosedMessage } from "@/lib/telegram";

const EXPIRY_HOURS = 24;

function calculatePnL(signal, status, closedPrice) {
  const entry = signal.price;
  if (status === "EXPIRED") {
    return signal.direction === "LONG"
      ? ((closedPrice - entry) / entry) * 100
      : ((entry - closedPrice) / entry) * 100;
  }
  if (status === "WON") {
    const tp = signal.take_profit;
    return signal.direction === "LONG"
      ? ((tp - entry) / entry) * 100
      : ((entry - tp) / entry) * 100;
  }
  const sl = signal.stop_loss;
  return signal.direction === "LONG"
    ? ((sl - entry) / entry) * 100
    : ((entry - sl) / entry) * 100;
}

export async function checkActiveSignals(currentSignals, autoSend, user) {
  const activeDBSignals = await base44.entities.Signal.filter({ status: "ACTIVE" }, "-sent_at", 50);
  const stillActivePairs = new Set();

  for (const dbSignal of activeDBSignals) {
    const current = currentSignals.find((s) => s.pair === dbSignal.pair);
    if (!current) {
      stillActivePairs.add(dbSignal.pair);
      continue;
    }

    const currentPrice = current.price;
    let status = null;
    let closedPrice = null;

    if (dbSignal.direction === "LONG") {
      if (currentPrice >= dbSignal.take_profit) {
        status = "WON";
        closedPrice = dbSignal.take_profit;
      } else if (currentPrice <= dbSignal.stop_loss) {
        status = "LOST";
        closedPrice = dbSignal.stop_loss;
      }
    } else if (dbSignal.direction === "SHORT") {
      if (currentPrice <= dbSignal.take_profit) {
        status = "WON";
        closedPrice = dbSignal.take_profit;
      } else if (currentPrice >= dbSignal.stop_loss) {
        status = "LOST";
        closedPrice = dbSignal.stop_loss;
      }
    }

    if (!status && dbSignal.sent_at) {
      const elapsed = Date.now() - new Date(dbSignal.sent_at).getTime();
      if (elapsed > EXPIRY_HOURS * 60 * 60 * 1000) {
        status = "EXPIRED";
        closedPrice = currentPrice;
      }
    }

    if (status) {
      const pnlPercent = calculatePnL(dbSignal, status, closedPrice);
      await base44.entities.Signal.update(dbSignal.id, {
        status,
        closed_price: closedPrice,
        closed_at: new Date().toISOString(),
        pnl_percent: pnlPercent,
      });

      if (autoSend && user?.telegram_bot_token && user?.telegram_channel_id && status !== "EXPIRED") {
        try {
          await sendTelegramMessage(
            user.telegram_bot_token,
            user.telegram_channel_id,
            formatTradeClosedMessage({ ...dbSignal, status, closed_price: closedPrice, pnl_percent: pnlPercent })
          );
        } catch (e) {
          console.error("Close notification failed for", dbSignal.pair, e);
        }
      }
    } else {
      stillActivePairs.add(dbSignal.pair);
    }
  }

  return stillActivePairs;
}

export async function sendNewSignals(validSignals, activePairs, autoSend, user) {
  if (!autoSend || !user?.telegram_bot_token || !user?.telegram_channel_id) return;

  for (const sig of validSignals) {
    if (sig.type !== "STRONG_BUY" && sig.type !== "STRONG_SELL") continue;
    if (activePairs.has(sig.pair)) continue;

    try {
      await sendTelegramMessage(
        user.telegram_bot_token,
        user.telegram_channel_id,
        formatSignalMessage(sig)
      );
      await base44.entities.Signal.create({
        pair: sig.pair,
        signal_type: sig.type,
        direction: sig.direction,
        price: sig.price,
        take_profit: sig.tp,
        stop_loss: sig.sl,
        atr: sig.atr,
        rsi: sig.rsi,
        macd_histogram: sig.macd.histogram,
        ema_short: sig.emaShort,
        ema_long: sig.emaLong,
        change_24h: sig.change24h,
        reasons: sig.reasons,
        timeframe: "1hour",
        status: "ACTIVE",
        sent_to_telegram: true,
        sent_at: new Date().toISOString(),
      });
      activePairs.add(sig.pair);
    } catch (e) {
      console.error("Auto-send failed for", sig.pair, e);
    }
  }
}
```

---

**src/pages/Dashboard.jsx**
```jsx
import React, { useState, useEffect, useCallback, useRef } from "react";
import { base44 } from "@/api/base44Client";
import { fetchCandles, fetch24hrStats, DEFAULT_PAIRS } from "@/lib/kucoin";
import { generateSignal } from "@/lib/indicators";
import { sendTelegramMessage, formatSignalMessage } from "@/lib/telegram";
import { checkActiveSignals, sendNewSignals } from "@/lib/signalTracker";
import { useToast } from "@/components/ui/use-toast";
import SignalCard from "@/components/SignalCard";
import ControlBar from "@/components/ControlBar";
import TrackedPositions from "@/components/TrackedPositions";
import { TrendingUp, TrendingDown, Radio, Wifi } from "lucide-react";

export default function Dashboard() {
  const [signals, setSignals] = useState([]);
  const [trackedPositions, setTrackedPositions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [autoSend, setAutoSend] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [sendingPair, setSendingPair] = useState(null);
  const [user, setUser] = useState(null);
  const [pairs, setPairs] = useState(DEFAULT_PAIRS);
  const loadRef = useRef(null);
  const { toast } = useToast();

  useEffect(() => {
    base44
      .auth.me()
      .then((u) => {
        setUser(u);
        if (u.monitored_pairs?.length) setPairs(u.monitored_pairs);
        if (u.auto_send_telegram) setAutoSend(true);
      })
      .catch(() => {});
  }, []);

  const loadSignals = useCallback(async () => {
    try {
      setLoading(true);
      const results = await Promise.all(
        pairs.map(async (pair) => {
          try {
            const [candles, stats] = await Promise.all([fetchCandles(pair, "1hour"), fetch24hrStats(pair)]);
            const signal = generateSignal(candles);
            return {
              ...signal,
              pair,
              candles: candles.slice(-48),
              change24h: stats?.changeRate ? parseFloat(stats.changeRate) * 100 : 0,
            };
          } catch {
            return null;
          }
        })
      );

      const validSignals = results.filter((r) => r !== null);
      const order = { STRONG_BUY: 4, BUY: 3, STRONG_SELL: 2, SELL: 1, NEUTRAL: 0 };
      validSignals.sort((a, b) => order[b.type] - order[a.type]);

      setSignals(validSignals);
      setLastUpdate(new Date());

      const activePairs = await checkActiveSignals(validSignals, autoSend, user);
      await sendNewSignals(validSignals, activePairs, autoSend, user);

      try {
        const active = await base44.entities.Signal.filter({ status: "ACTIVE" }, "-sent_at", 20);
        setTrackedPositions(active);
      } catch {}
    } catch (e) {
      toast({ title: "Error loading signals", description: e.message, variant: "destructive" });
    } finally {
      setLoading(false);
    }
  }, [pairs, autoSend, user, toast]);

  loadRef.current = loadSignals;

  useEffect(() => {
    loadRef.current();
  }, []);

  useEffect(() => {
    if (!autoRefresh) return;
    const interval = setInterval(() => loadRef.current(), 60000);
    return () => clearInterval(interval);
  }, [autoRefresh]);

  const handleSendToTelegram = async (signal) => {
    if (!user?.telegram_bot_token || !user?.telegram_channel_id) {
      toast({ title: "Telegram not configured", description: "Go to Settings to set up your Telegram bot.", variant: "destructive" });
      return;
    }
    setSendingPair(signal.pair);
    try {
      await sendTelegramMessage(user.telegram_bot_token, user.telegram_channel_id, formatSignalMessage(signal));

      if (signal.direction) {
        await base44.entities.Signal.create({
          pair: signal.pair,
          signal_type: signal.type,
          direction: signal.direction,
          price: signal.price,
          take_profit: signal.tp,
          stop_loss: signal.sl,
          atr: signal.atr,
          rsi: signal.rsi,
          macd_histogram: signal.macd.histogram,
          ema_short: signal.emaShort,
          ema_long: signal.emaLong,
          change_24h: signal.change24h,
          reasons: signal.reasons,
          timeframe: "1hour",
          status: "ACTIVE",
          sent_to_telegram: true,
          sent_at: new Date().toISOString(),
        });
        const active = await base44.entities.Signal.filter({ status: "ACTIVE" }, "-sent_at", 20);
        setTrackedPositions(active);
      }
      toast({ title: "✅ Signal sent to Telegram", description: `${signal.pair.replace("-", "/")} — ${signal.type}` });
    } catch (e) {
      toast({ title: "Failed to send", description: e.message, variant: "destructive" });
    } finally {
      setSendingPair(null);
    }
  };

  const buyCount = signals.filter((s) => s.type === "BUY" || s.type === "STRONG_BUY").length;
  const sellCount = signals.filter((s) => s.type === "SELL" || s.type === "STRONG_SELL").length;
  const telegramConnected = !!(user?.telegram_bot_token && user?.telegram_channel_id);
  const currentPrices = {};
  signals.forEach((s) => { currentPrices[s.pair] = s.price; });

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-1">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-400 to-emerald-600 flex items-center justify-center shadow-lg shadow-emerald-500/20">
              <Radio size={20} className="text-white" />
            </div>
            <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
              Crypto Signal Bot
            </h1>
          </div>
          <p className="text-slate-400 text-sm">Futures trading signals · KuCoin data · TP/SL tracking · Telegram delivery</p>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-6">
            <div className="bg-slate-900/60 rounded-xl border border-slate-800 p-4 flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-emerald-500/10 flex items-center justify-center">
                <TrendingUp size={18} className="text-emerald-400" />
              </div>
              <div>
                <div className="text-xs text-slate-500 uppercase">Buy</div>
                <div className="text-xl font-bold text-emerald-400">{buyCount}</div>
              </div>
            </div>
            <div className="bg-slate-900/60 rounded-xl border border-slate-800 p-4 flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-red-500/10 flex items-center justify-center">
                <TrendingDown size={18} className="text-red-400" />
              </div>
              <div>
                <div className="text-xs text-slate-500 uppercase">Sell</div>
                <div className="text-xl font-bold text-red-400">{sellCount}</div>
              </div>
            </div>
            <div className="bg-slate-900/60 rounded-xl border border-slate-800 p-4 flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-blue-500/10 flex items-center justify-center">
                <Wifi size={18} className="text-blue-400" />
              </div>
              <div>
                <div className="text-xs text-slate-500 uppercase">Pairs</div>
                <div className="text-xl font-bold text-white">{pairs.length}</div>
              </div>
            </div>
            <div className="bg-slate-900/60 rounded-xl border border-slate-800 p-4">
              <div className="text-xs text-slate-500 uppercase">Telegram</div>
              <div className="text-xl font-bold">
                {telegramConnected ? <span className="text-emerald-400">Connected</span> : <span className="text-slate-500">Off</span>}
              </div>
            </div>
          </div>
        </div>

        <ControlBar
          autoRefresh={autoRefresh}
          onToggleAutoRefresh={() => setAutoRefresh((v) => !v)}
          autoSend={autoSend}
          onToggleAutoSend={() => setAutoSend((v) => !v)}
          onRefresh={loadSignals}
          loading={loading}
          lastUpdate={lastUpdate}
          signalCount={signals.length}
          telegramConnected={telegramConnected}
        />

        <TrackedPositions positions={trackedPositions} currentPrices={currentPrices} />

        {loading && signals.length === 0 ? (
          <div className="flex items-center justify-center py-20">
            <div className="w-8 h-8 border-4 border-slate-700 border-t-emerald-400 rounded-full animate-spin" />
          </div>
        ) : signals.length === 0 ? (
          <div className="text-center py-20 text-slate-500">No signals available. Check your connection.</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {signals.map((signal) => (
              <SignalCard
                key={signal.pair}
                signal={signal}
                onSendToTelegram={handleSendToTelegram}
                sending={sendingPair === signal.pair}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
```

---

**src/pages/Settings.jsx**
```jsx
import React, { useState, useEffect } from "react";
import { base44 } from "@/api/base44Client";
import { testTelegramConnection } from "@/lib/telegram";
import { useToast } from "@/components/ui/use-toast";
import { Link } from "react-router-dom";
import { ArrowLeft, Save, TestTube, Plus, X, Bot, Coins } from "lucide-react";
import { DEFAULT_PAIRS } from "@/lib/kucoin";

export default function Settings() {
  const [botToken, setBotToken] = useState("");
  const [channelId, setChannelId] = useState("");
  const [pairs, setPairs] = useState(DEFAULT_PAIRS);
  const [newPair, setNewPair] = useState("");
  const [saving, setSaving] = useState(false);
  const [testing, setTesting] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    base44
      .auth.me()
      .then((u) => {
        setBotToken(u.telegram_bot_token || "");
        setChannelId(u.telegram_channel_id || "");
        if (u.monitored_pairs?.length) setPairs(u.monitored_pairs);
      })
      .catch(() => {});
  }, []);

  const handleSave = async () => {
    setSaving(true);
    try {
      await base44.auth.updateMe({
        telegram_bot_token: botToken,
        telegram_channel_id: channelId,
        monitored_pairs: pairs,
      });
      toast({ title: "✅ Settings saved" });
    } catch (e) {
      toast({ title: "Failed to save", description: e.message, variant: "destructive" });
    } finally {
      setSaving(false);
    }
  };

  const handleTest = async () => {
    if (!botToken || !channelId) {
      toast({ title: "Enter bot token and channel ID first", variant: "destructive" });
      return;
    }
    setTesting(true);
    try {
      await testTelegramConnection(botToken, channelId);
      toast({ title: "✅ Test message sent to Telegram!" });
    } catch (e) {
      toast({ title: "Connection failed", description: e.message, variant: "destructive" });
    } finally {
      setTesting(false);
    }
  };

  const addPair = () => {
    const pair = newPair.trim().toUpperCase();
    if (pair && !pairs.includes(pair)) {
      setPairs([...pairs, pair]);
      setNewPair("");
    }
  };

  const removePair = (pair) => {
    setPairs(pairs.filter((p) => p !== pair));
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-2xl mx-auto px-4 py-6">
        <Link to="/" className="inline-flex items-center gap-2 text-slate-400 hover:text-white text-sm mb-6 transition-colors">
          <ArrowLeft size={16} /> Back to Dashboard
        </Link>

        <h1 className="text-2xl font-bold mb-8">Settings</h1>

        <div className="bg-slate-900/60 rounded-2xl border border-slate-800 p-6 mb-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-lg bg-blue-500/10 flex items-center justify-center">
              <Bot size={18} className="text-blue-400" />
            </div>
            <div>
              <h2 className="text-lg font-semibold">Telegram Bot</h2>
              <p className="text-sm text-slate-400">Free — create a bot via @BotFather on Telegram</p>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1">Bot Token</label>
              <input
                type="password"
                value={botToken}
                onChange={(e) => setBotToken(e.target.value)}
                placeholder="123456789:ABCdefGHIjklMNOpqrSTUvwxYZ"
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-1">Channel / Chat ID</label>
              <input
                type="text"
                value={channelId}
                onChange={(e) => setChannelId(e.target.value)}
                placeholder="@mychannel or -1001234567890"
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors"
              />
              <p className="text-xs text-slate-500 mt-1">
                For channels: add the bot as admin. For groups: use the numeric chat ID.
              </p>
            </div>
            <div className="flex gap-3 pt-1">
              <button
                onClick={handleSave}
                disabled={saving}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-emerald-500 text-white text-sm font-semibold hover:bg-emerald-600 disabled:opacity-50 transition-colors"
              >
                <Save size={14} /> {saving ? "Saving..." : "Save"}
              </button>
              <button
                onClick={handleTest}
                disabled={testing}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-800 text-white text-sm font-medium hover:bg-slate-700 disabled:opacity-50 border border-slate-700 transition-colors"
              >
                <TestTube size={14} /> {testing ? "Testing..." : "Test Connection"}
              </button>
            </div>
          </div>
        </div>

        <div className="bg-slate-900/60 rounded-2xl border border-slate-800 p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-lg bg-emerald-500/10 flex items-center justify-center">
              <Coins size={18} className="text-emerald-400" />
            </div>
            <div>
              <h2 className="text-lg font-semibold">Monitored Pairs</h2>
              <p className="text-sm text-slate-400">KuCoin trading pairs (format: BTC-USDT)</p>
            </div>
          </div>

          <div className="flex gap-2 mb-4">
            <input
              type="text"
              value={newPair}
              onChange={(e) => setNewPair(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && addPair()}
              placeholder="Add pair (e.g. ATOM-USDT)"
              className="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition-colors"
            />
            <button
              onClick={addPair}
              className="flex items-center gap-1 px-3 py-2 rounded-lg bg-slate-800 text-white hover:bg-slate-700 border border-slate-700 transition-colors"
            >
              <Plus size={14} /> Add
            </button>
          </div>

          <div className="flex flex-wrap gap-2">
            {pairs.map((pair) => (
              <div key={pair} className="flex items-center gap-2 bg-slate-800 rounded-lg px-3 py-1.5 text-sm border border-slate-700">
                <span>{pair.replace("-", "/")}</span>
                <button onClick={() => removePair(pair)} className="text-slate-500 hover:text-red-400 transition-colors">
                  <X size={14} />
                </button>
              </div>
            ))}
          </div>

          <button
            onClick={handleSave}
            disabled={saving}
            className="mt-4 flex items-center gap-2 px-4 py-2 rounded-lg bg-emerald-500 text-white text-sm font-semibold hover:bg-emerald-600 disabled:opacity-50 transition-colors"
          >
            <Save size={14} /> Save Pairs
          </button>
        </div>

        <div className="bg-slate-900/60 rounded-2xl border border-slate-800 p-6 mt-6">
          <h2 className="text-lg font-semibold mb-3">How it works</h2>
          <ol className="space-y-2 text-sm text-slate-400">
            <li>1. Create a free Telegram bot via <span className="text-blue-400">@BotFather</span> and get the token</li>
            <li>2. Create a Telegram channel and add your bot as admin (or use a group chat ID)</li>
            <li>3. Enter the bot token and channel ID above, then Save</li>
            <li>4. Click <span className="text-emerald-400">Test Connection</span> to verify</li>
            <li>5. Go back to the dashboard and enable <span className="text-blue-400">Auto-Send TG</span></li>
            <li>6. The bot will automatically send new buy/sell signals to your Telegram channel</li>
          </ol>
          <div className="mt-4 p-3 rounded-lg bg-slate-800/50 text-xs text-slate-400">
            💡 <span className="font-medium">Data source:</span> KuCoin public API (free, unlimited crypto pairs).
            <br />
            💡 <span className="font-medium">Delivery:</span> Telegram Bot API (free, no subscription needed).
            <br />
            ⚠️ <span className="font-medium">Not financial advice.</span> Signals are based on technical indicators only.
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

**src/pages/Login.jsx**
```jsx
import React, { useState } from "react";
import { Link } from "react-router-dom";
import { base44 } from "@/api/base44Client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { LogIn, Mail, Lock, Loader2 } from "lucide-react";
import AuthLayout from "@/components/AuthLayout";
import GoogleIcon from "@/components/GoogleIcon";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await base44.auth.loginViaEmailPassword(email, password);
      window.location.href = "/";
    } catch (err) {
      setError(err.message || "Invalid email or password");
    } finally {
      setLoading(false);
    }
  };

  const handleGoogle = () => {
    base44.auth.loginWithProvider("google", "/");
  };

  return (
    <AuthLayout
      icon={LogIn}
      title="Welcome back"
      subtitle="Log in to your account"
      footer={
        <>
          Don't have an account?{" "}
          <Link to="/register" className="text-primary font-medium hover:underline">
            Create one
          </Link>
        </>
      }
    >
      <Button
        variant="outline"
        className="w-full h-12 text-sm font-medium mb-6"
        onClick={handleGoogle}
      >
        <GoogleIcon className="w-5 h-5 mr-2" />
        Continue with Google
      </Button>

      <div className="relative mb-6">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-border" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-card px-3 text-muted-foreground">or</span>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 rounded-lg bg-destructive/10 text-destructive text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" aria-hidden="true" />
            <Input
              id="email"
              type="email"
              autoComplete="email"
              autoFocus
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="pl-10 h-12"
              required
            />
          </div>
        </div>
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <Label htmlFor="password">Password</Label>
            <Link to="/forgot-password" className="text-xs text-primary hover:underline">
              Forgot password?
            </Link>
          </div>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" aria-hidden="true" />
            <Input
              id="password"
              type="password"
              autoComplete="current-password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="pl-10 h-12"
              required
            />
          </div>
        </div>
        <Button type="submit" className="w-full h-12 font-medium" disabled={loading}>
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              Logging in...
            </>
          ) : (
            "Log in"
          )}
        </Button>
      </form>
    </AuthLayout>
  );
}
```

---

**src/pages/Register.jsx**
```jsx
import React, { useState } from "react";
import { Link } from "react-router-dom";
import { base44 } from "@/api/base44Client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { UserPlus, Mail, Lock, Loader2 } from "lucide-react";
import { InputOTP, InputOTPGroup, InputOTPSlot } from "@/components/ui/input-otp";
import AuthLayout from "@/components/AuthLayout";
import GoogleIcon from "@/components/GoogleIcon";
import { toast } from "@/components/ui/use-toast";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showOtp, setShowOtp] = useState(false);
  const [otpCode, setOtpCode] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }
    setLoading(true);
    try {
      await base44.auth.register({ email, password });
      setShowOtp(true);
    } catch (err) {
      setError(err.message || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  const handleVerify = async () => {
    setError("");
    setLoading(true);
    try {
      const result = await base44.auth.verifyOtp({ email, otpCode });
      if (result?.access_token) {
        base44.auth.setToken(result.access_token);
      }
      window.location.href = "/";
    } catch (err) {
      setError(err.message || "Invalid verification code");
    } finally {
      setLoading(false);
    }
  };

  const handleResend = async () => {
    setError("");
    try {
      await base44.auth.resendOtp(email);
      toast({
        title: "Code sent",
        description: "Check your email for the new code.",
      });
    } catch (err) {
      setError(err.message || "Failed to resend code");
    }
  };

  const handleGoogle = () => {
    base44.auth.loginWithProvider("google", "/");
  };

  if (showOtp) {
    return (
      <AuthLayout
        icon={Mail}
        title="Verify your email"
        subtitle={`We sent a code to ${email}`}
      >
        {error && (
          <div className="mb-4 p-3 rounded-lg bg-destructive/10 text-destructive text-sm">
            {error}
          </div>
        )}
        <div className="flex justify-center mb-6">
          <InputOTP
            maxLength={6}
            value={otpCode}
            onChange={setOtpCode}
            autoFocus
            autoComplete="one-time-code"
          >
            <InputOTPGroup>
              <InputOTPSlot index={0} />
              <InputOTPSlot index={1} />
              <InputOTPSlot index={2} />
              <InputOTPSlot index={3} />
              <InputOTPSlot index={4} />
              <InputOTPSlot index={5} />
            </InputOTPGroup>
          </InputOTP>
        </div>
        <Button
          className="w-full h-12 font-medium"
          onClick={handleVerify}
          disabled={loading || otpCode.length < 6}
        >
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              Verifying...
            </>
          ) : (
            "Verify"
          )}
        </Button>
        <p className="text-center text-sm text-muted-foreground mt-4">
          Didn't receive the code?{" "}
          <button onClick={handleResend} className="text-primary font-medium hover:underline">
            Resend
          </button>
        </p>
      </AuthLayout>
    );
  }

  return (
    <AuthLayout
      icon={UserPlus}
      title="Create your account"
      subtitle="Sign up to get started"
      footer={
        <>
          Already have an account?{" "}
          <Link to="/login" className="text-primary font-medium hover:underline">
            Log in
          </Link>
        </>
      }
    >
      <Button
        variant="outline"
        className="w-full h-12 text-sm font-medium mb-6"
        onClick={handleGoogle}
      >
        <GoogleIcon className="w-5 h-5 mr-2" />
        Continue with Google
      </Button>

      <div className="relative mb-6">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-border" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-card px-3 text-muted-foreground">or</span>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 rounded-lg bg-destructive/10 text-destructive text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" aria-hidden="true" />
            <Input
              id="email"
              type="email"
              autoComplete="email"
              autoFocus
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="pl-10 h-12"
              required
            />
          </div>
        </div>
        <div className="space-y-2">
          <Label htmlFor="password">Password</Label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" aria-hidden="true" />
            <Input
              id="password"
              type="password"
              autoComplete="new-password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="pl-10 h-12"
              required
            />
          </div>
        </div>
        <div className="space-y-2">
          <Label htmlFor="confirm">Confirm Password</Label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" aria-hidden="true" />
            <Input
              id="confirm"
              type="password"
              autoComplete="new-password"
              placeholder="••••••••"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="pl-10 h-12"
              required
            />
          </div>
        </div>
        <Button type="submit" className="w-full h-12 font-medium" disabled={loading}>
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              Creating account...
            </>
          ) : (
            "Create account"
          )}
        </Button>
      </form>
    </AuthLayout>
  );
}
```

---

**src/pages/ForgotPassword.jsx**
```jsx
import React, { useState } from "react";
import { Link } from "react-router-dom";
import { base44 } from "@/api/base44Client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Mail, ArrowLeft, Loader2 } from "lucide-react";
import AuthLayout from "@/components/AuthLayout";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await base44.auth.resetPasswordRequest(email);
    } catch {
    } finally {
      setLoading(false);
      setSent(true);
    }
  };

  return (
    <AuthLayout
      icon={Mail}
      title="Reset password"
      subtitle="We'll send you a link to reset it"
      footer={
        <Link to="/login" className="text-primary font-medium hover:underline">
          <ArrowLeft className="w-3 h-3 inline mr-1" />Back to log in
        </Link>
      }
    >
      {sent ? (
        <p className="text-sm text-foreground text-center">
          If an account exists with that email, you'll receive a password reset link shortly.
        </p>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email address</Label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" aria-hidden="true" />
              <Input
                id="email"
                type="email"
                autoComplete="email"
                autoFocus
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="pl-10 h-12"
                required
              />
            </div>
          </div>
          <Button type="submit" className="w-full h-12 font-medium" disabled={loading}>
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Sending...
              </>
            ) : (
              "Send reset link"
            )}
          </Button>
        </form>
      )}
    </AuthLayout>
  );
}
```

---

**src/pages/ResetPassword.jsx**
```jsx
import React, { useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { base44 } from "@/api/base44Client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Lock, Loader2, AlertTriangle } from "lucide-react";
import AuthLayout from "@/components/AuthLayout";

export default function ResetPassword() {
  const [searchParams] = useSearchParams();
  const resetToken = searchParams.get("token");

  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    if (newPassword !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }
    setLoading(true);
    try {
      await base44.auth.resetPassword({ resetToken, newPassword });
      window.location.href = "/login";
    } catch (err) {
      setError(err.message || "Failed to reset password");
    } finally {
      setLoading(false);
    }
  };

  if (!resetToken) {
    return (
      <AuthLayout
        icon={AlertTriangle}
        title="Invalid reset link"
        subtitle="This password reset link is missing or invalid"
        footer={
          <Link to="/forgot-password" className="text-primary font-medium hover:underline">
            Request a new link
          </Link>
        }
      >
        <p className="text-sm text-foreground text-center">
          The link you used appears to be incomplete. Please request a new password reset email.
        </p>
      </AuthLayout>
    );
  }

  return (
    <AuthLayout
      icon={Lock}
      title="New password"
      subtitle="Enter your new password below"
    >
      {error && (
        <div className="mb-4 p-3 rounded-lg bg-destructive/10 text-destructive text-sm">
          {error}
        </div>
      )}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="password">New Password</Label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" aria-hidden="true" />
            <Input
              id="password"
              type="password"
              autoComplete="new-password"
              autoFocus
              placeholder="••••••••"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              className="pl-10 h-12"
              required
            />
          </div>
        </div>
        <div className="space-y-2">
          <Label htmlFor="confirm">Confirm Password</Label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" aria-hidden="true" />
            <Input
              id="confirm"
              type="password"
              autoComplete="new-password"
              placeholder="••••••••"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="pl-10 h-12"
              required
            />
          </div>
        </div>
        <Button type="submit" className="w-full h-12 font-medium" disabled={loading}>
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              Resetting...
            </>
          ) : (
            "Reset password"
          )}
        </Button>
      </form>
    </AuthLayout>
  );
}
```

---

**src/components/ControlBar.jsx**
```jsx
import React from "react";
import { RefreshCw, Send, Activity, Clock, Settings as SettingsIcon } from "lucide-react";
import { Link } from "react-router-dom";

export default function ControlBar({ autoRefresh, onToggleAutoRefresh, autoSend, onToggleAutoSend, onRefresh, loading, lastUpdate, signalCount, telegramConnected }) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
      <div className="flex items-center gap-4 flex-wrap">
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${loading ? "bg-yellow-400 animate-pulse" : "bg-emerald-400 animate-pulse"}`} />
          <span className="text-sm text-slate-400">{loading ? "Updating..." : "Live"}</span>
        </div>
        <div className="flex items-center gap-1.5 text-sm text-slate-400">
          <Activity size={14} />
          <span>{signalCount} pairs</span>
        </div>
        {lastUpdate && (
          <div className="flex items-center gap-1.5 text-sm text-slate-400">
            <Clock size={14} />
            <span>{lastUpdate.toLocaleTimeString()}</span>
          </div>
        )}
      </div>

      <div className="flex items-center gap-2 flex-wrap">
        <button
          onClick={onToggleAutoSend}
          disabled={!telegramConnected}
          title={!telegramConnected ? "Configure Telegram in Settings first" : ""}
          className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${autoSend ? "bg-blue-500/20 text-blue-400 border border-blue-500/40" : "bg-slate-800 text-slate-400 border border-slate-700"} disabled:opacity-40 disabled:cursor-not-allowed`}
        >
          <Send size={14} />
          Auto-Send TG
        </button>
        <button
          onClick={onToggleAutoRefresh}
          className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${autoRefresh ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/40" : "bg-slate-800 text-slate-400 border border-slate-700"}`}
        >
          <RefreshCw size={14} className={autoRefresh && loading ? "animate-spin" : ""} />
          Auto
        </button>
        <button
          onClick={onRefresh}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-1.5 rounded-lg bg-white text-slate-900 text-sm font-semibold hover:bg-slate-200 transition-colors disabled:opacity-50"
        >
          <RefreshCw size={14} className={loading ? "animate-spin" : ""} />
          Refresh
        </button>
        <Link
          to="/settings"
          className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-800 text-slate-400 text-sm font-medium hover:text-white border border-slate-700 transition-colors"
        >
          <SettingsIcon size={14} />
          Settings
        </Link>
      </div>
    </div>
  );
}
```

---

**src/components/SignalCard.jsx**
```jsx
import React from "react";
import { AreaChart, Area, ResponsiveContainer, YAxis } from "recharts";
import { Send, Loader2, Target, Shield } from "lucide-react";

const SIGNAL_CONFIG = {
  STRONG_BUY: { label: "STRONG BUY", badge: "bg-emerald-500", text: "text-emerald-400", border: "border-emerald-500/30", glow: "shadow-emerald-500/10", dir: "LONG" },
  BUY: { label: "BUY", badge: "bg-green-500", text: "text-green-400", border: "border-green-500/30", glow: "shadow-green-500/10", dir: "LONG" },
  NEUTRAL: { label: "NEUTRAL", badge: "bg-slate-600", text: "text-slate-400", border: "border-slate-700", glow: "", dir: null },
  SELL: { label: "SELL", badge: "bg-orange-500", text: "text-orange-400", border: "border-orange-500/30", glow: "shadow-orange-500/10", dir: "SHORT" },
  STRONG_SELL: { label: "STRONG SELL", badge: "bg-red-500", text: "text-red-400", border: "border-red-500/30", glow: "shadow-red-500/10", dir: "SHORT" },
};

function formatPrice(price) {
  if (!price) return "—";
  if (price >= 1) return price.toLocaleString("en-US", { maximumFractionDigits: 2 });
  return price.toFixed(6);
}

export default function SignalCard({ signal, onSendToTelegram, sending }) {
  const config = SIGNAL_CONFIG[signal.type] || SIGNAL_CONFIG.NEUTRAL;
  const isBullish = signal.type === "STRONG_BUY" || signal.type === "BUY";
  const isBearish = signal.type === "STRONG_SELL" || signal.type === "SELL";
  const changePositive = signal.change24h >= 0;
  const chartColor = isBullish ? "#10b981" : isBearish ? "#ef4444" : "#6b7280";

  const chartData = (signal.candles || []).map((c, i) => ({ i, price: c.close }));
  const gradId = `grad-${signal.pair.replace(/[^a-zA-Z0-9]/g, "")}`;

  const risk = signal.tp && signal.sl ? Math.abs(signal.price - signal.sl) : 0;
  const reward = signal.tp && signal.sl ? Math.abs(signal.tp - signal.price) : 0;
  const rr = risk > 0 ? (reward / risk).toFixed(1) : "—";

  const slPercent = signal.sl ? Math.abs((signal.sl - signal.price) / signal.price) * 100 : 0;
  let leverage = 10;
  if (slPercent > 0 && slPercent < 2) leverage = 20;
  else if (slPercent < 4) leverage = 10;
  else leverage = 5;

  return (
    <div className={`relative rounded-2xl border ${config.border} bg-slate-900/60 backdrop-blur-xl p-5 transition-all hover:scale-[1.01] hover:shadow-xl ${config.glow}`}>
      <div className="flex items-start justify-between mb-3">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="text-lg font-bold text-white">{signal.pair.replace("-", "/")}</h3>
            {signal.direction && (
              <span className={`text-[10px] px-1.5 py-0.5 rounded font-bold ${isBullish ? "bg-emerald-500/20 text-emerald-400" : "bg-red-500/20 text-red-400"}`}>
                {signal.direction}
              </span>
            )}
          </div>
          <div className="flex items-baseline gap-2 mt-1">
            <span className="text-2xl font-bold text-white">${formatPrice(signal.price)}</span>
            <span className={`text-sm font-semibold ${changePositive ? "text-emerald-400" : "text-red-400"}`}>
              {changePositive ? "▲" : "▼"} {Math.abs(signal.change24h).toFixed(2)}%
            </span>
          </div>
        </div>
        <div className={`px-3 py-1.5 rounded-lg ${config.badge} text-white text-[11px] font-bold tracking-wide whitespace-nowrap`}>
          {config.label}
        </div>
      </div>

      {chartData.length > 1 && (
        <div className="h-14 mb-3 -mx-1">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id={gradId} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor={chartColor} stopOpacity={0.35} />
                  <stop offset="100%" stopColor={chartColor} stopOpacity={0} />
                </linearGradient>
              </defs>
              <Area type="monotone" dataKey="price" stroke={chartColor} strokeWidth={1.5} fill={`url(#${gradId})`} />
              <YAxis domain={["dataMin", "dataMax"]} hide />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}

      {signal.direction && (
        <div className="grid grid-cols-3 gap-2 mb-3">
          <div className="bg-slate-800/50 rounded-lg p-2 border border-slate-700/50">
            <div className="flex items-center gap-1 text-[10px] uppercase text-slate-500 font-medium">
              <Target size={10} className="text-emerald-400" /> TP
            </div>
            <div className="text-sm font-bold text-emerald-400">${formatPrice(signal.tp)}</div>
          </div>
          <div className="bg-slate-800/50 rounded-lg p-2 border border-slate-700/50">
            <div className="flex items-center gap-1 text-[10px] uppercase text-slate-500 font-medium">
              <Shield size={10} className="text-red-400" /> SL
            </div>
            <div className="text-sm font-bold text-red-400">${formatPrice(signal.sl)}</div>
          </div>
          <div className="bg-slate-800/50 rounded-lg p-2 border border-slate-700/50">
            <div className="text-[10px] uppercase text-slate-500 font-medium">R:R / Lev</div>
            <div className="text-sm font-bold text-white">1:{rr} · {leverage}x</div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-3 gap-2 mb-3">
        <div className="bg-slate-800/50 rounded-lg p-2">
          <div className="text-[10px] uppercase text-slate-500 font-medium">RSI</div>
          <div className={`text-sm font-bold ${signal.rsi < 30 ? "text-emerald-400" : signal.rsi > 70 ? "text-red-400" : "text-white"}`}>
            {signal.rsi.toFixed(1)}
          </div>
        </div>
        <div className="bg-slate-800/50 rounded-lg p-2">
          <div className="text-[10px] uppercase text-slate-500 font-medium">MACD</div>
          <div className={`text-sm font-bold ${signal.macd.histogram >= 0 ? "text-emerald-400" : "text-red-400"}`}>
            {signal.macd.histogram >= 0 ? "Bull" : "Bear"}
          </div>
        </div>
        <div className="bg-slate-800/50 rounded-lg p-2">
          <div className="text-[10px] uppercase text-slate-500 font-medium">Trend</div>
          <div className={`text-sm font-bold ${signal.emaShort > signal.emaLong ? "text-emerald-400" : "text-red-400"}`}>
            {signal.emaShort > signal.emaLong ? "Up" : "Down"}
          </div>
        </div>
      </div>

      <div className="flex flex-wrap gap-1 mb-3">
        {signal.reasons.slice(0, 3).map((r, i) => (
          <span key={i} className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-400">
            {r}
          </span>
        ))}
      </div>

      <button
        onClick={() => onSendToTelegram(signal)}
        disabled={sending}
        className="w-full flex items-center justify-center gap-2 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-white text-sm font-medium transition-colors disabled:opacity-50 border border-slate-700"
      >
        {sending ? <Loader2 size={14} className="animate-spin" /> : <Send size={14} />}
        {sending ? "Sending..." : "Send to Telegram"}
      </button>
    </div>
  );
}
```

---

**src/components/TrackedPositions.jsx**
```jsx
import React from "react";
import { Target, TrendingUp, TrendingDown, Clock } from "lucide-react";

function formatPrice(price) {
  if (!price) return "—";
  if (price >= 1) return price.toLocaleString("en-US", { maximumFractionDigits: 2 });
  return price.toFixed(6);
}

export default function TrackedPositions({ positions, currentPrices }) {
  if (!positions?.length) return null;

  return (
    <div className="mb-8">
      <div className="flex items-center gap-2 mb-4">
        <Target size={18} className="text-blue-400" />
        <h2 className="text-xl font-bold text-white">Tracked Positions</h2>
        <span className="text-sm text-slate-500">({positions.length} active)</span>
      </div>
      <div className="space-y-2">
        {positions.map((pos) => {
          const currentPrice = currentPrices[pos.pair];
          const pnl =
            pos.direction === "LONG" && currentPrice
              ? ((currentPrice - pos.price) / pos.price) * 100
              : pos.direction === "SHORT" && currentPrice
              ? ((pos.price - currentPrice) / pos.price) * 100
              : 0;
          const pnlPositive = pnl >= 0;
          const isLong = pos.direction === "LONG";
          const elapsed = pos.sent_at
            ? Math.round((Date.now() - new Date(pos.sent_at).getTime()) / (1000 * 60))
            : 0;

          return (
            <div
              key={pos.id}
              className="bg-slate-900/60 rounded-xl border border-slate-800 p-4 flex flex-wrap items-center justify-between gap-3"
            >
              <div className="flex items-center gap-3">
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${isLong ? "bg-emerald-500/10" : "bg-red-500/10"}`}>
                  {isLong ? <TrendingUp size={16} className="text-emerald-400" /> : <TrendingDown size={16} className="text-red-400" />}
                </div>
                <div>
                  <div className="font-bold text-white">{pos.pair.replace("-", "/")}</div>
                  <div className={`text-xs font-medium ${isLong ? "text-emerald-400" : "text-red-400"}`}>{pos.direction}</div>
                </div>
              </div>

              <div className="flex items-center gap-5 text-sm flex-wrap">
                <div>
                  <div className="text-[10px] uppercase text-slate-500">Entry</div>
                  <div className="text-white font-medium">${formatPrice(pos.price)}</div>
                </div>
                <div>
                  <div className="text-[10px] uppercase text-slate-500">TP</div>
                  <div className="text-emerald-400 font-medium">${formatPrice(pos.take_profit)}</div>
                </div>
                <div>
                  <div className="text-[10px] uppercase text-slate-500">SL</div>
                  <div className="text-red-400 font-medium">${formatPrice(pos.stop_loss)}</div>
                </div>
                {currentPrice && (
                  <div>
                    <div className="text-[10px] uppercase text-slate-500">Live P&L</div>
                    <div className={`font-bold ${pnlPositive ? "text-emerald-400" : "text-red-400"}`}>
                      {pnlPositive ? "+" : ""}{pnl.toFixed(2)}%
                    </div>
                  </div>
                )}
                <div className="flex items-center gap-1 text-xs text-slate-500">
                  <Clock size={12} />
                  {elapsed}m
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
```

---

**src/components/ProtectedRoute.jsx**
```jsx
import { useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import { useAuth } from '@/lib/AuthContext';
import UserNotRegisteredError from '@/components/UserNotRegisteredError';

const DefaultFallback = () => (
  <div className="fixed inset-0 flex items-center justify-center">
    <div className="w-8 h-8 border-4 border-slate-200 border-t-slate-800 rounded-full animate-spin"></div>
  </div>
);

export default function ProtectedRoute({ fallback = <DefaultFallback />, unauthenticatedElement }) {
  const { isAuthenticated, isLoadingAuth, authChecked, authError, checkUserAuth } = useAuth();

  useEffect(() => {
    if (!authChecked && !isLoadingAuth) {
      checkUserAuth();
    }
  }, [authChecked, isLoadingAuth, checkUserAuth]);

  if (isLoadingAuth || !authChecked) {
    return fallback;
  }

  if (authError) {
    if (authError.type === 'user_not_registered') {
      return <UserNotRegisteredError />;
    }
    return unauthenticatedElement;
  }

  if (!isAuthenticated) {
    return unauthenticatedElement;
  }

  return <Outlet />;
}
```

---

**src/components/AuthLayout.jsx**
```jsx
import React from "react";

export default function AuthLayout({ icon: Icon, title, subtitle, footer, children }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-10">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-primary mb-4">
            <Icon className="w-7 h-7 text-primary-foreground" aria-hidden="true" />
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">{title}</h1>
          {subtitle && <p className="text-muted-foreground mt-2">{subtitle}</p>}
        </div>
        <div className="bg-card rounded-2xl shadow-sm border border-border p-8">
          {children}
        </div>
        {footer && (
          <p className="text-center text-sm text-muted-foreground mt-6">{footer}</p>
        )}
      </div>
    </div>
  );
}
```

---

**src/components/GoogleIcon.jsx**
```jsx
import React from "react";

export default function GoogleIcon({ className = "w-5 h-5" }) {
  return (
    <svg className={className} viewBox="0 0 24 24" aria-hidden="true">
      <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4" />
      <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
      <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
      <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
    </svg>
  );
}
```

---

**src/components/ScrollToTop.jsx**
```jsx
import { useEffect } from "react";
import { useLocation, useNavigationType } from "react-router-dom";

const getHashId = (hash) => {
  const rawId = hash.slice(1);
  try {
    return decodeURIComponent(rawId);
  } catch {
    return rawId;
  }
};

export default function ScrollToTop() {
  const { pathname, hash } = useLocation();
  const navigationType = useNavigationType();

  useEffect(() => {
    if (navigationType === "POP") return;

    if (hash) {
      const id = getHashId(hash);
      const timer = window.setTimeout(() => {
        document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
      }, 50);
      return () => window.clearTimeout(timer);
    }

    window.scrollTo({ top: 0, left: 0, behavior: "instant" });
  }, [pathname, hash, navigationType]);

  return null;
}
```

---

**src/components/UserNotRegisteredError.jsx**
```jsx
import React from 'react';

const UserNotRegisteredError = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-white to-slate-50">
      <div className="max-w-md w-full p-8 bg-white rounded-lg shadow-lg border border-slate-100">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 mb-6 rounded-full bg-orange-100">
            <svg className="w-8 h-8 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-slate-900 mb-4">Access Restricted</h1>
          <p className="text-slate-600 mb-8">
            You are not registered to use this application. Please contact the app administrator to request access.
          </p>
          <div className="p-4 bg-slate-50 rounded-md text-sm text-slate-600">
            <p>If you believe this is an error, you can:</p>
            <ul className="list-disc list-inside mt-2 space-y-1">
              <li>Verify you are logged in with the correct account</li>
              <li>Contact the app administrator for access</li>
              <li>Try logging out and back in again</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserNotRegisteredError;
```

---

**base44/entities/Signal.jsonc**
```jsonc
{
  "name": "Signal",
  "type": "object",
  "properties": {
    "pair": {
      "type": "string",
      "title": "Trading Pair"
    },
    "signal_type": {
      "type": "string",
      "enum": ["STRONG_BUY", "BUY", "NEUTRAL", "SELL", "STRONG_SELL"],
      "title": "Signal Type",
      "default": "NEUTRAL"
    },
    "direction": {
      "type": "string",
      "enum": ["LONG", "SHORT"],
      "title": "Direction"
    },
    "price": {
      "type": "number",
      "title": "Entry Price"
    },
    "take_profit": {
      "type": "number",
      "title": "Take Profit"
    },
    "stop_loss": {
      "type": "number",
      "title": "Stop Loss"
    },
    "atr": {
      "type": "number",
      "title": "ATR at Entry"
    },
    "rsi": {
      "type": "number",
      "title": "RSI Value"
    },
    "macd_histogram": {
      "type": "number",
      "title": "MACD Histogram"
    },
    "ema_short": {
      "type": "number",
      "title": "EMA Short (9)"
    },
    "ema_long": {
      "type": "number",
      "title": "EMA Long (50)"
    },
    "change_24h": {
      "type": "number",
      "title": "24h Change %"
    },
    "reasons": {
      "type": "array",
      "items": { "type": "string" },
      "title": "Signal Reasons"
    },
    "timeframe": {
      "type": "string",
      "title": "Timeframe",
      "default": "1hour"
    },
    "status": {
      "type": "string",
      "enum": ["ACTIVE", "WON", "LOST", "EXPIRED"],
      "title": "Status",
      "default": "ACTIVE"
    },
    "sent_to_telegram": {
      "type": "boolean",
      "title": "Sent to Telegram",
      "default": false
    },
    "sent_at": {
      "type": "string",
      "format": "date-time",
      "title": "Sent At"
    },
    "closed_price": {
      "type": "number",
      "title": "Closed Price"
    },
    "closed_at": {
      "type": "string",
      "format": "date-time",
      "title": "Closed At"
    },
    "pnl_percent": {
      "type": "number",
      "title": "P&L %"
    }
  },
  "required": ["pair", "signal_type", "price"]
}