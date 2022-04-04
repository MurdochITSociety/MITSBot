import Collection from "@discordjs/collection";
import { REST } from "@discordjs/rest";
import { Routes } from "discord-api-types/v10";
import fs from "fs";
import path from "path";
import Bot from "../Bot";
import { Command } from "../types/Command";
import * as config from "../config.json";

export class CommandHandler {
    public commands: Collection<string, Command>;

    constructor() {
        this.commands = new Collection<string, Command>();
    }

    public async registerCommands(bot: Bot): Promise<void> {
        const rest = new REST({ version: '10' }).setToken(config.token);
        const commandsDir = path.join(__dirname, "..", "commands");
        const commandsFiles = fs.readdirSync(commandsDir).filter(f => f.endsWith(".ts"));

        for (const file of commandsFiles) {
            const { command } = await import(`${commandsDir}/${file}`);

            if (!command)
                continue;

            this.commands.set(command.data.name, command);
        }

        await rest
            .put(
                Routes.applicationGuildCommands(
                    config.applicationId,
                    config.server),
                { body: Array.from(this.commands.values()).map(v => v.data.toJSON()) })
            .then(() => console.log("Registered commands successfully!"))
            .catch((e) => console.log(e));
    }

    public async handleInteractions(bot: Bot): Promise<void> {
        bot.on('interactionCreate', async (intr) => {
            if (!intr.isCommand())
                return;

            if (!this.commands.has(intr.commandName))
                return;

            await this.commands.get(intr.commandName)?.exec(bot, intr);
        });
    }

}
