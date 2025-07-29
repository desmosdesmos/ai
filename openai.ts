import { OpenAI } from "openai";

const openai = new OpenAI({ 
  apiKey: "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"
});

export async function getPostFromTopic(topic: string): Promise<string> {
  try {
    const res = await openai.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [{ 
        role: "user", 
        content: `Напиши Telegram-пост по теме: "${topic}". Структура: 1. Заголовок с emoji 2. Затравка в первом абзаце 3. Полезный или провокационный контент 4. Завершение и Call to Action. Оформи для Telegram: отступы, emoji, короткие предложения.`
      }],
      temperature: 0.9,
      max_tokens: 300
    });
    
    return res.choices[0]?.message?.content || "Ошибка генерации";
  } catch (error) {
    console.error("Ошибка OpenAI:", error);
    return "Ошибка генерации поста";
  }
}
