namespace AutoGenCapCS
{
    public interface IRuntime
    {
        // Definition of IRuntime interface
    }
}
namespace AutoGenCapCS
{
    public interface IRuntime
    {
        void Register(IMsgActor actor);
        IMessageReceiver GetNewMsgReceiver();
        void Connect(string address);
        void Disconnect();
        IMsgActor FindByTopic(string topic);
        IMsgActor FindByName(string name);
        IMsgActor FindTermination();
        IMsgActor FindByNameRegex(string pattern);
    }
}
