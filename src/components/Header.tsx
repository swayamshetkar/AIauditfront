import Link from "next/link";
import { CredexLogo } from "./CredexLogo";

export function Header() {
  return (
    <header className="mx-auto w-full px-4 pt-6 pb-2 z-50 relative max-w-7xl">
      <div className="flex items-center justify-between rounded border bg-card px-6 py-4">
        
        {/* Left: Logo */}
        <Link href="/" className="transition-opacity hover:opacity-90">
          <CredexLogo />
        </Link>

        {/* Right: GitHub Project Link */}
        <div className="flex items-center">
          <a 
            href="https://github.com/swayamshetkar/AIauditfront" 
            target="_blank" 
            rel="noreferrer" 
            className="flex items-center gap-2 rounded px-4 py-2 text-sm font-semibold text-muted-foreground hover:bg-secondary hover:text-foreground transition-colors border border-transparent hover:border-border"
          >
            <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-github"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.2c3-.3 6-1.5 6-6.5a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 5 3 6.2 6 6.5a4.8 4.8 0 0 0-1 3.2v4"/><path d="M9 18c-4.5 1-5-2.5-5-2.5"/></svg>
            <span className="hidden sm:inline">GitHub Project</span>
          </a>
        </div>

      </div>
    </header>
  );
}
