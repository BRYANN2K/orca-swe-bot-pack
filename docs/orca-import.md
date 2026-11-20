# Import and distribution in Orca

Source review pin: Orca v1.4.266. The installed CLI was 1.4.266. The paths below describe the shipped code and CLI, with transfer through Orca Cloud pending a two-account smoke test.

| Option | How Orca handles it | Pack fit |
| --- | --- | --- |
| Built-in Templates | Versioned catalog compiled into Orca. The template RPC inspected is `bots.templates.suggest`. Creating a known template reads the host catalog. | An upstream contribution could add native tiles. Each supported host would need the shipped catalog. |
| Share Bot link | Share opens a review of selected parts and publishes a versioned package on Orca Cloud. Link review precedes creating a new bot. Recipients can choose host, agent, permission and which tools to import. Ask for approval starts selected. | Best native distribution candidate. Publish one clean reference bot per role and list six links in the release README. |
| Import from another app | Finds OpenClaw, Hermes or OpenBot on the machine, or takes an export folder. A bot reads selected source files, proposes what to migrate and waits for user approval. | Migration path for an existing bot. The folder selection starts a guided import and is separate from receiving a Share Bot archive. |
| New bot + Markdown | The owner starts an ordinary bot and pastes the generated role as a first message. | Pack's direct install. No dependence on a sharing account or Cloud link. Orca's own bot and connector support still applies. |
| Share Skills | The installed CLI exposes `orca skills share`. | Can distribute reusable instructions. A skill install is separate from creating a bot, its permissions and automations. |

## What Share Bot carries

The native package has versioned `dev.orca.bot-sharing/bot.json` and transport manifest, a `SOUL.md`, and optional avatar, selected skills and selected memory. The reviewed content is what the new bot receives. Skills are sanitized to plain documents, and supported remote tools share their endpoint metadata without credentials. Export filters out command tools and event webhooks. Imported memory is excluded, and ordinary memory remains opt-in. Publishing can be refused when secret scanning flags the content.

Schedules are imported paused. Event automations are offered as suggestions, with the recipient supplying targets and connectors. Some event suggestions carry the kind and name only in the recipient setup note, so keep the full recipe in the Markdown template. The application does not establish that a published update rewrites bots already installed from that link. Treat each installed bot as its own configuration and offer explicit upgrade review.

## Prepare the six native links

1. Create six dedicated reference bots, one per generated Markdown file. Use clean histories and no live repo profile, credentials, tools or runtime data.
2. Put the generated role content into the reference bot's `SOUL.md` through its workspace editor. Keep the launch instruction explicit. Use this share setup note: “Run the setup interview. Confirm repository, workflow and permissions before registering routines.”
3. Use Share Bot and inspect the candidate content. Choose only portable parts. Leave memory, private repo selectors, real connection details and environment-specific schedules off. The bundled recipes ask for timezone and triggers after import.
4. After publication is authorized, publish one unlisted link per role from the intended Orca profile. Record the published package version and digest in release metadata when available.
5. On a clean recipient profile, open the link and select an agent, host and approval mode. Verify the reviewed content, ask the first-run question in chat if the host does not launch the interview automatically, and confirm sample connections and routines stay disabled until chosen. Try one manual read-only run. Repeat for each role before listing the links publicly.

The project artifacts are portable Markdown. No general local bot-package ZIP or JSON import was found in the inspected CLI, catalog RPC, sharing renderer or migration UI. The archive schema describes the link transport. Producing a lookalike ZIP would leave users without a supported installation path. Using an unpublished internal Cloud RPC would make this pack depend on a private contract.

## Source pointers

- [Built-in catalog](https://github.com/stablyai/orca/blob/v1.4.266/src/shared/bots/bot-templates.ts) and [catalog RPC](https://github.com/stablyai/orca/blob/v1.4.266/src/main/runtime/rpc/methods/bots-templates.ts)
- [Sharing UI RPC](https://github.com/stablyai/orca/blob/v1.4.266/src/renderer/src/components/bots/sharing/bot-share-rpc.ts), [recipient dialog](https://github.com/stablyai/orca/blob/v1.4.266/src/renderer/src/components/bots/sharing/NewBotFromShareDialog.tsx) and [package schema](https://github.com/stablyai/orca/blob/v1.4.266/src/shared/bots/bot-package.ts)
- [Export source filtering](https://github.com/stablyai/orca/blob/v1.4.266/src/main/bots/sharing/bot-share-sources.ts), [document sanitization](https://github.com/stablyai/orca/blob/v1.4.266/src/main/bots/sharing/bot-package-content.ts) and [application of imported content](https://github.com/stablyai/orca/blob/v1.4.266/src/main/bots/sharing/bot-share-create.ts)
- [Migration guide](https://github.com/stablyai/orca/blob/v1.4.266/skill-guides/orca-cli/references/bot-import.md)
