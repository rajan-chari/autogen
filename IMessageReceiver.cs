public interface IMessageReceiver
{
    void Init(string actorName);
    void AddListener(string topic);
    object GetMessage();
    void Stop();
}
