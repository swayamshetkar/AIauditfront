import SpendForm from "@/components/SpendForm";

export default function Home() {
  return (
    <div className="flex-1 flex flex-col pt-12 md:pt-24 pb-12">
      <div className="container mx-auto px-4 max-w-5xl">
        <div className="text-center space-y-6 mb-16">
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight">
            Stop Overpaying for <span className="text-primary">AI Tools</span>
          </h1>
          <p className="text-2xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            Audit your team&apos;s AI software stack in seconds. Identify duplicate functionality, unused seats, and uncover thousands in monthly savings.
          </p>
        </div>

        <SpendForm />
      </div>
    </div>
  );
}
