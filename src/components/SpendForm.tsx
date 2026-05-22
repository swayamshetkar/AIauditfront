"use client";

import { useState, useEffect } from "react";
import { useForm, useFieldArray } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Plus, Trash2, Loader2, ArrowRight, CheckCircle2, Check, ChevronsUpDown } from "lucide-react";

import { cn } from "@/lib/utils";
import { getTools, getAuditPreview, submitAuditAndSend } from "@/lib/api";
import { AuditPreviewResponse } from "@/types/api";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";


const formSchema = z.object({
  team_size: z.coerce.number().min(1, "Team size must be at least 1").max(1000000, "Invalid size"),
  primary_use_case: z.string().trim().min(1, "Please select a primary use case").max(100),
  tools: z.array(
    z.object({
      tool: z.string().trim().min(1, "Please select a tool").max(100),
      plan: z.string().trim().min(1, "Please select a plan").max(100),
      monthly_spend: z.coerce.number().min(0, "Spend cannot be negative").max(100000000, "Spend too large"),
      seats: z.coerce.number().min(1, "Required").max(1000000, "Invalid amount"),
    })
    .strict()
  ).min(1, "Add at least one tool to audit").max(50, "Too many tools"),
}).strict();

type FormValues = z.infer<typeof formSchema>;

const leadSchema = z.object({
  email: z.string().trim().email("Invalid email address").max(100, "Email too long"),
  company_name: z.string().trim().min(2, "Company name is required").max(100, "Name too long"),
  role: z.string().trim().min(2, "Role is required").max(100, "Role too long"),
  website: z.string().trim().optional(), // Honeypot
}).strict();

type LeadValues = z.infer<typeof leadSchema>;

const USE_CASES = [
  { value: "coding", label: "Coding / Engineering" },
  { value: "writing", label: "Content / Writing" },
  { value: "data", label: "Data Analysis" },
  { value: "research", label: "Research" },
  { value: "mixed", label: "Mixed / General" },
];

const formatName = (str: string) => {
  if (!str) return "";
  const overrides: Record<string, string> = {
    chatgpt: "ChatGPT",
    github_copilot: "GitHub Copilot",
    openai_api: "OpenAI API",
  };
  if (overrides[str]) return overrides[str];
  return str.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
};

