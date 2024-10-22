public interface IMsgActor
{
    void OnConnect(IRuntime runtime);
    bool OnTxtMsg(string msg, string msgType, string receiver, string sender);
    bool OnBinMsg(byte[] msg, string msgType, string receiver, string sender);
    void OnStart(IRuntime runtime);
    void Stop();
    void DispatchMessage(object message);
}
