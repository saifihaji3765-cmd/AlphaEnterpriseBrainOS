"use client";
import { useState } from "react";
import OpenAI from "openai";

export default function FutureGuardAI() {
  const [result, setResult] = useState(null);

  async function analyze() {
    const openai = new OpenAI({
      apiKey: process.env.NEXT_PUBLIC_OPENAI_KEY,
      dangerouslyAllowBrowser: true
    });

    // 1️⃣ Signals
    let signals = [];
    if (3 < 5) signals.push("Growth Slow");
    if (4 > 3) signals.push("Customer Churn");
    if (6 > 3) signals.push("Product Confusion");

    // 2️⃣ Risk Mapping
    let risk = "Low Risk";
    let probability = 20;
    let time = "No threat";

    if (signals.length >= 2) {
      risk = "Business Decline Risk";
      probability = 70;
      time = "30–60 days";
    }

    // 3️⃣ AI Warning
    const prompt = `
You are a business early-warning AI.

Signals: ${signals.join(", ")}
Risk: ${risk}
Probability: ${probability}%
Time: ${time}

Give a warning and 3 actions.
`;

    const completion = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [{ role: "user", content: prompt }],
    });

    setResult({
      signals,
      risk,
      probability,
      time,
      warning: completion.choices[0].message.content,
    });
  }

  return (
    <main style={{ padding: 40 }}>
      <h1>🚨 FutureGuard AI</h1>

      <button onClick={analyze}>
        Generate Business Warning
      </button>

      {result && (
        <div style={{ marginTop: 20 }}>
          <p><b>Signals:</b> {result.signals.join(", ")}</p>
          <p><b>Risk:</b> {result.risk}</p>
          <p><b>Probability:</b> {result.probability}%</p>
          <p><b>Time Window:</b> {result.time}</p>
          <pre>{result.warning}</pre>
        </div>
      )}
    </main>
  );
}
