"use client";

import { useEffect, useState } from "react";
import { PublicAuditResponse, GenerateSummaryResponse } from "@/types/api";
import { generateSummary } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Sparkles, Zap, CheckCircle2, AlertTriangle, XCircle } from "lucide-react";

export default function AuditClient({ 
  publicId, 
  initialData 
}: { 
  publicId: string; 
  initialData: PublicAuditResponse 
}) {
  const [summaryData, setSummaryData] = useState<GenerateSummaryResponse | null>(null);
  const [summaryLoading, setSummaryLoading] = useState(true);

  const audit = initialData.audit;


  // Calculate Efficiency Score (100 - overspend)
  // An overspend of 0 means 100% efficient
  const efficiencyScore = 100 - audit.overspend_score;

  useEffect(() => {

    // If it's the owner (or just viewing it fresh), generate the AI summary
    // The requirement says "independently trigger" - doing this regardless of owner for the premium feel
    generateSummary({ audit_result: audit })
      .then(res => {
        setSummaryData(res);
        setSummaryLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch summary:", err);
        setSummaryLoading(false);
      });
  }, [publicId, audit]);

  // Map score to color and icon
  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-primary";
    if (score >= 50) return "text-foreground";
    return "text-destructive";
  };

  const ScoreIcon = efficiencyScore >= 80 ? CheckCircle2 : (efficiencyScore >= 50 ? AlertTriangle : XCircle);

  return (
    <div className="space-y-10 animate-in fade-in slide-in-from-bottom-4 duration-700">
      
      {/* Hero Section */}
      <section className="text-center space-y-4 pt-8">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight">
          Your Liquidity Analysis
        </h1>
        <p className="text-xl text-muted-foreground">
          We unlocked <span className="font-bold text-primary">${audit.total_estimated_monthly_savings.toLocaleString()}</span> in potential monthly liquidity.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mt-8">
          <Card className="w-full sm:w-64 bg-primary text-primary-foreground border-primary shadow-none">
            <CardContent className="pt-6">
              <div className="text-sm font-medium opacity-90">Annual Liquidity</div>
              <div className="text-4xl font-bold mt-2">
                ${audit.total_estimated_annual_savings.toLocaleString()}
              </div>
            </CardContent>
          </Card>
          
          <Card className="w-full sm:w-64 shadow-none">
            <CardContent className="pt-6">
              <div className="text-sm font-medium text-muted-foreground">Credit Efficiency Score</div>
              <div className={`text-4xl font-bold mt-2 flex items-center justify-center gap-2 ${getScoreColor(efficiencyScore)}`}>
                {efficiencyScore}/100
              </div>
              <div className="text-xs text-muted-foreground mt-1">{audit.score_label}</div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* AI Summary Block */}
      <section>
        <Card className="bg-card shadow-none border-border">
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center text-lg">
              <Sparkles className="w-5 h-5 mr-2 text-primary" />
              Marketplace Executive Summary
            </CardTitle>
          </CardHeader>
          <CardContent>
            {summaryLoading ? (
              <div className="space-y-2">
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 w-[90%]" />
                <Skeleton className="h-4 w-[95%]" />
                <Skeleton className="h-4 w-[80%]" />
              </div>
            ) : summaryData ? (
              <p className="text-muted-foreground leading-relaxed">
                {summaryData.summary}
              </p>
            ) : (
              <p className="text-muted-foreground italic">Summary unavailable.</p>
            )}
          </CardContent>
        </Card>
      </section>

      {/* Per-Tool Recommendations */}
      <section className="space-y-4">
        <h2 className="text-2xl font-bold">Liquidity Opportunities</h2>
        <div className="grid grid-cols-1 gap-4">
          {audit.recommendations.map((rec, index) => (
            <Card key={index} className="overflow-hidden transition-all hover:border-primary shadow-none border border-border">
              <CardContent className="p-0">
                <div className="flex flex-col md:flex-row">
                  <div className="bg-muted p-6 md:w-1/4 flex flex-col justify-center border-b md:border-b-0 md:border-r">
                    <div className="font-bold text-lg capitalize">{rec.tool.replace('_', ' ')}</div>
                    <div className="text-sm text-muted-foreground mt-1">
                      Unlock <span className="font-semibold text-foreground">${rec.estimated_monthly_savings}/mo</span>
                    </div>
                  </div>
                  <div className="p-6 md:w-3/4 space-y-3">
                    <div>
                      <span className="font-semibold text-destructive text-sm uppercase tracking-wider">Issue</span>
                      <p className="text-sm mt-1">{rec.issue}</p>
                    </div>
                    <div className="pt-2 border-t border-dashed">
                      <span className="font-semibold text-primary text-sm uppercase tracking-wider">Action</span>
                      <p className="font-medium mt-1 flex items-start gap-2">
                        <Zap className="w-4 h-4 mt-0.5 text-primary shrink-0" />
                        {rec.recommendation}
                      </p>
                    </div>
                    <div className="text-sm text-muted-foreground italic">
                      &quot;{rec.reasoning}&quot;
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}

          {audit.recommendations.length === 0 && (
            <Card>
              <CardContent className="pt-6 text-center text-muted-foreground">
                No major optimization opportunities found. Your stack is lean!
              </CardContent>
            </Card>
          )}
        </div>
      </section>

    </div>
  );
}
