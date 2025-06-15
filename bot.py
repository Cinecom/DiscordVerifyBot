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
        intents.guilds = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        
        self.verification_channel = None
        
    async def setup_hook(self):
        """Called when the bot is starting up."""
        # Add persistent views
        self.add_view(VerificationView())
        self.add_view(ClassSelectionView())
        self.add_view(RoleSelectionView())
        
        logger.info("Bot setup completed")
    
    async def on_ready(self):
        """Called when the bot has successfully connected to Discord."""
        logger.info(f'{self.user} has connected to Discord!')
        
        # Get the verification channel
        self.verification_channel = self.get_channel(VERIFICATION_CHANNEL_ID)
        
        if self.verification_channel:
            logger.info(f"Verification channel found: {self.verification_channel.name}")
            await self.post_welcome_message()
        else:
            logger.error(f"Could not find verification channel with ID: {VERIFICATION_CHANNEL_ID}")
    
    async def post_welcome_message(self):
        """Post the welcome message with verification button."""
        try:
            # Create embed for welcome message
            embed = discord.Embed(
                title="🛡️ Server Verification",
                description=WELCOME_MESSAGE,
                color=0x00ff00
            )
            embed.set_footer(text="Click the button below to begin verification")
            
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
