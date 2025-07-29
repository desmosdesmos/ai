import { Bot } from "grammy";
import { getPostFromTopic } from "./openai.js";
import { initDB, canGenerate, increaseCount } from "./db.js";

const bot = new Bot("8212092084:AAFArafCif5HOkXjO95ig4O8mLA2BNvEvfA");

// Обработчик сигналов для graceful shutdown
process.on('SIGTERM', async () => {
  console.log('Получен SIGTERM, останавливаю бота...');
  await bot.stop();
  process.exit(0);
});

process.on('SIGINT', async () => {
  console.log('Получен SIGINT, останавливаю бота...');
  await bot.stop();
  process.exit(0);
});

bot.command("start", (ctx) =>
  ctx.reply("Привет! Я — AI-контент-бот. Напиши /post и тему, я сгенерирую пост.")
);

bot.command("post", async (ctx) => {
  const userId = ctx.from?.id;
  const text = ctx.message?.text?.split(" ").slice(1).join(" ");

  if (!userId || !text) {
    return ctx.reply("Напиши тему: /post Твоя тема");
  }

  ctx.reply("Генерирую пост...");

  try {
    const post = await getPostFromTopic(text);
    console.log("Сгенерирован пост:", post.substring(0, 100) + "...");
    await ctx.reply(post);
  } catch (error) {
    console.error("Ошибка в команде post:", error);
    await ctx.reply("Произошла ошибка при генерации поста. Попробуй еще раз.");
  }
});

// Инициализация
(async () => {
  try {
    await initDB();
    console.log("База данных инициализирована");
    
    bot.start({
      onStart: () => {
        console.log("Бот успешно запущен и готов к работе!");
      },
      onError: (err) => {
        console.error("Ошибка в боте:", err);
      }
    });
  } catch (error) {
    console.error("Ошибка запуска:", error);
    process.exit(1);
  }
})();
