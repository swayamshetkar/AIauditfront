import type { Metadata } from "next";
import { Space_Grotesk } from "next/font/google";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import "./globals.css";

const font = Space_Grotesk({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Spend Node by Credex | Unused AI and Cloud Credits",
  description: "Unlock liquidity from unused credits. Fast-growing teams get access to verified compute at lower cost.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${font.className} min-h-screen flex flex-col bg-background text-foreground antialiased selection:bg-primary/30 selection:text-primary-foreground`}>
        <Header />
        <main className="flex-1 flex flex-col relative z-10">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
