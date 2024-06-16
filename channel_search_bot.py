import discord
from discord.ext import commands
from dotenv import load_dotenv
from langchain.prompts import SystemMessagePromptTemplate, PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.schema import HumanMessage
from langchain_pinecone import PineconeVectorStore
from tools.retriever_tools import retriever_tool
from tools.voyage_embeddings import vo_embed
import os

load_dotenv()

embeddings = vo_embed()

#Vector DB
index_name = "langchain"
vectorstore = PineconeVectorStore.from_existing_index(
    embedding=embeddings, index_name=index_name)

retriever = retriever_tool(vectorstore)
chat = ChatOpenAI(model = "gpt-4o",temperature=0.8)

prompt_template = """You are a helpful Discord bot that helps users with programming and answers about the channel.

{context}

Please provide the most suitable response for the users question.
Answer:"""

prompt = PromptTemplate(
    template=prompt_template, input_variables=["context"]
)
system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)

#Discord Logic
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def search(ctx, *, query):
    channel = ctx.channel
    messages = await channel.history(limit=1000).flatten()
    
    matching_messages = []
    for message in messages:
        if query.lower() in message.content.lower():
            matching_messages.append(message.content)
    
    if matching_messages:
        # Format the matching messages into a prompt
        formatted_messages = "\n".join(matching_messages)
        prompt = system_message_prompt.format(context=formatted_messages)
        
        # Generate a response using the GPT-4 model
        response = chat(prompt)
        
        # Send the response as a message in Discord
        await ctx.send(response.content)
    else:
        await ctx.send("No matching messages found.")

bot.run(os.getenv("DISCORD_TOKEN"))