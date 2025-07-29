import { Bot } from "grammy";
import { OpenAI } from "openai";

const bot = new Bot("8212092084:AAFArafCif5HOkXjO95ig4O8mLA2BNvEvfA");

const openai = new OpenAI({ 
  apiKey: "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"
});

async function getPostFromTopic(topic) {
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

// Добавляем обработчик ошибок
bot.catch((err) => {
  console.error("Ошибка в боте:", err);
});

bot.command("start", (ctx) =>
  ctx.reply("Привет! Я — AI-контент-бот. Напиши /post и тему, я сгенерирую пост.")
);

bot.command("post", async (ctx) => {
  const text = ctx.message?.text?.split(" ").slice(1).join(" ");

  if (!text) {
    return ctx.reply("Напиши тему: /post Твоя тема");
  }

  ctx.reply("Генерирую пост...");

  try {
    const post = await getPostFromTopic(text);
    console.log("Сгенерирован пост:", post.substring(0, 100) + "...");
    await ctx.reply(post);
  } catch (error) {
    console.error("Ошибка:", error);
    await ctx.reply("Ошибка генерации. Попробуй еще раз.");
  }
});

console.log("Запускаю бота...");
bot.start();
console.log("Бот запущен!");
