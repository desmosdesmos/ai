import { Bot } from "grammy";
import { config } from "dotenv";
import { getPostFromTopic } from "./openai.js";
import { initDB, canGenerate, increaseCount } from "./db.js";

config();
const bot = new Bot("8212092084:AAFArafCif5HOkXjO95ig4O8mLA2BNvEvfA");
await initDB();

bot.command("start", (ctx) =>
  ctx.reply("Привет! Я — AI-контент-бот. Напиши /post и тему, я сгенерирую пост.")
);

bot.command("post", async (ctx) => {
  const userId = ctx.from?.id;
  const text = ctx.message?.text?.split(" ").slice(1).join(" ");

  if (!userId || !text) return ctx.reply("Напиши тему: /post Твоя тема");

  const can = await canGenerate(userId);
  if (!can) return ctx.reply("Ограничение 3 поста в день. Купи доступ ��");

  ctx.reply("Генерирую пост...");

  const post = await getPostFromTopic(text);
  await increaseCount(userId);
  ctx.reply(post);
});

bot.start();
