import { Bot } from "grammy";
import { getPostFromTopic } from "./openai.js";
import { initDB, canGenerate, increaseCount } from "./db.js";

const bot = new Bot("8212092084:AAFArafCif5HOkXjO95ig4O8mLA2BNvEvfA");

bot.command("start", (ctx) =>
  ctx.reply("Привет! Я — AI-контент-бот. Напиши /post и тему, я сгенерирую пост.")
);

bot.command("post", async (ctx) => {
  const userId = ctx.from?.id;
  const text = ctx.message?.text?.split(" ").slice(1).join(" ");

  if (!userId || !text) return ctx.reply("Напиши тему: /post Твоя тема");

  ctx.reply("Генерирую пост...");

  try {
    const post = await getPostFromTopic(text);
    ctx.reply(post);
  } catch (error) {
    ctx.reply("Ошибка генерации поста.");
  }
});

// Инициализация и запуск
(async () => {
  try {
    await initDB();
    bot.start();
  } catch (error) {
    console.error("Ошибка запуска:", error);
  }
})();
