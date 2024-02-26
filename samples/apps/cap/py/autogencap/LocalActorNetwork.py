import zmq
from .DebugLog import Debug, Warn
from .ActorConnector import ActorConnector
from .Broker import Broker
from .Constants import Termination_Topic
from .Actor import Actor


class LocalActorNetwork:
    def __init__(self, name="Local Agent Network"):
        self.agents = {}
        self.name: str = name
        self._context: zmq.Context = zmq.Context()
        self._broker: Broker = Broker(self._context)

    def __str__(self):
        return f"{self.name}"

    def register(self, agent: Actor):
        # Get agent's name and description and add to a dictionary so
        # that we can look up the agent by name
        self.agents[agent.agent_name] = agent
        agent.start_recv_thread(self._context)
        Debug("Local_Agent_Network", f"{agent.agent_name} registered in the network.")

    def connect(self):
        if not self._broker.start():
            self._broker = None
        for agent in self.agents.values():
            agent.connect(self)

    def disconnect(self):
        for agent in self.agents.values():
            agent.disconnect(self)
        if self._broker: 
            self._broker.stop()

    def agent_connector_by_topic(self, topic: str) -> ActorConnector:
        return ActorConnector(self._context, topic)

    def lookup_actor(self, name: str) -> ActorConnector:
        agent = self.agents.get(name, None)
        if agent is None:
            Warn("Local_Agent_Network", f"{name}, not found in the network.")
            return None
        Debug("Local_Agent_Network", f"[{name}] found in the network.")
        return self.agent_connector_by_topic(name)

    def lookup_termination(self) -> ActorConnector:
        termination_topic: str = Termination_Topic
        return self.agent_connector_by_topic(termination_topic)