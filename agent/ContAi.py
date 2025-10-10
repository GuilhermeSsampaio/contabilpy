from agno.agent import Agent
from agno.models.google import Gemini

# from tools.convert_files import convert_csv_to_excel

contAgent = Agent(
    name="ContAgent",
    model=Gemini(id="gemini-2.0-flash"),
    # instructions=["Use sua ferramenta para converter arquivos csv para excel, e mostre o caminho retornado pro user"],
    # tools=[convert_csv_to_excel()]
)

# contAgent.cli_app(stream=True)

