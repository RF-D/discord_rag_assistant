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
chat = ChatOpenAI(model = "gpt-4o-mini",temperature=0.8)

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
async def ask(ctx, *, question):
    try:
        docs = retriever
        formatted_prompt = system_message_prompt.format(context=docs)

        messages = [formatted_prompt, HumanMessage(content=question)]
        result = chat(messages)

        # Split the response into chunks of 2000 characters or less
        response_chunks = [result.content[i:i+2000] for i in range(0, len(result.content), 2000)]

        # Send each chunk as a separate message
        for chunk in response_chunks:
            await ctx.send(chunk)

    except Exception as e:
        print(f"Error occurred: {e}")
        await ctx.send(f"Sorry, I was unable to process your question. /n{e}")


bot.run(os.getenv("DISCORD_TOKEN"))