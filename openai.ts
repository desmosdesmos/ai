import { OpenAI } from "openai";
import { POST_PROMPT } from "./prompts/postPrompt.js";
import "dotenv/config";

const openai = new OpenAI({ 
  apiKey: "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"
});

export async function getPostFromTopic(topic: string): Promise<string> {
  const prompt = POST_PROMPT.replace("{topic}", topic);
  const res = await openai.chat.completions.create({
    model: "gpt-3.5-turbo",
    messages: [{ role: "user", content: prompt }],
    temperature: 0.9,
  });
  return res.choices[0].message.content || "Ошибка генерации.";
}
