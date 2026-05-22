import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function proxy(request: NextRequest) {
  // Only apply CSRF protection to API routes that mutate data (POST, PUT, DELETE, PATCH)
  if (request.nextUrl.pathname.startsWith('/api/') && request.method !== 'GET' && request.method !== 'OPTIONS') {
    const origin = request.headers.get('origin') ?? request.headers.get('referer');
    const host = request.headers.get('host'); // e.g., localhost:3000 or your-vercel-app.vercel.app

    // If there is no origin/referer (e.g., cURL, automated scripts without headers) 
    // or if the origin does not match our host, reject the request.
    if (!origin || !host) {
      return new NextResponse(
        JSON.stringify({ error: 'CSRF Protection: Missing Origin or Host header' }),
        { status: 403, headers: { 'content-type': 'application/json' } }
      );
    }

    try {
      const originUrl = new URL(origin);
      // Compare the hostname + port of the Origin against the Host header
      if (originUrl.host !== host) {
        return new NextResponse(
          JSON.stringify({ error: 'CSRF Protection: Origin mismatch' }),
          { status: 403, headers: { 'content-type': 'application/json' } }
        );
      }
    } catch (e) {
      return new NextResponse(
        JSON.stringify({ error: 'CSRF Protection: Invalid Origin URL' }),
        { status: 403, headers: { 'content-type': 'application/json' } }
      );
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: '/api/:path*',
};
