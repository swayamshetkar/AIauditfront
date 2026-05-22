import SpendForm from "@/components/SpendForm";

export default function Home() {
  return (
    <div className="flex-1 flex flex-col justify-center py-12 md:py-24">
      <div className="container mx-auto px-4 max-w-5xl">
        <div className="text-center space-y-6 mb-12">
          <h1 className="text-4xl md:text-6xl font-bold tracking-tight">
            Stop Overpaying for <span className="text-primary">AI Tools</span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Audit your team&apos;s AI software stack in seconds. Identify duplicate functionality, unused seats, and uncover thousands in monthly savings.
          </p>
        </div>

        <SpendForm />
      </div>
    </div>
  );
}
