import { Bot } from "grammy";
import { getPostFromTopic } from "./openai.js";

const bot = new Bot("8212092084:AAFArafCif5HOkXjO95ig4O8mLA2BNvEvfA");

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
    await ctx.reply(post);
  } catch (error) {
    console.error("Ошибка:", error);
    await ctx.reply("Ошибка генерации. Попробуй еще раз.");
  }
});

// Быстрый запуск
console.log("Запускаю бота...");
bot.start();
console.log("Бот запущен!");
