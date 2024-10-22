public interface IRuntime
{
    void Register(IMsgActor actor);
    IMessageReceiver GetNewMsgReceiver();
    void Connect();
    void Disconnect();
    IActorConnector FindByTopic(string topic);
    IActorConnector FindByName(string name);
}
