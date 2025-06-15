"""
Main Discord bot class and event handlers
"""
import discord
from discord.ext import commands
import logging
from config import *
from views import VerificationView, ClassSelectionView, RoleSelectionView, CharacterNameModal

logger = logging.getLogger(__name__)

class VerificationBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True

        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )

        self.verification_channel = None

    async def setup_hook(self):
        """Called when the bot is starting up."""
        logger.info("Setting up bot...")

        # Add persistent views
        self.add_view(VerificationView())
        self.add_view(ClassSelectionView())
        self.add_view(RoleSelectionView())
        logger.info("Added persistent views")

        # Manually add the command to ensure it's registered
        try:
            # Create the command function
            @commands.hybrid_command(name='post_welcome', description='Post the welcome verification message')
            @commands.has_permissions(administrator=True)
            async def post_welcome_cmd(ctx):
                """Command to manually post the welcome message."""
                logger.info(f"post_welcome command called by {ctx.author}")

                if ctx.channel.id == VERIFICATION_CHANNEL_ID:
                    await ctx.bot.post_welcome_message()
                    await ctx.send("Welcome message posted!", ephemeral=True, delete_after=3)
                    logger.info("Welcome message posted via command")
                else:
                    await ctx.send("This command can only be used in the verification channel.", ephemeral=True, delete_after=5)
                    logger.warning(f"post_welcome command used in wrong channel: {ctx.channel.name}")

            # Add the command to the bot
            self.add_command(post_welcome_cmd)
            logger.info("post_welcome command added successfully")

        except Exception as e:
            logger.error(f"Failed to add post_welcome command: {e}")

        # Sync slash commands
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} slash command(s)")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")

        # Log available commands
        logger.info(f"Available commands: {[cmd.name for cmd in self.commands]}")

        logger.info("Bot setup completed")

    async def on_ready(self):
        """Called when the bot has successfully connected to Discord."""
        logger.info(f'{self.user} has connected to Discord!')
        logger.info(f"Bot ID: {self.user.id}")
        logger.info(f"Guild count: {len(self.guilds)}")

        # Get the verification channel
        self.verification_channel = self.get_channel(VERIFICATION_CHANNEL_ID)

        if self.verification_channel:
            logger.info(f"Verification channel found: {self.verification_channel.name}")
            logger.info("Bot ready - verification system active")
        else:
            logger.error(f"Could not find verification channel with ID: {VERIFICATION_CHANNEL_ID}")

        # Log commands again after ready
        logger.info(f"Commands after ready: {[cmd.name for cmd in self.commands]}")

    async def on_command_error(self, ctx, error):
        """Handle command errors."""
        if isinstance(error, commands.CommandNotFound):
            logger.warning(f"Command not found: {ctx.message.content}")
            await ctx.send(f"Command not found. Available commands: {[cmd.name for cmd in self.commands]}", delete_after=5)
        elif isinstance(error, commands.MissingPermissions):
            logger.warning(f"Missing permissions for command: {ctx.command}")
            await ctx.send("You don't have permission to use this command.", delete_after=5)
        elif isinstance(error, commands.CheckFailure):
            logger.warning(f"Check failure for command: {ctx.command}")
            await ctx.send("Command check failed.", delete_after=5)
        else:
            logger.error(f"Command error: {error}")
            await ctx.send("An error occurred while executing the command.", delete_after=5)

    async def post_welcome_message(self):
        """Post the welcome message with verification button."""
        try:
            if not self.verification_channel:
                logger.error("Verification channel not set")
                return

            # Create embed for welcome message
            embed = discord.Embed(
                title="✅ Guild Verification",
                description=WELCOME_MESSAGE,
                color=0x00ff00
            )

            # Create view with start verification button
            view = VerificationView()

            # Send the message
            await self.verification_channel.send(embed=embed, view=view)
            logger.info("Welcome message posted successfully")

        except Exception as e:
            logger.error(f"Failed to post welcome message: {e}")

    async def on_error(self, event, *args, **kwargs):
        """Handle bot errors."""
        logger.error(f"An error occurred in event {event}: {args[0] if args else 'Unknown error'}")

    async def notify_officers(self, user):
        """Notify officers about new member verification."""
        try:
            officer_role = discord.utils.get(user.guild.roles, id=OFFICER_ROLE_ID)

            if officer_role:
                message = f"{officer_role.mention} a new player has signed up to the Discord. Please verify the membership of {user.mention}"
                await self.verification_channel.send(message)
                logger.info(f"Officer notification sent for user: {user.display_name}")
            else:
                logger.error(f"Officer role not found with ID: {OFFICER_ROLE_ID}")

        except Exception as e:
            logger.error(f"Failed to notify officers: {e}")

    @commands.hybrid_command(name='post_welcome', description='Post the welcome verification message')
    @commands.has_permissions(administrator=True)
    async def post_welcome_command(self, ctx):
        """Command to manually post the welcome message."""
        logger.info(f"post_welcome command called by {ctx.author}")

        if ctx.channel.id == VERIFICATION_CHANNEL_ID:
            await self.post_welcome_message()
            await ctx.send("Welcome message posted!", ephemeral=True, delete_after=3)
            logger.info("Welcome message posted via command")
        else:
            await ctx.send("This command can only be used in the verification channel.", ephemeral=True, delete_after=5)
            logger.warning(f"post_welcome command used in wrong channel: {ctx.channel.name}")