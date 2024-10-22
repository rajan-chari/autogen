namespace AutoGenCapCS
{
    public interface IMessageReceiver
    {
        // Definition of IMessageReceiver interface
    }
}
namespace AutoGenCapCS
{
    public interface IMessageReceiver
    {
        void Init(string actorName);
        void AddListener(string topic);
        string GetMessage();
        void Stop();
    }
}
