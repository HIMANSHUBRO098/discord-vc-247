import discord
import asyncio
import os
import io

# Env vars from Render
token = os.environ['DISCORD_TOKEN']
channel_id = int(os.environ['CHANNEL_ID'])

intents = discord.Intents.default()
client = discord.Client(intents=intents, self_bot=True)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} – Joining VC 24/7!')
    try:
        channel = client.get_channel(channel_id)
        if not channel:
            print('❌ Invalid VC ID – Check your env var.')
            return

        # Connect to VC
        voice_client = await channel.connect(reconnect=True, timeout=10)
        print(f'✅ Joined {channel.name}!')

        # Play infinite silence (prevents kick – uses /dev/zero for zero audio)
        silence_source = discord.FFmpegPCMAudio(io.BytesIO(b''), pipe=True, options='-f s16le -ar 48000 -ac 2 -i /dev/zero')
        voice_client.play(silence_source, after=lambda e: print(f'Voice error: {e}') if e else None)

        # Auto-mute/deafen (optional)
        await client.change_voice_state(channel=channel, self_mute=True, self_deaf=True)
        print('🔇 Muted & Deafened.')

    except Exception as e:
        print(f'❌ Error joining VC: {e}')

    # Keep alive forever
    while True:
        await asyncio.sleep(60)

client.run(token, bot=False)
