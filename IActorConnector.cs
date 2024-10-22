public interface IActorConnector
{
    void SendTxtMsg(string msg);
    void SendBinMsg(string msgType, byte[] msg);
    void Close();
}

public class ActorConnector : IActorConnector
{
    public void SendTxtMsg(string msg)
    {
        // Implementation
    }

    public void SendBinMsg(string msgType, byte[] msg)
    {
        // Implementation
    }

    public void Close()
    {
        // Implementation
    }
}
