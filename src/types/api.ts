export interface ToolInput {
  tool: string;
  plan: string;
  monthly_spend: number;
  seats?: number;
}

export interface AuditRequest {
  team_size: number;
  primary_use_case: string;
  tools: ToolInput[];
}

export interface Recommendation {
  tool: string;
  issue: string;
  recommendation: string;
  reasoning: string;
  estimated_monthly_savings: number;
}

export interface AuditData {
  overspend_score: number;
  score_label: string;
  recommendations: Recommendation[];
  total_monthly_spend: number;
  total_estimated_monthly_savings: number;
  total_estimated_annual_savings: number;
}

export interface AuditResponse {
  public_id: string;
  created_at: string;
  audit: AuditData;
}

export interface GenerateSummaryRequest {
  audit_result: AuditData;
}

export interface GenerateSummaryResponse {
  summary: string;
  source: string;
}

export interface SaveLeadRequest {
  email: string;
  company_name: string;
  role: string;
  team_size: number;
  audit_id: string;
  website: string; // Honeypot
}

export interface SaveLeadResponse {
  success: boolean;
  message: string;
}

export interface PublicAuditResponse {
  public_id: string;
  audit: AuditData;
  og: {
    title: string;
    description: string;
  };
}

export interface ToolSchema {
  plans: string[];
}

export interface ToolsResponse {
  tools: Record<string, ToolSchema>;
}
