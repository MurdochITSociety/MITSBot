import { Client, GatewayIntentBits } from "discord.js"; //changes from v13->v14
import { CommandHandler } from "./handlers/CommandHandler";
import * as config from "./config.json";

export default class Bot extends Client {
    public commandHandler: CommandHandler;

    constructor() {
        super({
            intents: [GatewayIntentBits.Guilds] //changes from v13->v14
        });

        this.commandHandler = new CommandHandler();
    }

    public async start(): Promise<void> {
        try {
            this.commandHandler.registerCommands(this);
            this.commandHandler.handleInteractions(this);
            await this.login(config.tokens.discord_bot)
                .then(() => console.log(`Logged in as ${this.application?.client.user?.username}`));
        } catch (e) {
            console.error(e);
        }
    }
}
