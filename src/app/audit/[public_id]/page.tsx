import { getPublicAudit } from "@/lib/api";
import { Metadata } from "next";
import AuditClient from "@/components/AuditClient";
import { notFound } from "next/navigation";

interface AuditPageProps {
  params: Promise<{ public_id: string }>;
}

export async function generateMetadata({ params }: AuditPageProps): Promise<Metadata> {
  const { public_id } = await params;
  try {
    const data = await getPublicAudit(public_id);
    return {
      title: data.og?.title || "Credex Liquidity Analysis",
      description: data.og?.description || "Check out this AI & Cloud liquidity analysis.",
      openGraph: {
        title: data.og?.title || "Credex Liquidity Analysis",
        description: data.og?.description || "Check out this AI & Cloud liquidity analysis.",
      }
    };
  } catch (e) {
    return {
      title: "Credex Liquidity Analysis",
    };
  }
}

export default async function AuditPage({ params }: AuditPageProps) {
  const { public_id } = await params;
  
  try {
    const data = await getPublicAudit(public_id);
    return (
      <div className="flex-1 bg-muted/30 py-8">
        <div className="container mx-auto px-4 max-w-5xl">
          <AuditClient publicId={public_id} initialData={data} />
        </div>
      </div>
    );
  } catch (error) {
    console.error("Failed to load audit:", error);
    notFound();
  }
}