// Reusable Select Component for FormFields
function DropdownField({ 
  value, 
  onChange, 
  options, 
  placeholder, 
  disabled = false,
  className = ""
}: { 
  value: string; 
  onChange: (value: string) => void; 
  options: { value: string; label: string }[]; 
  placeholder: string; 
  disabled?: boolean;
  className?: string;
}) {
  return (
    <Select value={value} onValueChange={(val) => val && onChange(val)} disabled={disabled}>
      <FormControl>
        <SelectTrigger className={cn("w-full bg-background hover:bg-muted/50 transition-colors", !value && "text-muted-foreground", className)}>
          <span className="truncate flex-1 text-left">
            {value ? options.find(o => o.value === value)?.label : placeholder}
          </span>
        </SelectTrigger>
      </FormControl>
      <SelectContent>
        {options.map((option) => (
          <SelectItem key={option.value} value={option.value}>
            {option.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}

export default function SpendForm() {
  type FormState = "input" | "preview" | "success";
  const [step, setStep] = useState<FormState>("input");
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [mounted, setMounted] = useState(false);
  const [toolsConfig, setToolsConfig] = useState<Record<string, { plans: string[] }> | null>(null);
  
  const [auditData, setAuditData] = useState<FormValues | null>(null);
  const [previewResult, setPreviewResult] = useState<AuditPreviewResponse | null>(null);

  useEffect(() => {
    getTools()
      .then(res => setToolsConfig(res.tools))
      .catch(err => console.error("Failed to load tools", err));
  }, []);

  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      team_size: 1,
      primary_use_case: "",
      tools: [{ tool: "", plan: "", monthly_spend: 0, seats: 1 }],
    },
  });

  const leadForm = useForm({
    resolver: zodResolver(leadSchema),
    defaultValues: {
      email: "",
      company_name: "",
      role: "",
      website: "",
    },
  });

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: "tools",
  });

  const watchTools = form.watch("tools");

  // Load from local storage
  useEffect(() => {
    setMounted(true);
    const saved = localStorage.getItem("airev_form_state");
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        form.reset(parsed);
      } catch (e) {
        console.error("Failed to parse saved form state", e);
      }
    }
  }, [form]);

  // Save to local storage on change
  useEffect(() => {
    if (!mounted) return;
    const subscription = form.watch((value) => {
      localStorage.setItem("airev_form_state", JSON.stringify(value));
    });
    return () => subscription.unsubscribe();
  }, [form, mounted]);

  async function onCalculate(data: FormValues) {
    setIsSubmitting(true);
    try {
      const response = await getAuditPreview(data);
      setAuditData(data);
      setPreviewResult(response);
      setStep("preview");
    } catch (error) {
      console.error("Failed to get preview", error);
      alert("Failed to analyze stack. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function onFinalSubmit(leadData: LeadValues) {
    if (!auditData) return;
    setIsSubmitting(true);
    try {
      await submitAuditAndSend({
        ...auditData,
        email: leadData.email,
        company_name: leadData.company_name,
        role: leadData.role,
        website: leadData.website || "",
      });
      setStep("success");
    } catch (error) {
      console.error("Failed to send audit", error);
      alert("Failed to send report. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  }

  if (!mounted) {
    return null;
  }

  if (step === "success") {
    return (
      <div className="max-w-2xl mx-auto text-center space-y-6 py-12 animate-in fade-in zoom-in duration-500">
        <div className="w-20 h-20 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto shadow-sm">
          <CheckCircle2 className="w-10 h-10" />
        </div>
        <h2 className="text-3xl font-bold tracking-tight">Success! Check your inbox.</h2>
        <p className="text-xl text-muted-foreground">
          We just emailed you a secure link to your full, personalized AI optimization report.
        </p>
      </div>
    );
  }

  if (step === "preview" && previewResult) {
    const efficiencyScore = 100 - previewResult.overspend_score;
    const isEfficient = efficiencyScore >= 80;
    const scoreColor = isEfficient ? "text-emerald-500" : (efficiencyScore >= 50 ? "text-amber-500" : "text-rose-500");

    return (
      <div className="w-full max-w-2xl mx-auto space-y-10 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <Card className="text-center p-8 border-none shadow-sm bg-muted/30">
          <CardContent className="pt-0 space-y-4">
            <h2 className="text-2xl font-bold tracking-tight">Your Efficiency Score</h2>
            <div className={`text-7xl font-extrabold ${scoreColor}`}>
              {efficiencyScore}/100
            </div>
            <p className="text-lg text-muted-foreground">
              Your stack has been analyzed! Enter your email to receive your full personalized AI optimization report.
            </p>
          </CardContent>
        </Card>

        <Card className="border-none shadow-lg">
          <CardContent className="pt-8">
            <Form {...leadForm}>
              <form onSubmit={leadForm.handleSubmit(onFinalSubmit)} className="space-y-6">
                {/* Honeypot field */}
                <div className="hidden">
                  <FormField
                    control={leadForm.control}
                    name="website"
                    render={({ field }) => (
                      <FormItem>
                        <FormControl>
                          <Input tabIndex={-1} autoComplete="off" {...field} />
                        </FormControl>
                      </FormItem>
                    )}
                  />
                </div>

                <FormField
                  control={leadForm.control}
                  name="email"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Work Email</FormLabel>
                      <FormControl>
                        <Input type="email" placeholder="you@company.com" className="h-12 bg-background" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <FormField
                    control={leadForm.control}
                    name="company_name"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Company Name</FormLabel>
                        <FormControl>
                          <Input placeholder="Acme Inc" className="h-12 bg-background" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={leadForm.control}
                    name="role"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Your Role</FormLabel>
                        <FormControl>
                          <Input placeholder="e.g. CTO, Founder" className="h-12 bg-background" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                <Button type="submit" size="lg" className="w-full text-lg h-14" disabled={isSubmitting}>
                  {isSubmitting ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      Generating Secure Report...
                    </>
                  ) : (
                    <>
                      Get My Full Report
                      <ArrowRight className="w-5 h-5 ml-2" />
                    </>
                  )}
                </Button>
              </form>
            </Form>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Generate tool options correctly formatted
  const toolOptions = toolsConfig 
    ? Object.keys(toolsConfig).map(t => ({ value: t, label: formatName(t) })) 
    : [];

  // STEP: "input"
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onCalculate)} className="space-y-10 w-full max-w-3xl mx-auto">
        <div className="space-y-6">
          <FormField
            control={form.control}
            name="team_size"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Team Size</FormLabel>
                <FormControl>
                  <Input type="number" min="1" placeholder="e.g. 10" className="h-12 text-lg shadow-sm" {...field} value={field.value as number | string} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="primary_use_case"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Primary AI Use Case</FormLabel>
                <DropdownField
                  value={field.value}
                  onChange={field.onChange}
                  options={USE_CASES}
                  placeholder="Select primary use case..."
                  className="h-12 text-lg shadow-sm"
                />
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <div className="space-y-4 pt-4">
          <div className="mb-6">
            <h3 className="text-xl font-bold tracking-tight">Your AI Stack</h3>
            <p className="text-muted-foreground mt-1">List the tools your team currently uses to generate your audit.</p>
          </div>

          {fields.map((field, index) => (
            <Card key={field.id} className="relative overflow-visible border-border/50 shadow-sm transition-all hover:shadow-md">
              <CardContent className="pt-6 grid grid-cols-1 md:grid-cols-12 gap-4 items-start">
                <div className="md:col-span-3">
                  <FormField
                    control={form.control}
                    name={`tools.${index}.tool`}
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-xs font-semibold">Tool</FormLabel>
                        <DropdownField
                          value={field.value}
                          onChange={(val) => {
                            field.onChange(val);
                            // Auto-reset plan when tool changes
                            form.setValue(`tools.${index}.plan`, "");
                          }}
                          options={toolOptions}
                          placeholder="Select tool..."
                        />
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
                
                <div className="md:col-span-3">
                  <FormField
                    control={form.control}
                    name={`tools.${index}.plan`}
                    render={({ field }) => {
                      const currentTool = watchTools?.[index]?.tool;
                      const availablePlans = currentTool && toolsConfig ? toolsConfig[currentTool]?.plans || [] : [];
                      const planOptions = availablePlans.map((p: string) => ({ value: p, label: formatName(p) }));
                      
                      return (
                        <FormItem>
                          <FormLabel className="text-xs font-semibold">Plan</FormLabel>
                          <DropdownField
                            value={field.value}
                            onChange={field.onChange}
                            options={planOptions}
                            placeholder={currentTool ? "Select plan..." : "Tool first"}
                            disabled={!currentTool || planOptions.length === 0}
                          />
                          <FormMessage />
                        </FormItem>
                      );
                    }}
                  />
                </div>

                <div className="md:col-span-3">
                  <FormField
                    control={form.control}
                    name={`tools.${index}.monthly_spend`}
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-xs font-semibold">Monthly Spend ($) *</FormLabel>
                        <FormControl>
                          <Input type="number" min="0" step="0.01" className="bg-background" {...field} value={field.value as number | string} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                <div className="md:col-span-2">
                  <FormField
                    control={form.control}
                    name={`tools.${index}.seats`}
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-xs font-semibold">Seats *</FormLabel>
                        <FormControl>
                          <Input type="number" min="1" placeholder="Required" className="bg-background" {...field} value={(field.value as number | string) || ''} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                <div className="md:col-span-1 flex items-end justify-end md:justify-center pt-6">
                  {fields.length > 1 && (
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      className="text-muted-foreground hover:text-rose-500 hover:bg-rose-50"
                      onClick={() => remove(index)}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
          <Button
            type="button"
            variant="outline"
            className="w-full border-dashed border-2 h-16 text-base font-medium text-muted-foreground hover:text-foreground mt-4 hover:border-primary/50 transition-colors bg-muted/10 hover:bg-muted/30"
            onClick={() => append({ tool: "", plan: "", monthly_spend: 0, seats: 1 })}
          >
            <Plus className="w-5 h-5 mr-2" />
            Add Another Tool
          </Button>
        </div>

        <div className="pt-4">
          <Button type="submit" size="lg" className="w-full h-14 text-xl shadow-md transition-transform hover:scale-[1.01]" disabled={isSubmitting}>
            {isSubmitting ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                Calculating Savings...
              </>
            ) : (
              <>
                Calculate Savings
                <ArrowRight className="w-5 h-5 ml-2" />
              </>
            )}
          </Button>
        </div>
      </form>
    </Form>
  );
}
