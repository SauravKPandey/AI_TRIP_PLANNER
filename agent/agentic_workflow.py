from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition

from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool



class GraphBuilder():
    def __init__(self, model_provider : str = "gemini"):
        self.model_loader=ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()

        self.tools = [ ]
        self.weather_tools = WeatherInfoTool()
        self.place_search_tools = PlaceSearchTool()
        self.calculator_tools = CalculatorTool()
        self.currency_converter_tools = CurrencyConverterTool()

        self.tools.extend([* self.weather_tools.weather_tool_list,
                           * self.place_search_tools.place_search_tool_list,
                           * self.calculator_tools.calculator_tool_list,
                           * self.currency_converter_tools.currency_converter_tool_list
        ])

        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        self.graph = None
        self.system_promp=SYSTEM_PROMPT
    def agent_function(self, state:MessagesState):
        """ Main Agent fn"""
        user_question = state["messages"]
        print(user_question)
        input_question = [self.system_promp] + user_question
        print(input_question)
        response = self.llm_with_tools.invoke(input_question)
        print(response)
        return {"messages": [response]}

    def build_graph(self):
        graph_builder = StateGraph(MessagesState)
        print("adding agent")
        graph_builder.add_node("agent", self.agent_function)
        print("adding tools")
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        print("adding start node")
        graph_builder.add_edge(START, "agent")
        print("conditional edge b/w agent and tools")
        graph_builder.add_conditional_edges("agent", tools_condition)
        print("edge b/w tools and agent")
        graph_builder.add_edge("tools", "agent")
        print("End Node")
        graph_builder.add_edge("agent", END)
        print("compiling....")
        self.graph =  graph_builder.compile()
        print("graph built")
        return self.graph
    def __call__(self):
        return self.build_graph()