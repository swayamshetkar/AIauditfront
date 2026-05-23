import { getPublicAudit } from "@/lib/api";
import { Metadata } from "next";
import AuditClient from "@/components/AuditClient";
import { BlueprintBackground } from "@/components/BlueprintBackground";
import { notFound } from "next/navigation";

interface AuditPageProps {
  params: Promise<{ public_id: string }>;
}

export async function generateMetadata({ params }: AuditPageProps): Promise<Metadata> {
  const { public_id } = await params;
  try {
    const data = await getPublicAudit(public_id);
    return {
      title: data.og?.title || "Spend Node Liquidity Analysis",
      description: data.og?.description || "Check out this AI & Cloud liquidity analysis.",
      openGraph: {
        title: data.og?.title || "Spend Node Liquidity Analysis",
        description: data.og?.description || "Check out this AI & Cloud liquidity analysis.",
      }
    };
  } catch (e) {
    return {
      title: "Spend Node Liquidity Analysis",
    };
  }
}

export default async function AuditPage({ params }: AuditPageProps) {
  const { public_id } = await params;
  
  try {
    const data = await getPublicAudit(public_id);
    return (
      <BlueprintBackground>
        <div className="flex-1 py-8">
          <div className="container mx-auto px-4 max-w-5xl">
            <AuditClient publicId={public_id} initialData={data} />
          </div>
        </div>
      </BlueprintBackground>
    );
  } catch (error) {
    console.error("Failed to load audit:", error);
    notFound();
  }
}
