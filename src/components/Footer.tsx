import Link from "next/link";
import { CredexLogo } from "./CredexLogo";
import { Mail, Globe } from "lucide-react";

export function Footer() {
  return (
    <footer className="w-full bg-white border-t border-border mt-auto">
      <div className="container mx-auto px-4 max-w-5xl py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div className="md:col-span-2 space-y-4">
            <CredexLogo />
            <p className="text-muted-foreground max-w-sm">
              The marketplace layer for AI and cloud infrastructure. Unlock liquidity from unused credits or access verified compute at a fraction of the cost.
            </p>
            <div className="flex items-center gap-4 pt-2 text-muted-foreground">
              <a href="https://github.com/swayamshetkar/AIauditfront" target="_blank" rel="noreferrer" className="hover:text-primary transition-colors flex items-center gap-2">
                <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-github"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.2c3-.3 6-1.5 6-6.5a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 5 3 6.2 6 6.5a4.8 4.8 0 0 0-1 3.2v4"/><path d="M9 18c-4.5 1-5-2.5-5-2.5"/></svg>
                <span>GitHub Repository</span>
              </a>
            </div>
          </div>
          
          <div className="space-y-4">
            <h4 className="font-semibold text-foreground">Contact</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <a href="mailto:hello@credex.rocks" className="hover:text-primary transition-colors flex items-center gap-2">
                  <Mail className="w-4 h-4" /> Support
                </a>
              </li>
              <li>
                <a href="https://credex.rocks/" target="_blank" rel="noreferrer" className="hover:text-primary transition-colors flex items-center gap-2">
                  <Globe className="w-4 h-4" /> credex.rocks
                </a>
              </li>
            </ul>
          </div>

          <div className="space-y-4">
            <h4 className="font-semibold text-foreground">Legal</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><Link href="#" className="hover:text-primary transition-colors">Terms of Service</Link></li>
              <li><Link href="#" className="hover:text-primary transition-colors">Privacy Policy</Link></li>
              <li><Link href="#" className="hover:text-primary transition-colors">License</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="pt-8 border-t border-border/50 text-sm text-muted-foreground flex flex-col md:flex-row items-center justify-between">
          <p>© {new Date().getFullYear()} Credex. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
