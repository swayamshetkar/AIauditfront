import React from "react";

export function BlueprintBackground({ children }: { children: React.ReactNode }) {
  return (
    <div className="relative min-h-screen w-full overflow-hidden bg-background">
      {/* 1. Dot Grid Background */}
      <div 
        className="absolute inset-0 z-0 opacity-[0.3]"
        style={{
          backgroundImage: `radial-gradient(circle at 1.5px 1.5px, #c3c5d9 1.5px, transparent 0)`,
          backgroundSize: '24px 24px'
        }}
      />

      {/* 2. Left Flank - The Data Node */}
      <div className="absolute left-8 top-32 z-0 hidden lg:flex flex-col gap-6 opacity-[0.4] pointer-events-none select-none transition-opacity duration-1000">
        {/* Connection line */}
        <div className="absolute -right-24 top-12 h-[1px] w-24 bg-primary" />
        
        {/* Wireframe Card */}
        <div className="w-56 rounded border border-primary bg-card/50 backdrop-blur-sm p-4 font-mono text-xs shadow-sm">
          <div className="mb-2 border-b border-border pb-2 font-bold text-primary uppercase tracking-wider">
            Node: Alpha-7
          </div>
          <div className="flex justify-between py-1">
            <span className="text-muted-foreground">Status</span>
            <span className="text-foreground">Active</span>
          </div>
          <div className="flex justify-between py-1">
            <span className="text-muted-foreground">Capacity</span>
            <span className="text-foreground font-semibold">98.2%</span>
          </div>
          <div className="flex justify-between py-1">
            <span className="text-muted-foreground">Latency</span>
            <span className="text-foreground">12ms</span>
          </div>
        </div>

        {/* Mini Ledger */}
        <div className="w-48 ml-4 rounded border border-border bg-card/50 backdrop-blur-sm p-4 font-mono text-[10px]">
          <div className="text-muted-foreground mb-1 uppercase tracking-widest border-b border-border pb-1">Ledger Stream</div>
          <div className="text-foreground mt-2">0x8f2A...4c2a <span className="text-emerald-500 float-right">+12T</span></div>
          <div className="text-foreground mt-1">0x3e1B...9b1f <span className="text-rose-500 float-right">-4T</span></div>
          <div className="text-foreground mt-1 opacity-50">0x7c9D...1a2b <span className="text-emerald-500 float-right">+8T</span></div>
        </div>
      </div>

      {/* 3. Right Flank - The Liquidity Node */}
      <div className="absolute right-8 top-48 z-0 hidden lg:flex flex-col items-end gap-8 opacity-[0.4] pointer-events-none select-none transition-opacity duration-1000">
        {/* Connection line */}
        <div className="absolute -left-32 top-20 h-[1px] w-32 bg-border" />

        {/* Abstract Chart */}
        <div className="w-64 rounded border border-border bg-card/50 backdrop-blur-sm p-4 shadow-sm">
          <div className="mb-3 font-mono text-xs font-bold text-muted-foreground uppercase tracking-wider flex items-center justify-between">
            <span>Liquidity Pool</span>
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
          </div>
          <div className="flex items-end gap-2 h-20 border-b border-l border-border p-2">
            <div className="w-1/4 bg-primary/40 h-[40%] rounded-t-sm" />
            <div className="w-1/4 bg-primary/60 h-[70%] rounded-t-sm" />
            <div className="w-1/4 bg-primary/80 h-[50%] rounded-t-sm" />
            <div className="w-1/4 bg-primary h-[90%] rounded-t-sm relative">
              <div className="absolute -top-6 -right-2 text-[10px] font-mono font-bold text-primary">MAX</div>
            </div>
          </div>
        </div>

        {/* Metric Block */}
        <div className="w-48 mr-4 rounded border border-primary bg-card/50 backdrop-blur-sm p-3 font-mono text-right relative">
          <div className="absolute -left-12 top-1/2 h-[1px] w-12 bg-primary/50" />
          <div className="text-[10px] text-muted-foreground uppercase tracking-widest">Compute Ready</div>
          <div className="text-sm font-bold text-foreground mt-1">4.2 PetaFLOPS</div>
        </div>
      </div>

      {/* 4. Main Content Wrapper */}
      <div className="relative z-10 flex w-full flex-col min-h-screen">
        {children}
      </div>
    </div>
  );
}
