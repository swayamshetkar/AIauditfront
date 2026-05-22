"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Loader2 } from "lucide-react";

import { saveLead } from "@/lib/api";
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
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const formSchema = z.object({
  email: z.string().email("Please enter a valid email address"),
  company_name: z.string().min(1, "Company name is required"),
  role: z.string().min(1, "Role is required"),
  team_size: z.coerce.number().min(1, "Team size is required"),
  website: z.string().max(0, "Invalid submission"), // honeypot
});

type FormValues = z.infer<typeof formSchema>;

export default function LeadCapture({ auditId, isHighSavings }: { auditId: string; isHighSavings: boolean }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: "",
      company_name: "",
      role: "",
      team_size: 1,
      website: "",
    },
  });

  async function onSubmit(data: FormValues) {
    setIsSubmitting(true);
    try {
      await saveLead({
        email: data.email,
        company_name: data.company_name,
        role: data.role,
        team_size: data.team_size,
        audit_id: auditId,
        website: data.website,
      });
      setSubmitted(true);
    } catch (error) {
      console.error("Failed to save lead", error);
      alert("Something went wrong. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  }

  if (submitted) {
    return (
      <Card className="bg-primary/5 border-primary/20">
        <CardContent className="pt-6 text-center">
          <h3 className="text-xl font-bold text-primary mb-2">
            {isHighSavings ? "Consultation Requested!" : "You're on the list!"}
          </h3>
          <p className="text-muted-foreground">
            {isHighSavings 
              ? "A Credex optimization expert will reach out to you shortly to help you capture these savings."
              : "We'll notify you if any new optimization opportunities arise for your stack."}
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="border-primary/20 shadow-md">
      <CardHeader>
        <CardTitle className="text-2xl">
          {isHighSavings ? "Capture these savings with Credex" : "Stay optimized"}
        </CardTitle>
        <CardDescription>
          {isHighSavings 
            ? "Connect with an expert to help renegotiate or consolidate your AI software contracts." 
            : "You're spending well! Join our waitlist to be notified when new optimizations apply to your stack."}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            {/* Honeypot field - visually hidden but available to screen readers/bots */}
            <div className="hidden" aria-hidden="true">
              <FormField
                control={form.control}
                name="website"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Website</FormLabel>
                    <FormControl>
                      <Input tabIndex={-1} autoComplete="off" {...field} />
                    </FormControl>
                  </FormItem>
                )}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Work Email</FormLabel>
                    <FormControl>
                      <Input placeholder="you@company.com" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="company_name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Company Name</FormLabel>
                    <FormControl>
                      <Input placeholder="Acme Inc." {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="role"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Your Role</FormLabel>
                    <FormControl>
                      <Input placeholder="CTO, Founder, etc." {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="team_size"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Team Size</FormLabel>
                    <FormControl>
                      <Input type="number" min="1" {...field} value={field.value as number | string} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <Button type="submit" className="w-full mt-4" disabled={isSubmitting}>
              {isSubmitting ? (
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              ) : null}
              {isHighSavings ? "Request Consultation" : "Notify Me"}
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}
