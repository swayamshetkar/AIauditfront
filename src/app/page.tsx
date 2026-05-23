import SpendForm from "@/components/SpendForm";
import { BlueprintBackground } from "@/components/BlueprintBackground";

export default function Home() {
  return (
    <BlueprintBackground>
      <div className="flex-1 flex flex-col pt-12 md:pt-24 pb-12">
        <div className="container mx-auto px-4 max-w-5xl">
          <div className="text-center space-y-6 mb-16">
            <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-balance">
              The liquidity engine for <span className="text-primary">AI and cloud</span> infrastructure
            </h1>
            <p className="text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
              Transform your unused credits into capital. Access high-performance compute on a secure, verified marketplace built for modern teams.
            </p>
          </div>

          <SpendForm />
        </div>
      </div>
    </BlueprintBackground>
  );
}
