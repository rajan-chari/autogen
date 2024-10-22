namespace AutoGenCapCS
{
    public interface IMsgActor
    {
        // Definition of IMsgActor interface
    }
}
namespace AutoGenCapCS
{
    public interface IMsgActor
    {
        void OnConnect();
        void OnTxtMsg(string message, string msgType, string receiver, string sender);
        void OnBinMsg(byte[] message, string msgType, string receiver, string sender);
        void DispatchMessage();
        string GetMessage();
        void OnStart();
        void DisconnectNetwork();
        void Stop();
    }
}
