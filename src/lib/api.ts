import {
  AuditRequest,
  AuditResponse,
  GenerateSummaryRequest,
  GenerateSummaryResponse,
  SaveLeadRequest,
  SaveLeadResponse,
  PublicAuditResponse,
  ToolsResponse,
  AuditPreviewRequest,
  AuditPreviewResponse,
  AuditAndSendRequest,
  AuditAndSendResponse,
} from "@/types/api";

// Isomorphic URL routing:
// - Server components (email link) use the absolute backend URL.
// - Client components use the local Next.js proxy (rewrites to backend).
const API_URL = typeof window === "undefined" 
  ? (process.env.BACKEND_API_URL || "https://swayamshetkar-ai-audit.hf.space") 
  : "";

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_URL}${endpoint}`;
  
  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!response.ok) {
    let errorMessage = `HTTP error! status: ${response.status}`;
    try {
      const errorData = await response.json();
      if (errorData.detail) {
        errorMessage = typeof errorData.detail === 'string' ? errorData.detail : JSON.stringify(errorData.detail);
      }
    } catch (e) {
      // Ignore JSON parse error for error responses
    }
    throw new ApiError(response.status, errorMessage);
  }

  return response.json();
}

export async function generateAudit(data: AuditRequest): Promise<AuditResponse> {
  return fetchApi<AuditResponse>("/api/audit", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getAuditPreview(data: AuditPreviewRequest): Promise<AuditPreviewResponse> {
  return fetchApi<AuditPreviewResponse>("/api/audit-preview", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function submitAuditAndSend(data: AuditAndSendRequest): Promise<AuditAndSendResponse> {
  return fetchApi<AuditAndSendResponse>("/api/audit-and-send", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function generateSummary(data: GenerateSummaryRequest): Promise<GenerateSummaryResponse> {
  return fetchApi<GenerateSummaryResponse>("/api/generate-summary", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function saveLead(data: SaveLeadRequest): Promise<SaveLeadResponse> {
  return fetchApi<SaveLeadResponse>("/api/save-lead", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getPublicAudit(publicId: string): Promise<PublicAuditResponse> {
  return fetchApi<PublicAuditResponse>(`/api/audit/${publicId}`, {
    method: "GET",
    // Adding no-store to ensure we always fetch the latest for public page
    cache: "no-store",
  });
}

export async function getTools(): Promise<ToolsResponse> {
  return fetchApi<ToolsResponse>("/api/tools", {
    method: "GET",
  });
}
