import { OpenAI } from "openai";
import { POST_PROMPT } from "./prompts/postPrompt.js";
import "dotenv/config";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY! });

export async function getPostFromTopic(topic: string): Promise<string> {
  const prompt = POST_PROMPT.replace("{topic}", topic);
  const res = await openai.chat.completions.create({
    model: "gpt-3.5-turbo",
    messages: [{ role: "user", content: prompt }],
    temperature: 0.9,
  });
  return res.choices[0].message.content || "Ошибка генерации.";
}
