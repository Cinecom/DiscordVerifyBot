"""
Discord UI views and modals for the verification process
"""
import discord
from discord import ui
import logging
from config import *

logger = logging.getLogger(__name__)

class CharacterNameModal(ui.Modal, title="Enter Your Character Name"):
    """Modal for collecting character name input."""
    
    def __init__(self):
        super().__init__()
        
    character_name = ui.TextInput(
        label="Character Name",
        placeholder="Enter your character name here...",
        required=True,
        max_length=32
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle character name submission."""
        try:
            # Update user's nickname
            await interaction.user.edit(nick=self.character_name.value)
            
            # Create embed for class selection
            embed = discord.Embed(
                title="⚔️ Class Selection",
                description=f"Great! Your character name has been set to **{self.character_name.value}**.\n\nNow, please select your class:",
                color=0x0099ff
            )
            
            # Create class selection view
            view = ClassSelectionView()
            
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            logger.info(f"Character name set for {interaction.user.display_name}: {self.character_name.value}")
            
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ I don't have permission to change your nickname. Please contact an administrator.",
                ephemeral=True
            )
            logger.error(f"Failed to set nickname for {interaction.user.display_name}: Permission denied")
        except Exception as e:
            await interaction.response.send_message(
                "❌ An error occurred while setting your character name. Please try again.",
                ephemeral=True
            )
            logger.error(f"Error setting character name: {e}")

class VerificationView(ui.View):
    """View for the initial verification button."""
    
    def __init__(self):
        super().__init__(timeout=None)
    
    @ui.button(label="Start Verification", style=discord.ButtonStyle.green, emoji="🚀")
    async def start_verification(self, interaction: discord.Interaction, button: ui.Button):
        """Handle start verification button click."""
        # Show character name modal
        modal = CharacterNameModal()
        await interaction.response.send_modal(modal)
        logger.info(f"Verification started for user: {interaction.user.display_name}")

class ClassSelectionView(ui.View):
    """View for class selection buttons."""
    
    def __init__(self):
        super().__init__(timeout=300)  # 5 minute timeout
        
        # Create buttons for each class
        for class_name, role_id in CLASS_ROLES.items():
            button = ui.Button(
                label=class_name,
                emoji=CLASS_ICONS.get(class_name, "⚔️"),
                style=discord.ButtonStyle.secondary,
                custom_id=f"class_{class_name.lower()}"
            )
            button.callback = self.create_class_callback(class_name, role_id)
            self.add_item(button)
    
    def create_class_callback(self, class_name, role_id):
        """Create callback function for class selection."""
        async def callback(interaction: discord.Interaction):
            try:
                # Get the role
                role = discord.utils.get(interaction.guild.roles, id=role_id)
                
                if role:
                    # Assign the role
                    await interaction.user.add_roles(role)
                    
                    # Create embed for role selection
                    embed = discord.Embed(
                        title="🎭 Role Selection",
                        description=f"Excellent! You've been assigned the **{class_name}** class.\n\nNow, please select your preferred role:",
                        color=0xff9900
                    )
                    
                    # Create role selection view
                    view = RoleSelectionView()
                    
                    await interaction.response.edit_message(embed=embed, view=view)
                    logger.info(f"Class {class_name} assigned to {interaction.user.display_name}")
                    
                else:
                    await interaction.response.send_message(
                        f"❌ Could not find the {class_name} role. Please contact an administrator.",
                        ephemeral=True
                    )
                    logger.error(f"Role not found: {class_name} (ID: {role_id})")
                    
            except discord.Forbidden:
                await interaction.response.send_message(
                    "❌ I don't have permission to assign roles. Please contact an administrator.",
                    ephemeral=True
                )
                logger.error(f"Failed to assign role {class_name}: Permission denied")
            except Exception as e:
                await interaction.response.send_message(
                    "❌ An error occurred while assigning your class. Please try again.",
                    ephemeral=True
                )
                logger.error(f"Error assigning class {class_name}: {e}")
        
        return callback

class RoleSelectionView(ui.View):
    """View for gameplay role selection buttons."""
    
    def __init__(self):
        super().__init__(timeout=300)  # 5 minute timeout
        
        # Create buttons for each role
        for role_name, role_id in GAMEPLAY_ROLES.items():
            button = ui.Button(
                label=role_name,
                emoji=ROLE_ICONS.get(role_name, "⚔️"),
                style=discord.ButtonStyle.primary,
                custom_id=f"role_{role_name.lower()}"
            )
            button.callback = self.create_role_callback(role_name, role_id)
            self.add_item(button)
    
    def create_role_callback(self, role_name, role_id):
        """Create callback function for role selection."""
        async def callback(interaction: discord.Interaction):
            try:
                # Get the role
                role = discord.utils.get(interaction.guild.roles, id=role_id)
                
                if role:
                    # Assign the role
                    await interaction.user.add_roles(role)
                    
                    # Create completion embed
                    embed = discord.Embed(
                        title="✅ Verification Complete!",
                        description=VERIFICATION_COMPLETE_MESSAGE,
                        color=0x00ff00
                    )
                    embed.add_field(
                        name="Your Roles",
                        value=f"🎭 Role: **{role_name}**\n🎯 Character: **{interaction.user.display_name}**",
                        inline=False
                    )
                    embed.set_footer(text="Welcome to the guild!")
                    
                    await interaction.response.edit_message(embed=embed, view=None)
                    
                    # Notify officers
                    bot = interaction.client
                    await bot.notify_officers(interaction.user)
                    
                    logger.info(f"Verification completed for {interaction.user.display_name} with role {role_name}")
                    
                else:
                    await interaction.response.send_message(
                        f"❌ Could not find the {role_name} role. Please contact an administrator.",
                        ephemeral=True
                    )
                    logger.error(f"Role not found: {role_name} (ID: {role_id})")
                    
            except discord.Forbidden:
                await interaction.response.send_message(
                    "❌ I don't have permission to assign roles. Please contact an administrator.",
                    ephemeral=True
                )
                logger.error(f"Failed to assign role {role_name}: Permission denied")
            except Exception as e:
                await interaction.response.send_message(
                    "❌ An error occurred while assigning your role. Please try again.",
                    ephemeral=True
                )
                logger.error(f"Error assigning role {role_name}: {e}")
        
        return callback
    
    async def on_timeout(self):
        """Handle view timeout."""
        for item in self.children:
            item.disabled = True
