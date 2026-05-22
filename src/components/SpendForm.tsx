"use client";

import { useState, useEffect } from "react";
import { useForm, useFieldArray } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useRouter } from "next/navigation";
import { Plus, Trash2, Loader2, ArrowRight } from "lucide-react";

import { generateAudit, getTools } from "@/lib/api";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card, CardContent } from "@/components/ui/card";

const formSchema = z.object({
  team_size: z.coerce.number().min(1, "Team size must be at least 1"),
  primary_use_case: z.string().min(1, "Please select a primary use case"),
  tools: z.array(
    z.object({
      tool: z.string().min(1, "Please select a tool"),
      plan: z.string().min(1, "Please select a plan"),
      monthly_spend: z.coerce.number().min(0, "Spend cannot be negative"),
      seats: z.coerce.number().optional(),
    })
  ).min(1, "Add at least one tool to audit"),
});

type FormValues = z.infer<typeof formSchema>;

export default function SpendForm() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [mounted, setMounted] = useState(false);
  const [toolsConfig, setToolsConfig] = useState<Record<string, { plans: string[] }> | null>(null);

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
      tools: [{ tool: "", plan: "", monthly_spend: 0 }],
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

  async function onSubmit(data: FormValues) {
    setIsSubmitting(true);
    try {
      const response = await generateAudit(data);
      
      // Store public_id to identify owner on results page
      const owned = JSON.parse(localStorage.getItem("airev_owned_audits") || "[]");
      if (!owned.includes(response.public_id)) {
        owned.push(response.public_id);
        localStorage.setItem("airev_owned_audits", JSON.stringify(owned));
      }

      router.push(`/audit/${response.public_id}`);
    } catch (error) {
      console.error("Failed to generate audit", error);
      alert("Failed to generate audit. Please try again.");
      setIsSubmitting(false);
    }
  }

  // Prevent hydration mismatch for defaultValues
  if (!mounted) {
    return null; // or a skeleton loader
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8 w-full max-w-3xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <FormField
            control={form.control}
            name="team_size"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Team Size</FormLabel>
                <FormControl>
                  <Input type="number" min="1" placeholder="e.g. 10" {...field} value={field.value as number | string} />
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
                <Select onValueChange={field.onChange} value={field.value}>
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Select primary use case" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem value="coding">Coding / Engineering</SelectItem>
                    <SelectItem value="writing">Content / Writing</SelectItem>
                    <SelectItem value="data">Data Analysis</SelectItem>
                    <SelectItem value="research">Research</SelectItem>
                    <SelectItem value="mixed">Mixed / General</SelectItem>
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-medium">Your AI Stack</h3>
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => append({ tool: "", plan: "", monthly_spend: 0 })}
            >
              <Plus className="w-4 h-4 mr-2" />
              Add Tool
            </Button>
          </div>

          {fields.map((field, index) => (
            <Card key={field.id} className="relative">
              <CardContent className="pt-6 grid grid-cols-1 md:grid-cols-12 gap-4 items-start">
                <div className="md:col-span-3">
                  <FormField
                    control={form.control}
                    name={`tools.${index}.tool`}
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-xs">Tool</FormLabel>
                        <Select onValueChange={field.onChange} value={field.value}>
                          <FormControl>
                            <SelectTrigger>
                              <SelectValue placeholder="Select tool" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            {toolsConfig && Object.keys(toolsConfig).map((toolKey) => (
                              <SelectItem key={toolKey} value={toolKey} className="capitalize">
                                {toolKey.replace(/_/g, ' ')}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
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
                      
                      return (
                        <FormItem>
                          <FormLabel className="text-xs">Plan</FormLabel>
                          <Select onValueChange={field.onChange} value={field.value} disabled={!currentTool}>
                            <FormControl>
                              <SelectTrigger>
                                <SelectValue placeholder={currentTool ? "Select plan" : "Select tool first"} />
                              </SelectTrigger>
                            </FormControl>
                            <SelectContent>
                              {availablePlans.map((planStr: string) => (
                                <SelectItem key={planStr} value={planStr} className="capitalize">
                                  {planStr.replace(/_/g, ' ')}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
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
                        <FormLabel className="text-xs">Monthly Spend ($)</FormLabel>
                        <FormControl>
                          <Input type="number" min="0" step="0.01" {...field} value={field.value as number | string} />
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
                        <FormLabel className="text-xs">Seats</FormLabel>
                        <FormControl>
                          <Input type="number" min="1" placeholder="Optional" {...field} value={(field.value as number | string) || ''} />
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
                      className="text-muted-foreground hover:text-destructive"
                      onClick={() => remove(index)}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <Button type="submit" size="lg" className="w-full text-lg" disabled={isSubmitting}>
          {isSubmitting ? (
            <>
              <Loader2 className="w-5 h-5 mr-2 animate-spin" />
              Analyzing Stack...
            </>
          ) : (
            <>
              Reveal Overspend
              <ArrowRight className="w-5 h-5 ml-2" />
            </>
          )}
        </Button>
      </form>
    </Form>
  );
}
