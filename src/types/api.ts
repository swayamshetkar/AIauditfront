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

export type AuditPreviewRequest = AuditRequest;

export interface AuditPreviewResponse {
  overspend_score: number;
  total_estimated_monthly_savings: number;
  total_estimated_annual_savings: number;
}

export interface AuditAndSendRequest extends AuditRequest {
  email: string;
  company_name: string;
  role: string;
  website: string; // Honeypot
}

export interface AuditAndSendResponse {
  success: boolean;
  message: string;
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

export interface GenerateSummaryRequest {
  audit_result: AuditData;
}

export interface GenerateSummaryResponse {
  summary: string;
  source: string;
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
